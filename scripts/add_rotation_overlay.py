# -*- coding: utf-8 -*-
"""
🦅 鳳凰 AI - 手機旋轉智能提示遮罩添加器
-------------------------------------------
作用：讀取 generate_henda_slides.py，為 index.html 及所有投影片模板
      原生注入基於 CSS Media Queries 的「手機直向轉橫向智能提示遮罩」，
      完美提升手機端的 C-Suite 觀看體驗。
"""

import codecs

file_path = "scripts/generate_henda_slides.py"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

# ── 1. 定義共用的 CSS 樣式與 HTML 代碼 ──
overlay_css = """
        @keyframes rotatePhone {
            0% { transform: rotate(0deg); }
            50% { transform: rotate(-90deg); }
            100% { transform: rotate(0deg); }
        }
        #mobile-rotate-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(7, 9, 19, 0.98);
            backdrop-filter: blur(20px);
            z-index: 99999;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #FFFFFF;
            text-align: center;
            padding: 40px;
        }
        @media (max-aspect-ratio: 1/1) and (max-width: 1024px) {
            #mobile-rotate-overlay {
                display: flex;
            }
        }
"""

overlay_html = """
    <div id="mobile-rotate-overlay">
        <div style="font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;">📱</div>
        <h2 style="font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">請旋轉您的手機</h2>
        <p style="font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>
    </div>
"""

# ── 2. 為 get_header() 注入 ──
# 尋找 get_header 中的 </style>
target_style = "        .animate-fade {{\n            animation: slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;\n        }}\n        .delay-1 {{ animation-delay: 0.1s; }}\n        .delay-2 {{ animation-delay: 0.25s; }}\n        .delay-3 {{ animation-delay: 0.4s; }}\n        {extra_style}\n    </style>"
replacement_style = target_style.replace("    </style>", overlay_css.replace("{", "{{").replace("}", "}}") + "\n    </style>")
content = content.replace(target_style, replacement_style)

# 尋找 get_header 中的 <body>
target_body = "<body>\n    <div class=\"grid-bg\"></div>"
replacement_body = "<body>\n" + overlay_html + "    <div class=\"grid-bg\"></div>"
content = content.replace(target_body, replacement_body)

# ── 3. 為 cover_html 注入 ──
content = content.replace(
    "        .delay-3 { animation-delay: 0.45s; }\n    </style>",
    "        .delay-3 { animation-delay: 0.45s; }\n" + overlay_css + "\n    </style>"
)
content = content.replace(
    "<body>\n    <div class=\"grid-bg\"></div>",
    "<body>\n" + overlay_html + "\n    <div class=\"grid-bg\"></div>"
)

# ── 4. 為 roadmap_html 注入 ──
content = content.replace(
    "        .delay-2 { animation-delay: 0.25s; }\n    </style>",
    "        .delay-2 { animation-delay: 0.25s; }\n" + overlay_css + "\n    </style>"
)
content = content.replace(
    "<body>\n    <div class=\"grid-bg\"></div>",
    "<body>\n" + overlay_html + "\n    <div class=\"grid-bg\"></div>"
)

# ── 5. 為 next_steps_html 注入 ──
content = content.replace(
    "        .delay-3 { animation-delay: 0.4s; }\n    </style>",
    "        .delay-3 { animation-delay: 0.4s; }\n" + overlay_css + "\n    </style>"
)
content = content.replace(
    "<body>\n    <div class=\"grid-bg\"></div>",
    "<body>\n" + overlay_html + "\n    <div class=\"grid-bg\"></div>"
)

# ── 6. 為 index_html 注入 (全局防護) ──
content = content.replace(
    "  @media print {\n    @page { size: 1920px 1080px; margin: 0; }",
    "  /* 手機提示 */\n" + overlay_css + "\n  @media print {\n    @page { size: 1920px 1080px; margin: 0; }"
)
content = content.replace(
    "<body>\n<div id=\"stage\">",
    "<body>\n" + overlay_html + "\n<div id=\"stage\">"
)

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(content)

print("🦅 [Success] 智能手機旋轉遮罩已注入 generate_henda_slides.py 程式源碼！")
