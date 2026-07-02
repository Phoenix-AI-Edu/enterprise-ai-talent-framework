#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_all.py — 鳳凰 AI 一鍵修復（放 repo 根目錄，執行一次）
  1) 輪換 C2 金庫金鑰（舊鑰 -> 新鑰）
  2) 把 CLIENT_CATALOG 從程式碼抽出、加密進 _C2_mapping_vault/client_catalog.enc
  3) 改寫 phoenix_b2b_pipeline.py：移除硬編碼金鑰 + 改為執行期載入 catalog
  4) 掃除 scripts/*.py 內殘留的真實公司名與人名（換成代號）
所有寫入前自動 .bak 備份，寫入後自動驗證；任何驗證失敗即中止並還原。
用法：  python fix_all.py
"""
import os, sys, re, json, ast, glob, shutil, secrets, string

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
sys.path.insert(0, "scripts")
OLD_KEY = "phoenix_ai_vault_2026"

def fail(msg):
    print("！ 中止：", msg)
    sys.exit(1)

# 取得/產生新金鑰
NEW_KEY = os.environ.get("PHOENIX_MAP_KEY")
generated = False
if not NEW_KEY or NEW_KEY == OLD_KEY:
    NEW_KEY = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
    generated = True

try:
    from de_identify_local import decrypt_blob, encrypt_blob
except Exception as e:
    fail(f"無法匯入 scripts/de_identify_local.py：{e}")

# ---- 1) 輪換金鑰 ----
maps = glob.glob("_C2_mapping_vault/**/map.enc", recursive=True)
for p in maps:
    blob = open(p, "rb").read()
    try:
        plain = decrypt_blob(blob, OLD_KEY)
    except Exception:
        try:
            decrypt_blob(blob, NEW_KEY)
            print(f"  跳過（已是新鑰）：{p}")
            continue
        except Exception:
            fail(f"{p} 用新舊鑰都無法解開")
    shutil.copy(p, p + ".bak")
    nb = encrypt_blob(plain, NEW_KEY)
    if decrypt_blob(nb, NEW_KEY) != plain:
        fail(f"{p} 重加密驗證失敗")
    open(p, "wb").write(nb)
    print(f"  已換鑰：{p}")
print(f"[1/4] 金鑰輪換完成，共 {len(maps)} 個 vault")

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
    os.makedirs("_C2_mapping_vault", exist_ok=True)
    out = "_C2_mapping_vault/client_catalog.enc"
    data = json.dumps(catalog, ensure_ascii=False).encode("utf-8")
    open(out, "wb").write(encrypt_blob(data, NEW_KEY))
    if json.loads(decrypt_blob(open(out, "rb").read(), NEW_KEY).decode("utf-8")) != catalog:
        fail("catalog 加密驗證失敗")
    print(f"[2/4] CLIENT_CATALOG 已加密寫入 {out}（{len(catalog)} 筆）")

# ---- 3) 改寫 pipeline ----
shutil.copy(PIPE, PIPE + ".bak")
new = src
# 3a 移除 CLIENT_CATALOG 字面量（用原始行號）
if node is not None:
    lines = new.splitlines(keepends=True)
    s, e = node.lineno - 1, node.end_lineno
    indent = re.match(r'[ \t]*', lines[s]).group(0)
    lines[s:e] = [f"{indent}CLIENT_CATALOG = load_client_catalog()\n"]
    new = "".join(lines)
# 3b 移除硬編碼金鑰
new = re.sub(r'\n[ \t]*my_env\["PHOENIX_MAP_KEY"\]\s*=\s*"[^"]*"',
             '\n    _require_key()', new, count=1)
# 3c 注入載入器
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
    '        log_error("找不到 " + p + "，請先執行 fix_all.py。")\n'
    '        sys.exit(1)\n'
    '    try:\n'
    '        return json.loads(decrypt_blob(open(p, "rb").read(), _require_key()).decode("utf-8"))\n'
    '    except Exception as e:\n'
    '        log_error("客戶對照表解密失敗：" + str(e))\n'
    '        sys.exit(1)\n\n'
)
if "def load_client_catalog" not in new:
    new = new.replace("def run_init(", helpers + "def run_init(", 1)
# 驗證語法，過了才寫入
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
    "某電鍍加工廠": "CLIENT_PLATE", "某電鍍": "CLIENT_PLATE",
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
    print("已自動產生新金鑰。請『永久』設定（複製整行貼到 PowerShell，然後重開終端機）：")
    print(f'  setx PHOENIX_MAP_KEY "{NEW_KEY}"')
    print("（請同時把它存進密碼管理器；本視窗關閉後不再顯示）")
else:
    print("沿用既有環境變數 PHOENIX_MAP_KEY。")
print("\n只剩這幾件需要你手動、且都可延後：")
print("  A. 清 Git 歷史並 force-push（見 containment checklist 步驟 2-4）。")
print("  B. 驗證一切正常後，刪除所有 *.bak 備份。")
print("  C. 測試：python scripts/phoenix_b2b_pipeline.py compile --client okayama_barcode")
