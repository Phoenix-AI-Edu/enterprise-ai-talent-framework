# -*- coding: utf-8 -*-
import re
from pathlib import Path

def merge():
    proposal_path = Path("scripts/proposal_securities.md")
    slides_path = Path("G:/我的雲端硬碟/孟淑慧/PMC/AI人才培育計畫課程規劃/企業外評/證券商AI治理_董事會審議簡報_51張分層系統.md")
    
    if not proposal_path.exists():
        print("❌ Error: proposal_securities.md not found!")
        return
    if not slides_path.exists():
        print("❌ Error: 51 slides file not found!")
        return
        
    proposal_text = proposal_path.read_text(encoding="utf-8")
    slides_text = slides_path.read_text(encoding="utf-8")
    
    # 找到 proposal_securities.md 中的第一、二部分（Part 1 & 2）
    # 它在 # 第三部分： 之前
    part1_2_match = re.search(r'^(.*?)# 第三部分：', proposal_text, re.DOTALL)
    if not part1_2_match:
        part1_2_match = re.search(r'^(.*?)# 第三部分：10 頁投影片', proposal_text, re.DOTALL)
        
    if not part1_2_match:
        print("❌ Error: Could not locate Part 1 & 2 end in proposal_securities.md!")
        return
        
    part1_2 = part1_2_match.group(1).strip()
    
    # 找到 proposal_securities.md 中的第四部分（Part 4）
    # 它在 # 第四部分： 之後
    part4_match = re.search(r'(# 第四部分：.*)$', proposal_text, re.DOTALL)
    if not part4_match:
        print("❌ Error: Could not locate Part 4 in proposal_securities.md!")
        return
        
    part4 = part4_match.group(1).strip()
    
    # 從 51張分層系統.md 中提取所有的 slide-page 錨點與代碼塊
    # 我們可以找到第一個 <!-- slide-page: 01 --> 的位置
    slides_content_match = re.search(r'(<!-- slide-page: 01 -->.*)$', slides_text, re.DOTALL)
    if not slides_content_match:
        print("❌ Error: Could not locate slide-page 01 in slides file!")
        return
        
    slides_content = slides_content_match.group(1).strip()
    
    # 拼接新的 proposal_securities.md
    new_proposal = f"""{part1_2}

# 第三部分：51 頁投影片客製簡報配置與演講者備忘錄

> **主題（Theme）：** `obsidian-midnight`（曜夜奢華黑）
> **架構：** Tier 0 決策駕駛艙 ×1（Page 02）＋ Tier 1 上台脊椎 ×24（Page 01, 03–25）＋ Tier 2 防身附錄 ×26（Page 26–51）
> **編譯說明：** 各 `<!-- slide-page -->` 錨點對齊統一 JSON Schema。`content` ≤200 字。Tier 1 配充實 `speaker_notes`；Tier 2 標註「備而不講」用途。

{slides_content}

---

{part4}"""
    
    proposal_path.write_text(new_proposal, encoding="utf-8")
    print("✅ Successfully merged Part 1 & 2 with the 51-slide split deck and Part 4!")

if __name__ == "__main__":
    merge()
