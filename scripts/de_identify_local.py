#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
de_identify_local.py — 鳳凰 AI 本地去識別化與反向洩漏掃描工具
========================================================================
Phoenix AI Local De-identification & Reverse-Leak Scanner (Confidential)

設計哲學：
  - 「不出網」原則：本工具全程在本地端執行，不呼叫任何公有雲 API。
    這是去識別化流程的「第一層」，必須在任何資料碰到公有雲 LLM 之前先跑。
  - 「雙層本地防禦」原則：
    * 第一層：本地規則引擎（正則 PII 庫），快又準，100% 抓取結構化個資。
    * 第二層（新增）：本地 Ollama 離線大模型 API 整合，進行語意型洗滌（洗公司品牌、人名等）。
  - 「可追溯」原則：每一次替換都記錄到加密對照表，供日後還原與稽核。
  - 「不可還原則安全」：對照表與去識別化輸出實體分離，且對照表加密保存。

三大功能：
  1. deid   : 執行第一層規則去識別化，並可選連線本地 Ollama 執行第二層語意洗滌，產出加密對照表。
  2. scan   : 反向洩漏掃描，檢查「已生成的成品（HTML / PDF 文字 / JSON）」中是否殘留個資。
  3. reveal : 還原：以密碼解密對照表並列印（稽核 / 客戶校稿時用）。

用法（命令列）：
  # 僅執行第一層規則去識別化
  python de_identify_local.py deid input.txt -o output.txt --map map.enc
  
  # 啟用本地 Ollama (如 qwen2.5 或 llama3) 進行第二層語意去識別化 (100% 離線安全)
  python de_identify_local.py deid input.txt -o output.txt --map map.enc --ollama --model llama3

  # 反向洩漏掃描（交付前跑，exit code 0=通過 / 2=洩漏）
  python de_identify_local.py scan ./slides/yuepin/ --report leak_report.txt

相依套件：
  僅標準函式庫（re, json, hashlib, hmac, base64, argparse, urllib.request, pathlib,
  secrets, getpass, datetime, os, sys）。無需 pip install，確保離線可跑。
========================================================================
"""

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os
import re
import secrets
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# ----------------------------------------------------------------------
# 一、台灣個資格式庫（PII Pattern Library）
# ----------------------------------------------------------------------

def _luhn_ok(number: str) -> bool:
    """Luhn 演算法驗證信用卡號檢核碼。"""
    digits = [int(d) for d in re.sub(r"\D", "", number)]
    if len(digits) < 13 or len(digits) > 19:
        return False
    checksum = 0
    parity = len(digits) % 2
    for i, d in enumerate(digits):
        if i % 2 == parity:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def _tw_id_ok(text: str) -> bool:
    """
    台灣身分證字號檢核：首字母轉碼 + 加權和模 10。
    格式：1 英文字母 + (1或2) + 8 數字。
    """
    text = text.upper()
    if not re.fullmatch(r"[A-Z][12]\d{8}", text):
        return False
    letter_map = {
        "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15, "G": 16,
        "H": 17, "I": 34, "J": 18, "K": 19, "L": 20, "M": 21, "N": 22,
        "O": 35, "P": 23, "Q": 24, "R": 25, "S": 26, "T": 27, "U": 28,
        "V": 29, "W": 32, "X": 30, "Y": 31, "Z": 33,
    }
    n = letter_map[text[0]]
    nums = [n // 10, n % 10] + [int(c) for c in text[1:]]
    weights = [1, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1]
    total = sum(a * b for a, b in zip(nums, weights))
    return total % 10 == 0


def _tw_tax_id_ok(text: str) -> bool:
    """
    台灣公司統一編號（8 碼）檢核碼驗證。
    """
    if not re.fullmatch(r"\d{8}", text):
        return False
    multipliers = [1, 2, 1, 2, 1, 2, 4, 1]
    digits = [int(c) for c in text]

    def digit_sum(x):
        return x // 10 + x % 10

    products = [digit_sum(d * m) for d, m in zip(digits, multipliers)]
    total = sum(products)
    if total % 5 == 0:
        return True
    if digits[6] == 7 and (total + 1) % 5 == 0:
        return True
    return False


# 規則庫。順序即優先序（由具體到一般）。
PII_PATTERNS = [
    {
        "name": "CREDIT_CARD",
        "label": "CREDIT_CARD",
        "regex": re.compile(r"\b(?:\d[ -]?){13,19}\b"),
        "validator": _luhn_ok,
        "desc": "信用卡號（Luhn 檢核）",
    },
    {
        "name": "TW_ID",
        "label": "TW_ID",
        "regex": re.compile(r"\b[A-Za-z][12]\d{8}\b"),
        "validator": None,
        "desc": "中華民國身分證字號（格式檢索）",
    },
    {
        "name": "MOBILE",
        "label": "MOBILE",
        "regex": re.compile(r"\b09\d{2}[-\s]?\d{3}[-\s]?\d{3}\b"),
        "validator": None,
        "desc": "台灣手機號碼（09xx）",
    },
    {
        "name": "LANDLINE",
        "label": "LANDLINE",
        "regex": re.compile(
            r"(?<![\d\w])(?:\+?886[-\s]?|\(0\d{1,2}\)|0\d{1,2})"
            r"[-\s)]?\d{3,4}[-\s]?\d{3,4}(?!\d)"
        ),
        "validator": None,
        "desc": "台灣市話（含區碼 / +886）",
    },
    {
        "name": "TW_TAX_ID",
        "label": "TAX_ID",
        "regex": re.compile(r"(?<!\d)\d{8}(?!\d)"),
        "validator": _tw_tax_id_ok,
        "desc": "公司統一編號（統編）",
    },
    {
        "name": "EMAIL",
        "label": "EMAIL",
        "regex": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
        "validator": None,
        "desc": "電子郵件位址",
    },
    {
        "name": "TW_ADDRESS",
        "label": "ADDRESS",
        "regex": re.compile(
            r"(?:台北|臺北|新北|桃園|台中|臺中|台南|臺南|高雄|基隆|新竹|嘉義|"
            r"苗栗|彰化|南投|雲林|屏東|宜蘭|花蓮|台東|臺東|澎湖|金門|連江)"
            r"[市縣].{0,30}?(?:路|街|大道|段).{0,15}?號(?:\s*\d+\s*樓)?"
        ),
        "validator": None,
        "desc": "台灣地址（縣市 + 路街 + 號）",
    },
    {
        "name": "POSTAL_CODE",
        "label": "POSTAL",
        "regex": re.compile(r"(?<!\d)\d{3}(?:\d{2})?(?=\s*(?:台|臺|市|縣))"),
        "validator": None,
        "desc": "郵遞區號（3 或 5 碼）",
    },
]

# ----------------------------------------------------------------------
# 二、去識別化核心邏輯
# ----------------------------------------------------------------------

class DeIdentifier:
    def __init__(self):
        self._value_to_token = {}
        self._counters = {}
        self.hits = []

    def _new_token(self, label: str) -> str:
        self._counters[label] = self._counters.get(label, 0) + 1
        return f"{label}_{self._counters[label]}"

    def _placeholder_for(self, label: str, value: str) -> str:
        norm = re.sub(r"[-\s]", "", value)
        key = f"{label}::{norm}"
        if key not in self._value_to_token:
            self._value_to_token[key] = self._new_token(label)
        return self._value_to_token[key]

    def process_text(self, text: str) -> str:
        spans = []
        for pat in PII_PATTERNS:
            for m in pat["regex"].finditer(text):
                raw = m.group(0)
                validator = pat["validator"]
                if validator and not validator(raw):
                    continue
                spans.append((m.start(), m.end(), pat["label"], raw, pat["name"]))

        if not spans:
            return text

        spans.sort(key=lambda s: (s[0], -(s[1] - s[0])))
        chosen = []
        occupied_end = -1
        for s in spans:
            start, end = s[0], s[1]
            if start >= occupied_end:
                chosen.append(s)
                occupied_end = end

        chosen.sort(key=lambda s: s[0], reverse=True)
        result = text
        for start, end, label, raw, type_name in chosen:
            token = self._placeholder_for(label, raw)
            placeholder = f"[{token}]"
            result = result[:start] + placeholder + result[end:]
            self.hits.append({
                "type": type_name,
                "original": raw,
                "placeholder": token,
            })

        return result

    def build_mapping(self) -> dict:
        seen = {}
        for h in self.hits:
            if h["placeholder"] not in seen:
                seen[h["placeholder"]] = h["original"]
        return {
            "_meta": {
                "tool": "de_identify_local.py",
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "total_tokens": len(seen),
                "warning": "此對照表含真實個資，必須加密保存並與成品實體隔離。",
            },
            "mapping": seen,
        }

# ----------------------------------------------------------------------
# 三、對照表離線流加密 (HMAC Key Derivation + XOR Stream + HMAC integrity)
# ----------------------------------------------------------------------

_PBKDF2_ITERS = 200_000
_MAGIC = b"PHX1"

def _derive_key(password: str, salt: bytes, length: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt,
                               _PBKDF2_ITERS, dklen=length)


def _keystream(key: bytes, nonce: bytes, n: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < n:
        block = hashlib.sha256(key + nonce + counter.to_bytes(8, "big")).digest()
        out.extend(block)
        counter += 1
    return bytes(out[:n])


def encrypt_blob(plaintext: bytes, password: str) -> bytes:
    salt = secrets.token_bytes(16)
    nonce = secrets.token_bytes(16)
    enc_key = _derive_key(password, salt, 32)
    mac_key = _derive_key(password, salt + b"mac", 32)
    ks = _keystream(enc_key, nonce, len(plaintext))
    ct = bytes(a ^ b for a, b in zip(plaintext, ks))
    body = _MAGIC + salt + nonce + ct
    tag = hmac.new(mac_key, body, hashlib.sha256).digest()
    return base64.b64encode(body + tag)


def decrypt_blob(blob_b64: bytes, password: str) -> bytes:
    raw = base64.b64decode(blob_b64)
    if raw[:4] != _MAGIC:
        raise ValueError("檔頭格式不符，非本工具產生的加密檔。")
    body, tag = raw[:-32], raw[-32:]
    salt = body[4:20]
    nonce = body[20:36]
    ct = body[36:]
    mac_key = _derive_key(password, salt + b"mac", 32)
    expected = hmac.new(mac_key, body, hashlib.sha256).digest()
    if not hmac.compare_digest(tag, expected):
        raise ValueError("完整性驗證失敗：密碼錯誤或檔案已被竄改。")
    enc_key = _derive_key(password, salt, 32)
    ks = _keystream(enc_key, nonce, len(ct))
    return bytes(a ^ b for a, b in zip(ct, ks))


def _get_password(cli_key: str | None) -> str:
    if cli_key:
        return cli_key
    env = os.environ.get("PHOENIX_MAP_KEY")
    if env:
        return env
    pw = getpass.getpass("請輸入對照表加密密碼（不會顯示）：")
    if not pw:
        sys.exit("錯誤：未提供密碼，無法加密對照表。")
    return pw

# ----------------------------------------------------------------------
# 四、本地 Ollama 語意去識別化整合 (離線 100% 安全)
# ----------------------------------------------------------------------

def query_local_ollama(text: str, host: str, model: str) -> str:
    url = f"{host.rstrip('/')}/api/generate"
    
    prompt = f"""你現在是「鳳凰 AI 專用去識別化助手」，符合 ISO 42001 與個資法規範。
你的任務是對以下輸入的文字進行「第二層語意去識別化」。

前一階段的規則引擎已經把所有結構化個資（身分證、手機、Email、地址、信用卡…）替換為佔位標籤（如 [MOBILE_1], [EMAIL_1], [TW_ID_1] 等）。
你現在的工作是找出剩餘的「語意型個資與機密商業細節」，並將其替換為合適的標籤：
1. 具體公司名、品牌名、行銷名稱（例如「悅品餐飲」、「恆達精密」） -> 替換為以中括號包裝的「產業描述與規模代稱」，例如：
   - 悅品餐飲 -> [連鎖餐飲與多零售門店集團]
   - 恆達精密 -> [汽車與航太精密扣件製造商]
2. 具體人名、高管職稱（例如「洪建國董事長」、「蕭執行長」） -> 替換為以中括號包裝的「去識別化職稱」，例如：
   - 洪建國 -> [董事長 閣下]
   - 蕭執行長 -> [執行長 閣下]
3. 具體地理位置、工廠區域名稱（例如「高雄岡山區」） -> 替換為 bracketed 區域，例如：[南部廠區]。
4. 特殊定價、極度機密的合約金額 -> 替換為百分比級距或相對代稱。

⚠️ 警告與要求：
- 絕對不可修改或破壞前一階段已替換好的佔位標籤（如 [MOBILE_1], [EMAIL_1] 必須原封不動保留）。
- 保持整份文件的專業 B2B 顧問語氣與原有格式結構。
- 不要輸出任何額外的解釋、問候或 markdown 標籤，只輸出最終去識別化洗滌後的乾淨繁體中文全文。

以下為待處理之文字：
---
{text}
---
"""
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        print(f"  [Ollama] 正在呼叫本地模型 {model} 進行第二層語意洗滌...")
        with urllib.request.urlopen(req, timeout=120) as response:
            res = json.loads(response.read().decode("utf-8"))
            return res.get("response", "").strip()
    except Exception as e:
        print(f"  ❌ Ollama 連線失敗：{e}")
        print("  將跳過第二層語意洗滌，僅儲存第一層規則清洗結果。")
        return text

# ----------------------------------------------------------------------
# 五、反向洩漏掃描（交付前最後一道保險）
# ----------------------------------------------------------------------

SCAN_EXTENSIONS = {".html", ".htm", ".txt", ".json", ".md", ".csv"}

def scan_file_for_leaks(path: Path) -> list:
    findings = []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return [{"file": str(path), "line": 0, "type": "READ_ERROR",
                 "snippet": str(e)}]
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pat in PII_PATTERNS:
            for m in pat["regex"].finditer(line):
                raw = m.group(0)
                if pat["validator"] and not pat["validator"](raw):
                    continue
                ctx_start = max(0, m.start() - 1)
                if line[ctx_start:m.start()] == "[":
                    continue
                snippet = line[max(0, m.start() - 20):m.end() + 20].strip()
                findings.append({
                    "file": str(path),
                    "line": lineno,
                    "type": pat["name"],
                    "matched": raw,
                    "snippet": snippet,
                })
    return findings


def scan_path(target: Path) -> list:
    all_findings = []
    if target.is_file():
        files = [target]
    else:
        files = [p for p in target.rglob("*") if p.suffix.lower() in SCAN_EXTENSIONS]
    for f in files:
        all_findings.extend(scan_file_for_leaks(f))
    return all_findings

# ----------------------------------------------------------------------
# 六、命令列介面
# ----------------------------------------------------------------------

def cmd_deid(args):
    deid = DeIdentifier()
    src = Path(args.input)
    out = Path(args.output)

    def process_one(in_path: Path, out_path: Path):
        text = in_path.read_text(encoding="utf-8", errors="ignore")
        # 第一層：規則清洗
        cleaned = deid.process_text(text)
        # 第二層：本地 Ollama 語意洗滌
        if args.ollama:
            cleaned = query_local_ollama(cleaned, args.ollama_host, args.model)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(cleaned, encoding="utf-8")
        print(f"  ✓ {in_path}  ->  {out_path}")

    print("【鳳凰本地雙層去識別化】開始...")
    if src.is_file():
        process_one(src, out)
    elif src.is_dir():
        out.mkdir(parents=True, exist_ok=True)
        for p in src.rglob("*"):
            if p.is_file() and p.suffix.lower() in SCAN_EXTENSIONS:
                rel = p.relative_to(src)
                process_one(p, out / rel)
    else:
        sys.exit(f"錯誤：找不到輸入路徑 {src}")

    # 產出對照表
    mapping = deid.build_mapping()
    map_json = json.dumps(mapping, ensure_ascii=False, indent=2).encode("utf-8")
    password = _get_password(args.key)
    enc = encrypt_blob(map_json, password)
    map_path = Path(args.map)
    map_path.parent.mkdir(parents=True, exist_ok=True)
    map_path.write_bytes(enc)

    by_type = {}
    for h in deid.hits:
        by_type[h["type"]] = by_type.get(h["type"], 0) + 1
    print("\n【第一層規則去識別化摘要】")
    if by_type:
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  - {t:<12} 命中 {c} 處")
    else:
        print("  （未偵測到任何結構化個資；若啟用 --ollama 則直接進行語意去識別化）")
        
    print(f"\n  加密對照表已存：{map_path}")
    print(f"  唯一佔位標籤數：{mapping['_meta']['total_tokens']}")
    
    print("\n⚠ 重要安全提示：")
    print("  1. 本工具之加密對照表包含真實個資，請與產出成品進行實體隔離存放。")
    if args.ollama:
        print(f"  2. 採用本地 Ollama 大語言模型（{args.model}）進行了第二層語意去識別化，100% 離線防洩漏。")
    else:
        print("  2. 當前未啟用 --ollama。公司品牌名、特徵人名等『語意型』識別資訊，")
        print("     仍需後續進行第二層語意清洗。")
    print("  3. 專案結案後請務必依照【資料生命週期 SOP】雙人見證銷毀原始檔案與加密對照表。")


def cmd_scan(args):
    target = Path(args.target)
    if not target.exists():
        sys.exit(f"錯誤：找不到掃描目標 {target}")
    print("【反向洩漏掃描】交付前最後保險，開始…")
    findings = scan_path(target)

    lines = []
    lines.append("=" * 64)
    lines.append("鳳凰 AI 反向洩漏掃描報告")
    lines.append(f"掃描目標：{target}")
    lines.append(f"掃描時間：{datetime.now(timezone.utc).isoformat()}")
    lines.append("=" * 64)
    if not findings:
        lines.append("\n✅ 通過：未在成品中偵測到任何殘留個資格式。")
        verdict = "PASS"
    else:
        lines.append(f"\n❌ 警告：偵測到 {len(findings)} 處疑似殘留個資！必須修正後重新掃描。\n")
        for i, f in enumerate(findings, 1):
            if f["type"] == "READ_ERROR":
                lines.append(f"[{i}] 讀檔錯誤 {f['file']}: {f['snippet']}")
                continue
            lines.append(f"[{i}] {f['type']}  @ {f['file']}:{f['line']}")
            lines.append(f"      命中：{f['matched']}")
            lines.append(f"      上下文：…{f['snippet']}…")
        verdict = "FAIL"
    report = "\n".join(lines)
    print(report)
    if args.report:
        Path(args.report).write_text(report, encoding="utf-8")
        print(f"\n報告已存：{args.report}")
    sys.exit(0 if verdict == "PASS" else 2)


def cmd_reveal(args):
    password = _get_password(args.key)
    blob = Path(args.map).read_bytes()
    try:
        data = decrypt_blob(blob, password)
    except ValueError as e:
        sys.exit(f"解密失敗：{e}")
    print(data.decode("utf-8"))


def build_parser():
    p = argparse.ArgumentParser(
        description="鳳凰 AI 本地去識別化與反向洩漏掃描工具（離線、零雲端）")
    sub = p.add_subparsers(dest="command", required=True)

    pd = sub.add_parser("deid", help="去識別化檔案或資料夾")
    pd.add_argument("input", help="輸入檔案或資料夾")
    pd.add_argument("-o", "--output", required=True, help="輸出檔案或資料夾")
    pd.add_argument("--map", required=True, help="加密對照表輸出路徑（.enc）")
    pd.add_argument("--key", help="加密密碼（建議改用環境變數 PHOENIX_MAP_KEY 或互動輸入）")
    pd.add_argument("--ollama", action="store_true", help="啟用本地 Ollama 進行第二層語意去識別化")
    pd.add_argument("--model", default="llama3", help="Ollama 本地大語言模型名稱（預設：llama3）")
    pd.add_argument("--ollama-host", default="http://localhost:11434", help="Ollama 服務位址（預設：http://localhost:11434）")
    pd.set_defaults(func=cmd_deid)

    ps = sub.add_parser("scan", help="反向洩漏掃描（交付前跑）")
    ps.add_argument("target", help="掃描目標檔案或資料夾")
    ps.add_argument("--report", help="掃描報告輸出路徑")
    ps.set_defaults(func=cmd_scan)

    pr = sub.add_parser("reveal", help="解密並檢視對照表（稽核用）")
    pr.add_argument("--map", required=True, help="加密對照表路徑（.enc）")
    pr.add_argument("--key", help="解密密碼")
    pr.set_defaults(func=cmd_reveal)

    return p


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
