# -*- coding: utf-8 -*-
import csv
import sys
import os

def run_deep_audit():
    files = [
        '1_企業_AI_場景盤點資料庫_岡山九校聯播.csv',
        '2_資料基礎與方案架構資料庫_岡山九校聯播.csv',
        '3_試點驗證與阻力評估資料庫_岡山九校聯播.csv',
        '4_營運_治理與組織變革資料庫_岡山九校聯播.csv'
    ]
    
    report = []
    report.append("================================================================================")
    report.append("        PHOENIX AI NOTION MASTER DATABASES - COMPREHENSIVE DEEP AUDIT REPORT   ")
    report.append("================================================================================")
    
    # 1. Check file existence
    data = {}
    for f in files:
        if not os.path.exists(f):
            report.append(f"❌ Error: File {f} does not exist!")
            return "\n".join(report)
        with open(f, 'r', encoding='utf-8-sig') as file:
            reader = list(csv.reader(file))
            rows = [row for row in reader if row and any(cell.strip() for cell in row)]
            data[f] = rows
            report.append(f"✅ Loaded {f}: {len(rows)} rows (1 header + {len(rows)-1} data rows)")
            
    report.append("\n" + "="*80)
    report.append("1. STRUCTURAL AND ROW COUNT ALIGNMENT CHECK")
    report.append("="*80)
    
    # Check row counts
    counts = {f: len(data[f]) for f in files}
    all_equal = len(set(counts.values())) == 1
    if all_equal:
        report.append(f"✅ Row Count Alignment: Perfect! All files have exactly {counts[files[0]]} rows.")
    else:
        report.append("❌ Row Count Mismatch!")
        for f, cnt in counts.items():
            report.append(f"   - {f}: {cnt} rows")
            
    # Check columns
    report.append("\nDatabase Columns:")
    for f in files:
        headers = data[f][0]
        report.append(f"  • {f}:")
        report.append(f"    Columns ({len(headers)}): {', '.join(headers)}")
        
    report.append("\n" + "="*80)
    report.append("2. PRIMARY KEY RELATIONSHIP & SEMANTIC ALIGNMENT SCANS")
    report.append("="*80)
    report.append("Checking row-by-row mapping between DB1 (對應場景專案) and DB2/3/4 (對應場景專案):")
    
    pk_mismatches = []
    for idx in range(1, 46):
        pk1 = data[files[0]][idx][0].strip()
        pk2 = data[files[1]][idx][0].strip()
        pk3 = data[files[2]][idx][0].strip()
        pk4 = data[files[3]][idx][0].strip()
        
        # Check alignment among DB1, DB2, DB3, DB4
        all_aligned = (pk1 == pk2 == pk3 == pk4)
        
        if not all_aligned:
            pk_mismatches.append((idx, pk1, pk2, pk3, pk4))
            
    if pk_mismatches:
        report.append(f"🚨 Found {len(pk_mismatches)} rows with primary key mismatches:")
        for idx, p1, p2, p3, p4 in pk_mismatches:
            report.append(f"  Row {idx}:")
            report.append(f"    DB1: \"{p1}\"")
            report.append(f"    DB2: \"{p2}\"")
            report.append(f"    DB3: \"{p3}\"")
            report.append(f"    DB4: \"{p4}\"")
    else:
        report.append("✅ All 4 databases have 100% identical primary keys across all 45 rows! Relations will match perfectly in Notion!")
        
    report.append("\n" + "="*80)
    report.append("3. DATA QUALITY, EMPTY CELLS, AND PLACEHOLDER DETECTIONS")
    report.append("="*80)
    
    placeholders = ["無", "無此", "同上", "n/a", "na", "tbd", "todo", "placeholder", "待定", "空白", "none", "null", "---", "-"]
    lazy_count = 0
    empty_count = 0
    
    for f in files:
        headers = data[f][0]
        for row_idx, row in enumerate(data[f][1:], 1):
            # Check length mismatch
            if len(row) != len(headers):
                report.append(f"🚨 Row Length Mismatch in {f} at Row {row_idx}: expected {len(headers)} columns, got {len(row)}.")
                continue
            for col_idx, cell in enumerate(row):
                val = cell.strip()
                if not val:
                    empty_count += 1
                    report.append(f"⚠️ Empty cell: {f} -> Row {row_idx}, Col '{headers[col_idx]}'")
                elif val.lower() in placeholders:
                    lazy_count += 1
                    report.append(f"⚠️ Placeholder '{val}': {f} -> Row {row_idx}, Col '{headers[col_idx]}'")
                    
    report.append(f"\nScan complete: Found {empty_count} empty cells and {lazy_count} placeholders.")
    
    report.append("\n" + "="*80)
    report.append("4. DETAILED DATA METRICS AND VALUE ANOMALIES")
    report.append("="*80)
    
    # Analyze priorities and ROI in DB1
    db1_rows = data[files[0]]
    priorities = {}
    roi_errors = []
    
    for idx, row in enumerate(db1_rows[1:], 1):
        # Column 8 is priority in new 9-column format
        prio = row[8].strip() if len(row) > 8 else "N/A"
        # Column 7 is ROI in new 9-column format
        roi_str = row[7].strip() if len(row) > 7 else "N/A"
        
        priorities[prio] = priorities.get(prio, 0) + 1
        
        try:
            val_clean = roi_str.strip()
            val_float = float(val_clean)
        except ValueError:
            roi_errors.append((idx, row[0], roi_str))
            
    report.append("Database 1 - Priority Distribution:")
    for prio, count in priorities.items():
        report.append(f"  • {prio}: {count} cases")
        
    if roi_errors:
        report.append("\n🚨 ROI Index parsing anomalies (non-numeric or irregular formats):")
        for idx, name, val in roi_errors:
            report.append(f"  Row {idx}: \"{name[:20]}...\" has ROI value \"{val}\"")
    else:
        report.append("\n✅ All ROI Index values are parsed as clean floats and perfectly standardized!")
        
    return "\n".join(report)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    audit_text = run_deep_audit()
    print(audit_text)
    
    # Save the audit report to scratch directory
    with open(r'g:\我的雲端硬碟\AI_Talent\scratch\deep_notion_audit_report.txt', 'w', encoding='utf-8') as f:
        f.write(audit_text)
