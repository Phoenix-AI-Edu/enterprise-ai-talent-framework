# -*- coding: utf-8 -*-
"""
🦅 鳳凰 AI - B2B 高奢簡報自動化編譯器 (Metadata-Driven Slide Compiler)
-----------------------------------------------------------------
作用：讀取包含簡報內容與結構的 JSON 設定檔，自動套用極致奢華的 Obsidian Midnight 
      視覺樣式與高對比排版，編譯並產出包含互動式組件、JS 計算器及等比適應機制的 HTML 簡報組件。
"""

import os
import json
import codecs
import sys

def get_header(title, client_badge, logo_text, extra_style=""):
    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <!-- 引入 Outfit (標題) 與 Inter (內文) 高階字型 -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-midnight: #070913;
            --white: #FFFFFF;
            --gray-300: #CBD5E1;
            --gray-400: #9CA3AF;
            --phoenix-orange: #FF5B35;
            --phoenix-teal: #00F2FE;
            --phoenix-gold: #F5A623;
            --glass-bg: rgba(255, 255, 255, 0.02);
            --glass-border: rgba(255, 255, 255, 0.08);
            --font-display: 'Outfit', sans-serif;
            --font-body: 'Inter', sans-serif;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background: var(--bg-midnight);
            color: var(--white);
            font-family: var(--font-body);
            width: 1920px;
            height: 1080px;
            overflow: hidden;
            position: relative;
        }}

        /* 奢華流光背景 */
        .grid-bg {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 91, 53, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(0, 242, 254, 0.04) 0%, transparent 50%);
            z-index: 1;
            pointer-events: none;
        }}

        /* 16:9 簡報舞台 */
        #stage {{
            width: 1920px;
            height: 1080px;
            padding: 80px 100px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: absolute;
            top: 0; left: 0;
            z-index: 2;
        }}

        /* 頁頂導航列 */
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 24px;
            margin-bottom: 40px;
        }}

        .logo-group {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .brand-badge {{
            font-family: var(--font-display);
            font-size: 13px;
            font-weight: 800;
            color: var(--phoenix-orange);
            border: 1px solid rgba(255, 91, 53, 0.3);
            background: rgba(255, 91, 53, 0.06);
            padding: 6px 14px;
            border-radius: 30px;
            letter-spacing: 1px;
        }}

        .logo-txt {{
            font-family: var(--font-display);
            font-size: 15px;
            font-weight: 700;
            color: var(--white);
            letter-spacing: 0.5px;
        }}

        .nav-right-tag {{
            font-size: 13px;
            color: var(--phoenix-teal);
            font-weight: 600;
            background: rgba(0, 242, 254, 0.05);
            border: 1px solid rgba(0, 242, 254, 0.15);
            padding: 6px 14px;
            border-radius: 30px;
        }}

        /* 頁面主要內容 */
        .content-body {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }}

        /* 頁底聲明列 */
        footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 24px;
            margin-top: 40px;
            font-size: 13px;
            color: var(--gray-400);
        }}

        .security-tag {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--phoenix-gold);
            font-weight: 600;
        }}

        /* 漸變文字與特效 */
        .text-gradient-orange {{
            background: linear-gradient(135deg, var(--white) 30%, var(--phoenix-orange) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .text-gradient-teal {{
            background: linear-gradient(135deg, var(--white) 30%, var(--phoenix-teal) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* 動畫效果 */
        @keyframes slideInUp {{
            from {{ opacity: 0; transform: translateY(30px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .animate-fade {{
            animation: slideInUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}
        .delay-1 {{ animation-delay: 0.1s; }}
        .delay-2 {{ animation-delay: 0.25s; }}
        .delay-3 {{ animation-delay: 0.4s; }}
        {extra_style}
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div id="stage">
        <header class="animate-fade">
            <div class="logo-group">
                <span class="brand-badge">{client_badge}</span>
                <span class="logo-txt">{logo_text}</span>
            </div>
            <div class="nav-right-tag">B2B CORPORATE AI CONSULTING</div>
        </header>
        <div class="content-body">
"""

def get_footer(page_num, total_pages):
    return f"""
        </div>
        <footer class="animate-fade delay-3">
            <div class="security-tag">🛡️ 本簡報所有關鍵商業細節及專利技術已完全進行深度去識別化處理</div>
            <div>PHOENIX AI CONSULTING &copy; 2026 ｜ PAGE {page_num} OF {total_pages}</div>
        </footer>
    </div>

    <!-- 原生無干擾等比例縮放引擎 (Fit Engine) -->
    <script>
        function fit() {{
            const stage = document.getElementById('stage');
            const w = window.innerWidth;
            const h = window.innerHeight;
            const scale = Math.min(w / 1920, h / 1080);
            stage.style.transform = `scale(${{scale}})`;
            stage.style.left = `${{(w - 1920 * scale) / 2}}px`;
            stage.style.top = `${{(h - 1080 * scale) / 2}}px`;
            stage.style.transformOrigin = 'top left';
            stage.style.position = 'absolute';
        }}
        window.addEventListener('resize', fit);
        window.addEventListener('load', fit);
    </script>
</body>
</html>
"""

def generate_cover(slide, client_badge, logo_text, page_num, total_pages):
    title = slide["title"]
    subtitle = slide["subtitle"]
    
    # 封面專屬背光與樣式
    extra_style = """
        .cover-container {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 100%;
            position: relative;
        }
        .cover-halo {
            position: absolute;
            width: 800px;
            height: 800px;
            background: radial-gradient(circle, rgba(255, 91, 53, 0.08) 0%, transparent 60%);
            z-index: -1;
            filter: blur(80px);
        }
        .cover-title {
            font-family: var(--font-display);
            font-size: 56px;
            font-weight: 800;
            line-height: 1.25;
            margin-bottom: 24px;
            max-width: 1400px;
        }
        .cover-sub {
            font-size: 24px;
            color: var(--gray-300);
            letter-spacing: 1px;
            max-width: 900px;
            line-height: 1.6;
        }
    """
    
    html = get_header(title, client_badge, logo_text, extra_style)
    html += f"""
            <div class="cover-container">
                <div class="cover-halo animate-fade"></div>
                <h1 class="cover-title text-gradient-orange animate-fade delay-1">{title}</h1>
                <p class="cover-sub animate-fade delay-2">{subtitle}</p>
            </div>
    """
    html += get_footer(page_num, total_pages)
    return html

def generate_dual_track(slide, client_badge, logo_text, page_num, total_pages):
    title = slide["title"]
    subtitle = slide["subtitle"]
    badge_left = slide.get("badge_left", "C-SUITE STRATEGY")
    title_left = slide.get("title_left", "Left Pillar")
    content_left = slide.get("content_left", "")
    badge_right = slide.get("badge_right", "TECHNICAL IMPLEMENTATION")
    title_right = slide.get("title_right", "Right Pillar")
    content_right = slide.get("content_right", "")

    extra_style = """
        .slide-title-row {
            margin-bottom: 30px;
        }
        .slide-main-title {
            font-family: var(--font-display);
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .slide-subtitle {
            font-size: 18px;
            color: var(--gray-400);
        }
        .dual-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 50px;
            align-items: stretch;
            height: 520px;
        }
        .luxury-card {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            backdrop-filter: blur(16px);
            transition: all 0.3s ease;
        }
        .luxury-card:hover {
            transform: translateY(-5px);
        }
        .luxury-card.left-card:hover {
            border-color: rgba(255, 91, 53, 0.3);
            box-shadow: 0 20px 40px rgba(255, 91, 53, 0.05);
        }
        .luxury-card.right-card:hover {
            border-color: rgba(0, 242, 254, 0.3);
            box-shadow: 0 20px 40px rgba(0, 242, 254, 0.05);
        }
        .card-badge {
            align-self: flex-start;
            font-family: var(--font-display);
            font-size: 12px;
            font-weight: 800;
            padding: 6px 14px;
            border-radius: 6px;
            margin-bottom: 24px;
            letter-spacing: 0.5px;
        }
        .left-card .card-badge {
            background: rgba(255, 91, 53, 0.1);
            border: 1px solid rgba(255, 91, 53, 0.3);
            color: var(--phoenix-orange);
        }
        .right-card .card-badge {
            background: rgba(0, 242, 254, 0.1);
            border: 1px solid rgba(0, 242, 254, 0.3);
            color: var(--phoenix-teal);
        }
        .card-title {
            font-family: var(--font-display);
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 20px;
            line-height: 1.3;
        }
        .card-content {
            font-size: 17px;
            color: var(--gray-300);
            line-height: 1.7;
        }
    """

    html = get_header(title, client_badge, logo_text, extra_style)
    html += f"""
            <div class="slide-title-row animate-fade">
                <h2 class="slide-main-title text-gradient-orange">{title}</h2>
                <p class="slide-subtitle">{subtitle}</p>
            </div>
            <div class="dual-grid">
                <!-- 左軌 (橘軌 - 戰略) -->
                <div class="luxury-card left-card animate-fade delay-1">
                    <span class="card-badge">{badge_left}</span>
                    <h3 class="card-title text-gradient-orange">{title_left}</h3>
                    <p class="card-content">{content_left}</p>
                </div>
                <!-- 右軌 (藍軌 - 實務) -->
                <div class="luxury-card right-card animate-fade delay-2">
                    <span class="card-badge">{badge_right}</span>
                    <h3 class="card-title text-gradient-teal">{title_right}</h3>
                    <p class="card-content">{content_right}</p>
                </div>
            </div>
    """
    html += get_footer(page_num, total_pages)
    return html

def generate_interactive_roi(slide, client_badge, logo_text, page_num, total_pages):
    title = slide["title"]
    subtitle = slide["subtitle"]
    intro_text = slide.get("intro_text", "")
    slider_min = slide.get("slider_min", 10)
    slider_max = slide.get("slider_max", 90)
    slider_default = slide.get("slider_default", 30)
    cost_base = slide.get("cost_base", 1200000)
    num_workers = slide.get("num_workers", 5)

    extra_style = f"""
        .slide-title-row {{
            margin-bottom: 24px;
        }}
        .slide-main-title {{
            font-family: var(--font-display);
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 8px;
        }}
        .slide-subtitle {{
            font-size: 18px;
            color: var(--gray-400);
        }}
        .roi-wrapper {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 48px;
            height: 520px;
        }}
        .calculator-panel {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            backdrop-filter: blur(16px);
        }}
        .roi-intro-txt {{
            font-size: 16.5px;
            color: var(--gray-300);
            line-height: 1.7;
            margin-bottom: 24px;
        }}
        .slider-section {{
            margin-bottom: 30px;
        }}
        .slider-label-row {{
            display: flex;
            justify-content: space-between;
            font-size: 15px;
            font-weight: 700;
            margin-bottom: 12px;
            color: var(--phoenix-gold);
        }}
        .slider-input {{
            width: 100%;
            height: 8px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
            outline: none;
            -webkit-appearance: none;
            cursor: pointer;
        }}
        .slider-input::-webkit-slider-thumb {{
            -webkit-appearance: none;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: var(--phoenix-gold);
            cursor: pointer;
            box-shadow: 0 0 10px rgba(245, 166, 35, 0.8);
            transition: transform 0.1s ease;
        }}
        .slider-input::-webkit-slider-thumb:hover {{
            transform: scale(1.2);
        }}
        .results-panel {{
            background: linear-gradient(135deg, rgba(245, 166, 35, 0.08) 0%, rgba(255, 91, 53, 0.02) 100%);
            border: 1px dashed rgba(245, 166, 35, 0.35);
            border-radius: 24px;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .result-item {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 20px;
            margin-bottom: 20px;
        }}
        .result-item:last-child {{
            border: none;
            padding: 0; margin: 0;
        }}
        .result-lbl {{
            font-size: 14px;
            color: var(--gray-400);
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 8px;
        }}
        .result-val {{
            font-family: var(--font-display);
            font-size: 44px;
            font-weight: 800;
            color: var(--white);
        }}
        .result-val.highlight {{
            color: var(--phoenix-gold);
            text-shadow: 0 0 20px rgba(245, 166, 35, 0.3);
        }}
    """

    html = get_header(title, client_badge, logo_text, extra_style)
    html += f"""
            <div class="slide-title-row animate-fade">
                <h2 class="slide-main-title text-gradient-orange">{title}</h2>
                <p class="slide-subtitle">{subtitle}</p>
            </div>
            <div class="roi-wrapper">
                <!-- 左側：滑塊與引言 -->
                <div class="calculator-panel animate-fade delay-1">
                    <div>
                        <h3 style="font-size: 22px; font-weight: 700; margin-bottom: 16px; color: var(--white);">實時精算模擬器</h3>
                        <p class="roi-intro-txt">{intro_text}</p>
                    </div>
                    <div class="slider-section">
                        <div class="slider-label-row">
                            <span>製程工時省減率：</span>
                            <span id="slider-val-display">{slider_default}%</span>
                        </div>
                        <input type="range" class="slider-input" id="roi-slider" min="{slider_min}" max="{slider_max}" value="{slider_default}">
                    </div>
                </div>

                <!-- 右側：動態結果 -->
                <div class="results-panel animate-fade delay-2">
                    <div class="result-item">
                        <div class="result-lbl">單人年節省成本 (機會成本)</div>
                        <div class="result-val" id="single-savings">NT$ 0</div>
                    </div>
                    <div class="result-item">
                        <div class="result-lbl">廠區規模 (以 {num_workers} 人為基準)</div>
                        <div class="result-val" style="font-size: 28px; color: var(--phoenix-teal);">{num_workers} 名資深師傅 / 製程產線</div>
                    </div>
                    <div class="result-item">
                        <div class="result-lbl">廠區每年節省總額 (Total ROI)</div>
                        <div class="result-val highlight" id="total-savings">NT$ 0</div>
                    </div>
                </div>
            </div>

            <script>
                document.getElementById('roi-slider').addEventListener('input', function(e) {{
                    const val = parseInt(e.target.value);
                    document.getElementById('slider-val-display').innerText = val + '%';
                    
                    const costBase = {cost_base};
                    const numWorkers = {num_workers};
                    
                    const singleSaved = costBase * (val / 100);
                    const totalSaved = singleSaved * numWorkers;
                    
                    document.getElementById('single-savings').innerText = 'NT$ ' + singleSaved.toLocaleString();
                    document.getElementById('total-savings').innerText = 'NT$ ' + totalSaved.toLocaleString();
                }});
                
                // 初始化觸發一次
                document.getElementById('roi-slider').dispatchEvent(new Event('input'));
            </script>
    """
    html += get_footer(page_num, total_pages)
    return html

def generate_interactive_wave(slide, client_badge, logo_text, page_num, total_pages):
    title = slide["title"]
    subtitle = slide["subtitle"]
    intro_text = slide.get("intro_text", "")

    extra_style = """
        .slide-title-row {
            margin-bottom: 24px;
        }
        .slide-main-title {
            font-family: var(--font-display);
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .slide-subtitle {
            font-size: 18px;
            color: var(--gray-400);
        }
        .wave-wrapper {
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 48px;
            height: 520px;
        }
        .desc-panel {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            backdrop-filter: blur(16px);
        }
        .wave-panel {
            background: rgba(7, 9, 19, 0.95);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            box-shadow: inset 0 0 50px rgba(0, 0, 0, 0.8);
            position: relative;
        }
        .wave-btn {
            background: rgba(0, 242, 254, 0.08);
            border: 1px solid rgba(0, 242, 254, 0.25);
            color: var(--phoenix-teal);
            padding: 16px 36px;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            outline: none;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .wave-btn:hover {
            background: linear-gradient(135deg, var(--phoenix-teal) 0%, #00b4d8 100%);
            border-color: transparent;
            color: var(--bg-midnight);
            box-shadow: 0 10px 20px rgba(0, 242, 254, 0.25);
            transform: translateY(-2px);
        }
        .wave-btn.filtered {
            background: rgba(255, 91, 53, 0.08);
            border: 1px solid rgba(255, 91, 53, 0.25);
            color: var(--phoenix-orange);
        }
        .wave-btn.filtered:hover {
            background: linear-gradient(135deg, var(--phoenix-orange) 0%, #e94560 100%);
            border-color: transparent;
            color: var(--white);
            box-shadow: 0 10px 20px rgba(255, 91, 53, 0.25);
        }
        .wave-box {
            width: 100%;
            height: 240px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .status-txt {
            font-size: 16px;
            font-weight: 700;
            color: var(--phoenix-teal);
            letter-spacing: 1px;
        }
    """

    html = get_header(title, client_badge, logo_text, extra_style)
    html += f"""
            <div class="slide-title-row animate-fade">
                <h2 class="slide-main-title text-gradient-orange">{title}</h2>
                <p class="slide-subtitle">{subtitle}</p>
            </div>
            <div class="wave-wrapper">
                <!-- 左側：技術說明 -->
                <div class="desc-panel animate-fade delay-1">
                    <div>
                        <h3 style="font-size: 22px; font-weight: 700; margin-bottom: 16px; color: var(--white);">技術實現：RNNoise 邊緣濾波</h3>
                        <p style="font-size: 16.5px; color: var(--gray-300); line-height: 1.7;">{intro_text}</p>
                    </div>
                    <div style="font-size: 14.5px; color: var(--phoenix-gold); font-weight: 600; line-height: 1.5;">
                        💡 點擊右側降噪測試按鈕，可動態查看聲學波形在邊緣端被即時平滑過濾的動畫過程。
                    </div>
                </div>

                <!-- 右側：波形展示器 -->
                <div class="wave-panel animate-fade delay-2">
                    <div class="status-txt" id="wave-status">🟢 CURRENT STATUS: RAW NOISY AUDIO (85dB)</div>
                    <div class="wave-box">
                        <svg width="450" height="150" viewBox="0 0 450 150">
                            <!-- 原始噪音路徑 (Noisy wave) -->
                            <path id="wave-path" d="M 0,75 L 30,10 L 60,130 L 90,20 L 120,120 L 150,15 L 180,135 L 210,30 L 240,110 L 270,25 L 300,125 L 330,10 L 360,140 L 390,30 L 420,110 L 450,75" fill="none" stroke="var(--phoenix-teal)" stroke-width="2.5" style="transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1); stroke-linecap: round; stroke-linejoin: round;" />
                        </svg>
                    </div>
                    <button class="wave-btn" id="filter-trigger">ACTIVATE FILTER ON</button>
                </div>
            </div>

            <script>
                let isFiltered = false;
                document.getElementById('filter-trigger').addEventListener('click', function(e) {{
                    isFiltered = !isFiltered;
                    const path = document.getElementById('wave-path');
                    const status = document.getElementById('wave-status');
                    
                    if (isFiltered) {{
                        // 切換為平滑過濾後波形
                        path.setAttribute('d', 'M 0,75 Q 37.5,45 75,75 T 150,75 T 225,75 T 300,75 T 375,75 T 450,75');
                        path.setAttribute('stroke', 'var(--phoenix-orange)');
                        status.innerText = '🔴 CURRENT STATUS: RNNOISE FILTER ACTIVE (0.8s LATENCY)';
                        status.style.color = 'var(--phoenix-orange)';
                        e.target.innerText = 'DEACTIVATE FILTER OFF';
                        e.target.classList.add('filtered');
                    }} else {{
                        // 還原為噪音波形
                        path.setAttribute('d', 'M 0,75 L 30,10 L 60,130 L 90,20 L 120,120 L 150,15 L 180,135 L 210,30 L 240,110 L 270,25 L 300,125 L 330,10 L 360,140 L 390,30 L 420,110 L 450,75');
                        path.setAttribute('stroke', 'var(--phoenix-teal)');
                        status.innerText = '🟢 CURRENT STATUS: RAW NOISY AUDIO (85dB)';
                        status.style.color = 'var(--phoenix-teal)';
                        e.target.innerText = 'ACTIVATE FILTER ON';
                        e.target.classList.remove('filtered');
                    }}
                }});
            </script>
    """
    html += get_footer(page_num, total_pages)
    return html

def generate_interactive_roadmap(slide, client_badge, logo_text, page_num, total_pages):
    title = slide["title"]
    subtitle = slide["subtitle"]
    tabs = slide.get("tabs", [])

    extra_style = """
        .slide-title-row {
            margin-bottom: 24px;
        }
        .slide-main-title {
            font-family: var(--font-display);
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .slide-subtitle {
            font-size: 18px;
            color: var(--gray-400);
        }
        .roadmap-container {
            display: flex;
            flex-direction: column;
            gap: 24px;
            height: 520px;
        }
        .tab-btn-row {
            display: flex;
            gap: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            padding-bottom: 16px;
        }
        .tab-btn {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--glass-border);
            color: var(--gray-300);
            padding: 14px 28px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s ease;
            outline: none;
        }
        .tab-btn.active {
            background: rgba(255, 91, 53, 0.08);
            border-color: var(--phoenix-orange);
            color: var(--white);
            box-shadow: 0 0 15px rgba(255, 91, 53, 0.2);
        }
        .roadmap-view-panel {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            backdrop-filter: blur(16px);
            position: relative;
        }
        .roadmap-card-content {
            font-size: 18px;
            color: var(--gray-300);
            line-height: 1.8;
        }
        .gantt-chart-mock {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.05);
            padding-top: 24px;
        }
        .gantt-bar-row {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .gantt-lbl {
            width: 140px;
            font-size: 13px;
            color: var(--gray-400);
            font-weight: 600;
        }
        .gantt-bar {
            height: 12px;
            border-radius: 6px;
            background: rgba(255,255,255,0.05);
            flex-grow: 1;
            position: relative;
            overflow: hidden;
        }
        .gantt-fill {
            height: 100%;
            border-radius: 6px;
            position: absolute;
            left: 0; top: 0;
            width: 0%;
            transition: all 0.6s cubic-bezier(0.25, 0.8, 0.25, 1);
        }
        .gantt-fill.orange { background: var(--phoenix-orange); }
        .gantt-fill.teal { background: var(--phoenix-teal); }
        .gantt-fill.gold { background: var(--phoenix-gold); }
    """

    html = get_header(title, client_badge, logo_text, extra_style)
    html += f"""
            <div class="slide-title-row animate-fade">
                <h2 class="slide-main-title text-gradient-orange">{title}</h2>
                <p class="slide-subtitle">{subtitle}</p>
            </div>
            <div class="roadmap-container">
                <!-- 分頁按鈕 -->
                <div class="tab-btn-row animate-fade delay-1">
    """
    for i, t in enumerate(tabs):
        active_class = "active" if i == 0 else ""
        html += f"""
                    <button class="tab-btn {active_class}" onclick="switchTab({i})">{t["name"]}</button>
        """
    html += f"""
                </div>

                <!-- 分頁內容展示區 -->
                <div class="roadmap-view-panel animate-fade delay-2">
                    <p class="roadmap-card-content" id="tab-desc-text">Select a month to load.</p>
                    
                    <div class="gantt-chart-mock">
                        <div class="gantt-bar-row">
                            <span class="gantt-lbl">1. 數據備份與安全網閘</span>
                            <div class="gantt-bar"><div class="gantt-fill orange" id="bar1"></div></div>
                        </div>
                        <div class="gantt-bar-row">
                            <span class="gantt-lbl">2. 現場機台與特警部署</span>
                            <div class="gantt-bar"><div class="gantt-fill teal" id="bar2"></div></div>
                        </div>
                        <div class="gantt-bar-row">
                            <span class="gantt-lbl">3. 補助款申報核銷軌跡</span>
                            <div class="gantt-bar"><div class="gantt-fill gold" id="bar3"></div></div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                const tabData = {json.dumps(tabs, ensure_ascii=False)};
                
                function switchTab(index) {{
                    const buttons = document.querySelectorAll('.tab-btn');
                    buttons.forEach((b, i) => {{
                        if (i === index) b.classList.add('active');
                        else b.classList.remove('active');
                    }});
                    
                    document.getElementById('tab-desc-text').innerHTML = tabData[index].content;
                    
                    // 動態更新甘特圖模擬填充度
                    if (index === 0) {{
                        document.getElementById('bar1').style.width = '80%';
                        document.getElementById('bar2').style.width = '10%';
                        document.getElementById('bar3').style.width = '0%';
                    }} else if (index === 1) {{
                        document.getElementById('bar1').style.width = '100%';
                        document.getElementById('bar2').style.width = '65%';
                        document.getElementById('bar3').style.width = '10%';
                    }} else if (index === 2) {{
                        document.getElementById('bar1').style.width = '100%';
                        document.getElementById('bar2').style.width = '100%';
                        document.getElementById('bar3').style.width = '95%';
                    }}
                }}
                
                // 初始化
                switchTab(0);
            </script>
    """
    html += get_footer(page_num, total_pages)
    return html

def generate_next_steps(slide, client_badge, logo_text, page_num, total_pages):
    title = slide["title"]
    subtitle = slide["subtitle"]
    card1_title = slide.get("card1_title", "Action 1")
    card1_desc = slide.get("card1_desc", "")
    card2_title = slide.get("card2_title", "Action 2")
    card2_desc = slide.get("card2_desc", "")
    card3_title = slide.get("card3_title", "Action 3")
    card3_desc = slide.get("card3_desc", "")

    extra_style = """
        .slide-title-row {
            margin-bottom: 30px;
        }
        .slide-main-title {
            font-family: var(--font-display);
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 8px;
        }
        .slide-subtitle {
            font-size: 18px;
            color: var(--gray-400);
        }
        .cards-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 32px;
            align-items: stretch;
            height: 520px;
        }
        .action-card {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 36px;
            backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            position: relative;
            overflow: hidden;
        }
        .action-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; width: 100%; height: 4px;
            background: linear-gradient(90deg, var(--phoenix-orange), var(--phoenix-teal));
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        .action-card:hover::before {
            opacity: 1;
        }
        .action-card:hover {
            transform: translateY(-8px);
            border-color: rgba(245, 166, 35, 0.35);
            box-shadow: 0 20px 40px rgba(245, 166, 35, 0.08);
        }
        .action-icon {
            font-size: 44px;
            margin-bottom: 24px;
        }
        .action-title-txt {
            font-family: var(--font-display);
            font-size: 23px;
            font-weight: 700;
            color: var(--white);
            margin-bottom: 16px;
        }
        .action-desc {
            font-size: 15px;
            color: var(--gray-300);
            line-height: 1.6;
        }
        .action-badge {
            align-self: flex-start;
            font-size: 11px;
            font-weight: 700;
            color: var(--phoenix-gold);
            background: rgba(245, 166, 35, 0.08);
            border: 1px solid rgba(245, 166, 35, 0.2);
            padding: 4px 10px;
            border-radius: 4px;
            margin-top: 16px;
            letter-spacing: 0.5px;
        }
    """

    html = get_header(title, client_badge, logo_text, extra_style)
    html += f"""
            <div class="slide-title-row animate-fade">
                <h2 class="slide-main-title text-gradient-orange">{title}</h2>
                <p class="slide-subtitle">{subtitle}</p>
            </div>
            <div class="cards-container">
                <!-- Action 1 -->
                <div class="action-card animate-fade delay-1">
                    <div>
                        <div class="action-icon">🎯</div>
                        <h3 class="action-title-txt">{card1_title}</h3>
                        <p class="action-desc">{card1_desc}</p>
                    </div>
                    <span class="action-badge">C-LEVEL WORKSHOP</span>
                </div>
                <!-- Action 2 -->
                <div class="action-card animate-fade delay-2">
                    <div>
                        <div class="action-icon">💸</div>
                        <h3 class="action-title-txt">{card2_title}</h3>
                        <p class="action-desc">{card2_desc}</p>
                    </div>
                    <span class="action-badge">MATCHING & GRANTS</span>
                </div>
                <!-- Action 3 -->
                <div class="action-card animate-fade delay-3">
                    <div>
                        <div class="action-icon">👑</div>
                        <h3 class="action-title-txt">{card3_title}</h3>
                        <p class="action-desc">{card3_desc}</p>
                    </div>
                    <span class="action-badge">ACCELERATION BENEFIT</span>
                </div>
            </div>
    """
    html += get_footer(page_num, total_pages)
    return html

def generate_index(slides, client_badge, logo_text, output_dir):
    # 編譯 index.html (播放總控器)
    iframe_srcs = [f"01-cover.html"] + [f"{s['page']}-{s['layout']}.html" for s in slides[1:]]
    iframe_srcs_json = json.dumps(iframe_srcs)
    
    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{client_badge} 高階客製化教材簡報播控器 ｜ PHOENIX AI</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-deep: #070913;
      --glass-bg: rgba(255, 255, 255, 0.02);
      --glass-border: rgba(255, 255, 255, 0.08);
      --phoenix-orange: #FF5B35;
      --phoenix-teal: #00F2FE;
    }}

    * {{
      margin: 0; padding: 0; box-sizing: border-box;
    }}

    body {{
      background: var(--bg-deep);
      font-family: 'Inter', sans-serif;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }}

    #stage {{
      width: 1920px;
      height: 1080px;
      position: absolute;
      box-shadow: 0 50px 100px rgba(0,0,0,0.8);
      border: 1px solid var(--glass-border);
      border-radius: 12px;
      overflow: hidden;
      background: #000;
    }}

    iframe {{
      width: 100%;
      height: 100%;
      border: none;
      background: var(--bg-deep);
      transition: opacity 0.3s ease;
    }}

    /* 進度指示條 */
    .progress-bar-container {{
      position: absolute;
      bottom: 0; left: 0;
      width: 100%; height: 6px;
      background: rgba(255,255,255,0.05);
      z-index: 999;
    }}

    .progress-fill {{
      height: 100%;
      width: 0%;
      background: linear-gradient(90deg, var(--phoenix-orange), var(--phoenix-teal));
      transition: width 0.3s cubic-bezier(0.1, 0.8, 0.25, 1);
    }}

    /* 快捷鍵控制指示 */
    .control-hint {{
      position: absolute;
      bottom: 20px;
      right: 40px;
      background: rgba(0,0,0,0.6);
      border: 1px solid rgba(255,255,255,0.1);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 11px;
      color: #9CA3AF;
      z-index: 1000;
      font-family: monospace;
      pointer-events: none;
      backdrop-filter: blur(8px);
    }}
  </style>
</head>
<body>

  <div id="stage">
    <iframe id="slide-frame" src="{iframe_srcs[0]}"></iframe>
    <div class="progress-bar-container">
      <div class="progress-fill" id="progress-indicator"></div>
    </div>
    <div class="control-hint">LEFT/RIGHT ARROWS OR SPACE TO NAVIGATE ｜ PRESS 'P' TO PRINT</div>
  </div>

  <script>
    const slides = {iframe_srcs_json};
    let currentIndex = 0;

    const frame = document.getElementById('slide-frame');
    const indicator = document.getElementById('progress-indicator');

    function updateProgress() {{
      const pct = ((currentIndex + 1) / slides.length) * 100;
      indicator.style.width = pct + '%';
    }}

    function goToSlide(index) {{
      if (index < 0 || index >= slides.length) return;
      
      // 淡出效果
      frame.style.opacity = 0;
      
      setTimeout(() => {{
        currentIndex = index;
        frame.src = slides[currentIndex];
        
        frame.onload = () => {{
          frame.style.opacity = 1;
        }};
        
        updateProgress();
      }}, 150);
    }}

    // 鍵盤導航
    window.addEventListener('keydown', function(e) {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        if (currentIndex < slides.length - 1) {{
          goToSlide(currentIndex + 1);
        }}
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        if (currentIndex > 0) {{
          goToSlide(currentIndex - 1);
        }}
      }} else if (e.key === 'p' || e.key === 'P') {{
        // 列印呼叫
        frame.contentWindow.print();
      }}
    }});

    // 全局防干擾聚焦
    window.addEventListener('click', () => {{
      frame.focus();
    }});

    // 確保等比例縮放舞台
    function fit() {{
      const stage = document.getElementById('stage');
      const w = window.innerWidth;
      const h = window.innerHeight;
      const scale = Math.min(w / 1920, h / 1080);
      stage.style.transform = `scale(${{scale}})`;
      stage.style.left = `${{(w - 1920 * scale) / 2}}px`;
      stage.style.top = `${{(h - 1080 * scale) / 2}}px`;
    }}
    window.addEventListener('resize', fit);
    window.addEventListener('load', () => {{
      fit();
      updateProgress();
      frame.focus();
    }});
  </script>
</body>
</html>
"""
    return html

def compile_all(config_path):
    print("[Phoenix Slide Compiler] Start B2B luxury slide compilation engine...")
    
    with codecs.open(config_path, "r", "utf-8") as f:
        config = json.load(f)
        
    client_name = config["client_name"]
    client_badge = config["client_badge"]
    logo_text = config["logo_text"]
    output_dir = config["output_dir"]
    slides = config["slides"]
    total_pages = len(slides)
    
    # 建立目錄
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"[Directory] Created output directory: {output_dir}")
        
    # 編譯單頁 Slides
    for i, slide in enumerate(slides):
        layout = slide["layout"]
        page_num = i + 1
        page_str = slide["page"]
        
        print(f"[Compile] Compiling slide: {page_str}-{layout}.html (Page: {page_num}/{total_pages})")
        
        html_content = ""
        if layout == "cover":
            html_content = generate_cover(slide, client_badge, logo_text, page_num, total_pages)
            filename = "01-cover.html" # 強制第一頁使用標準檔名
        else:
            filename = f"{page_str}-{layout}.html"
            
            if layout == "dual-track":
                html_content = generate_dual_track(slide, client_badge, logo_text, page_num, total_pages)
            elif layout == "interactive-roi":
                html_content = generate_interactive_roi(slide, client_badge, logo_text, page_num, total_pages)
            elif layout == "interactive-wave":
                html_content = generate_interactive_wave(slide, client_badge, logo_text, page_num, total_pages)
            elif layout == "interactive-roadmap":
                html_content = generate_interactive_roadmap(slide, client_badge, logo_text, page_num, total_pages)
            elif layout == "next-steps":
                html_content = generate_next_steps(slide, client_badge, logo_text, page_num, total_pages)
            else:
                print(f"[Warning] Unknown layout style: {layout}, skipping page!")
                continue
                
        # 寫入檔案
        filepath = os.path.join(output_dir, filename)
        with codecs.open(filepath, "w", "utf-8") as out:
            out.write(html_content)
        print(f"   └─ Saved successfully: {filepath}")
        
    # 編譯 index.html
    index_html_content = generate_index(slides, client_badge, logo_text, output_dir)
    index_path = os.path.join(output_dir, "index.html")
    with codecs.open(index_path, "w", "utf-8") as out:
        out.write(index_html_content)
    print(f"[Complete] Control index created at: {index_path}")
    print(f"[Success] Corporate client [{client_name}] luxury slides compiled successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("💡 Please provide slides JSON configuration file path! Example:")
        print("   python scripts/compile_slides.py scripts/slides_config_sample.json")
    else:
        compile_all(sys.argv[1])
