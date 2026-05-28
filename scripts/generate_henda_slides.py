# -*- coding: utf-8 -*-
"""
🦅 鳳凰 AI - 恆達精密客製化簡報自動生成器 (Henda Slides Generator) ➔ 終極互動高保真重構版
----------------------------------------------------------------------------------
作用：在本地 slides/henda/ 目錄下，全量生成符合 /huashu-design 規範的
      12 頁 Obsidian Midnight 奢華風格高保真 HTML 簡報，原生整合：
      - 實時聲學降噪「互動波形對比器」（Slide 04）
      - 語音 RAG「互動指令沙盒」（Slide 05）
      - 模具預測性維護「實時點擊財務 ROI 計算器」（Slide 07）
      - 5大政府核銷保命手冊「翻開 3D 書頁/展示摘要」動態卡片（Slide 09）
      - 6個月變革管理時程「點擊交互時間線」（Slide 10）
      確保大字體、極亮對比度、以及極致的視覺美學。
"""

import os
import codecs
import sys

# 強制將標準輸出重置為 UTF-8，防範 Windows 控制台 cp950 編碼報錯
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # 舊版本 Python 忽略

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HENDA_DIR = os.path.join(BASE_DIR, "slides", "henda")
os.makedirs(HENDA_DIR, exist_ok=True)

# ── 1. 定義通用的 HTML 頭部與尾部（融入高對比度、高級圖形佈局與極致奢華的視覺語法） ──
def get_header(title, module_name, slide_num, extra_style=""):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #070913;
            --primary-accent: #FF5B35;
            --secondary-accent: #00F2FE;
            --text-main: #FFFFFF;
            --text-muted: #E2E8F0;
            --glass-bg: rgba(255, 255, 255, 0.025);
            --glass-border: rgba(255, 255, 255, 0.15);
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            width: 1920px;
            height: 1080px;
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-body);
            overflow: hidden;
            position: relative;
            padding: 70px 90px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .grid-bg {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.01) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.01) 1px, transparent 1px);
            background-size: 80px 80px;
            z-index: 1;
        }}
        .glow-radial {{
            position: absolute;
            top: 30%; left: 50%;
            width: 1200px; height: 800px;
            background: radial-gradient(circle, rgba(255, 91, 53, 0.04) 0%, rgba(0, 242, 254, 0.03) 50%, transparent 100%);
            filter: blur(120px);
            z-index: 2;
            transform: translate(-50%, -50%);
        }}
        .slide-header {{
            position: relative;
            z-index: 10;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 1px solid rgba(255,255,255,0.08);
            padding-bottom: 20px;
        }}
        .module-num {{
            font-family: var(--font-display);
            font-size: 18px;
            font-weight: 700;
            color: var(--primary-accent);
            letter-spacing: 0.15em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }}
        .slide-title {{
            font-family: var(--font-display);
            font-size: 46px;
            font-weight: 800;
            letter-spacing: -0.01em;
            background: linear-gradient(135deg, #FFF, #E2E8F0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .brand-watermark {{
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 600;
            color: var(--text-muted);
            letter-spacing: 0.25em;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .brand-watermark::before {{ content: '🦅'; }}
        .content-area {{
            position: relative;
            z-index: 10;
            height: 740px;
            margin-top: 30px;
        }}
        .panel {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 35px;
            position: relative;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .panel:hover {{
            border-color: rgba(255, 255, 255, 0.2);
            background: rgba(255, 255, 255, 0.04);
            box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        }}
        .panel-title {{
            font-size: 30px;
            font-weight: 800;
            color: #FFF;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .panel-title::before {{
            content: '';
            display: inline-block;
            width: 5px;
            height: 28px;
            background-color: var(--primary-accent);
            border-radius: 2.5px;
        }}
        .panel-title.teal::before {{
            background-color: var(--secondary-accent);
        }}
        .panel-title.purple::before {{
            background-color: #A855F7;
        }}
        .bottom-alert {{
            background: rgba(255, 255, 255, 0.015);
            border-left: 4px solid var(--secondary-accent);
            padding: 16px 24px;
            border-radius: 0 12px 12px 0;
            font-size: 18px;
            color: #F8FAFC;
            line-height: 1.6;
        }}
        .bottom-alert strong {{ color: var(--primary-accent); }}
        
        /* 視覺元件基礎樣式 */
        .highlight-number {{
            font-family: var(--font-display);
            font-size: 64px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary-accent), #FF8A00);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            line-height: 1;
        }}
        .highlight-number.teal {{
            background: linear-gradient(135deg, var(--secondary-accent), #00A3FF);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        @keyframes slideInUp {{
            from {{ opacity: 0; transform: translateY(35px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .animate-fade {{
            animation: slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}
        .delay-1 {{ animation-delay: 0.1s; }}
        .delay-2 {{ animation-delay: 0.25s; }}
        .delay-3 {{ animation-delay: 0.4s; }}
        {extra_style}

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

    </style>
</head>
<body>

    <div id="mobile-rotate-overlay">
        <div style="font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;">📱</div>
        <h2 style="font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">請旋轉您的手機</h2>
        <p style="font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>
    </div>
    <div class="grid-bg"></div>
    <div class="glow-radial"></div>
    <div class="slide-header">
        <div>
            <div class="module-num">{module_name} ｜ SLIDE {slide_num}</div>
            <h2 class="slide-title">{title}</h2>
        </div>
        <div class="brand-watermark">PHOENIX AI CONSULTING</div>
    </div>
    <div class="content-area">
"""

footer = """
    </div>
</body>
</html>
"""

# Slide 01: Cover (極致奢華標題頁，專屬恆達與洪董事長)
cover_html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>恆達精密專屬：2026 鳳凰 AI 企業級營運落地與人才培育課程方案</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #070913;
            --primary-accent: #FF5B35;
            --secondary-accent: #00F2FE;
            --text-main: #FFFFFF;
            --text-muted: #E2E8F0;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.15);
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            width: 1920px; height: 1080px;
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-body);
            overflow: hidden;
            position: relative;
        }
        .grid-bg {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
            background-size: 80px 80px;
            z-index: 1;
        }
        .glow-orange {
            position: absolute; top: -200px; right: -100px; width: 900px; height: 900px;
            background: radial-gradient(circle, rgba(255, 91, 53, 0.1) 0%, transparent 70%);
            filter: blur(100px); z-index: 2;
        }
        .glow-blue {
            position: absolute; bottom: -300px; left: -200px; width: 1000px; height: 1000px;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.08) 0%, transparent 70%);
            filter: blur(120px); z-index: 2;
        }
        .container {
            position: relative; z-index: 10;
            width: 100%; height: 100%;
            display: flex; flex-direction: column;
            justify-content: space-between;
            padding: 90px 110px;
        }
        .header { display: flex; justify-content: space-between; align-items: center; }
        .brand { display: flex; align-items: center; gap: 12px; }
        .brand-logo {
            width: 38px; height: 38px;
            background: linear-gradient(135deg, var(--primary-accent), #FF8A00);
            border-radius: 10px; display: flex; align-items: center; justify-content: center;
            font-weight: 800; font-family: var(--font-display); font-size: 22px; color: #fff;
            box-shadow: 0 0 25px rgba(255, 91, 53, 0.4);
        }
        .brand-name {
            font-family: var(--font-display); font-weight: 700; font-size: 24px;
            letter-spacing: 0.15em; background: linear-gradient(to right, #FFF, #C2CFE0);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .badge {
            background: rgba(255, 91, 53, 0.15); border: 1px solid rgba(255, 91, 53, 0.3);
            color: #FF7D5A; padding: 8px 20px; border-radius: 20px;
            font-size: 16px; font-weight: 700; letter-spacing: 0.08em;
        }
        .hero { max-width: 1400px; margin-top: 20px; }
        .client-tag {
            font-size: 28px; font-weight: 700; color: var(--secondary-accent);
            letter-spacing: 0.2em; margin-bottom: 24px; display: flex; align-items: center; gap: 16px;
        }
        .client-tag::before {
            content: ''; display: inline-block; width: 32px; height: 3px; background-color: var(--secondary-accent);
        }
        .title {
            font-family: var(--font-display); font-size: 80px; font-weight: 900;
            line-height: 1.15; letter-spacing: -0.015em; margin-bottom: 30px;
            background: linear-gradient(135deg, #FFFFFF 0%, #E2ECF6 50%, #A5B6CA 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .title span {
            background: linear-gradient(135deg, var(--primary-accent), #FF8E53);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            font-weight: 900;
        }
        .subtitle {
            font-size: 26px; font-weight: 400; color: #FFF;
            max-width: 1200px; line-height: 1.65; letter-spacing: 0.05em;
        }
        .footer {
            display: grid; grid-template-columns: 1.1fr 0.9fr;
            border-top: 1px solid var(--glass-border); padding-top: 35px; margin-top: 30px;
        }
        .meta-group { display: flex; flex-direction: column; gap: 8px; }
        .meta-label {
            font-size: 16px; text-transform: uppercase; letter-spacing: 0.15em;
            color: var(--primary-accent); font-weight: 700;
        }
        .meta-value { font-size: 24px; font-weight: 700; color: #FFFFFF; }
        .meta-value span { color: var(--secondary-accent); font-size: 18px; font-weight: 500; margin-left: 8px; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(25px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade { animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .delay-1 { animation-delay: 0.15s; }
        .delay-2 { animation-delay: 0.3s; }
        .delay-3 { animation-delay: 0.45s; }

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

    </style>
</head>
<body>

    <div id="mobile-rotate-overlay">
        <div style="font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;">📱</div>
        <h2 style="font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">請旋轉您的手機</h2>
        <p style="font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>
    </div>
    <div class="grid-bg"></div>
    <div class="glow-orange"></div>
    <div class="glow-blue"></div>
    <div class="container">
        <div class="header animate-fade">
            <div class="brand">
                <div class="brand-logo">🦅</div>
                <div class="brand-name">PHOENIX AI</div>
            </div>
            <div class="badge">CONFIDENTIAL &amp; PROPRIETARY</div>
        </div>
        <div class="hero">
            <div class="client-tag animate-fade delay-1">HENDAR PRECISION FASTENERS</div>
            <h1 class="title animate-fade delay-2">
                恆達精密扣件專屬<br>
                <span>2026 鳳凰 AI</span> 企業級營運落地<br>
                與人才培育課程方案
            </h1>
            <p class="subtitle animate-fade delay-3">
                針對高雄岡山螺絲聚落「高噪、滿手油污、車規零容錯」極端產線客製。全面實施「無痛去技術化、客製情境化、國際出口合規與政策轉化」重構，協助貴公司建立剛性競爭力。
            </p>
        </div>
        <div class="footer animate-fade delay-3">
            <div class="meta-group">
                <span class="meta-label">Prepared For ｜ 致</span>
                <span class="meta-value">洪建國 董事長暨總經理 閣下 <span>恆達精密扣件 (岡山螺絲大廠 / 數百人規模)</span></span>
            </div>
            <div class="meta-group" style="padding-left: 60px; border-left: 1px solid rgba(255,255,255,0.08);">
                <span class="meta-label">Presented By ｜ 由</span>
                <span class="meta-value">鳳凰 AI 顧問團隊 <span>首席顧問 孟淑慧 ＆ 策略長 陳文家</span></span>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Slide 02: Intro / Executive Summary (可點擊交互卡片設計)
intro_body = """
    <div style="display: grid; grid-template-columns: 0.95fr 1.05fr; gap: 40px; height: 100%;">
        <!-- 左欄：大膽的核心承諾卡片 -->
        <div class="panel animate-fade delay-1" style="display: flex; flex-direction: column; justify-content: space-between; border-left: 5px solid var(--primary-accent);">
            <div>
                <h3 class="panel-title">恆達精密專屬 ｜ 實事求是的承諾</h3>
                <div style="font-size: 22px; color: #FFF; line-height: 1.75; display: flex; flex-direction: column; gap: 24px; margin-top: 20px;">
                    <p style="font-size: 28px; font-weight: 900; color: var(--primary-accent); line-height: 1.4;">
                        「我們不跟黑手師傅講虛無縹緲的 AI 理論，我們直接對齊產線保命的痛點！」
                    </p>
                    <p>
                        在冷鍛機運作 <strong style="color: var(--secondary-accent); font-size: 26px;">85 分貝噪音</strong>、滿是防鏽油與鐵粉的極端現場，任何繁雜的平板 UI 都是廢紙。
                    </p>
                    <p>
                        本方案絕不講「畫大餅」的噱頭。每個模組完全對齊產線實況，將公版框架徹底<strong>去技術化、情境化、財務量化</strong>，直擊商業損益。
                    </p>
                </div>
            </div>
            <div class="bottom-alert">
                <strong>🦅 顧問精神：</strong> 「教材即程式碼」。寫得出來、講得清楚、在廠房裡做得到，才叫落地。
            </div>
        </div>
        
        <!-- 右欄：四大戰實對標指標（排版清新通透，可點擊動態高亮） -->
        <div style="display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
            <div class="panel animate-fade delay-2" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h3 class="panel-title teal">四項最真實的實戰對標評判 <span>(滑鼠懸停觸發發光)</span></h3>
                    <div style="display: flex; flex-direction: column; gap: 18px; margin-top: 15px;">
                        <div class="interactive-card" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 18px 24px; border-radius: 12px; font-size: 19px; line-height: 1.6; transition: all 0.3s; cursor: pointer;" onmouseover="this.style.borderColor='#00F2FE'; this.style.boxShadow='0 0 15px rgba(0,242,254,0.2)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.12)'; this.style.boxShadow='none';">
                            <strong style="color: var(--secondary-accent); font-size: 21px; display: block; margin-bottom: 4px;">🛠️ 01. 現場落地性 ─ 解放雙手</strong>
                            語音 AI 徹底解放雙手，岡山口音專用語意詞庫，85dB 高噪拾音（識別率 &ge; 92%）。
                        </div>
                        <div class="interactive-card" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 18px 24px; border-radius: 12px; font-size: 19px; line-height: 1.6; transition: all 0.3s; cursor: pointer;" onmouseover="this.style.borderColor='#00F2FE'; this.style.boxShadow='0 0 15px rgba(0,242,254,0.2)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.12)'; this.style.boxShadow='none';">
                            <strong style="color: var(--secondary-accent); font-size: 21px; display: block; margin-bottom: 4px;">💰 02. 財務控本性 ─ 輕量 API</strong>
                            拒做高昂大模型自研。採取 API 輕量架構，優化 TCO，極速收回轉型資本。
                        </div>
                        <div class="interactive-card" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 18px 24px; border-radius: 12px; font-size: 19px; line-height: 1.6; transition: all 0.3s; cursor: pointer;" onmouseover="this.style.borderColor='#00F2FE'; this.style.boxShadow='0 0 15px rgba(0,242,254,0.2)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.12)'; this.style.boxShadow='none';">
                            <strong style="color: var(--secondary-accent); font-size: 21px; display: block; margin-bottom: 4px;">🇪🇺 03. 國際外銷合規 ─ 審計軌跡</strong>
                            對齊 ISO 42001 安全數據治理與 Audit Trails 密碼日誌，應對車廠 Supplier Audit。
                        </div>
                        <div class="interactive-card" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 18px 24px; border-radius: 12px; font-size: 19px; line-height: 1.6; transition: all 0.3s; cursor: pointer;" onmouseover="this.style.borderColor='#00F2FE'; this.style.boxShadow='0 0 15px rgba(0,242,254,0.2)';" onmouseout="this.style.borderColor='rgba(255,255,255,0.12)'; this.style.boxShadow='none';">
                            <strong style="color: var(--secondary-accent); font-size: 21px; display: block; margin-bottom: 4px;">💸 04. 政策轉化套利 ─ 百萬補助</strong>
                            深度對接產發署智慧製造/綠色升級補助，以政府政策紅利為企業自身研發買單。
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

# Slide 03: Module 1 (M01 CEO 戰略速覽 - 重構為上中下視覺流與水平時間軸)
module1_body = """
    <div style="display: grid; grid-template-rows: 1.25fr 0.75fr; gap: 30px; height: 100%;">
        <!-- 上排：AI 三種型態 3 欄式卡片（視覺對比強烈，字大） -->
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px;">
            <div class="panel animate-fade delay-1" style="border-top: 5px solid var(--primary-accent); justify-content: flex-start; padding: 30px;">
                <h4 style="font-size: 26px; color: var(--primary-accent); margin-bottom: 12px; font-weight: 800;">🧠 1. 生成式 AI</h4>
                <p style="font-size: 20px; color: #FFF; line-height: 1.65;">
                    <strong>會寫 SOP、會跟師傅對話。</strong><br><br>
                    主要用於文書、異常語音即時通報、換模語音導引與現場歷史障礙 RAG 語音檢索。
                </p>
            </div>
            <div class="panel animate-fade delay-2" style="border-top: 5px solid var(--secondary-accent); justify-content: flex-start; padding: 30px;">
                <h4 style="font-size: 26px; color: var(--secondary-accent); margin-bottom: 12px; font-weight: 800;">👁️ 2. 鑑別式 AI</h4>
                <p style="font-size: 20px; color: #FFF; line-height: 1.65;">
                    <strong>會挑瑕疵、會抓規格混料。</strong><br><br>
                    主要應用於 <strong>AOI 光學影像篩選機的二次覆檢</strong>，非侵入式外掛架構抓取缺陷。
                </p>
            </div>
            <div class="panel animate-fade delay-3" style="border-top: 5px solid #A855F7; justify-content: flex-start; padding: 30px;">
                <h4 style="font-size: 26px; color: #A855F7; margin-bottom: 12px; font-weight: 800;">⚙️ 3. 決策式 AI</h4>
                <p style="font-size: 20px; color: #FFF; line-height: 1.65;">
                    <strong>會預測針壽命、會排程最佳化。</strong><br><br>
                    主要用於打頭機<strong>沖棒與打頭針斷裂預測</strong>，建立 3級預警機制避免無預警機損。
                </p>
            </div>
        </div>
        
        <!-- 下排：P&L 損益表對齊與 18個月路線時間軸 -->
        <div class="panel animate-fade delay-3" style="display: flex; flex-direction: row; justify-content: space-between; align-items: center; padding: 25px 40px;">
            <div style="max-width: 45%; border-right: 1px solid rgba(255,255,255,0.1); padding-right: 40px;">
                <h4 style="font-size: 24px; color: var(--primary-accent); margin-bottom: 8px; font-weight: 800;">📊 P&L 損益表對齊法</h4>
                <p style="font-size: 19px; color: #E2E8F0; line-height: 1.6;">
                    不講科技噱頭，只算<strong>「省多少模具費、降低多少退貨罰金、節省多少 QC 人力」</strong>。現場提供 <strong>AI 專案 ROI 一頁試算表</strong>。
                </p>
            </div>
            
            <div style="flex-grow: 1; padding-left: 40px;">
                <h4 style="font-size: 24px; color: var(--secondary-accent); margin-bottom: 15px; font-weight: 800;">📅 18 個月漸進式戰略路線軸</h4>
                <!-- 視覺化流程 -->
                <div style="display: flex; justify-content: space-between; align-items: center; position: relative;">
                    <div style="position: absolute; left: 5%; right: 5%; height: 3px; background: rgba(255,255,255,0.15); z-index: 1;"></div>
                    <div style="z-index: 2; background: var(--bg-color); border: 2px solid var(--primary-accent); border-radius: 10px; padding: 8px 16px; text-align: center; width: 28%; box-shadow: 0 0 15px rgba(255, 91, 53, 0.2);">
                        <span style="font-size: 17px; font-weight: 800; color: var(--primary-accent); display: block;">1-3M ｜ 盤點期</span>
                        <span style="font-size: 16px; color: #FFF; font-weight: 600;">Quick-Win 試點場景</span>
                    </div>
                    <div style="z-index: 2; background: var(--bg-color); border: 2px solid var(--secondary-accent); border-radius: 10px; padding: 8px 16px; text-align: center; width: 28%; box-shadow: 0 0 15px rgba(0, 242, 254, 0.2);">
                        <span style="font-size: 17px; font-weight: 800; color: var(--secondary-accent); display: block;">4-9M ｜ 試點期</span>
                        <span style="font-size: 16px; color: #FFF; font-weight: 600;">第一條冷鍛線降噪訓練</span>
                    </div>
                    <div style="z-index: 2; background: var(--bg-color); border: 2px solid #A855F7; border-radius: 10px; padding: 8px 16px; text-align: center; width: 28%; box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);">
                        <span style="font-size: 17px; font-weight: 800; color: #A855F7; display: block;">10-18M ｜ 複製期</span>
                        <span style="font-size: 16px; color: #FFF; font-weight: 600;">全廠複製、ISO與碳合規</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
"""

# Slide 04: Module 2 - Part 1 (M06 工業語音 AI - 實施實時聲學降噪「互動波形對比器」)
module2_1_body = """
    <div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; height: 100%;">
        <!-- 左欄：聲學降噪與工法字典視覺展示 -->
        <div class="panel animate-fade delay-1" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 class="panel-title">85分貝冷鍛高噪產線 ｜ 骨傳導聲學降噪實務</h3>
                
                <!-- 互動聲學面板 -->
                <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--glass-border); border-radius: 15px; padding: 25px; margin-top: 15px; position: relative;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <span style="font-size: 18px; font-weight: 800; color: var(--primary-accent);" id="soundStatus">🔊 產線環境噪音 (模擬 85分貝)</span>
                        <button onclick="toggleNoise()" id="noiseBtn" style="background: linear-gradient(135deg, var(--secondary-accent), #00A3FF); border: 0; color: #000; padding: 8px 20px; border-radius: 20px; font-size: 17px; font-weight: 700; cursor: pointer; transition: all 0.3s; box-shadow: 0 0 15px rgba(0,242,254,0.3);" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            🎚️ 開啟 RNNoise 降噪模式
                        </button>
                    </div>
                    
                    <div style="display: flex; align-items: center; justify-content: space-between; height: 120px; gap: 15px; background: rgba(0,0,0,0.4); border-radius: 10px; padding: 15px;">
                        <!-- 左側：原始噪聲 -->
                        <div style="width: 45%; height: 100%; position: relative;">
                            <svg width="100%" height="100%" viewBox="0 0 200 100">
                                <path id="noiseWave" d="M 0,50 Q 5,20 10,80 T 20,20 T 30,85 T 40,15 T 50,75 T 60,30 T 70,80 T 80,10 T 90,90 T 100,20 T 110,85 T 120,20 T 130,70 T 140,25 T 150,85 T 160,15 T 170,80 T 180,30 T 190,75 T 200,50" fill="none" stroke="#FF5B35" stroke-width="3"></path>
                            </svg>
                            <span style="position: absolute; bottom: 5px; left: 10px; font-size: 14px; font-weight: 700; color: #FF5B35; background: rgba(0,0,0,0.6); padding: 2px 6px; border-radius: 4px;">輸入音訊 (環境干擾)</span>
                        </div>
                        
                        <!-- 骨傳導顴骨拾音 -->
                        <div style="text-align: center; width: 10%; flex-shrink: 0;">
                            <span style="font-size: 32px; display: block;" id="headphoneEmoji">🎧</span>
                        </div>
                        
                        <!-- 右側：降噪後 -->
                        <div style="width: 45%; height: 100%; position: relative;">
                            <svg width="100%" height="100%" viewBox="0 0 200 100">
                                <path id="cleanWave" d="M 0,50 Q 5,20 10,80 T 20,20 T 30,85 T 40,15 T 50,75 T 60,30 T 70,80 T 80,10 T 90,90 T 100,20 T 110,85 T 120,20 T 130,70 T 140,25 T 150,85 T 160,15 T 170,80 T 180,30 T 190,75 T 200,50" fill="none" stroke="#8E9AA8" stroke-width="2"></path>
                            </svg>
                            <span id="cleanBadge" style="position: absolute; bottom: 5px; right: 10px; font-size: 14px; font-weight: 700; color: #FFF; background: rgba(0,0,0,0.6); padding: 2px 6px; border-radius: 4px;">未降噪</span>
                        </div>
                    </div>
                </div>
                
                <div style="font-size: 20px; color: #FFF; line-height: 1.65; margin-top: 25px; display: flex; flex-direction: column; gap: 15px;">
                    <p>
                        <strong>骨傳導耳麥</strong> 直接拾取顴骨聲帶震動，可自然衰減 <strong>20-30 dB</strong> 的外部敲擊與搓牙高頻噪音。
                    </p>
                    <p>
                        <strong>邊緣降噪盒子</strong> 於產線端部署 <code>RNNoise</code>，將殘餘噪音剝離，只將乾淨的人聲送上雲端，降低推論延遲。
                    </p>
                </div>
            </div>
            
            <div class="bottom-alert">
                <strong>💡 岡山國語與日式術語微調：</strong> 收錄「si-to-ma (檔塊)」、「ゲージ (Gauge)」等外來語，<strong>語意識別率 &ge; 92%</strong>！
            </div>
        </div>
        
        <!-- 右欄：Realtime API 與 RAG 設計 -->
        <div class="panel animate-fade delay-2" style="display: flex; flex-direction: column; justify-content: space-between; border-right: 5px solid var(--secondary-accent);">
            <div>
                <h3 class="panel-title teal">即時對話 API 與 RAG 知識檢索</h3>
                <div style="display: flex; flex-direction: column; gap: 24px; margin-top: 20px;">
                    <div style="background: rgba(0,242,254,0.03); border: 1px solid rgba(0,242,254,0.15); padding: 22px 26px; border-radius: 12px;">
                        <strong style="color: var(--secondary-accent); font-size: 22px; display: block; margin-bottom: 8px;">⚡ Realtime API 極速響應</strong>
                        <span style="font-size: 18.5px; color: #FFF; line-height: 1.65; display: block;">
                            摒棄傳統 3-5 秒的高延遲語音流程，延遲壓在 <strong>&lt; 0.8 秒</strong>，師傅能隨時打斷 AI 說話，AI 亦能即時追問。
                        </span>
                    </div>
                    
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 22px 26px; border-radius: 12px;">
                        <strong style="color: #FFF; font-size: 22px; display: block; margin-bottom: 8px;">📚 檢索增強生成 (RAG)</strong>
                        <span style="font-size: 18.5px; color: #E2E8F0; line-height: 1.65; display: block;">
                            師傅提問「M8 螺絲牙搓不上」時，AI 即時檢索中央知識庫、過去 3 個月不良品歷史分析、搓牙機參數 SOP 進行播報。
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="bottom-alert" style="border-left-color: var(--primary-accent);">
                <strong>🏆 核心產出：</strong> 骨傳導耳麥 + 降噪網閘 + 語音 RAG，並發布 500 個術語的**工法專用詞庫 v1.0**。
            </div>
        </div>
    </div>
    
    <script>
        let noiseMode = false;
        function toggleNoise() {
            noiseMode = !noiseMode;
            const noiseWave = document.getElementById('noiseWave');
            const cleanWave = document.getElementById('cleanWave');
            const cleanBadge = document.getElementById('cleanBadge');
            const noiseBtn = document.getElementById('noiseBtn');
            const soundStatus = document.getElementById('soundStatus');
            const headphoneEmoji = document.getElementById('headphoneEmoji');
            
            if (noiseMode) {
                // 降噪狀態
                noiseBtn.innerText = "🔇 重置環境噪音模式";
                noiseBtn.style.background = "linear-gradient(135deg, var(--primary-accent), #FF8A00)";
                soundStatus.innerHTML = "🟢 語音極速降噪過濾中 (剩餘干擾 &lt; 5%)";
                soundStatus.style.color = "var(--secondary-accent)";
                cleanBadge.innerText = "RNNoise 降噪啟用";
                cleanBadge.style.color = "var(--secondary-accent)";
                cleanBadge.style.background = "rgba(0,242,254,0.15)";
                headphoneEmoji.innerHTML = "⚡";
                
                // 動態扁平波形
                cleanWave.setAttribute('d', "M 0,50 Q 15,45 30,55 T 60,40 T 90,60 T 120,40 T 150,60 T 180,45 T 200,50");
                cleanWave.setAttribute('stroke', "#00F2FE");
                cleanWave.setAttribute('stroke-width', "3");
            } else {
                // 還原原始高噪波形
                noiseBtn.innerText = "🎚️ 開啟 RNNoise 降噪模式";
                noiseBtn.style.background = "linear-gradient(135deg, var(--secondary-accent), #00A3FF)";
                soundStatus.innerHTML = "🔊 產線環境噪音 (模擬 85分貝)";
                soundStatus.style.color = "var(--primary-accent)";
                cleanBadge.innerText = "未降噪";
                cleanBadge.style.color = "#FFF";
                cleanBadge.style.background = "rgba(0,0,0,0.6)";
                headphoneEmoji.innerHTML = "🎧";
                
                // 動態混亂波形
                cleanWave.setAttribute('d', "M 0,50 Q 5,20 10,80 T 20,20 T 30,85 T 40,15 T 50,75 T 60,30 T 70,80 T 80,10 T 90,90 T 100,20 T 110,85 T 120,20 T 130,70 T 140,25 T 150,85 T 160,15 T 170,80 T 180,30 T 190,75 T 200,50");
                cleanWave.setAttribute('stroke', "#8E9AA8");
                cleanWave.setAttribute('stroke-width', "2");
            }
        }
    </script>
"""

# Slide 05: Module 2 - Part 2 (M06 語音 AI 實施「互動指令沙盒」)
module2_2_body = """
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; height: 100%;">
        <!-- 左欄：三大語音試點場景 (精簡文字，點擊連動右側沙盒) -->
        <div class="panel animate-fade delay-1" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 class="panel-title">現場「解放雙手」三大語音試點場景 <span>(點擊模擬執行)</span></h3>
                <div style="display: flex; flex-direction: column; gap: 16px; margin-top: 15px;">
                    <div onclick="runSandbox('A')" id="cardA" style="background: rgba(0,242,254,0.06); border: 2px solid var(--secondary-accent); padding: 18px 24px; border-radius: 12px; cursor: pointer; transition: all 0.3s;">
                        <strong style="color: var(--secondary-accent); font-size: 22px; display: block; margin-bottom: 4px;">場景 A ｜ 換模 SOP 語音導引</strong>
                        <span style="font-size: 18px; color: #FFF; line-height: 1.6; display: block;">
                            新進師傅更換 M10 螺絲模具時，耳機裡的 AI 語音導引每一步鎖緊力矩，喊「下一個」繼續。
                        </span>
                    </div>
                    <div onclick="runSandbox('B')" id="cardB" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 18px 24px; border-radius: 12px; cursor: pointer; transition: all 0.3s;">
                        <strong style="color: var(--primary-accent); font-size: 22px; display: block; margin-bottom: 4px;">場景 B ｜ 異常通報與語音即時派工</strong>
                        <span style="font-size: 18px; color: #FFF; line-height: 1.6; display: block;">
                            師傅聽到機台異音，喊一句：「3 號打頭機異音，疑似沖棒裂。」系統在 MES 自動派工建單。
                        </span>
                    </div>
                    <div onclick="runSandbox('C')" id="cardC" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 18px 24px; border-radius: 12px; cursor: pointer; transition: all 0.3s;">
                        <strong style="color: #A855F7; font-size: 22px; display: block; margin-bottom: 4px;">場景 C ｜ 現場歷史障礙快速語音問答</strong>
                        <span style="font-size: 18px; color: #FFF; line-height: 1.6; display: block;">
                            「上次 SUS304 搓牙崩牙是怎麼解的？」AI 自動翻查歷史排障報告並即時用語音播報。
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="bottom-alert">
                <strong>💡 現場驗收指標：</strong> 新人上崗第一天，無需人員現場陪同，完全靠語音引導順利完成換模。
            </div>
        </div>
        
        <!-- 右欄：語音 RAG 沙盒模擬終端 (高對比度，大字體，動態輸出) -->
        <div class="panel animate-fade delay-2" style="display: flex; flex-direction: column; justify-content: space-between; border-right: 5px solid var(--secondary-accent);">
            <div>
                <h3 class="panel-title teal">RAG 實時資訊流 ─ 沙盒模擬器</h3>
                
                <!-- 沙盒終端機 -->
                <div style="background: #000; border: 2px solid var(--glass-border); border-radius: 15px; padding: 25px; height: 350px; font-family: monospace; font-size: 18px; display: flex; flex-direction: column; gap: 15px; color: #00FF66;" id="sandboxTerminal">
                    <div><span style="color:#FFF;">[系統監控]</span> 語音 RAG 沙盒已就緒，請點擊左側場景...</div>
                    <div style="color: var(--secondary-accent); font-weight: bold; font-size: 20px;">[師傅語音輸入]:</div>
                    <div id="termInput" style="color: #FFF; padding-left: 20px;">「師傅喊：『下一步』」</div>
                    <div style="color: #FF5B35; font-weight: bold; font-size: 20px;">[中央 RAG 檢索]:</div>
                    <div id="termRAG" style="color: #CBD5E1; padding-left: 20px;">檢索 M10模具換模手冊 ➔ 步驟 3/8: 清潔模仁及沖棒公差。</div>
                    <div style="color: #A855F7; font-weight: bold; font-size: 20px;">[0.8秒實時語音播報 (TTS)]:</div>
                    <div id="termOutput" style="color: #00FF66; padding-left: 20px;">🔊 「師傅，第三步，請用乾淨棉布將模仁內腔擦拭乾淨，並檢查沖棒間隙。」</div>
                </div>
            </div>
            
            <div class="bottom-alert" style="border-left-color: var(--primary-accent);">
                <strong>💡 岡山國語優勢：</strong> 無痛降噪與術語微調，消除了一線藍領移工與師傅對新設備的抗拒心理。
            </div>
        </div>
    </div>
    
    <script>
        const sandboxData = {
            A: {
                title: "場景 A ｜ 換模 SOP 語音導引",
                input: "「師傅喊：『下一步』」",
                rag: "檢索 M10 模具換模 SOP ➔ 步驟 3/8: 清潔模仁及檢查沖棒間隙。",
                output: "🔊 「師傅，第三步，請用乾淨棉布將模仁內腔擦拭乾淨，並檢查打頭針鎖緊間隙。」"
            },
            B: {
                title: "場景 B ｜ 異常通報與語音即時派工",
                input: "「師傅喊：『3號機疑似打頭針斷裂』」",
                rag: "觸發異常特徵匹配 ➔ 自動寫入 MES 派工系統 ➔ 建立保全維修工單。",
                output: "🔊 「收到！3號冷鍛機異常已立案，保全維修課已收到簡訊通報，預計5分鐘內到達。」"
            },
            C: {
                title: "場景 C ｜ 現場歷史障礙快速語音問答",
                input: "「師傅問：『SUS304 不鏽鋼搓牙崩牙怎麼辦？』」",
                rag: "檢索歷史排障報告 ➔ 提取 2025.10 岡山廠搓牙事故 ➔ 判定崩牙肇因。",
                output: "🔊 「師傅，根據三個月前紀錄，建議將滾牙輪轉速調降 5%，並改用極壓型二號成型油。」"
            }
        };
        
        function runSandbox(scene) {
            // 變更卡片高亮
            ['A', 'B', 'C'].forEach(s => {
                const card = document.getElementById('card' + s);
                if (s === scene) {
                    card.style.background = s === 'A' ? 'rgba(0,242,254,0.06)' : (s === 'B' ? 'rgba(255,91,53,0.06)' : 'rgba(168,85,247,0.06)');
                    card.style.borderColor = s === 'A' ? 'var(--secondary-accent)' : (s === 'B' ? 'var(--primary-accent)' : '#A855F7');
                    card.style.borderWidth = '2px';
                } else {
                    card.style.background = 'rgba(255,255,255,0.02)';
                    card.style.borderColor = 'var(--glass-border)';
                    card.style.borderWidth = '1px';
                }
            });
            
            // 變更終端機內容
            document.getElementById('termInput').innerText = sandboxData[scene].input;
            document.getElementById('termRAG').innerText = sandboxData[scene].rag;
            document.getElementById('termOutput').innerText = sandboxData[scene].output;
        }
    </script>
"""

# Slide 06: Module 3 (M05 + Unit 5 AOI 篩選機二次覆檢 - 大對比與混淆矩陣重構)
module3_body = """
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; height: 100%;">
        <!-- 左欄：非侵入式外掛架構 -->
        <div class="panel animate-fade delay-1" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 class="panel-title">M05 ｜ 既有百萬 AOI 篩選機的 AI 二次覆檢</h3>
                
                <!-- 視覺化外掛流程圖 -->
                <div style="background: rgba(0,0,0,0.2); border: 1px solid var(--glass-border); border-radius: 15px; padding: 25px; margin-top: 15px; text-align: center;">
                    <div style="display: flex; align-items: center; justify-content: space-around; gap: 10px;">
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--glass-border); padding: 15px; border-radius: 10px; width: 30%;">
                            <span style="font-size: 30px; display: block; margin-bottom: 5px;">⚙️</span>
                            <span style="font-size: 17px; font-weight: 700; color: #FFF;">原廠 AOI 篩選機</span>
                        </div>
                        <span style="font-size: 24px; color: var(--primary-accent);">➔</span>
                        <div style="background: rgba(255,91,53,0.1); border: 2px solid var(--primary-accent); padding: 15px; border-radius: 10px; width: 35%;">
                            <span style="font-size: 16px; font-weight: 800; color: var(--primary-accent); display: block; margin-bottom: 5px;">分流拷貝 ➔ 不動設備</span>
                            <span style="font-size: 18px; font-weight: 700; color: #FFF;">AI 二次品檢控制層</span>
                        </div>
                        <span style="font-size: 24px; color: var(--secondary-accent);">➔</span>
                        <div style="background: rgba(0,242,254,0.1); border: 2px solid var(--secondary-accent); padding: 15px; border-radius: 10px; width: 30%;">
                            <span style="font-size: 30px; display: block; margin-bottom: 5px;">🖥️</span>
                            <span style="font-size: 17px; font-weight: 700; color: #FFF;">YOLOv8 推論 &lt;50ms</span>
                        </div>
                    </div>
                </div>
                
                <div style="font-size: 20px; color: #FFF; line-height: 1.6; margin-top: 25px; display: flex; flex-direction: column; gap: 15px;">
                    <p>
                        <strong>非侵入式外掛架構：</strong> 直接從篩選機的相機輸出端（USB/網孔）複製一份影像，原機運作速度完全不受影響。
                    </p>
                    <p>
                        <strong>零硬體保固風險：</strong> 絕不動到進口設備的封閉黑盒子系統，做壞了隨時拔掉，零風險。
                    </p>
                </div>
            </div>
            
            <div class="bottom-alert">
                <strong>💡 缺陷數據集：</strong> 每種缺陷（牙紋不全、頭部裂、生鏽等）在現場採集 <strong>500 張正例 + 2000 張反例</strong>，確保模型精準。
            </div>
        </div>
        
        <!-- 右欄：混淆矩陣與成本大圖 (高對比度，大字體) -->
        <div class="panel animate-fade delay-2" style="display: flex; flex-direction: column; justify-content: space-between; border-right: 5px solid var(--secondary-accent);">
            <div>
                <h3 class="panel-title teal">二次品檢混淆矩陣與車規成本精算</h3>
                
                <!-- 成本精算卡片 -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 15px;">
                    <div style="background: rgba(255,91,53,0.08); border: 2px solid var(--primary-accent); padding: 20px; border-radius: 12px;">
                        <span style="font-size: 16px; font-weight: 800; color: var(--primary-accent); display: block; margin-bottom: 5px;">⚠️ 偽陰性 (漏檢) FN</span>
                        <strong style="font-size: 22px; color: #FFF; display: block;">車規客戶退貨、抽單</strong>
                        <span style="font-size: 15px; color: #FFF; margin-top: 5px; display: block;">➔ 客訴賠償，成本高昂！</span>
                    </div>
                    
                    <div style="background: rgba(255,138,0,0.08); border: 2px solid #FF8A00; padding: 20px; border-radius: 12px;">
                        <span style="font-size: 16px; font-weight: 800; color: #FF8A00; display: block; margin-bottom: 5px;">⚠️ 偽陽性 (誤殺) FP</span>
                        <strong style="font-size: 22px; color: #FFF; display: block;">良品誤判為不良品</strong>
                        <span style="font-size: 15px; color: #FFF; margin-top: 5px; display: block;">➔ 二手人工覆檢工時成本。</span>
                    </div>
                </div>
                
                <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 18px; margin-top: 25px;">
                    <thead>
                        <tr style="border-bottom: 2px solid rgba(255,255,255,0.15); background: rgba(255,255,255,0.03);">
                            <th style="padding: 12px; color: var(--secondary-accent); font-weight: 700;">分類結果</th>
                            <th style="padding: 12px; color: var(--secondary-accent); font-weight: 700;">實際為良品</th>
                            <th style="padding: 12px; color: var(--secondary-accent); font-weight: 700;">實際為不良品</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);">
                            <td style="padding: 14px; font-weight: 700;">AI 良品</td>
                            <td style="padding: 14px; color: #FFF;">真陰性 (TN) ｜ ✅ 通過</td>
                            <td style="padding: 14px; color: var(--primary-accent); font-weight: 800;">偽陰性 (FN) ｜ ❌ 漏檢</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.08);">
                            <td style="padding: 14px; font-weight: 700;">AI 不良</td>
                            <td style="padding: 14px; color: #FF8A00;">偽陽性 (FP) ｜ ⚠️ 誤判</td>
                            <td style="padding: 14px; color: var(--secondary-accent); font-weight: 800;">真陽性 (TP) ｜ ✅ 攔截</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="bottom-alert" style="border-left-color: var(--primary-accent);">
                <strong>🏆 車規安全防線：</strong> 模型調校時刻意往「寧可錯殺、不可漏檢」偏置，最大化保障車規合規。
            </div>
        </div>
    </div>
"""

# Slide 07: Module 4 (Unit 4 補強 - 模具預測 PdM 實施「實時財務 ROI 計算器」)
module4_body = """
    <div style="display: grid; grid-template-rows: 1fr 1fr; gap: 30px; height: 100%;">
        <!-- 上排：感測器高頻採樣視覺儀表板 (SVG) -->
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px;">
            <!-- 振動加速規 -->
            <div class="panel animate-fade delay-1" style="border-top: 4px solid var(--primary-accent); justify-content: flex-start; padding: 20px 25px;">
                <h4 style="font-size: 22px; color: var(--primary-accent); margin-bottom: 6px; font-weight: 800;">🔊 10 kHz 振動加速規</h4>
                <p style="font-size: 17px; color: #FFF; line-height: 1.5; margin-bottom: 8px;">
                    裝在模座上，捕捉沖棒疲勞高頻邊帶特徵。
                </p>
                <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; height: 50px; padding: 5px;">
                    <svg width="100%" height="100%" viewBox="0 0 400 50">
                        <path d="M 0,25 Q 5,10 10,40 T 20,25 T 35,45 T 50,15 T 60,35 T 75,5 T 90,45 T 105,25 T 120,35 T 135,15 L 400,25" fill="none" stroke="#FF5B35" stroke-width="2"></path>
                    </svg>
                </div>
            </div>
            
            <!-- 電流感測器 -->
            <div class="panel animate-fade delay-2" style="border-top: 4px solid var(--secondary-accent); justify-content: flex-start; padding: 20px 25px;">
                <h4 style="font-size: 22px; color: var(--secondary-accent); margin-bottom: 6px; font-weight: 800;">⚡ 1 kHz 電流感測器</h4>
                <p style="font-size: 17px; color: #FFF; line-height: 1.5; margin-bottom: 8px;">
                    裝在主軸馬達，抓取撞擊力道波形突變。
                </p>
                <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; height: 50px; padding: 5px;">
                    <svg width="100%" height="100%" viewBox="0 0 400 50">
                        <path d="M 0,25 L 100,25 L 120,5 L 130,45 L 140,25 L 400,25" fill="none" stroke="#00F2FE" stroke-width="2"></path>
                    </svg>
                </div>
            </div>
            
            <!-- 壓力感測器 -->
            <div class="panel animate-fade delay-3" style="border-top: 4px solid #A855F7; justify-content: flex-start; padding: 25px 30px;">
                <h4 style="font-size: 22px; color: #A855F7; margin-bottom: 6px; font-weight: 800;">🩸 1 kHz 液壓感測器</h4>
                <p style="font-size: 17px; color: #FFF; line-height: 1.5; margin-bottom: 8px;">
                    監控液壓管路，提取滑動窗口與俏度指標。
                </p>
                <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05); border-radius: 8px; height: 50px; padding: 5px;">
                    <svg width="100%" height="100%" viewBox="0 0 400 50">
                        <path d="M 0,25 Q 50,15 100,30 T 200,20 T 300,35 T 400,25" fill="none" stroke="#A855F7" stroke-width="2"></path>
                    </svg>
                </div>
            </div>
        </div>
        
        <!-- 下排：實時點擊財務 ROI 計算器（完整互動滑桿） -->
        <div class="panel animate-fade delay-3" style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 40px; padding: 25px 35px; align-items: center;">
            <div style="display: flex; flex-direction: column; gap: 15px; border-right: 1px solid rgba(255,255,255,0.1); padding-right: 40px;">
                <h4 style="font-size: 23px; color: var(--primary-accent); font-weight: 800;">⚙️ 實時產線財務 ROI 模擬計算器 (拉動滑桿計算)</h4>
                
                <!-- 互動滑桿 1 -->
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <label style="font-size: 18px; font-weight: bold; width: 45%;">全廠冷鍛打頭機台數:</label>
                    <input type="range" min="2" max="25" value="8" id="machineRange" oninput="calculateROI()" style="flex-grow: 1; margin: 0 15px; cursor: pointer;">
                    <span style="font-size: 20px; font-weight: bold; color: var(--secondary-accent); width: 10%; text-align: right;" id="machineVal">8 台</span>
                </div>
                
                <!-- 互動滑桿 2 -->
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <label style="font-size: 18px; font-weight: bold; width: 45%;">每台年均斷針裂模次數:</label>
                    <input type="range" min="1" max="10" value="3" id="breakRange" oninput="calculateROI()" style="flex-grow: 1; margin: 0 15px; cursor: pointer;">
                    <span style="font-size: 20px; font-weight: bold; color: var(--secondary-accent); width: 10%; text-align: right;" id="breakVal">3 次</span>
                </div>
            </div>
            
            <div style="padding-left: 10px; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h4 style="font-size: 21px; color: var(--secondary-accent); font-weight: 800; margin-bottom: 6px;">AI 預測性維護年省金額</h4>
                    <p style="font-size: 18px; color: #FFF; line-height: 1.5;">
                        原事故全廠年損失: <span id="lossVal" style="color: #FF5B35; font-weight: bold;">336</span> 萬<br>
                        AI 攔截 70% 斷模損失 ➔ <strong style="color: #00FF66;" id="saveVal">年省 235 萬</strong>
                    </p>
                </div>
                <div style="text-align: right; background: rgba(0,242,254,0.05); border: 2px solid var(--secondary-accent); padding: 12px 20px; border-radius: 12px; min-width: 160px;">
                    <span style="font-size: 14px; color: var(--secondary-accent); font-weight: 800; display: block; text-transform: uppercase;">回本週期 (ROI)</span>
                    <strong class="highlight-number teal" style="font-size: 48px;" id="roiVal">5.1個月</strong>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function calculateROI() {
            const machines = parseInt(document.getElementById('machineRange').value);
            const breaks = parseInt(document.getElementById('breakRange').value);
            
            document.getElementById('machineVal').innerText = machines + " 台";
            document.getElementById('breakVal').innerText = breaks + " 次";
            
            // 損耗計算 (1次事故折合模損 8萬 + 停線損 6萬 = 14萬)
            const singleLoss = 14; 
            const totalLoss = machines * breaks * singleLoss;
            const savings = totalLoss * 0.70; // 攔截 70%
            
            // 回本期 (以建置費 100 萬為自籌基準)
            const cost = 100;
            const roiMonths = (cost / (savings / 12)).toFixed(1);
            
            document.getElementById('lossVal').innerText = totalLoss.toFixed(0);
            document.getElementById('saveVal').innerText = "年省 " + savings.toFixed(0) + " 萬";
            document.getElementById('roiVal').innerText = roiMonths + "個月";
        }
    </script>
"""

# Slide 08: Module 5 (Unit 3 + M13 國際貿易碳關稅與 ISO 42001 安全治理)
module5_body = """
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; height: 100%;">
        <!-- 左欄：CBAM 歐盟碳關稅盤查 -->
        <div class="panel animate-fade delay-1" style="display: flex; flex-direction: column; justify-content: space-between; border-left: 5px solid var(--primary-accent);">
            <div>
                <h3 class="panel-title">M13 ｜ 歐盟 CBAM 碳關稅自動化盤查</h3>
                
                <div style="display: flex; flex-direction: column; gap: 20px; margin-top: 20px;">
                    <!-- 範疇一 -->
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 16px 20px; border-radius: 10px;">
                        <strong style="color: var(--primary-accent); font-size: 21px; display: block; margin-bottom: 4px;">範疇一 ｜ 直接碳排放</strong>
                        <span style="font-size: 18px; color: #FFF; line-height: 1.5;">天然氣、柴油等製程中直接燃燒的能源碳排放。</span>
                    </div>
                    <!-- 範疇二 -->
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 16px 20px; border-radius: 10px;">
                        <strong style="color: var(--primary-accent); font-size: 21px; display: block; margin-bottom: 4px;">範疇二 ｜ 外購電力能耗</strong>
                        <span style="font-size: 18px; color: #FFF; line-height: 1.5;">台電外購電能耗，由 AI 自動抓取數表進行日誌對齊。</span>
                    </div>
                    <!-- 範疇三 -->
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 16px 20px; border-radius: 10px;">
                        <strong style="color: var(--primary-accent); font-size: 21px; display: block; margin-bottom: 4px;">範疇三 ｜ 上游原料碳足跡</strong>
                        <span style="font-size: 18px; color: #FFF; line-height: 1.5;">中鋼/盤元原料之環境宣告 (EPD) 自動串接盤點。</span>
                    </div>
                </div>
            </div>
            
            <div class="bottom-alert">
                <strong>⚠️ 貿易警示：</strong> CBAM 屬於貿易法律文件，AI 自動盤查必須附帶完整、能被審計的可追溯數據鏈。
            </div>
        </div>
        
        <!-- 右欄：ISO 42001 安全防線 -->
        <div class="panel animate-fade delay-2" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 class="panel-title teal">ISO/IEC 42001 與 Audit Trails 出海口治理</h3>
                
                <div style="display: flex; flex-direction: column; gap: 24px; margin-top: 25px;">
                    <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); padding: 22px 26px; border-radius: 12px;">
                        <strong style="color: var(--secondary-accent); font-size: 22px; display: block; margin-bottom: 8px;">🛡️ 1. ISO 42001 國際安全標準</strong>
                        <span style="font-size: 18.5px; color: #FFF; line-height: 1.65; display: block;">
                            發布<strong>「員工 AI 使用守則」</strong>，明令紅線條款。嚴禁將客戶圖紙、報價單與模具機密配方餵入公網大模型，防範商業泄密。
                        </span>
                    </div>
                    
                    <div style="background: rgba(0,242,254,0.03); border: 1px solid rgba(0,242,254,0.15); padding: 22px 26px; border-radius: 12px;">
                        <strong style="color: var(--secondary-accent); font-size: 22px; display: block; margin-bottom: 8px;">🗝️ 2. 密碼學安全審計軌跡 (Audit Trails)</strong>
                        <span style="font-size: 18.5px; color: #FFF; line-height: 1.65; display: block;">
                            記錄每一次 AI 品檢與對話判定（時間、影像 Hash、模型版本、人員），保存 7 年。**國際大廠稽核時，10 分鐘內秒級調出證明**。
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="bottom-alert" style="border-left-color: var(--primary-accent);">
                <strong>🏆 競爭優勢：</strong> 這是一張出海歐洲的綠色與安全通行證，讓企業在國際搶單中自帶合規護城河。
            </div>
        </div>
    </div>
"""

# Slide 09: Module 6 (M12 政府補助對接 ─ 實施「翻開 3D 書頁/展示摘要」可點擊導引手冊)
module6_body = """
    <div style="display: grid; grid-template-columns: 0.95fr 1.05fr; gap: 40px; height: 100%;">
        <!-- 左欄：計畫提案書黃金骨架 -->
        <div class="panel animate-fade delay-1" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3 class="panel-title">M12 ｜ 政府智慧機械與減碳升級補助</h3>
                
                <div style="font-size: 20px; color: #FFF; line-height: 1.65; display: flex; flex-direction: column; gap: 18px; margin-top: 15px;">
                    <p style="font-size: 24px; font-weight: 800; color: var(--primary-accent);">
                        對接產發署與中企署智慧/減碳補助（上限 100 - 1000 萬元）
                    </p>
                    <p>
                        <strong>提案計畫書 4 大必過骨架：</strong>
                    </p>
                    <p>
                        1. **痛點描述**：明確列出模具異常耗損與 AOI 漏檢率對企業財務的直接損傷。<br>
                        2. **技術選型**：詳細交代 Edge AI 與 Voice Realtime API 帶來的技術降噪突破。<br>
                        3. **可量化效益**：預估模具耗損下降 30%，品質漏檢率趨近零。<br>
                        4. **產學加分項**：<strong>對接南部高科大、台南大學等學校研究資源</strong>，實測過件率提升 15%！
                    </p>
                </div>
            </div>
            
            <div class="bottom-alert">
                <strong>💡 評審規則：</strong> 評審只花 20 分鐘看計畫書。首頁的執行摘要必須在 1 分鐘內展現最強烈的商業轉型意願。
            </div>
        </div>
        
        <!-- 右欄：核銷五大保命手冊 (可點擊切換，書頁式展開) -->
        <div class="panel animate-fade delay-2" style="display: flex; flex-direction: column; justify-content: space-between; border-right: 5px solid var(--secondary-accent);">
            <div>
                <h3 class="panel-title teal">核銷保命五大工作手冊 <span>(點擊翻閱審查清單)</span></h3>
                
                <!-- 手冊選擇鈕 -->
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <button onclick="openBook(1)" id="btnBook1" style="background: rgba(0,242,254,0.15); border: 2px solid var(--secondary-accent); color:#FFF; padding: 6px 12px; border-radius: 8px; font-size:15px; font-weight:bold; cursor:pointer; transition:all 0.2s;">手冊一</button>
                    <button onclick="openBook(2)" id="btnBook2" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); color:#FFF; padding: 6px 12px; border-radius: 8px; font-size:15px; font-weight:bold; cursor:pointer; transition:all 0.2s;">手冊二</button>
                    <button onclick="openBook(3)" id="btnBook3" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); color:#FFF; padding: 6px 12px; border-radius: 8px; font-size:15px; font-weight:bold; cursor:pointer; transition:all 0.2s;">手冊三</button>
                    <button onclick="openBook(4)" id="btnBook4" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); color:#FFF; padding: 6px 12px; border-radius: 8px; font-size:15px; font-weight:bold; cursor:pointer; transition:all 0.2s;">手冊四</button>
                    <button onclick="openBook(5)" id="btnBook5" style="background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); color:#FFF; padding: 6px 12px; border-radius: 8px; font-size:15px; font-weight:bold; cursor:pointer; transition:all 0.2s;">手冊五</button>
                </div>
                
                <!-- 書頁展示區 -->
                <div style="background: rgba(0,0,0,0.3); border: 2px solid var(--glass-border); border-radius: 12px; padding: 20px; margin-top: 15px; min-height: 180px;" id="bookContent">
                    <strong style="color: var(--secondary-accent); font-size: 20px; display: block; margin-bottom: 8px;" id="bookTitle">📖 手冊一 ｜ 月度執行進度與查核追蹤表</strong>
                    <p style="font-size: 17.5px; color: #FFF; line-height: 1.6;" id="bookDesc">
                        - 對比計畫書，每月追蹤打頭機 PdM 特徵採集與語音 API 開發查核點。<br>
                        - 建立「進度落後通報警示」，若落後 10% 立即啟動外部顧問介入機制。<br>
                        - 防止因查核進度落後，遭政府審核委員刪減期中補助經費。
                    </p>
                </div>
                
                <div style="background: rgba(168, 85, 247, 0.05); border: 1.5px dashed rgba(168, 85, 247, 0.3); padding: 15px 20px; border-radius: 10px; color: #E2E8F0; font-size: 18px; line-height: 1.5; margin-top: 15px;">
                    <strong>🎓 孟顧問誠信加分項：</strong> 南部學校（高科大、台南大學）產學資源對接，提升評審青睞度！
                </div>
            </div>
            
            <div class="bottom-alert">
                <strong>🏆 政策套利：</strong> 手把手教您如何合法自籌、實發薪資核銷，將經費核准風險壓至最低。
            </div>
        </div>
    </div>
    
    <script>
        const bookData = {
            1: {
                title: "📖 手冊一 ｜ 月度執行進度與查核追蹤表",
                desc: "- 對比計畫書，每月追蹤打頭機 PdM 特徵採集與語音 API 開發查核點。<br>- 建立「進度落後通報警示」，若落後 10% 立即啟動外部顧問介入機制。<br>- 防止因查核進度落後，遭政府審核委員刪減期中補助經費。"
            },
            2: {
                title: "📖 手冊二 ｜ 發票與請款憑證分類歸檔規範",
                desc: "- 全廠採購之感測器、網閘主機及開發委外合約，發票歸檔必須與科目嚴格一致。<br>- 每張發票上必須加蓋政府計畫專用章印，防範多處重疊申報。<br>- 杜絕會計科目交叉污染，保障查帳一次過關。"
            },
            3: {
                title: "📖 手冊三 ｜ 人事月核銷與勞健保申報證明",
                desc: "- 明確記錄參與計畫之課長、師傅投入人月工時比例。<br>- 嚴格核對每月薪資扣繳憑單、劃撥證明與勞健保扣繳單。<br>- 保障人事成本核銷 100% 符規合憲，免遭查退。"
            },
            4: {
                title: "📖 手冊四 ｜ 補助設備資產列管與防處分",
                desc: "- 補助款項購買之工業伺服器與檢測工業電腦，必須於實體機身張貼政府補助資產標籤。<br>- 三年內計畫資產不得私自變賣、轉讓或處分，防止查核退回經費。<br>- 每年底配合主管機關進行實地資產盤查。"
            },
            5: {
                title: "📖 手冊五 ｜ 期中期末查核報告合理性撰寫",
                desc: "- 精準包裝「未完全達成指標」之合理工藝性原因，避開評審罰則。<br>- 一線師傅訪談大綱擬定，防止在查核委員面前失言。<br>- 確保期末審查順利結案，拿到尾款。"
            }
        };
        
        function openBook(id) {
            // 切換按鈕樣式
            for (let i = 1; i <= 5; i++) {
                const btn = document.getElementById('btnBook' + i);
                if (i === id) {
                    btn.style.background = "rgba(0,242,254,0.15)";
                    btn.style.borderColor = "var(--secondary-accent)";
                } else {
                    btn.style.background = "rgba(255,255,255,0.02)";
                    btn.style.borderColor = "var(--glass-border)";
                }
            }
            
            // 書頁動畫切換
            const bookContent = document.getElementById('bookContent');
            bookContent.style.opacity = 0.5;
            setTimeout(() => {
                document.getElementById('bookTitle').innerHTML = bookData[id].title;
                document.getElementById('bookDesc').innerHTML = bookData[id].desc;
                bookContent.style.opacity = 1;
            }, 150);
        }
    </script>
"""

# Slide 10: Module 7 (M10 變革管理與多國籍移工四語防呆教育訓練 - 點擊交互時間線)
module7_body = """
    <div style="display: grid; grid-template-rows: 1fr 1.05fr; gap: 30px; height: 100%;">
        <!-- 上排：三大角色變革痛點與尊嚴設計 -->
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px;">
            <div class="panel animate-fade delay-1" style="border-top: 4px solid var(--primary-accent); padding: 20px 25px;">
                <h4 style="font-size: 21px; color: var(--primary-accent); margin-bottom: 8px; font-weight: 800;">👨‍🔧 黑手老師傅 ─ 尊嚴設計</h4>
                <p style="font-size: 17.5px; color: #FFF; line-height: 1.55;">
                    抗拒被 AI 指導，覺得被機器命令。<br>
                    <strong>對策：</strong> AI 語氣改為「請教」，僅提供歷史案例參考，將<strong>最終決策權</strong>保留給老師傅。
                </p>
            </div>
            
            <div class="panel animate-fade delay-2" style="border-top: 4px solid var(--secondary-accent); padding: 20px 25px;">
                <h4 style="font-size: 21px; color: var(--secondary-accent); margin-bottom: 8px; font-weight: 800;">🧑‍💼 中階課長 ─ 飯碗安撫</h4>
                <p style="font-size: 17.5px; color: #FFF; line-height: 1.55;">
                    焦慮被 AI 取代，或者失去現場控制力。<br>
                    <strong>對策：</strong> 輔導主管考取「AI 數字排程與預防運作分析師」，轉型為握有數據的 AI 管理官。
                </p>
            </div>
            
            <div class="panel animate-fade delay-3" style="border-top: 4px solid #A855F7; padding: 20px 25px;">
                <h4 style="font-size: 21px; color: #A855F7; margin-bottom: 8px; font-weight: 800;">🧑‍💻 外籍移工 ─ 四語防呆</h4>
                <p style="font-size: 17.5px; color: #FFF; line-height: 1.55;">
                    害怕按錯 UI 被處罰扣薪水。<br>
                    <strong>對策：</strong> 中、越、泰、印尼四語界面。強制極簡圖形與色溫防呆，下發 90秒短影片。
                </p>
            </div>
        </div>
        
        <!-- 下排：變革管理時間軸 (點擊交互更新內容) -->
        <div class="panel animate-fade delay-3" style="display: flex; flex-direction: column; justify-content: space-between; padding: 25px 35px;">
            <h4 style="font-size: 22px; color: var(--secondary-accent); font-weight: 800;" id="timelineTitle">📅 恆達變革時間線 ─ 第一階段 ｜ 溝通期 (點擊切換階段)</h4>
            
            <!-- 水平按鈕時間線 -->
            <div style="display: flex; justify-content: space-between; align-items: center; position: relative; margin-top: 10px;">
                <div style="position: absolute; left: 5%; right: 5%; height: 3px; background: rgba(255,255,255,0.15); z-index: 1;"></div>
                
                <div onclick="selectTimeline(1)" id="timeNode1" style="z-index: 2; background: var(--bg-color); border: 2.5px solid var(--primary-accent); border-radius: 8px; padding: 8px 14px; text-align: center; width: 22%; cursor: pointer; transition: all 0.2s;">
                    <span style="font-size: 16px; font-weight: 800; color: var(--primary-accent); display: block;">M1 ｜ 溝通期</span>
                    <span style="font-size: 14.5px; color: #FFF; font-weight:600;" id="txtNode1">宣示不裁員、召集大會</span>
                </div>
                <div onclick="selectTimeline(2)" id="timeNode2" style="z-index: 2; background: var(--bg-color); border: 1px solid var(--glass-border); border-radius: 8px; padding: 8px 14px; text-align: center; width: 22%; cursor: pointer; transition: all 0.2s;">
                    <span style="font-size: 16px; font-weight: 800; color: #FF8A00; display: block;">M2 ｜ 培訓期</span>
                    <span style="font-size: 14.5px; color: #FFF;" id="txtNode2">移工種子教練挑選</span>
                </div>
                <div onclick="selectTimeline(3)" id="timeNode3" style="z-index: 2; background: var(--bg-color); border: 1px solid var(--glass-border); border-radius: 8px; padding: 8px 14px; text-align: center; width: 22%; cursor: pointer; transition: all 0.2s;">
                    <span style="font-size: 16px; font-weight: 800; color: var(--secondary-accent); display: block;">M3-4 ｜ 試點期</span>
                    <span style="font-size: 14.5px; color: #FFF;" id="txtNode3">首條冷鍛線試跑吐槽</span>
                </div>
                <div onclick="selectTimeline(4)" id="timeNode4" style="z-index: 2; background: var(--bg-color); border: 1px solid var(--glass-border); border-radius: 8px; padding: 8px 14px; text-align: center; width: 22%; cursor: pointer; transition: all 0.2s;">
                    <span style="font-size: 16px; font-weight: 800; color: #A855F7; display: block;">M5-6 ｜ 推廣期</span>
                    <span style="font-size: 14.5px; color: #FFF;" id="txtNode4">同儕激勵、發放獎金</span>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        const timelineData = {
            1: {
                title: "📅 恆達變革時間線 ─ 第一階段 ｜ 溝通期",
                node1: "宣示不裁員、召集大會",
                node2: "移工種子教練挑選",
                node3: "首條冷鍛線試跑吐槽",
                node4: "同儕激勵、發放獎金"
            },
            2: {
                title: "📅 恆達變革時間線 ─ 第二階段 ｜ 培訓與四語部署",
                node1: "越南/泰國/印尼手冊印製",
                node2: "🚀 15名移工種子教練上崗",
                node3: "宿舍交誼廳微視頻輪播",
                node4: "班長與教練對齊獎金機制"
            },
            3: {
                title: "📅 恆達變革時間線 ─ 第三階段 ｜ 試跑與容錯調整",
                node1: "允許出錯、鼓勵現場改動",
                node2: "每週召開「槽點檢討大會」",
                node3: "🚀 滾牙/打頭線試點修正",
                node4: "AI 詞典岡山腔二次微調"
            },
            4: {
                title: "📅 恆達變革時間線 ─ 第四階段 ｜ 內化與績效激勵",
                node1: "AI操作納入月度績效考核",
                node2: "種子教練進度完成檢閱",
                node3: "全廠冷鍛打頭線橫向鋪開",
                node4: "🚀 發放2000-5000激勵獎金"
            }
        };
        
        function selectTimeline(step) {
            // 修改標題
            document.getElementById('timelineTitle').innerText = timelineData[step].title;
            
            // 修改各節點文字
            document.getElementById('txtNode1').innerText = timelineData[step].node1;
            document.getElementById('txtNode2').innerText = timelineData[step].node2;
            document.getElementById('txtNode3').innerText = timelineData[step].node3;
            document.getElementById('txtNode4').innerText = timelineData[step].node4;
            
            // 動態高亮節點
            for (let i = 1; i <= 4; i++) {
                const node = document.getElementById('timeNode' + i);
                if (i === step) {
                    node.style.borderWidth = '2.5px';
                    node.style.borderColor = i === 1 ? 'var(--primary-accent)' : (i === 2 ? '#FF8A00' : (i === 3 ? 'var(--secondary-accent)' : '#A855F7'));
                    node.style.boxShadow = '0 0 15px rgba(255,255,255,0.15)';
                } else {
                    node.style.borderWidth = '1px';
                    node.style.borderColor = 'var(--glass-border)';
                    node.style.boxShadow = 'none';
                }
            }
        }
    </script>
"""

# Slide 11: Roadmap (Gantt 時程 - 優化高度與字體大小對比)
roadmap_html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鳳凰 AI 恆達專案升級與改進時程</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #070913;
            --primary-accent: #FF5B35;
            --secondary-accent: #00F2FE;
            --text-main: #FFFFFF;
            --text-muted: #E2E8F0;
            --glass-bg: rgba(255, 255, 255, 0.025);
            --glass-border: rgba(255, 255, 255, 0.15);
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            width: 1920px; height: 1080px;
            background-color: var(--bg-color); color: var(--text-main);
            font-family: var(--font-body); overflow: hidden;
            position: relative; padding: 80px 100px;
            display: flex; flex-direction: column; justify-content: space-between;
        }
        .grid-bg {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.01) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.01) 1px, transparent 1px);
            background-size: 80px 80px; z-index: 1;
        }
        .glow-radial {
            position: absolute; top: 80%; left: 30%; width: 900px; height: 700px;
            background: radial-gradient(circle, rgba(168, 85, 247, 0.04) 0%, transparent 70%);
            filter: blur(100px); z-index: 2;
        }
        .slide-header {
            position: relative; z-index: 10;
            display: flex; justify-content: space-between; align-items: flex-start;
            border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 24px;
        }
        .module-num {
            font-family: var(--font-display); font-size: 20px; font-weight: 700;
            color: var(--primary-accent); letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 8px;
        }
        .slide-title {
            font-family: var(--font-display); font-size: 48px; font-weight: 800;
            letter-spacing: -0.01em; background: linear-gradient(135deg, #FFF, #C2CFE0);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .brand-watermark {
            font-family: var(--font-display); font-size: 14px; font-weight: 600;
            color: var(--text-muted); letter-spacing: 0.25em; display: flex; align-items: center; gap: 8px;
        }
        .brand-watermark::before { content: '🦅'; }
        .content-grid {
            position: relative; z-index: 10;
            display: grid; grid-template-columns: 0.85fr 1.15fr; gap: 40px;
            margin-top: 30px; height: 720px;
        }
        .panel {
            background: var(--glass-bg); border: 1px solid var(--glass-border);
            border-radius: 20px; padding: 35px;
            display: flex; flex-direction: column; justify-content: space-between; position: relative;
        }
        .panel-title {
            font-size: 32px; font-weight: 800; color: #FFF; margin-bottom: 24px;
            display: flex; align-items: center; gap: 12px;
        }
        .panel-title::before {
            content: ''; display: inline-block; width: 5px; height: 28px; background-color: var(--primary-accent); border-radius: 2.5px;
        }
        .panel-title.purple::before { background-color: #A855F7; }
        .gap-container { display: flex; flex-direction: column; gap: 18px; }
        .gap-card {
            background: rgba(0,0,0,0.2); border-left: 4px solid var(--primary-accent);
            border-radius: 0 12px 12px 0; padding: 18px 24px;
            border-top: 1px solid rgba(255,255,255,0.04); border-right: 1px solid rgba(255,255,255,0.04); border-bottom: 1px solid rgba(255,255,255,0.04);
        }
        .gap-card:nth-child(2) { border-left-color: var(--secondary-accent); }
        .gap-card:nth-child(3) { border-left-color: #A855F7; }
        .gap-header { font-size: 20px; font-weight: 800; color: #FFF; margin-bottom: 8px; }
        .gap-desc { font-size: 17.5px; color: #FFF; line-height: 1.6; }
        .gantt-box {
            background: rgba(0,0,0,0.25); border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px; padding: 30px; height: 100%;
            display: flex; flex-direction: column; justify-content: space-between;
        }
        .gantt-header {
            display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
            text-align: center; border-bottom: 2px solid rgba(255,255,255,0.1);
            padding-bottom: 15px; font-size: 18px; font-weight: 700; color: var(--secondary-accent); letter-spacing: 0.05em;
        }
        .gantt-header span:first-child { text-align: left; color: #FFF; }
        .gantt-rows { display: flex; flex-direction: column; gap: 24px; margin-top: 25px; }
        .gantt-row { display: grid; grid-template-columns: 1.8fr 3.2fr; align-items: center; gap: 20px; }
        .task-name { font-size: 19px; font-weight: 700; color: #FFFFFF; line-height: 1.5; }
        .bar-container {
            width: 100%; height: 38px; background: rgba(255,255,255,0.02);
            border-radius: 8px; position: relative; border: 1px solid rgba(255,255,255,0.06);
        }
        .gantt-bar {
            height: 100%; border-radius: 7px; position: absolute;
            display: flex; align-items: center; padding-left: 14px;
            font-size: 15px; font-weight: 700; color: #FFF;
            box-shadow: 0 5px 15px rgba(0,0,0,0.4);
        }
        .gantt-bar.t1 {
            left: 0%; width: 45%;
            background: linear-gradient(90deg, var(--primary-accent), #FF8A00);
            box-shadow: 0 0 20px rgba(255, 91, 53, 0.35);
        }
        .gantt-bar.t2 {
            left: 20%; width: 25%;
            background: linear-gradient(90deg, var(--secondary-accent), #00A3FF);
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.35);
        }
        .gantt-bar.t3 {
            left: 45%; width: 30%;
            background: linear-gradient(90deg, #A855F7, #D8B4FE);
            box-shadow: 0 0 20px rgba(168, 85, 247, 0.35);
        }
        .gantt-bar.t4 {
            left: 55%; width: 35%;
            background: linear-gradient(90deg, #E040FB, #F3E5F5);
        }
        .gantt-bar.t5 {
            left: 28%; width: 65%;
            background: rgba(255,255,255,0.08);
            border: 1px dashed rgba(255,255,255,0.2);
            color: #E2E8F0;
        }
        .bottom-alert {
            background: rgba(255, 255, 255, 0.015); border-left: 4px solid var(--secondary-accent);
            padding: 16px 24px; border-radius: 0 12px 12px 0;
            font-size: 18px; color: #FFF; line-height: 1.6;
        }
        .bottom-alert strong { color: var(--primary-accent); }
        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade { animation: slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.25s; }

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

    </style>
</head>
<body>

    <div id="mobile-rotate-overlay">
        <div style="font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;">📱</div>
        <h2 style="font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">請旋轉您的手機</h2>
        <p style="font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>
    </div>
    <div class="grid-bg"></div>
    <div class="glow-radial"></div>
    <div class="slide-header">
        <div>
            <div class="module-num">ROADMAP ｜ 恆達專案升級與改進時程</div>
            <h2 class="slide-title">鳳凰 AI 顧問團隊誠信自我檢視與升級行動時程表 (v2026.Q2-Q3)</h2>
        </div>
        <div class="brand-watermark">PHOENIX AI CONSULTING</div>
    </div>
    <div class="content-grid">
        <div class="panel animate-fade delay-1">
            <div>
                <h3 class="panel-title">1. 真實自我審查 ｜ 傳產盲區自我修正</h3>
                <div class="gap-container">
                    <div class="gap-card">
                        <div class="gap-header">
                            <span>🚨 偏重製造重工業，增補扣件特徵</span>
                        </div>
                        <p class="gap-desc">現有範例缺乏打頭針、沖棒退化等具體感測器特徵代碼。將在 6 月前補齊真實特徵工程案例。</p>
                    </div>
                    <div class="gap-card">
                        <div class="gap-header">
                            <span>🚨 M10 變革模組增補多國籍移工四語防呆</span>
                        </div>
                        <p class="gap-desc">忽略了南部扣件業大量越南、泰國、印尼籍一線移工的文字障礙。本次升級正式發布四語簡易防呆說明與影片範本。</p>
                    </div>
                    <div class="gap-card">
                        <div class="gap-header">
                            <span>🚨 M04 AI 採購偏重 Build，增強 SaaS 防禦</span>
                        </div>
                        <p class="gap-desc">中小傳產多外購 SaaS。增設 SLA 效能保證條款以及廠商倒閉數據 Exit 保障。</p>
                    </div>
                </div>
            </div>
            <div class="bottom-alert" style="border-left-color: var(--primary-accent);">
                <strong>💡 誠信承諾：</strong> 與恆達合作的精華成果，我們將於 Q3 前全量開源併入公版框架。
            </div>
        </div>
        <div class="panel right animate-fade delay-2">
            <div>
                <h3 class="panel-title purple">2. 鳳凰 AI 恆達專案升級行動時程表</h3>
                <div class="gantt-box">
                    <div>
                        <div class="gantt-header">
                            <span>計畫項目 (Project / Task)</span>
                            <span>6 月 ｜ JUN</span>
                            <span>7 月 ｜ JUL</span>
                            <span>8 月 ｜ AUG</span>
                        </div>
                        <div class="gantt-rows">
                            <div class="gantt-row">
                                <div class="task-name">1. 傳產模具 PdM 智慧特徵工程併入 Unit 4</div>
                                <div class="bar-container"><div class="gantt-bar t1">進行中 ｜ ACTIVE</div></div>
                            </div>
                            <div class="gantt-row">
                                <div class="task-name">2. 恆達 C-Suite 方案 B 實戰工作坊啟動</div>
                                <div class="bar-container"><div class="gantt-bar t2">進行中</div></div>
                            </div>
                            <div class="gantt-row">
                                <div class="task-name">3. 發布《傳產四語 AI-Native 變革操作指引》</div>
                                <div class="bar-container"><div class="gantt-bar t3">規劃中</div></div>
                            </div>
                            <div class="gantt-row">
                                <div class="task-name">4. 增補《AI SaaS 採購 SLA 合約條款範本》</div>
                                <div class="bar-container"><div class="gantt-bar t4">規劃中</div></div>
                            </div>
                            <div class="gantt-row">
                                <div class="task-name">5. 產發署智慧製造補助計畫書撰寫與輔導</div>
                                <div class="bar-container"><div class="gantt-bar t5">持續陪跑輔導期</div></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bottom-alert">
                <strong>💡 財務亮點：</strong> 本時程完美咬合產發署今年度補助收件窗口，時間零浪費。
            </div>
        </div>
    </div>
</body>
</html>
"""

# Slide 12: Next Steps (優化卡片間距與易讀性，字體極致放大)
next_steps_html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>恆達精密專案推進下一步行動指引</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #070913;
            --primary-accent: #FF5B35;
            --secondary-accent: #00F2FE;
            --text-main: #FFFFFF;
            --text-muted: #E2E8F0;
            --glass-bg: rgba(255, 255, 255, 0.025);
            --glass-border: rgba(255, 255, 255, 0.15);
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            width: 1920px; height: 1080px;
            background-color: var(--bg-color); color: var(--text-main);
            font-family: var(--font-body); overflow: hidden;
            position: relative; padding: 80px 100px;
            display: flex; flex-direction: column; justify-content: space-between;
        }
        .grid-bg {
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.01) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.01) 1px, transparent 1px);
            background-size: 80px 80px; z-index: 1;
        }
        .glow-radial {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 1200px; height: 700px;
            background: radial-gradient(circle, rgba(255, 91, 53, 0.04) 0%, rgba(0, 242, 254, 0.02) 50%, transparent 100%);
            filter: blur(100px); z-index: 2;
        }
        .slide-header {
            position: relative; z-index: 10;
            display: flex; justify-content: space-between; align-items: flex-start;
            border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 24px;
        }
        .module-num {
            font-family: var(--font-display); font-size: 20px; font-weight: 700;
            color: var(--primary-accent); letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 8px;
        }
        .slide-title {
            font-family: var(--font-display); font-size: 48px; font-weight: 800;
            letter-spacing: -0.01em; background: linear-gradient(135deg, #FFF, #C2CFE0);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .brand-watermark {
            font-family: var(--font-display); font-size: 14px; font-weight: 600;
            color: var(--text-muted); letter-spacing: 0.25em; display: flex; align-items: center; gap: 8px;
        }
        .brand-watermark::before { content: '🦅'; }
        .steps-container {
            position: relative; z-index: 10;
            display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 30px;
            margin-top: 30px; height: 520px;
        }
        .step-card {
            background: var(--glass-bg); border: 1px solid var(--glass-border);
            border-radius: 20px; padding: 40px;
            display: flex; flex-direction: column; justify-content: space-between;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); position: relative;
        }
        .step-card:hover {
            transform: translateY(-5px); border-color: rgba(255, 255, 255, 0.25);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.5); background: rgba(255, 255, 255, 0.04);
        }
        .card-top { display: flex; flex-direction: column; gap: 20px; }
        .step-badge {
            font-family: var(--font-display); font-size: 16px; font-weight: 700;
            color: var(--primary-accent); letter-spacing: 0.1em; display: flex; align-items: center; gap: 8px;
        }
        .step-badge::before { content: ''; display: inline-block; width: 20px; height: 3px; background-color: var(--primary-accent); }
        .step-card:nth-child(2) .step-badge { color: var(--secondary-accent); }
        .step-card:nth-child(2) .step-badge::before { background-color: var(--secondary-accent); }
        .step-card:nth-child(3) .step-badge { color: #A855F7; }
        .step-card:nth-child(3) .step-badge::before { background-color: #A855F7; }
        .step-title { font-size: 30px; font-weight: 800; color: #FFF; line-height: 1.4; }
        .step-desc { font-size: 20px; color: #FFFFFF; line-height: 1.65; }
        .step-desc strong { color: var(--primary-accent); }
        .step-desc span.highlight { color: var(--primary-accent); font-weight: 700; }
        .step-card:nth-child(2) span.highlight { color: var(--secondary-accent); }
        .step-card:nth-child(2) .step-desc strong { color: var(--secondary-accent); }
        .step-card:nth-child(3) span.highlight { color: #D8B4FE; }
        .step-card:nth-child(3) .step-desc strong { color: #D8B4FE; }
        .step-footer-link {
            font-size: 16px; font-weight: 600; color: var(--text-muted);
            display: flex; align-items: center; gap: 8px; border-top: 1px solid rgba(255,255,255,0.1);
            padding-top: 20px; margin-top: 20px;
        }
        .step-card:hover .step-footer-link { color: #FFF; }
        .bottom-quote-panel {
            position: relative; z-index: 10; text-align: center;
            background: rgba(255,255,255,0.015); border: 1px solid rgba(255,255,255,0.04);
            border-radius: 14px; padding: 30px; margin-top: 30px;
        }
        .quote-text {
            font-family: var(--font-display); font-size: 28px; font-weight: 700; font-style: italic;
            letter-spacing: 0.05em; background: linear-gradient(135deg, var(--primary-accent), #FF8E53);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .quote-author { font-size: 15px; color: var(--text-muted); margin-top: 8px; letter-spacing: 0.1em; text-transform: uppercase; }
        @keyframes slideInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade { animation: slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
        .delay-1 { animation-delay: 0.1s; }
        .delay-2 { animation-delay: 0.25s; }
        .delay-3 { animation-delay: 0.4s; }

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

    </style>
</head>
<body>

    <div id="mobile-rotate-overlay">
        <div style="font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;">📱</div>
        <h2 style="font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">請旋轉您的手機</h2>
        <p style="font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>
    </div>
    <div class="grid-bg"></div>
    <div class="glow-radial"></div>
    <div class="slide-header">
        <div>
            <div class="module-num">NEXT STEPS ｜ 下一步專案推進指引</div>
            <h2 class="slide-title">恆達精密專案推進下一步行動指引 (Next Steps)</h2>
        </div>
        <div class="brand-watermark">PHOENIX AI CONSULTING</div>
    </div>
    <div class="steps-container">
        <div class="step-card animate-fade delay-1">
            <div class="card-top">
                <span class="step-badge">ACTION 01</span>
                <h3 class="step-title">正式啟動 ｜ 企業 AI 一頁式戰術畫布實戰工作坊</h3>
                <p class="step-desc">
                    帶領恆達董事長、廠長與核心幕僚，利用「4+1 戰術畫布」在 1 天內盤點並確立 <span class="highlight">20 大 AI 潛力落地場景</span>。<br><br>
                    現場計算 Buy vs. Build vs. Rent 財務可行性，快速篩選出高回收的 <strong>Quick-Win 首發試點專案</strong>。
                </p>
            </div>
            <div class="step-footer-link">
                🛠️ 傳產決策與深度合規導入工作坊 ➔
            </div>
        </div>
        <div class="step-card animate-fade delay-2">
            <div class="card-top">
                <span class="step-badge">ACTION 02</span>
                <h3 class="step-title">併行開展 ｜ 經濟部產發署智慧製造補助申請</h3>
                <p class="step-desc">
                    顧問團隊深度輔導，將工作坊中篩選出最具創新價值的 3 大場景（叫貨、排障、備料），包裝撰寫為 **產發署計畫書**，<span class="highlight">爭取 150 - 1000 萬政府上限補助</span>。<br><br>
                    孟顧問親自指導產學合作對接與 KPI 80% 安全防線，為企業轉型經費買單。
                </p>
            </div>
            <div class="step-footer-link">
                💰 政府智慧製造升級補助紅利爭取 ➔
            </div>
        </div>
        <div class="step-card animate-fade delay-3">
            <div class="card-top">
                <span class="step-badge">ACTION 03</span>
                <h3 class="step-title">特惠折抵 ｜ 品牌加速夥伴專屬折抵機制</h3>
                <p class="step-desc">
                    本案適用恆達專屬的 <span class="highlight">「品牌加速夥伴特惠折抵機制」</span>。<br><br>
                    工作坊順利完成後，若恆達精密決定委託我們進行後續的「90天 AI 落地變革管理陪跑輔導」，本工作坊之全部費用將可 <strong>100% 全額折抵</strong> 陪跑專案款項！
                </p>
            </div>
            <div class="step-footer-link">
                💎 預算極致 ROI 確保 ➔
            </div>
        </div>
    </div>
    <div class="bottom-quote-panel animate-fade delay-3">
        <div class="quote-text">「這不是寫給學術界的教科書，而是一套寫給變革者看的戰術手冊。」</div>
        <div class="quote-author">─ 鳳凰 AI 顧問團隊 孟淑慧 ＆ 陳文家</div>
    </div>
</body>
</html>
"""

# index.html customized for Henda
index_html = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<title>恆達精密扣件專屬：2026 鳳凰 AI 企業級營運落地與人才培育課程方案</title>
<script>
  window.DECK_MANIFEST = [
    { file: "01-cover.html",       label: "方案封面 (Cover)" },
    { file: "02-intro.html",       label: "開場白 ｜ 實事求是" },
    { file: "03-module1.html",     label: "模組一 ｜ CEO 戰略速覽" },
    { file: "04-module2-noise.html", label: "模組二 ｜ 工業語音 AI 降噪" },
    { file: "05-module2-scenarios.html", label: "模組二 ｜ 語音 AI 應用場景" },
    { file: "06-module3-aoi.html",   label: "模組三 ｜ AOI 影像二次覆檢" },
    { file: "07-module4-maintenance.html", label: "模組四 ｜ 模具預測性維護" },
    { file: "08-module5-compliance.html", label: "模組五 ｜ 國際貿易與數據治理" },
    { file: "09-module6-grants.html", label: "模組六 ｜ 政府補助與核銷實戰" },
    { file: "10-module7-change.html", label: "模組七 ｜ 變革管理與移工訓練" },
    { file: "11-roadmap.html",     label: "自我審查與 Q2-Q3 行動時程" },
    { file: "12-next-steps.html",   label: "下一步專案推進指引" }
  ];
  window.DECK_WIDTH = 1920;
  window.DECK_HEIGHT = 1080;
</script>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    height: 100%; background: #05060b; overflow: hidden;
    font-family: -apple-system, "PingFang SC", "Noto Sans TC", sans-serif;
  }
  #stage {
    position: fixed; top: 50%; left: 50%; transform-origin: top left;
    will-change: transform; background: #070913; box-shadow: 0 10px 60px rgba(0,0,0,0.6);
  }
  iframe { width: 100%; height: 100%; border: 0; display: block; background: #070913; }
  .counter {
    position: fixed; bottom: 20px; right: 20px; background: rgba(7, 9, 19, 0.85);
    border: 1px solid rgba(255,255,255,0.08); color: #fff; padding: 8px 18px;
    border-radius: 999px; font-size: 14px; letter-spacing: 0.05em; font-variant-numeric: tabular-nums;
    z-index: 100; user-select: none; opacity: 0.7; transition: opacity 0.2s; backdrop-filter: blur(10px);
  }
  .counter:hover { opacity: 1; }
  .counter .label { color: #FF5B35; margin-left: 8px; font-weight: 500; }
  .nav-zone { position: fixed; top: 0; bottom: 0; width: 15%; cursor: pointer; z-index: 50; }
  .nav-zone.left  { left: 0; }
  .nav-zone.right { right: 0; }
  .nav-hint {
    position: absolute; top: 50%; transform: translateY(-50%); width: 48px; height: 48px;
    border-radius: 999px; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.06);
    color: rgba(255,255,255,0.5); display: flex; align-items: center; justify-content: center;
    font-size: 24px; opacity: 0; transition: opacity 0.2s;
  }
  .nav-zone.left  .nav-hint { left: 20px; }
  .nav-zone.right .nav-hint { right: 20px; }
  .nav-zone:hover .nav-hint { opacity: 1; background: rgba(255,255,255,0.08); color: #FFF; }
  /* 手機提示 */

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

  @media print {
    @page { size: 1920px 1080px; margin: 0; }
    html, body { background: #fff; overflow: visible; height: auto; }
    #stage { position: static; transform: none !important; box-shadow: none; }
    .counter, .nav-zone { display: none !important; }
    .print-stack { display: block; }
    .print-stack iframe { width: 1920px; height: 1080px; page-break-after: always; display: block; }
  }
</style>
</head>
<body>

    <div id="mobile-rotate-overlay">
        <div style="font-size: 80px; margin-bottom: 20px; animation: rotatePhone 2s infinite ease-in-out;">📱</div>
        <h2 style="font-family: var(--font-display); font-size: 32px; font-weight: 800; margin-bottom: 15px; background: linear-gradient(135deg, var(--primary-accent), #FF8A00); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">請旋轉您的手機</h2>
        <p style="font-size: 20px; color: #CBD5E1; line-height: 1.6; max-width: 450px;">為了獲得最佳的高保真簡報與實時財務計算機互動體驗，請將手機旋轉為橫向模式播放。</p>
    </div>

<div id="stage"><iframe id="frame" src="about:blank"></iframe></div>
<div class="nav-zone left"  id="navL"><div class="nav-hint">‹</div></div>
<div class="nav-zone right" id="navR"><div class="nav-hint">›</div></div>
<div class="counter" id="counter">1 / 1</div>
<div class="print-stack" id="printStack" style="display:none;"></div>
<script>
(function () {
  const W = window.DECK_WIDTH || 1920;
  const H = window.DECK_HEIGHT || 1080;
  const deck = window.DECK_MANIFEST || [];
  const stage = document.getElementById('stage');
  const frame = document.getElementById('frame');
  const counter = document.getElementById('counter');
  const printStack = document.getElementById('printStack');
  const storageKey = 'deck-index-' + location.pathname;
  let current = 0;
  stage.style.width  = W + 'px';
  stage.style.height = H + 'px';
  function fit() {
    const s = Math.min(window.innerWidth / W, window.innerHeight / H);
    const x = (window.innerWidth  - W * s) / 2;
    const y = (window.innerHeight - H * s) / 2;
    stage.style.transform = `translate(${x}px, ${y}px) scale(${s})`;
    stage.style.top = '0'; stage.style.left = '0';
  }
  function show(idx) {
    if (idx < 0 || idx >= deck.length) return;
    current = idx;
    frame.src = deck[idx].file;
    counter.innerHTML = `${idx + 1} / ${deck.length} <span class="label">${deck[idx].label || ''}</span>`;
    try { localStorage.setItem(storageKey, String(idx)); } catch (_) {}
    if (location.hash !== '#' + (idx + 1)) { history.replaceState(null, '', '#' + (idx + 1)); }
  }
  function next() { show(Math.min(current + 1, deck.length - 1)); }
  function prev() { show(Math.max(current - 1, 0)); }
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    switch (e.key) {
      case 'ArrowRight': case ' ': case 'PageDown': e.preventDefault(); next(); break;
      case 'ArrowLeft':  case 'PageUp':              e.preventDefault(); prev(); break;
      case 'Home':                                    e.preventDefault(); show(0); break;
      case 'End':                                     e.preventDefault(); show(deck.length - 1); break;
      case 'p': case 'P':                             window.print(); break;
      default:
        if (e.key >= '1' && e.key <= '9') {
          const i = parseInt(e.key, 10) - 1;
          if (i < deck.length) { e.preventDefault(); show(i); }
        }
    }
  });
  document.getElementById('navL').addEventListener('click', prev);
  document.getElementById('navR').addEventListener('click', next);
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => {
    const m = location.hash.match(/^#(\d+)$/);
    if (m) show(parseInt(m[1], 10) - 1);
  });
  const hashMatch = location.hash.match(/^#(\d+)$/);
  if (hashMatch) current = Math.min(parseInt(hashMatch[1], 10) - 1, deck.length - 1);
  else try {
    const v = parseInt(localStorage.getItem(storageKey), 10);
    if (!isNaN(v) && v >= 0 && v < deck.length) current = v;
  } catch (_) {}
  fit(); show(current);
  window.addEventListener('beforeprint', () => {
    printStack.innerHTML = '';
    deck.forEach(item => {
      const f = document.createElement('iframe');
      f.src = item.file;
      printStack.appendChild(f);
    });
    printStack.style.display = 'block';
    document.getElementById('stage').style.display = 'none';
  });
  window.addEventListener('afterprint', () => {
    printStack.innerHTML = '';
    printStack.style.display = 'none';
    document.getElementById('stage').style.display = '';
  });
})();
</script>
</body>
</html>
"""

# ── 3. 實體檔案寫入 ──
def save_html(filename, content):
    filepath = os.path.join(HENDA_DIR, filename)
    with codecs.open(filepath, "w", "utf-8") as f:
        f.write(content)
    print(f"Saved: {filepath}")

# 封面
save_html("01-cover.html", cover_html)

# 簡報總經理播控頁
save_html("index.html", index_html)

# 投影片 02
save_html("02-intro.html", get_header("開場白 ｜ 實事求是、黑手聽得懂", "EXECUTIVE SUMMARY", 2) + intro_body + footer)

# 投影片 03 (M01)
save_html("03-module1.html", get_header("模組一 ｜ 老闆 90 分鐘搞懂 AI 在你廠裡能幹嘛", "MODULE 01", 3) + module1_body + footer)

# 投影片 04 (M06 Part 1)
save_html("04-module2-noise.html", get_header("模組二 ｜ 85分貝高噪音環境的聲學降噪與工法語意識別", "MODULE 02 (Part 1)", 4) + module2_1_body + footer)

# 投影片 05 (M06 Part 2)
save_html("05-module2-scenarios.html", get_header("模組二 ｜ 語音 AI 三選一試點場景與資料流架構", "MODULE 02 (Part 2)", 5) + module2_2_body + footer)

# 投影片 06 (M05 + Unit 5)
save_html("06-module3-aoi.html", get_header("模組三 ｜ AOI 二次覆檢與品質混淆矩陣成本精算", "MODULE 03", 6) + module3_body + footer)

# 投影片 07 (Unit 4 補強)
save_html("07-module4-maintenance.html", get_header("模組四 ｜ 打頭針與沖棒模具壽命預測性維護 (PdM)", "MODULE 04", 7) + module4_body + footer)

# 投影片 08 (Unit 3 + M13)
save_html("08-module5-compliance.html", get_header("模組五 ｜ 歐盟 CBAM 碳關稅申報與 ISO 42001 安全治理", "MODULE 05", 8) + module5_body + footer)

# 投影片 09 (M12)
save_html("09-module6-grants.html", get_header("模組六 ｜ 政府補助對接提案與核銷五大保命工作手冊", "MODULE 06", 9) + module6_body + footer)

# 投影片 10 (M10 補強)
save_html("10-module7-change.html", get_header("模組七 ｜ 傳產變革管理、移工四語防呆與同儕激勵", "MODULE 07", 10) + module7_body + footer)

# 投影片 11
save_html("11-roadmap.html", roadmap_html)

# 投影片 12
save_html("12-next-steps.html", next_steps_html)

print("🦅 [Henda] 12 頁高保真簡報 HTML 建立完成！")
