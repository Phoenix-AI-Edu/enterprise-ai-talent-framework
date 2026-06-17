# -*- coding: utf-8 -*-
import os
import re
import sys

# Mappings from long pain points to concise solution names
MAPPING = {
    # okayama_fastener
    "自建地端 RAG 資料雜亂致 AI 給出嚴重幻覺": "自建地端 RAG",
    "茂雄師習慣台語交班排斥打字與平板提示詞": "大師傅台語語音轉譯",
    "地端實體伺服器硬體維護成本 TCO 每年50萬": "地端伺服器輕量化",
    "大模型呼叫 API 敏感個資與專利進價洩密": "DLP 去敏感過濾",
    # okayama_forge
    "冷鍛模具磨損崩刀致不良品流出BMW客訴": "模具壽命聲學預警",
    "現場滿手油污無法在 iPad 上打字報工": "現場語音免打字報工",
    "CIO 廖經理防範 AI 寫入核心 ERP 污染數據": "ERP 唯讀中介緩衝",
    "CFO 劉總監防範算力 Token 帳單失控": "API 算力計費監控",
    # okayama_heat
    "出口螺絲熱處理製程爐溫失衡": "出口螺絲熱處理爐溫優化",
    "熱處理碳勢濃度失控引發氫脆": "熱處理碳勢濃度預估",
    "老舊廠房 API 斷訊死機起火隱患": "本地離線熔斷安全盒",
    "師傅黑手經驗流失與新技術斷層": "輝哥專家大腦調度庫",
    "熱處理連續電爐能耗過高": "爐溫燃氣優化配比",
    "外銷車廠 ISO 42001 安全審計": "外銷車廠安全審計對位",
    # okayama_cbam
    "歐盟 CBAM 申報工時嚴重超載": "CBAM RAG 申報",
    "委外熱處理能耗與碳足跡不透明": "委外熱處理能耗盤查",
    "委外電鍍藥水與廢水排污碳足跡黑盒": "電鍍排污能耗分析",
    "木箱包裝碳足跡手動計算易出錯": "木箱體積視覺檢測",
    # okayama_filter
    "AI 缺陷誤報率高達 15% 引發人眼疲勞": "缺陷誤報雙向校準",
    "品管人員現場實體翻找複檢工時翻倍": "有人在環瑕疵分流",
    "缺陷影像未標記導致模型無法微調進化": "標記教練津貼機制",
    "表面沾油與反光陰影過濾": "物理偏振曝光濾光",
    # okayama_electroplate
    "電鍍廢水超標排放面臨開罰勒令停產": "廢水排污多變量預測",
    "化學大師傅數據作假導致模型無法收斂": "專家配方冠名收斂",
    "汽車螺栓鹽霧測試良率低於 94%": "電鍍良率尋優推薦",
    "歐盟 CBAM 綠色碳稅申報超載": "電鍍能耗向量化對接",
    # luzhu_coldheading
    "高速冷鐓機沖頭滑塊瞬間卡死崩壞導致交期索賠": "冷鐓機沖頭壽命預警",
    "手沾油污拿扳手不便在 iPad 平板上打字報工": "車間語音報工系統",
    "現場電磁干擾與網路中斷導致雲端預警失靈": "地端 CM4 隔離分析",
    "Token 大模型呼叫開銷失控與死循環引發爆表": "算力路由與 Loop Guard",
    # okayama_barcode
    "出貨混料導致車廠退貨索賠": "出貨混料防錯主管線",
    "規格相近螺絲肉眼難辨(M6×1.0 vs M6×1.25)": "規格細部辨識子管線",
    "中高齡員工平板抗拒導致資料斷糧": "鳳姐介面與隱形標記蒐集",
    "包裝速度與品檢精度的取捨困境": "包裝速度推論優化",
    "新人訓練曲線過長(看不懂規格差異)": "新人 AI 輔助辨識",
    "標籤客戶混貼(規格對但客戶錯)": "標籤客戶混貼防線",
    # okayama_sbir
    "一線報工報修無法落地(手套油污)": "語音報工",
    "外銷 ISO 42001 認證缺口(DLP/審計日誌)": "ISO 42001 DLP/審計日誌",
    "CIO 防範 AI 污染鼎新 ERP": "ERP 唯讀緩衝",
    "CFO 防範雲端 API 成本失控": "API 財務熔斷",
    "自籌款龐大、CFO 反彈": "SBIR 補助 / 產創研抵",
    "鍛造件光學缺陷檢測(油污反光干擾)": "光學缺陷檢測",
    "歐盟 CBAM 碳關稅申報耗時易錯": "CBAM 碳足跡 RAG",
    "一線員工 AI 取代恐懼與抗拒": "AI-Native 績效重塑",
    "AI 供應商倒閉與 vendor lock-in": "供應商退場機制"
}

def clean_markdown_formatting(text):
    return re.sub(r'[\*_`~]', '', text).strip()

def get_concise_project_name(long_pain_point):
    clean_p = clean_markdown_formatting(long_pain_point)
    for k, v in MAPPING.items():
        if clean_markdown_formatting(k) == clean_p:
            return v
    return long_pain_point

def clean_priority(prio):
    prio = clean_markdown_formatting(prio)
    if 'P0' in prio or '首期' in prio or '大限' in prio or '前提' in prio or '關鍵' in prio or '軟性' in prio or '放行' in prio or '啟動' in prio:
        return '🌟 P0 優先級 (首期試點)'
    elif 'P1' in prio or '第二' in prio or '次要' in prio or '上線' in prio or '納入' in prio or '同期' in prio or '實作' in prio:
        return '🌟 P1 優先級 (第二階段)'
    elif 'P2' in prio or '第三' in prio:
        return '🌟 P2 優先級 (第三階段)'
    return prio

def clean_roi(roi):
    roi = clean_markdown_formatting(roi)
    val_clean = roi.split('/')[0].strip()
    try:
        val_float = float(val_clean)
        return f"{val_float:.1f}"
    except ValueError:
        return roi

def build_markdown_table(headers, rows):
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    return "\n".join(lines)

def parse_markdown_tables(lines):
    """
    Parses tables from lines.
    Returns a list of dicts:
    {
        "start_idx": int, (0-indexed line index)
        "end_idx": int, (0-indexed line index, inclusive)
        "headers": [str, ...],
        "rows": [[str, ...], ...]
    }
    """
    tables = []
    in_table = False
    current_table = None
    
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if all(re.match(r'^:?-+:?$', c) for c in cells):
                continue
            if not in_table:
                in_table = True
                current_table = {
                    "start_idx": idx,
                    "end_idx": idx,
                    "headers": cells,
                    "rows": []
                }
            else:
                current_table["rows"].append(cells)
                current_table["end_idx"] = idx
        else:
            if in_table:
                if current_table["rows"]:
                    tables.append(current_table)
                in_table = False
                current_table = None
                
    if in_table and current_table["rows"]:
        tables.append(current_table)
        
    return tables

def migrate_file(file_path):
    print(f"Migrating: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    lines = content.splitlines()
    tables = parse_markdown_tables(lines)
    
    if len(tables) < 4:
        print(f"⚠️  Warning: Expected at least 4 tables, found {len(tables)} in {file_path}. Skipping.")
        return
        
    # The last 4 tables are the Notion tables
    notion_tables = tables[-4:]
    
    # 1. Transform Table 1 (Scenario Inventory)
    t1 = notion_tables[0]
    t1_headers = [
        "對應場景專案", "業務痛點", "主責部門", "核心 AI 任務", 
        "商業價值評估 (V)", "數據就緒度評估 (D)", "一線使用阻力評估 (R)", 
        "ROI 綜合評估指數", "導入優先級決策"
    ]
    t1_rows = []
    for r in t1["rows"]:
        original_pain_point = r[0]
        project_name = get_concise_project_name(original_pain_point)
        # Pad row to match original columns if needed
        # Original Table 1 had: 0: PainPoint, 1: Dept, 2: Task, 3: V, 4: D, 5: R, 6: ROI, 7: Prio
        # New Table 1 has: 0: ProjectName, 1: PainPoint, 2: Dept, 3: Task, 4: V, 5: D, 6: R, 7: ROI, 8: Prio
        dept = r[1] if len(r) > 1 else ""
        task = r[2] if len(r) > 2 else ""
        v_val = r[3] if len(r) > 3 else ""
        d_val = r[4] if len(r) > 4 else ""
        r_val = r[5] if len(r) > 5 else ""
        roi = clean_roi(r[6]) if len(r) > 6 else ""
        prio = clean_priority(r[7]) if len(r) > 7 else ""
        
        t1_rows.append([
            project_name, original_pain_point, dept, task, 
            v_val, d_val, r_val, roi, prio
        ])
    t1_markdown = build_markdown_table(t1_headers, t1_rows)
    
    # 2. Transform Table 2 (Solution Architecture)
    t2 = notion_tables[1]
    t2_headers = ["對應場景專案", "技術路徑選擇", "核心模型配置", "敏感資料防線", "主動安全防禦", "合規審計稽核"]
    t2_rows = []
    for r in t2["rows"]:
        project_name = get_concise_project_name(r[0])
        rest = r[1:]
        while len(rest) < 5:
            rest.append("")
        t2_rows.append([project_name] + rest)
    t2_markdown = build_markdown_table(t2_headers, t2_rows)
    
    # 3. Transform Table 3 (Pilot Validation & Resistance)
    t3 = notion_tables[2]
    t3_headers = ["對應場景專案", "試點部門與範圍", "試點週期", "Quick-Win 量化 KPI", "一線員工主要阻力", "變革管理化解方案"]
    t3_rows = []
    for r in t3["rows"]:
        project_name = get_concise_project_name(r[0])
        rest = r[1:]
        while len(rest) < 5:
            rest.append("")
        t3_rows.append([project_name] + rest)
    t3_markdown = build_markdown_table(t3_headers, t3_rows)
    
    # 4. Transform Table 4 (Operations & Governance)
    t4 = notion_tables[3]
    t4_headers = ["對應場景專案", "人機協作角色設計 (HITL)", "單月 API 財務告警閾值", "持續維運分工 (LLMOps)", "技能升級與培訓", "財務熔斷保護"]
    t4_rows = []
    for r in t4["rows"]:
        project_name = get_concise_project_name(r[0])
        rest = r[1:]
        while len(rest) < 5:
            rest.append("")
        t4_rows.append([project_name] + rest)
    t4_markdown = build_markdown_table(t4_headers, t4_rows)
    
    # Reassemble the file content by replacing lines of each table
    # We must replace them in reverse order so that indices don't shift!
    t_list = [
        (t1, t1_markdown),
        (t2, t2_markdown),
        (t3, t3_markdown),
        (t4, t4_markdown)
    ]
    
    # Sort by start_idx descending
    t_list.sort(key=lambda x: x[0]["start_idx"], reverse=True)
    
    new_lines = list(lines)
    for table_info, table_md in t_list:
        start = table_info["start_idx"]
        end = table_info["end_idx"]
        
        # We replace the slice from start to end + 1 with the table_md split into lines
        new_lines[start:end+1] = table_md.splitlines()
        
    new_content = "\n".join(new_lines)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"  ✅ Re-wrote {file_path} successfully.")

def main():
    cases = [
        'scripts/proposal_okayama_fastener.md',
        'scripts/proposal_okayama_forge.md',
        'scripts/proposal_okayama_heat.md',
        'scripts/proposal_okayama_cbam.md',
        'scripts/proposal_okayama_filter.md',
        'scripts/proposal_okayama_electroplate.md',
        'scripts/proposal_luzhu_coldheading.md',
        'scripts/proposal_okayama_barcode.md',
        'scripts/proposal_okayama_sbir.md'
    ]
    for path in cases:
        migrate_file(path)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
