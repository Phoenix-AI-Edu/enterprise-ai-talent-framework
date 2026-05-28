#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_md_to_json.py — 鳳凰 AI 顧問簡報自動轉譯工具 (雙模式自適應版)
========================================================================
作用：
  讀取 B2B 顧問解決方案文檔（.md），
  解析其內置的 HTML 簡報錨點（<!-- slide-page: ... -->）與結構化欄位，
  自動轉譯生成完全符合 slides_config.schema.json 的 JSON 簡報設定檔。

  【雙核心引擎】：
  1. 支持 Style B：直接在 HTML 註解後解析 ```json ... ``` 代碼塊，
     並利用「極智自適應對照層」自動將嵌套的 tracks, interactive, phases, actions
     以及各種自定義佈局（如 exec-cockpit, matrix, table, rule-library 等）
     扁平化映射到標準 Schema 的 badge_left, tabs, cardX_title 等 dual-track 欄位，補齊 progress_label。
  2. 支持 Style A：原本的 HTML 註解參數 + 列表鍵值對模式。

  實現「文檔即簡報源碼」的 100% 通用自動化與極致容錯。
========================================================================
"""

import json
import re
import argparse
import sys
from pathlib import Path

def parse_anchor_style_a(line):
    """
    解析 Style A 錨點註解：<!-- slide-page: "01", layout: "cover", progress_label: "COVER", ... -->
    """
    m = re.search(r'<!--\s*slide-page:\s*"([^"]+)",\s*layout:\s*"([^"]+)",\s*progress_label:\s*"([^"]+)"(.*?)-->', line)
    if not m:
        return None
    
    page = m.group(1)
    layout = m.group(2)
    progress_label = m.group(3)
    extra_str = m.group(4).strip()
    
    slide = {
        "page": page,
        "layout": layout,
        "progress_label": progress_label
    }
    
    # 解析額外的數值屬性（例如：slider_min: 5, slider_max: 40 等）
    if extra_str:
        if extra_str.startswith(','):
            extra_str = extra_str[1:].strip()
        pairs = re.split(r',\s*', extra_str)
        for pair in pairs:
            if ':' in pair:
                k, v = pair.split(':', 1)
                k = k.strip()
                v = v.strip()
                try:
                    if '.' in v:
                        slide[k] = float(v)
                    else:
                        slide[k] = int(v)
                except ValueError:
                    slide[k] = v.strip('"\'')
                    
    return slide

def parse_style_a(lines):
    """
    傳統 Style A 解析器（列表模式）
    """
    slides = []
    current_slide = None
    in_codeblock = False
    codeblock_key = None
    codeblock_lines = []
    
    in_tabs = False
    tabs_list = []
    current_tab = None
    
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        
        if stripped.startswith("```"):
            if in_codeblock:
                if current_slide and codeblock_key:
                    content = "\n".join(codeblock_lines).strip()
                    current_slide[codeblock_key] = content
                in_codeblock = False
                codeblock_key = None
                codeblock_lines = []
            else:
                in_codeblock = True
            continue
            
        if in_codeblock:
            codeblock_lines.append(line)
            continue
            
        if stripped.startswith("<!--") and "slide-page" in stripped:
            if current_slide:
                if in_tabs and tabs_list:
                    current_slide["tabs"] = tabs_list
                    in_tabs = False
                    tabs_list = []
                slides.append(current_slide)
                
            current_slide = parse_anchor_style_a(line)
            continue
            
        if current_slide:
            m_code_key = re.match(r'^-\s*\*\*(speaker_notes)\*\*:\s*$', stripped)
            if m_code_key:
                codeblock_key = m_code_key.group(1)
                continue
                
            if in_tabs:
                m_tab_name = re.match(r'^-\s*\*\*name\*\*:\s*(.*)$', stripped)
                if m_tab_name:
                    if current_tab:
                        tabs_list.append(current_tab)
                    current_tab = {"name": m_tab_name.group(1).strip()}
                    continue
                    
                m_tab_content = re.match(r'^\*\*content\*\*:\s*(.*)$', stripped)
                if m_tab_content and current_tab:
                    current_tab["content"] = m_tab_content.group(1).strip()
                    continue
                    
                if stripped.startswith("- **") and "name" not in stripped and "content" not in stripped:
                    if current_tab:
                        tabs_list.append(current_tab)
                        current_tab = None
                    current_slide["tabs"] = tabs_list
                    in_tabs = False
 
            m_kv = re.match(r'^-\s*\*\*([\w_]+)\*\*:\s*(.*)$', stripped)
            if m_kv:
                key = m_kv.group(1)
                val = m_kv.group(2).strip()
                
                if key == "tabs":
                    in_tabs = True
                    tabs_list = []
                    continue
                    
                current_slide[key] = val
                continue
                    
    if current_slide:
        if in_tabs and current_tab:
            tabs_list.append(current_tab)
            current_slide["tabs"] = tabs_list
        slides.append(current_slide)
        
    return slides

def main():
    parser = argparse.ArgumentParser(description="鳳凰 AI 顧問簡報自動轉譯工具 (MD ➡️ JSON)")
    parser.add_argument("md_path", help="待轉譯的 Markdown 建議書路徑")
    parser.add_argument("-o", "--output", help="輸出的 JSON 設定檔路徑（若未指定，自動生成於同目錄）")
    
    args = parser.parse_args()
    md_path = Path(args.md_path)
    if not md_path.exists():
        print(f"❌ 錯誤：找不到建議書檔案 {md_path}")
        sys.exit(1)

    print(f"【文檔轉譯器】開始讀取建議書：{md_path} ...")
    content = md_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    # 1. 嘗試用 Style B 解析
    style_b_blocks = re.findall(r'<!--\s*slide-page:\s*(\d+)\s*-->\s*```json\s*(.*?)\s*```', content, re.DOTALL)
    
    slides = []
    if style_b_blocks:
        print("   ✓ 檢測到 Style B (JSON代碼塊型) 投影片格式，啟動極智自適應對照層...")
        for page_num_str, json_str in style_b_blocks:
            try:
                slide_data = json.loads(json_str)
                page_val = int(slide_data.get("page", page_num_str))
                page_str = f"{page_val:02d}"
                layout = slide_data.get("layout", "cover")
                tier = slide_data.get("tier", "T1-spine")
                
                # 動態推導 progress_label
                if layout == "cover":
                    progress_label = "COVER"
                elif layout == "interactive-roi":
                    progress_label = "ROI"
                elif layout == "interactive-roadmap":
                    progress_label = "PLAN"
                elif layout == "next-steps":
                    progress_label = "NEXT"
                else:
                    progress_label = f"M{page_val-1:02d}"
                    
                # 構造扁平化的 slide
                flat_slide = {
                    "page": page_str,
                    "layout": layout,
                    "progress_label": progress_label,
                    "title": slide_data.get("title", ""),
                    "subtitle": slide_data.get("subtitle", ""),
                    "speaker_notes": slide_data.get("speaker_notes", "")
                }
                
                # 標準佈局映射
                if layout == "cover":
                    flat_slide["version"] = slide_data.get("version", "v2026.06.01")
                    flat_slide["date"] = slide_data.get("date", "2026-05-29")
                    
                elif layout == "dual-track":
                    tracks = slide_data.get("tracks", {})
                    left = tracks.get("left", {})
                    right = tracks.get("right", {})
                    
                    ltitle = left.get("title", "戰略防線")
                    m_left = re.match(r'^(.*?)[（\(\-\—\s]+(.*?)[）\)]*$', ltitle)
                    if m_left:
                        badge_left = m_left.group(1).strip()
                        title_left = m_left.group(2).strip()
                    else:
                        badge_left = "戰略防線"
                        title_left = ltitle
                        
                    rtitle = right.get("title", "實務落地")
                    m_right = re.match(r'^(.*?)[（\(\-\—\s]+(.*?)[）\)]*$', rtitle)
                    if m_right:
                        badge_right = m_right.group(1).strip()
                        title_right = m_right.group(2).strip()
                    else:
                        badge_right = "實務落地"
                        title_right = rtitle
                        
                    # 特殊處理研抵與保命手冊
                    if "第10條" in ltitle or "研抵" in ltitle:
                        badge_left = "第10條"
                        title_left = "研發活動抵減"
                    if "免剔除" in rtitle or "保命手冊" in rtitle:
                        badge_right = "核銷防線"
                        title_right = "免剔除保命手冊"
                        
                    flat_slide["badge_left"] = badge_left
                    flat_slide["title_left"] = title_left
                    flat_slide["content_left"] = "<br>".join([f"• {p}" for p in left.get("points", [])])
                    
                    flat_slide["badge_right"] = badge_right
                    flat_slide["title_right"] = title_right
                    flat_slide["content_right"] = "<br>".join([f"• {p}" for p in right.get("points", [])])
                    
                elif layout == "interactive-roi":
                    interactive = slide_data.get("interactive", {})
                    slider = interactive.get("slider", {})
                    
                    flat_slide["slider_min"] = slider.get("min_pct", 10)
                    flat_slide["slider_max"] = slider.get("max_pct", 60)
                    flat_slide["slider_default"] = slider.get("default_pct", 40)
                    
                    flat_slide["cost_base"] = interactive.get("annual_cost_per_head_twd", 1200000)
                    flat_slide["num_workers"] = interactive.get("base_headcount", 100)
                    
                    flat_slide["intro_text"] = slide_data.get("content", "")
                    
                    formula = interactive.get("formula", "")
                    note = interactive.get("project_cost_note", "")
                    flat_slide["translation_box"] = f"<strong>核心算式：</strong>{formula}<br><strong>投資回報：</strong>{note}"
                    
                elif layout == "interactive-roadmap":
                    interactive = slide_data.get("interactive", {})
                    phases = interactive.get("phases", [])
                    tabs = []
                    for phase in phases:
                        p_name = phase.get("phase", "")
                        p_track = phase.get("track", "")
                        p_milestones = phase.get("milestones", [])
                        content_str = f"<strong>方案主題：</strong>{p_track}<br><strong>關鍵里程碑：</strong><br>" + "<br>".join([f"• {m}" for m in p_milestones])
                        tabs.append({
                            "name": p_name,
                            "content": content_str
                        })
                    flat_slide["tabs"] = tabs
                    
                elif layout == "next-steps":
                    actions = slide_data.get("actions", [])
                    for i in range(1, 4):
                        if len(actions) >= i:
                            act = actions[i-1]
                            flat_slide[f"card{i}_title"] = act.get("title", "")
                            flat_slide[f"card{i}_desc"] = act.get("detail", "")
                        else:
                            flat_slide[f"card{i}_title"] = ""
                            flat_slide[f"card{i}_desc"] = ""
                            
                    flat_slide["closing_quote"] = slide_data.get("closing_quote", "")
                    consultants = slide_data.get("consultants", "")
                    if isinstance(consultants, list):
                        flat_slide["consultants"] = " ＆ ".join(consultants)
                    else:
                        flat_slide["consultants"] = consultants
                        
                else:
                    # 自定義佈局（exec-cockpit, matrix, rule-library 等），極智自適應對照為標準 dual-track Layout！
                    flat_slide["layout"] = "dual-track"
                    
                    badge_left = "戰略分析"
                    title_left = "核心概念"
                    content_left_list = []
                    
                    badge_right = "實務落地"
                    title_right = "技術配置"
                    content_right_list = []
                    
                    # 1. 優先使用嵌套的 tracks
                    if "tracks" in slide_data:
                        tracks = slide_data.get("tracks", {})
                        left = tracks.get("left", {})
                        right = tracks.get("right", {})
                        badge_left = left.get("title", "戰略分析")
                        title_left = "核心指標"
                        content_left_list = [f"• {p}" for p in left.get("points", [])]
                        
                        badge_right = right.get("title", "實務落地")
                        title_right = "技術配置"
                        content_right_list = [f"• {p}" for p in right.get("points", [])]
                        
                    # 2. 次要使用 items 列表
                    elif "items" in slide_data:
                        items = slide_data.get("items", [])
                        half = (len(items) + 1) // 2
                        left_items = items[:half]
                        right_items = items[half:]
                        
                        def format_item(item):
                            if not isinstance(item, dict):
                                return str(item)
                            parts = []
                            for k, v in item.items():
                                parts.append(f"<strong>{k}</strong>: {v}")
                            return "• " + " | ".join(parts)
                            
                        content_left_list = [format_item(it) for it in left_items]
                        content_right_list = [format_item(it) for it in right_items]
                        
                        # 針對特定版式微調標題與 Badge
                        if layout in ("exec-cockpit", "burning-platform", "matrix"):
                            badge_left = "決策層" if layout == "exec-cockpit" else "風險分析"
                            title_left = "核心考量" if layout == "exec-cockpit" else "生存挑戰"
                            badge_right = "實施層" if layout == "exec-cockpit" else "緩解措施"
                            title_right = "落地請求" if layout == "exec-cockpit" else "防禦策略"
                        elif layout == "flow-hitl":
                            badge_left = "第一/二簽"
                            title_left = "流程前段"
                            badge_right = "第三簽/熔斷"
                            title_right = "流程後段"
                        
                    # 3. 處理 table 格式
                    elif "table" in slide_data:
                        table = slide_data.get("table", {})
                        headers = table.get("headers", [])
                        rows = table.get("rows", [])
                        half = (len(rows) + 1) // 2
                        left_rows = rows[:half]
                        right_rows = rows[half:]
                        
                        def format_row(row):
                            if not isinstance(row, list):
                                return str(row)
                            parts = []
                            for idx, val in enumerate(row):
                                h_name = headers[idx] if idx < len(headers) else f"Col{idx+1}"
                                parts.append(f"<strong>{h_name}</strong>: {val}")
                            return "• " + " | ".join(parts)
                            
                        content_left_list = [format_row(r) for r in left_rows]
                        content_right_list = [format_row(r) for r in right_rows]
                        badge_left = "數據庫"
                        title_left = f"稽核主表 ({headers[0] if headers else 'A'})"
                        badge_right = "對照表"
                        title_right = f"稽核主表 ({headers[0] if headers else 'B'})"
                        
                    else:
                        # 兜底
                        content_left_list = [slide_data.get("content", "")]
                        
                    flat_slide["badge_left"] = badge_left
                    flat_slide["title_left"] = title_left
                    flat_slide["content_left"] = "<br>".join(content_left_list)
                    
                    flat_slide["badge_right"] = badge_right
                    flat_slide["title_right"] = title_right
                    flat_slide["content_right"] = "<br>".join(content_right_list)
                    
                slides.append(flat_slide)
                print(f"   ✓ 順利自適應解析轉譯第 {page_str} 頁 ({layout} ➡️ dual-track)")
            except Exception as ex:
                print(f"   ❌ 解析第 {page_num_str} 頁 JSON 失敗，內容：{json_str[:100]}... 原因：{ex}")
                sys.exit(1)
    else:
        # 2. 否則採用 Style A 列表解析器
        print("   ✓ 未檢測到 JSON 代碼塊，自適應採用 Style A (列表鍵值對) 投影片格式...")
        slides = parse_style_a(lines)
        
    if not slides:
        print("❌ 錯誤：未在建議書中找到任何投影片錨點標記！")
        sys.exit(1)
        
    # ─── 動態元數據解析與推導 ───
    filename = md_path.stem
    client_key = "client"
    if "proposal_" in filename:
        client_key = filename.replace("proposal_", "")
        
    client_zh = client_key
    for line in lines:
        if line.strip().startswith("# "):
            title_match = re.match(r'^#\s*(?:[^\w\s]|\s)*([A-Za-z0-9_\u4e00-\u9fa5\[\]（）\(\)\s\-]+?)｜', line.strip())
            if title_match:
                client_zh = title_match.group(1).strip()
                break
            title_match_fallback = re.match(r'^#\s*(?:[^\w\s]|\s)*([A-Za-z0-9_\u4e00-\u9fa5\[\]（）\(\)\s\-]+)', line.strip())
            if title_match_fallback:
                client_zh = title_match_fallback.group(1).strip()
                break

    client_badge = f"{client_key.upper().replace('_', ' ')} GROUP"
    logo_text = f"PHOENIX AI 顧問 x {client_zh}"
    output_dir = f"slides/{client_key}"
    
    # 組裝頂層中央設定檔
    config = {
        "client_name": client_zh,
        "client_badge": client_badge,
        "logo_text": logo_text,
        "output_dir": output_dir,
        "theme": "obsidian-midnight",
        "audience": "internal",  # 預設為客戶內部版
        "min_slides_required": len(slides),
        "slides": slides
    }
    
    # 輸出路徑
    if args.output:
        out_path = Path(args.output)
    else:
        out_path = md_path.parent / f"slides_config_{client_key}.json"
        
    out_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 轉譯成功！簡報設定檔已存至：{out_path}")
    print(f"   客戶中文名稱：{client_zh}")
    print(f"   客戶識別標籤：{client_badge}")
    print(f"   輸出簡報目錄：{output_dir}")
    print(f"   總投影片頁數：{len(slides)} 頁")

if __name__ == "__main__":
    main()
