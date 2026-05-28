# -*- coding: utf-8 -*-
"""
🦅 鳳凰 AI - 簡報易讀性與對比度優化腳本 (Slides Visibility Enhancer)
--------------------------------------------------------------
作用：讀取 generate_henda_slides.py，大幅提升字體大小、對比度，消除所有暗灰色小字。
      確保在 1920x1080 投影片觀看時，字體極其清晰亮麗、具有頂級商業大氣感。
"""

import codecs
import re

file_path = "scripts/generate_henda_slides.py"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

# 1. 優化全局變數與 CSS 樣式
replacements = {
    "--text-muted: #8E9AA8;": "--text-muted: #E2E8F0;",  # 灰色字改為亮灰白色，大幅提升對比度
    "--text-muted: #8E9AA8": "--text-muted: #E2E8F0",
    "--glass-border: rgba(255, 255, 255, 0.06);": "--glass-border: rgba(255, 255, 255, 0.15);", # 加深邊框，結構更清晰
    "font-size: 16px;": "font-size: 20px;", # 模組標題放大
    "font-size: 40px;": "font-size: 48px;", # 幻燈片大標題放大
    "font-size: 24px;": "font-size: 32px;", # 卡片標題放大
    "font-size: 14px;": "font-size: 18px;", # 底部 alert 放大
    "color: var(--text-muted);": "color: #FFF;", # 灰色字體一律改為白色
    "color: var(--text-muted)": "color: #FFF",
}

for src, dest in replacements.items():
    content = content.replace(src, dest)

# 2. 針對所有 Slide 內部的微小字體進行正則或字串替換
# 替換具體的 inline font-size 與 line-height
content = content.replace("font-size: 15px;", "font-size: 22px;")
content = content.replace("font-size: 13.5px;", "font-size: 20px;")
content = content.replace("font-size: 14px;", "font-size: 20px;")
content = content.replace("font-size: 14.5px;", "font-size: 21px;")
content = content.replace("font-size: 13px;", "font-size: 19px;")
content = content.replace("font-size: 11px;", "font-size: 16px;")
content = content.replace("font-size: 22px; font-weight: 300;", "font-size: 26px; font-weight: 400;")
content = content.replace("font-size: 20px; font-weight: 500;", "font-size: 24px; font-weight: 600;")
content = content.replace("font-size: 16px; font-weight: 300;", "font-size: 20px; font-weight: 400;")
content = content.replace("font-size: 24px; font-weight: 700;", "font-size: 32px; font-weight: 800;")
content = content.replace("font-size: 12px;", "font-size: 18px;")
content = content.replace("font-size: 22px; font-weight: 500; font-style: italic;", "font-size: 28px; font-weight: 600; font-style: italic;")

# 調整 line-height 以配合放大後的字體，避免字體擠壓
content = content.replace("line-height: 1.4;", "line-height: 1.65;")
content = content.replace("line-height: 1.4", "line-height: 1.65")
content = content.replace("line-height: 1.5;", "line-height: 1.7;")
content = content.replace("line-height: 1.55;", "line-height: 1.7;")
content = content.replace("line-height: 1.6;", "line-height: 1.75;")

# 3. 優化 Cover 的 meta 排版，使其更大更清晰
content = content.replace(".meta-label {", ".meta-label {\n            font-size: 16px;")
content = content.replace(".meta-value { font-size: 20px;", ".meta-value { font-size: 26px;")

# 4. 優化 Gantt 甘特圖的高度與字體大小
content = content.replace("height: 28px;", "height: 38px;")
content = content.replace("gap: 20px;", "gap: 24px;")
content = content.replace("padding: 24px;", "padding: 30px;")

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(content)

print("🦅 generate_henda_slides.py 字體清晰度與對比度優化完成！")
