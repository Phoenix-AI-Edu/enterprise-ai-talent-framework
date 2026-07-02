# -*- coding: utf-8 -*-
"""
validate_notion_tables.py — B2B AI 落地 Notion 四大專家資料庫 100% 欄位填滿率稽核腳本
========================================================================
This script performs a rigorous, professional audit on the 4 Notion Master 
Databases embedded in the 9 Okayama Precision Manufacturing Cluster proposals.
It ensures zero empty cells, zero placeholders (N/A, TBD, 同上, 無), and 
perfect structural alignment across all cases.
========================================================================
"""

import os
import re
import sys

# 強制設定 UTF-8 輸出，防範 Windows 環境編碼異常
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def log_banner():
    print("="*80)
    print("   📊  PHOENIX AI B2B AUDIT GATE — NOTION MASTER DATABASE INTEGRITY SCAN   ")
    print("      Target: 9 Okayama Precision Manufacturing & Forging Cluster Cases")
    print("="*80)

def parse_markdown_tables(content):
    """
    Parses all markdown tables in the content.
    Returns a list of tables, where each table is a dict:
    {
        "header": [col1, col2, ...],
        "rows": [[cell1, cell2, ...], ...],
        "start_line": int
    }
    """
    lines = content.splitlines()
    tables = []
    in_table = False
    current_table = None
    
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        # Markdown table row starts and ends with '|'
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            
            # Skip separator rows (e.g. |---|---| or |:---|:---|)
            if all(re.match(r'^:?-+:?$', c) for c in cells):
                continue
                
            if not in_table:
                in_table = True
                current_table = {
                    "header": cells,
                    "rows": [],
                    "start_line": idx
                }
            else:
                current_table["rows"].append(cells)
        else:
            if in_table:
                if current_table and current_table["rows"]:
                    tables.append(current_table)
                in_table = False
                current_table = None
                
    if in_table and current_table and current_table["rows"]:
        tables.append(current_table)
        
    return tables

def audit_table(file_name, table_idx, table):
    """
    Audits a parsed markdown table for placeholders and structural errors.
    """
    errors = []
    placeholders = ["無", "同上", "n/a", "tbd", "placeholder", "todo", "待定", "空白"]
    
    # Check column count alignment
    expected_cols = len(table["header"])
    
    for row_idx, row in enumerate(table["rows"], 1):
        if len(row) != expected_cols:
            errors.append(
                f"Line {table['start_line'] + row_idx}: Column count mismatch. "
                f"Header has {expected_cols} cols, but Row {row_idx} has {len(row)} cols."
            )
            continue
            
        for col_idx, cell in enumerate(row):
            clean_cell = cell.strip()
            
            # Check empty cell
            if not clean_cell:
                errors.append(
                    f"Line {table['start_line'] + row_idx}: Empty cell found in column "
                    f"'{table['header'][col_idx]}' (Col {col_idx+1})."
                )
                continue
                
            # Remove formatting markdown symbols for pure string comparison
            stripped_text = re.sub(r'[\*_`~]', '', clean_cell).strip()
            lower_cell = stripped_text.lower()
            
            is_placeholder = False
            # Check for exact matches
            if lower_cell in ["無", "無此", "同上", "n/a", "na", "tbd", "todo", "placeholder", "待定", "空白", "none", "null", "---", "-"]:
                is_placeholder = True
            # Check if very short string contains placeholders
            elif len(stripped_text) <= 4 and any(p in lower_cell for p in ["無", "同上", "na", "tbd", "todo"]):
                is_placeholder = True
            # Check if empty of meaningful characters
            elif not re.search(r'[\u4e00-\u9fa5\w]', stripped_text):
                is_placeholder = True
                
            if is_placeholder:
                errors.append(
                    f"Line {table['start_line'] + row_idx}: Lazy placeholder/empty content '{clean_cell}' "
                    f"found in column '{table['header'][col_idx]}' (Col {col_idx+1})."
                )
                
    return errors

def main():
    log_banner()
    
    cases = [
        {"key": "okayama_fastener", "file": "scripts/proposal_okayama_fastener.md", "name": "PHX-001 PMC 岡山扣件廠 (振豐精密)"},
        {"key": "okayama_forge", "file": "scripts/proposal_okayama_forge.md", "name": "PHX-021 冷鍛模具崩損岡山廠 (隆達精密)"},
        {"key": "okayama_heat", "file": "scripts/proposal_okayama_heat.md", "name": "PHX-022 高強度熱處理離線廠 (宏達熱處理)"},
        {"key": "okayama_cbam", "file": "scripts/proposal_okayama_cbam.md", "name": "PHX-023 航太扣件歐盟CBAM (吉翔航太)"},
        {"key": "okayama_filter", "file": "scripts/proposal_okayama_filter.md", "name": "PHX-024 影像篩選缺陷誤報 (聯發光學)"},
        {"key": "okayama_electroplate", "file": "scripts/proposal_okayama_electroplate.md", "name": "PHX-025 電鍍配方環保排污 (某電鍍加工廠)"},
        {"key": "luzhu_coldheading", "file": "scripts/proposal_luzhu_coldheading.md", "name": "PHX-026 路竹冷鐓停機預警 (龍門冷鐓)"},
        {"key": "okayama_barcode", "file": "scripts/proposal_okayama_barcode.md", "name": "PHX-027 條碼防錯中高齡安心 (興達包裝)"},
        {"key": "okayama_sbir", "file": "scripts/proposal_okayama_sbir.md", "name": "PHX-033 製造智慧防護SBIR (龍圖機械)"}
    ]
    
    overall_errors = 0
    overall_checked_tables = 0
    
    for case in cases:
        file_path = case["file"]
        print(f"\n🔍 審查 {case['name']} 的 Notion 知識庫段落...")
        
        if not os.path.exists(file_path):
            print(f"❌ [錯誤] 找不到建議書文件：{file_path}")
            overall_errors += 1
            continue
            
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse all markdown tables
        all_tables = parse_markdown_tables(content)
        
        # We expect exactly 4 Notion tables at the end of the proposal
        # (There might be a few standard markdown tables in Part 1 or 2, but the Notion database tables
        # are definitely present in Part 4. We will audit all tables found to be extra safe!)
        if len(all_tables) < 4:
            print(f"⚠️  [警告] 預計應有至少 4 張 Notion 資料表，實際僅偵測到 {len(all_tables)} 張表。")
            overall_errors += 1
            
        case_errors = 0
        for idx, table in enumerate(all_tables, 1):
            table_title = f"Table {idx} (Line {table['start_line']})"
            
            # Dynamically identify Notion tables by columns
            headers_str = "".join(table["header"])
            if "痛點" in headers_str or "RAG" in headers_str or "路徑" in headers_str or "試點" in headers_str or "HITL" in headers_str or "敏感" in headers_str or "治理" in headers_str or "變革" in headers_str:
                table_title = f"Notion Master Table (Col 1: '{table['header'][0]}')"
            
            errors = audit_table(file_path, idx, table)
            overall_checked_tables += 1
            
            if errors:
                print(f"  ❌ [{table_title}] 偵測到 {len(errors)} 個合規缺陷：")
                for err in errors:
                    print(f"     ↳ {err}")
                case_errors += len(errors)
                overall_errors += len(errors)
            else:
                print(f"  ✅ [{table_title}] 結構完整，100% 屬性填滿（欄位共 {len(table['header'])}，資料列共 {len(table['rows'])} 列）")
                
        if case_errors == 0:
            print(f"  🎉 {case['name']} Notion 資料表 100% 綠燈合規！")
            
    print("\n" + "="*80)
    print("      📊 PHOENIX B2B NOTION 資料表總體合規審核報告")
    print("="*80)
    print(f" 審核案例數：{len(cases)} 個")
    print(f" 審查資料表：{overall_checked_tables} 張")
    print(f" 缺陷總數：{'🔴 ' + str(overall_errors) if overall_errors > 0 else '🟢 0 (完美合規)'}")
    print("-"*80)
    if overall_errors == 0:
        print(" 👑 【卓越品質驗收】恭喜！所有精密製造案例的 Notion 資料表均已 100% 填滿且零空白/占位符！")
    else:
        print(" ⚠️  【品質警報】請根據上方報告修正對應 Markdown 建議書中的 Notion 資料表欄位！")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
