#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_all2.py — 鳳凰 AI 一鍵修復（修正版）。放 repo 根目錄，執行一次。
改進：1) 新金鑰在動檔案前先存檔，不會遺失；2) 開不了的 vault 跳過並列出，不中止。
用法：  python fix_all2.py
"""
import os, sys, re, json, ast, glob, shutil, secrets, string

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, "scripts")
OLD_KEY = "phoenix_ai_vault_2026"

def fail(msg):
    print("！ 中止：", msg)
    sys.exit(1)

try:
    from de_identify_local import decrypt_blob, encrypt_blob
except Exception as e:
    fail(f"無法匯入 scripts/de_identify_local.py：{e}")

# 取得/產生新金鑰，並『立刻』存檔（避免中途中止遺失）
NEW_KEY = os.environ.get("PHOENIX_MAP_KEY")
generated = False
if not NEW_KEY or NEW_KEY == OLD_KEY:
    NEW_KEY = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
    generated = True
os.makedirs("_C2_mapping_vault", exist_ok=True)
if generated:
    open("_C2_mapping_vault/NEW_KEY.txt", "w", encoding="utf-8").write(NEW_KEY)
    print(f"※ 已產生新金鑰並先存到 _C2_mapping_vault/NEW_KEY.txt（之後請搬進密碼管理器再刪）")

# ---- 1) 輪換金鑰（容錯：開不了就跳過並記錄）----
maps = glob.glob("_C2_mapping_vault/**/map.enc", recursive=True)
skipped = []
for p in maps:
    blob = open(p, "rb").read()
    plain, used = None, None
    for k in (OLD_KEY, NEW_KEY):
        try:
            plain = decrypt_blob(blob, k); used = k; break
        except Exception:
            continue
    if plain is None:
        skipped.append(p); print(f"  ⚠ 跳過（新舊鑰都開不了，可能用了其他密碼）：{p}"); continue
    if used == NEW_KEY:
        print(f"  跳過（已是新鑰）：{p}"); continue
    shutil.copy(p, p + ".bak")
    nb = encrypt_blob(plain, NEW_KEY)
    if decrypt_blob(nb, NEW_KEY) != plain:
        skipped.append(p); print(f"  ⚠ 跳過（重加密驗證失敗）：{p}"); continue
    open(p, "wb").write(nb); print(f"  已換鑰：{p}")
print(f"[1/4] 金鑰輪換完成（成功 {len(maps)-len(skipped)} / 共 {len(maps)}）")

# ---- 2) 抽出並加密 CLIENT_CATALOG ----
PIPE = "scripts/phoenix_b2b_pipeline.py"
if not os.path.exists(PIPE):
    fail(f"找不到 {PIPE}")
src = open(PIPE, encoding="utf-8").read()
node = None
for n in ast.walk(ast.parse(src)):
    if isinstance(n, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "CLIENT_CATALOG" for t in n.targets):
        node = n
if node is None:
    print("[2/4] 找不到 CLIENT_CATALOG（可能已外部化），略過")
    catalog = None
else:
    catalog = ast.literal_eval(node.value)
    out = "_C2_mapping_vault/client_catalog.enc"
    data = json.dumps(catalog, ensure_ascii=False).encode("utf-8")
    open(out, "wb").write(encrypt_blob(data, NEW_KEY))
    if json.loads(decrypt_blob(open(out, "rb").read(), NEW_KEY).decode("utf-8")) != catalog:
        fail("catalog 加密驗證失敗")
    print(f"[2/4] CLIENT_CATALOG 已加密寫入 {out}（{len(catalog)} 筆）")

# ---- 3) 改寫 pipeline ----
shutil.copy(PIPE, PIPE + ".bak")
new = src
if node is not None:
    lines = new.splitlines(keepends=True)
    s, e = node.lineno - 1, node.end_lineno
    indent = re.match(r'[ \t]*', lines[s]).group(0)
    lines[s:e] = [f"{indent}CLIENT_CATALOG = load_client_catalog()\n"]
    new = "".join(lines)
new = re.sub(r'\n[ \t]*my_env\["PHOENIX_MAP_KEY"\]\s*=\s*"[^"]*"',
             '\n    _require_key()', new, count=1)
helpers = (
    '\ndef _require_key():\n'
    '    key = os.environ.get("PHOENIX_MAP_KEY")\n'
    '    if not key:\n'
    '        log_error("未設定環境變數 PHOENIX_MAP_KEY，停止。")\n'
    '        sys.exit(1)\n'
    '    return key\n\n'
    'def load_client_catalog():\n'
    '    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\n'
    '    from de_identify_local import decrypt_blob\n'
    '    p = "_C2_mapping_vault/client_catalog.enc"\n'
    '    if not os.path.exists(p):\n'
    '        log_error("找不到 " + p + "，請先執行 fix_all2.py。")\n'
    '        sys.exit(1)\n'
    '    try:\n'
    '        return json.loads(decrypt_blob(open(p, "rb").read(), _require_key()).decode("utf-8"))\n'
    '    except Exception as e:\n'
    '        log_error("客戶對照表解密失敗：" + str(e))\n'
    '        sys.exit(1)\n\n'
)
if "def load_client_catalog" not in new:
    new = new.replace("def run_init(", helpers + "def run_init(", 1)
try:
    compile(new, PIPE, "exec")
except SyntaxError as ex:
    shutil.copy(PIPE + ".bak", PIPE)
    fail(f"改寫後語法錯誤，已還原 .bak：{ex}")
open(PIPE, "w", encoding="utf-8").write(new)
print("[3/4] phoenix_b2b_pipeline.py 已改寫（移除硬編碼金鑰 + 執行期載入 catalog）")

# ---- 4) 掃除 scripts/*.py 殘留真名 ----
NAME_MAP = {
    "振豐精密": "CLIENT_FASTENER", "振豐": "CLIENT_FASTENER",
    "隆達精密": "CLIENT_FORGE", "隆達": "CLIENT_FORGE",
    "宏達熱處理": "CLIENT_HEAT", "宏達": "CLIENT_HEAT",
    "吉翔航太": "CLIENT_CBAM", "吉翔": "CLIENT_CBAM",
    "聯發光學": "CLIENT_FILTER", "聯發": "CLIENT_FILTER",
    "振鑫表面": "CLIENT_PLATE", "振鑫": "CLIENT_PLATE",
    "龍門冷鐓": "CLIENT_COLDHEAD", "龍門": "CLIENT_COLDHEAD",
    "興達包裝": "CLIENT_BARCODE", "興達": "CLIENT_BARCODE",
    "龍圖機械": "CLIENT_SBIR", "龍圖": "CLIENT_SBIR",
    "恆達": "CLIENT_HENDA", "悅品": "CLIENT_YUEPIN", "鼎泰證券": "CLIENT_SEC",
    "陳茂雄": "PERSON", "王茂雄": "PERSON", "高志明": "PERSON",
    "陳春桂": "PERSON", "蔡嘉玲": "PERSON", "陳建忠": "PERSON",
}
swept = 0
for py in glob.glob("scripts/*.py"):
    t = open(py, encoding="utf-8").read()
    orig = t
    for a, b in NAME_MAP.items():
        t = t.replace(a, b)
    if t != orig:
        shutil.copy(py, py + ".bak")
        open(py, "w", encoding="utf-8").write(t)
        swept += 1
        print(f"  已掃除真名：{py}")
print(f"[4/4] scripts 真名掃除完成，共處理 {swept} 檔")

# ---- 完成 ----
print("\n========== 完成 ==========")
if generated:
    print("新金鑰請『永久』設定（複製整行貼到 PowerShell，然後重開終端機）：")
    print(f'  setx PHOENIX_MAP_KEY "{NEW_KEY}"')
    print("（金鑰也已暫存於 _C2_mapping_vault/NEW_KEY.txt，搬進密碼管理器後請刪除該檔）")
else:
    print("沿用既有環境變數 PHOENIX_MAP_KEY。")
if skipped:
    print("\n⚠ 下列 vault 當初用了不同密碼、未換鑰，請另外處理（不影響上面其他修復）：")
    for p in skipped:
        print("   -", p)
print("\n仍需你手動、可延後：A. 清 Git 歷史 force-push  B. 驗證後刪 *.bak  C. 測試 compile")
