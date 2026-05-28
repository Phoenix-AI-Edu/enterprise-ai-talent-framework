# -*- coding: utf-8 -*-
"""
🦅 鳳凰 AI - 手機旋轉提示遮罩移除器
-------------------------------------------
作用：讀取 generate_henda_slides.py，移除所有的手機旋轉提示遮罩，
      讓手機用戶可以直接自由觀看投影片，並配合原生的 fit() 自適應縮放機制。
"""

import codecs

file_path = "scripts/generate_henda_slides.py"

with codecs.open(file_path, "r", "utf-8") as f:
    content = f.read()

# 定義要移除的 CSS 和 HTML 代碼段
overlay_css_single = """
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

overlay_css_double = """
        @keyframes rotatePhone {{
            0% {{ transform: rotate(0deg); }}
            50% {{ transform: rotate(-90deg); }}
            100% {{ transform: rotate(0deg); }}
        }}
        #mobile-rotate-overlay {{
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
        }}
        @media (max-aspect-ratio: 1/1) and (max-width: 1024px) {{
            #mobile-rotate-overlay {{
                display: flex;
            }}
        }}
"""

overlay_html = """
    <div id="mobile-rotate-overlay">
        <div style="font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;">📱</div>
        <h2 style="font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">請旋轉您的手機</h2>
        <p style="font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>
    </div>
"""

# 清洗 content
# 1. 替換 HTML
content = content.replace(overlay_html, "")
# 2. 替換 CSS
content = content.replace(overlay_css_double, "")
content = content.replace(overlay_css_single, "")

# 雙重防呆：有些多餘的換行或空格
content = content.replace("<div id=\"mobile-rotate-overlay\">\n        <div style=\"font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;\">📱</div>\n        <h2 style=\"font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;\">請旋轉您的手機</h2>\n        <p style=\"font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;\">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>\n    </div>", "")

with codecs.open(file_path, "w", "utf-8") as f:
    f.write(content)

print("🦅 [Success] 手機旋轉提示遮罩已從 generate_henda_slides.py 中乾淨移除！")
