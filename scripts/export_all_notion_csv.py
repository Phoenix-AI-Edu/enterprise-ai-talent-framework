# -*- coding: utf-8 -*-
"""
export_all_notion_csv.py — 批次導出 9 大企業案例 Notion 資料表為 CSV (一鍵匯入 Notion)
========================================================================
This script extracts the 4 Notion tables from all 9 Okayama proposals, 
cleans formatting, merges the rows, and exports 4 unified CSV files.
These files can be imported directly into Notion in 1 click!
========================================================================
"""

import os
import re
import csv
import sys
import codecs

# 強制設定 UTF-8 輸出
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def log_banner():
    print("="*80)
    print("   🚀  PHOENIX AI B2B CSV EXPORTER — NOTION ONE-CLICK MERGE ENGINE   ")
    print("      Target: Combined 4 databases from 9 Okayama cluster cases")
    print("="*80)

def extract_tables_from_file(file_path):
    """
    Extracts all tables from a markdown file as rows of strings.
    """
    if not os.path.exists(file_path):
        return []
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.splitlines()
    tables = []
    in_table = False
    current_table = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            
            # Skip separator rows like |---|---|
            if all(re.match(r'^:?-+:?$', c) for c in cells):
                continue
                
            if not in_table:
                in_table = True
                current_table = [cells]
            else:
                current_table.append(cells)
        else:
            if in_table:
                if len(current_table) > 1:
                    tables.append(current_table)
                in_table = False
                current_table = []
                
    if in_table and len(current_table) > 1:
        tables.append(current_table)
        
    return tables

def classify_table(headers):
    headers_str = "".join(headers)
    if "痛點" in headers_str or "評估" in headers_str or "優先" in headers_str:
        return 1
    elif "路徑" in headers_str or "防線" in headers_str or "審計" in headers_str:
        return 2
    elif "試點" in headers_str or "KPI" in headers_str or "阻力" in headers_str:
        return 3
    elif "協作" in headers_str or "LLMOps" in headers_str or "熔斷" in headers_str:
        return 4
    return 0

def clean_text(text):
    # Remove markdown bold/italic formatting
    text = re.sub(r'[\*_`~]', '', text)
    # Standardize spaces
    return text.strip()

def main():
    log_banner()
    
    cases = [
        {"file": "scripts/proposal_okayama_fastener.md", "name": "PHX-001 PMC 岡山扣件廠 (振豐精密)"},
        {"file": "scripts/proposal_okayama_forge.md", "name": "PHX-021 冷鍛模具崩損岡山廠 (隆達精密)"},
        {"file": "scripts/proposal_okayama_heat.md", "name": "PHX-022 高強度熱處理離線廠 (宏達熱處理)"},
        {"file": "scripts/proposal_okayama_cbam.md", "name": "PHX-023 航太扣件歐盟CBAM (吉翔航太)"},
        {"file": "scripts/proposal_okayama_filter.md", "name": "PHX-024 影像篩選缺陷誤報 (聯發光學)"},
        {"file": "scripts/proposal_okayama_electroplate.md", "name": "PHX-025 電鍍配方環保排污 (某電鍍加工廠)"},
        {"file": "scripts/proposal_luzhu_coldheading.md", "name": "PHX-026 路竹冷鐓停機預警 (龍門冷鐓)"},
        {"file": "scripts/proposal_okayama_barcode.md", "name": "PHX-027 條碼防錯中高齡安心 (興達包裝)"},
        {"file": "scripts/proposal_okayama_sbir.md", "name": "PHX-033 製造智慧防護SBIR (龍圖機械)"}
    ]
    
    # 4 DBs combined lists
    db_lists = {1: [], 2: [], 3: [], 4: []}
    db_headers = {1: None, 2: None, 3: None, 4: None}
    
    for case in cases:
        file_path = case["file"]
        if not os.path.exists(file_path):
            print(f"⚠️  找不到檔案: {file_path}，跳過。")
            continue
            
        tables = extract_tables_from_file(file_path)
        for t in tables:
            header = t[0]
            db_class = classify_table(header)
            if db_class in [1, 2, 3, 4]:
                if db_headers[db_class] is None:
                    db_headers[db_class] = header
                    
                rows = t[1:]
                for r in rows:
                    cleaned_row = [clean_text(cell) for cell in r]
                    # Fill missing cells or pad
                    while len(cleaned_row) < len(header):
                        cleaned_row.append("")
                    db_lists[db_class].append(cleaned_row)
                    
    # Export 4 CSV files
    db_names = {
        1: "1_企業_AI_場景盤點資料庫_岡山九校聯播.csv",
        2: "2_資料基礎與方案架構資料庫_岡山九校聯播.csv",
        3: "3_試點驗證與阻力評估資料庫_岡山九校聯播.csv",
        4: "4_營運_治理與組織變革資料庫_岡山九校聯播.csv"
    }
    
    output_dir = "scripts"
    print("\n📦 開始批次導出至 Google Drive...")
    
    for db_idx in [1, 2, 3, 4]:
        file_name = db_names[db_idx]
        file_path = os.path.join(output_dir, file_name)
        root_path = file_name # Also export to root directory for easier user click!
        
        headers = db_headers[db_idx]
        rows = db_lists[db_idx]
        
        if not headers or not rows:
            print(f"⚠️  資料庫 {db_idx} 沒有資料，跳過。")
            continue
            
        # Write to scripts folder and root folder with UTF-8 BOM
        for path in [file_path, root_path]:
            with open(path, "w", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)
                
        print(f"  ✅ [匯出成功] 匯出 {len(rows)} 列數據 ➔ {root_path}")
        
    print("\n" + "="*80)
    print("      🎉 NOTION ONE-CLICK MERGE CSV FILES GENERATED SUCCESSFULLY!")
    print("="*80)
    print(" 檔案位置：專案根目錄 (已匯出成帶有 Excel 相容 BOM 的 UTF-8 格式 CSV)")
    print(" 1. 1_企業_AI_場景盤點資料庫_岡山九校聯播.csv")
    print(" 2. 2_資料基礎與方案架構資料庫_岡山九校聯播.csv")
    print(" 3. 3_試點驗證與阻力評估資料庫_岡山九校聯播.csv")
    print(" 4. 4_營運_治理與組織變革資料庫_岡山九校聯播.csv")
    print("-"*80)
    print(" 💡 接下來，請參考說明書的「Merge with CSV」步驟，將這些檔案一鍵匯入您的 Notion！")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
