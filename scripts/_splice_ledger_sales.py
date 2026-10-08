# splice ledger_container into build_solution_pages_20260809.py
from pathlib import Path

gen = Path(r"C:/Users/m1016/Documents/AI_Talent/scripts/build_solution_pages_20260809.py")
html = Path(r"C:/Users/m1016/Documents/AI_Talent/scripts/_ledger_sales_container.html").read_text(encoding="utf-8")
src = gen.read_text(encoding="utf-8")
start = src.index("ledger_container = \"\"\"")
end = src.index("# ── AI Allocation OS ──")
new_block = "ledger_container = \"\"\"" + html.rstrip() + "\n\"\"\"\n"
src = src[:start] + new_block + src[end:]
old_call = 'build("ledger-assist", ledger_container, "ledger_assist", "AI 會計工作台", "Accounting · LINE Workflow")'
new_call = (
    'build("ledger-assist", ledger_container, "ledger_assist", "AI 會計工作台", '
    '"給會計師事務所", '
    'meta_desc="客戶發票還在手上，掃描機解不了交件。AI 會計工作台：LINE 拍照上傳、人覆核後才匯出，每所私有部署。")'
)
if old_call not in src:
    raise SystemExit("build() call not found")
src = src.replace(old_call, new_call, 1)
gen.write_text(src, encoding="utf-8")
print("spliced", gen, "container_chars", len(html))
