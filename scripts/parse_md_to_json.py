#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parse_md_to_json.py — 鳳凰 AI 顧問簡報自動轉譯工具
========================================================================
作用：
  讀取 proposal_tea_franchise.md（C-Level 顧問解決方案文檔），
  解析其內置的 HTML 簡報錨點（<!-- slide-page: ... -->）與結構化欄位，
  自動轉譯生成完全符合 slides_config.schema.json 的 JSON 簡報設定檔。

實現「文檔即簡報源碼」的 100% 自動化，徹底避免人工手動複製 JSON 的排版錯誤。
========================================================================
"""

import json
import re
from pathlib import Path

def parse_anchor(line):
    """
    解析錨點註解：<!-- slide-page: "01", layout: "cover", progress_label: "COVER", ... -->
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
        # 去掉開頭的逗號
        if extra_str.startswith(','):
            extra_str = extra_str[1:].strip()
        pairs = re.split(r',\s*', extra_str)
        for pair in pairs:
            if ':' in pair:
                k, v = pair.split(':', 1)
                k = k.strip()
                v = v.strip()
                # 嘗試轉為數字
                try:
                    if '.' in v:
                        slide[k] = float(v)
                    else:
                        slide[k] = int(v)
                except ValueError:
                    # 如果不是數字就保留字串（去掉引號）
                    slide[k] = v.strip('"\'')
                    
    return slide

def main():
    md_path = Path("scripts/proposal_tea_franchise.md")
    if not md_path.exists():
        print(f"❌ 錯誤：找不到建議書檔案 {md_path}")
        return

    print("【文檔轉譯器】開始讀取建議書...")
    lines = md_path.read_text(encoding="utf-8").splitlines()
    
    slides = []
    current_slide = None
    in_codeblock = False
    codeblock_key = None
    codeblock_lines = []
    
    # 臨時暫存 tabs
    in_tabs = False
    tabs_list = []
    current_tab = None
    
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # 1. 處理程式碼區塊（多行字串，如 speaker_notes）
        if stripped.startswith("```"):
            if in_codeblock:
                # 程式碼區塊結束
                if current_slide and codeblock_key:
                    content = "\n".join(codeblock_lines).strip()
                    current_slide[codeblock_key] = content
                in_codeblock = False
                codeblock_key = None
                codeblock_lines = []
            else:
                # 程式碼區塊開始，檢查上一行是否為 key
                in_codeblock = True
            continue
            
        if in_codeblock:
            codeblock_lines.append(line)
            continue
            
        # 2. 辨識新投影片錨點
        if stripped.startswith("<!--") and "slide-page" in stripped:
            if current_slide:
                if in_tabs and tabs_list:
                    current_slide["tabs"] = tabs_list
                    in_tabs = False
                    tabs_list = []
                slides.append(current_slide)
                
            current_slide = parse_anchor(line)
            if current_slide:
                print(f"   ✓ 偵測到投影片：第 {current_slide['page']} 頁 ({current_slide['layout']})")
            continue
            
        # 3. 如果在投影片內部，解析欄位
        if current_slide:
            # 處理多行代碼塊的 key 前綴，例如：- **speaker_notes**:
            m_code_key = re.match(r'^-\s*\*\*(speaker_notes)\*\*:\s*$', stripped)
            if m_code_key:
                codeblock_key = m_code_key.group(1)
                continue
                
            # 處理 tabs 分頁的子欄位
            # 格式：- **name**: Month 1（啟動評估）
            #       **content**: 第一個月聚焦...
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
                    
                # 若遇到其他非縮排的 bullet point 且不是 name/content，表示 tabs 結束
                if stripped.startswith("- **") and "name" not in stripped and "content" not in stripped:
                    if current_tab:
                        tabs_list.append(current_tab)
                        current_tab = None
                    current_slide["tabs"] = tabs_list
                    in_tabs = False
                    # 不要 continue，讓它往下落入一般的 key-value 解析

            # 處理單行 key-value，例如：- **title**: 方案標題
            m_kv = re.match(r'^-\s*\*\*([\w_]+)\*\*:\s*(.*)$', stripped)
            if m_kv:
                key = m_kv.group(1)
                val = m_kv.group(2).strip()
                
                # 如果是 tabs 陣列開頭
                if key == "tabs":
                    in_tabs = True
                    tabs_list = []
                    continue
                    
                current_slide[key] = val
                continue
                    
    # 最後一頁收尾
    if current_slide:
        if in_tabs and current_tab:
            tabs_list.append(current_tab)
            current_slide["tabs"] = tabs_list
        slides.append(current_slide)
        
    # 組裝頂層中央設定檔
    config = {
        "client_name": "全球連鎖茶飲加盟集團",
        "client_badge": "MING CHA DAO GROUP",
        "logo_text": "PHOENIX AI 顧問 x 連鎖茶飲加盟集團",
        "output_dir": "slides/mingchadao",
        "theme": "obsidian-midnight",
        "audience": "internal",  # 預設為客戶內部版
        "min_slides_required": 10,
        "slides": slides
    }
    
    # 輸出為 JSON 設定檔
    out_path = Path("scripts/slides_config_tea.json")
    out_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ 轉譯成功！簡報設定檔已存至：{out_path}")
    print(f"   總投影片頁數：{len(slides)} 頁")

if __name__ == "__main__":
    main()
