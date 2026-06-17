# -*- coding: utf-8 -*-
import os
import re
import json
import sys

# Ensure stdout uses UTF-8 to prevent encoding crashes on Windows
sys.stdout.reconfigure(encoding='utf-8')

workspace_dir = r"g:\我的雲端硬碟\AI_Talent"
slides_base_dir = os.path.join(workspace_dir, "slides")
curriculum_dir = os.path.join(workspace_dir, "curriculum")

# Shared HTML Template parts
HTML_SLIDE_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_title}</title>
    <!-- Outfit, Inter, and Noto Serif TC/Noto Sans TC fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <!-- MathJax for rendering LaTeX formulas -->
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        :root {{
            --color-bg: #070913;
            --color-text: #FFFFFF;
            --color-text-muted: #E2E8F0;
            --color-brand: #FF5B35;       /* Phoenix Orange */
            --color-warning: #FF3B30;     /* Warning Red */
            --color-success: #00F2FE;     /* Vibrant Cyan/Teal */
            --color-info: #F5A623;        /* Gold */
            --glass-bg: rgba(255, 255, 255, 0.02);
            --glass-border: rgba(255, 255, 255, 0.15);
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
            
            --phoenix-orange: var(--color-brand);
            --phoenix-teal: var(--color-success);
            --phoenix-gold: var(--color-info);
            --white: var(--color-text);
            --gray-300: var(--color-text-muted);
            --gray-400: #94A3B8;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background: var(--color-bg);
            color: var(--color-text);
            font-family: var(--font-body);
            width: 1920px;
            height: 1080px;
            overflow: hidden;
            position: relative;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        /* Grid Background styling */
        .grid-bg {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 91, 53, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(0, 242, 254, 0.04) 0%, transparent 50%);
            z-index: 1;
            pointer-events: none;
        }}

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

        /* Header styling */
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
            font-size: 17px;
            font-weight: 800;
            color: var(--color-brand);
            border: 1px solid rgba(255, 91, 53, 0.3);
            background: rgba(255, 91, 53, 0.06);
            padding: 8px 18px;
            border-radius: 30px;
            letter-spacing: 1px;
        }}

        .logo-txt {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 700;
            color: var(--color-text);
            letter-spacing: 0.5px;
        }}

        .nav-right-tag {{
            font-size: 17px;
            color: var(--color-success);
            font-weight: 600;
            background: rgba(0, 242, 254, 0.05);
            border: 1px solid rgba(0, 242, 254, 0.15);
            padding: 8px 18px;
            border-radius: 30px;
        }}

        .progress-dots-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            padding: 6px 16px;
            border-radius: 30px;
        }}

        .progress-dot-segment {{
            font-family: var(--font-display);
            font-size: 13px;
            font-weight: 700;
            color: rgba(255, 255, 255, 0.25);
        }}

        .progress-dot-segment.active {{
            color: var(--color-success);
            text-shadow: 0 0 10px rgba(0, 242, 254, 0.4);
        }}

        .progress-dot-connector {{
            width: 20px;
            height: 1px;
            background: rgba(255, 255, 255, 0.1);
        }}

        /* Content Body styling */
        .content-body {{
            flex-grow: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            position: relative;
        }}

        .slide-title-row {{
            margin-bottom: 30px;
        }}

        .slide-main-title {{
            font-family: var(--font-display);
            font-size: 52px;
            font-weight: 800;
            margin-bottom: 8px;
            background: linear-gradient(135deg, var(--color-text) 30%, var(--color-brand) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .slide-subtitle {{
            font-size: 26px;
            color: var(--gray-400);
        }}

        /* Grid Layouts */
        .dual-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 40px;
            margin-top: 20px;
        }}

        .luxury-card {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            backdrop-filter: blur(16px);
            transition: all 0.3s ease;
        }}

        .luxury-card:hover {{
            border-color: rgba(255, 255, 255, 0.25);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
            transform: translateY(-5px);
        }}

        .card-badge {{
            display: inline-block;
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 700;
            padding: 6px 12px;
            border-radius: 6px;
            margin-bottom: 24px;
            letter-spacing: 0.5px;
        }}

        .left-card .card-badge {{
            background: rgba(255, 91, 53, 0.1);
            border: 1px solid rgba(255, 91, 53, 0.3);
            color: var(--phoenix-orange);
        }}

        .right-card .card-badge {{
            background: rgba(0, 242, 254, 0.1);
            border: 1px solid rgba(0, 242, 254, 0.3);
            color: var(--phoenix-teal);
        }}

        .card-title {{
            font-family: var(--font-display);
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 20px;
            line-height: 1.3;
        }}

        .left-card .card-title {{
            background: linear-gradient(135deg, #FFF, var(--phoenix-orange));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .right-card .card-title {{
            background: linear-gradient(135deg, #FFF, var(--phoenix-teal));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .card-content {{
            font-size: 24px;
            color: var(--gray-300);
            line-height: 1.7;
        }}

        /* List-based layouts */
        .list-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
            margin-top: 10px;
        }}

        .list-item-card {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 24px 32px;
            display: flex;
            align-items: flex-start;
            gap: 24px;
            backdrop-filter: blur(16px);
        }}

        .list-item-bullet {{
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background: rgba(255, 91, 53, 0.1);
            border: 1px solid rgba(255, 91, 53, 0.3);
            color: var(--phoenix-orange);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-display);
            font-weight: 700;
            font-size: 18px;
            flex-shrink: 0;
            margin-top: 4px;
        }}

        .list-item-text {{
            font-size: 24px;
            color: var(--color-text-muted);
            line-height: 1.6;
        }}

        .list-item-text strong {{
            color: #FFFFFF;
        }}

        /* Triple Grid layout */
        .triple-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }}

        /* Formula display box */
        .slide-formulas-box {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 20px;
            padding: 24px;
            margin-bottom: 30px;
            text-align: center;
            backdrop-filter: blur(8px);
        }}
        .formula-item {{
            font-size: 32px;
            font-weight: 600;
            color: var(--color-success);
            font-family: var(--font-display);
            text-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        }}

        /* Steps Timeline layout */
        .steps-container {{
            display: flex;
            justify-content: space-between;
            gap: 30px;
            margin-top: 40px;
        }}
        .step-card {{
            flex: 1;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px 32px 32px 32px;
            backdrop-filter: blur(16px);
            position: relative;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .step-card:hover {{
            border-color: var(--color-brand);
            box-shadow: 0 15px 30px rgba(255, 91, 53, 0.15);
            transform: translateY(-5px);
        }}
        .step-num {{
            position: absolute;
            top: -20px;
            left: 32px;
            background: linear-gradient(135deg, var(--color-brand), var(--color-info));
            color: #070913;
            font-weight: 800;
            font-family: var(--font-display);
            font-size: 15px;
            padding: 6px 18px;
            border-radius: 30px;
            letter-spacing: 1px;
            box-shadow: 0 4px 12px rgba(255, 91, 53, 0.3);
        }}
        .step-badge {{
            font-size: 24px;
            font-weight: 700;
            color: var(--color-success);
            margin-bottom: 16px;
            font-family: var(--font-display);
            background: linear-gradient(135deg, #FFF, var(--color-success));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .step-text {{
            font-size: 20px;
            color: var(--color-text-muted);
            line-height: 1.6;
        }}
        .step-text code {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2px 8px;
            border-radius: 6px;
            font-family: monospace;
            color: var(--color-brand);
        }}

        /* Speaker Notes Overlays */
        .speaker-notes-overlay {{
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            max-height: 35%;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            border-top: 2px solid rgba(245, 166, 35, 0.4);
            padding: 24px 40px;
            z-index: 9999;
            overflow-y: auto;
        }}

        .speaker-notes-overlay .notes-header {{
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 800;
            color: var(--color-info);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }}

        .speaker-notes-overlay .notes-body {{
            color: #E2E8F0;
            font-size: 18px;
            line-height: 1.8;
        }}

        .speaker-notes-overlay .notes-body p {{
            margin-bottom: 12px;
        }}

        .speaker-notes-overlay .notes-body strong {{
            color: var(--phoenix-orange);
        }}

        /* Footer styling */
        footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            padding-top: 24px;
            margin-top: 40px;
            font-size: 16px;
            color: var(--color-text-muted);
        }}

        .security-tag {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: var(--color-info);
            font-weight: 600;
        }}

        /* Animations */
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
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div id="stage">
        <header class="animate-fade">
            <div class="logo-group">
                <span class="brand-badge">📚 {unit_badge}</span>
                <span class="logo-txt">🦅 鳳凰 AI ── {unit_full_title} (v2026)</span>
            </div>
            {progress_dots_html}
            <div class="nav-right-tag">B2B CORPORATE AI CONSULTING</div>
        </header>

        <div class="content-body">
            <div class="slide-title-row animate-fade">
                <h2 class="slide-main-title">{slide_main_title}</h2>
                {slide_subtitle_html}
            </div>
            
            {slide_body_content_html}
        </div>

        <div class="speaker-notes-overlay" id="speaker-notes">
            <div class="notes-header">📋 SPEAKER NOTES ｜ PAGE {page_num} (PRESS N TO TOGGLE)</div>
            <div class="notes-body">
                {speaker_notes_html}
            </div>
        </div>

        <footer class="animate-fade delay-3">
            <div class="security-tag">🛡️ 本簡報所有關鍵商業細節及專利技術已完全進行深度去識別化處理</div>
            <div>PHOENIX AI CONSULTING &copy; 2026 ｜ PAGE {page_num} OF {total_pages}</div>
        </footer>
    </div>

    <!-- Scaler & keyboard hook scripts -->
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
        
        document.addEventListener('keydown', function(e) {{
            if (window.parent && window.parent !== window) {{
                window.parent.postMessage({{
                    type: 'keydown',
                    key: e.key,
                    keyCode: e.keyCode,
                    code: e.code
                }}, '*');
            }} else {{
                if (e.key === 'n' || e.key === 'N') {{
                    var el = document.getElementById('speaker-notes');
                    if (el) {{ el.style.display = el.style.display === 'none' ? 'block' : 'none'; }}
                }}
            }}
        }});

        window.addEventListener('message', function(e) {{
            if (e.data && e.data.type === 'toggle-notes') {{
                var el = document.getElementById('speaker-notes');
                if (el) {{ el.style.display = el.style.display === 'none' ? 'block' : 'none'; }}
            }} else if (e.data && e.data.type === 'print') {{
                window.print();
            }}
        }});
    </script>
</body>
</html>
"""

HTML_COVER_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{slide_title}</title>
    <!-- Outfit, Inter, and Noto Serif TC/Noto Sans TC fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=Noto+Serif+TC:wght@500;700&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-bg: #070913;
            --color-text: #FFFFFF;
            --color-brand: #FF5B35;
            --color-info: #F5A623;
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
        }}
        * {{
            margin: 0; padding: 0; box-sizing: border-box;
        }}
        body {{
            background: var(--color-bg);
            color: var(--color-text);
            font-family: var(--font-body);
            width: 1920px;
            height: 1080px;
            overflow: hidden;
            position: relative;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        .grid-bg {{
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(255, 91, 53, 0.04) 0%, transparent 50%),
                radial-gradient(circle at 90% 80%, rgba(0, 242, 254, 0.04) 0%, transparent 50%);
            z-index: 1;
            pointer-events: none;
        }}
        #stage {{
            width: 1920px;
            height: 1080px;
            padding: 80px 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: absolute;
            top: 0; left: 0;
            z-index: 2;
        }}
        .cover-container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            height: 100%;
            position: relative;
        }}
        .cover-halo {{
            position: absolute;
            width: 800px;
            height: 800px;
            background: radial-gradient(circle, rgba(255, 91, 53, 0.08) 0%, transparent 60%);
            z-index: -1;
            filter: blur(80px);
        }}
        .cover-title-big {{
            font-family: var(--font-display);
            font-size: 72px;
            font-weight: 800;
            line-height: 1.3;
            margin-bottom: 24px;
            max-width: 1400px;
            background: linear-gradient(135deg, #FFF 30%, var(--color-brand) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .cover-sub-big {{
            font-size: 32px;
            color: #94A3B8;
            max-width: 1100px;
            line-height: 1.6;
            margin-bottom: 48px;
        }}
        .cover-authors-badge {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 700;
            color: var(--color-info);
            background: rgba(245, 166, 35, 0.08);
            border: 1px solid rgba(245, 166, 35, 0.2);
            padding: 12px 36px;
            border-radius: 30px;
            letter-spacing: 1px;
        }}
        /* Speaker Notes Overlays */
        .speaker-notes-overlay {{
            display: none;
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            max-height: 35%;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(20px);
            border-top: 2px solid rgba(245, 166, 35, 0.4);
            padding: 24px 40px;
            z-index: 9999;
            overflow-y: auto;
        }}
        .speaker-notes-overlay .notes-header {{
            font-family: var(--font-display);
            font-size: 14px;
            font-weight: 800;
            color: var(--color-info);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 12px;
        }}
        .speaker-notes-overlay .notes-body {{
            color: #E2E8F0;
            font-size: 18px;
            line-height: 1.8;
            text-align: left;
        }}
        .speaker-notes-overlay .notes-body p {{
            margin-bottom: 12px;
        }}
        .speaker-notes-overlay .notes-body strong {{
            color: var(--color-brand);
        }}
        /* Animations */
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
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div id="stage">
        <div class="cover-container">
            <div class="cover-halo animate-fade"></div>
            <h1 class="cover-title-big animate-fade delay-1">{slide_main_title}</h1>
            <p class="cover-sub-big animate-fade delay-2">{slide_subtitle}</p>
            <div class="cover-authors-badge animate-fade delay-3">首席顧問 孟淑慧 ｜ 策略長 陳文家</div>
        </div>

        <div class="speaker-notes-overlay" id="speaker-notes">
            <div class="notes-header">📋 SPEAKER NOTES ｜ PAGE 1 (PRESS N TO TOGGLE)</div>
            <div class="notes-body">
                {speaker_notes_html}
            </div>
        </div>
    </div>

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
        
        document.addEventListener('keydown', function(e) {{
            if (window.parent && window.parent !== window) {{
                window.parent.postMessage({{
                    type: 'keydown',
                    key: e.key,
                    keyCode: e.keyCode,
                    code: e.code
                }}, '*');
            }} else {{
                if (e.key === 'n' || e.key === 'N') {{
                    var el = document.getElementById('speaker-notes');
                    if (el) {{ el.style.display = el.style.display === 'none' ? 'block' : 'none'; }}
                }}
            }}
        }});

        window.addEventListener('message', function(e) {{
            if (e.data && e.data.type === 'toggle-notes') {{
                var el = document.getElementById('speaker-notes');
                if (el) {{ el.style.display = el.style.display === 'none' ? 'block' : 'none'; }}
            }} else if (e.data && e.data.type === 'print') {{
                window.print();
            }}
        }});
    </script>
</body>
</html>
"""

HTML_PLAYER_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>👑 {unit_full_title} 簡報播控器 ｜ PHOENIX AI</title>
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
      transform-origin: top left;
    }}

    iframe {{
      width: 100%;
      height: 100%;
      border: none;
      background: var(--bg-deep);
      transition: opacity 0.3s ease;
    }}

    /* Progress bar */
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

    /* Control Bar Floating UI (Claude Audit: Mechanism 6) */
    .control-hint {{
      position: absolute;
      bottom: 20px;
      right: 40px;
      background: rgba(0,0,0,0.7);
      border: 1px solid rgba(255,255,255,0.1);
      padding: 10px 20px;
      border-radius: 8px;
      font-size: 13px;
      color: #E2E8F0;
      z-index: 1000;
      font-family: monospace;
      pointer-events: auto;
      backdrop-filter: blur(8px);
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .nav-btn {{
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.15);
      color: #FFF;
      padding: 4px 12px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 12px;
      transition: all 0.2s ease;
      font-family: inherit;
    }}
    .nav-btn:hover {{
      background: var(--phoenix-orange);
      border-color: var(--phoenix-orange);
    }}
    .slide-counter {{
      font-weight: 600;
      color: var(--phoenix-teal);
    }}
  </style>
</head>
<body>

  <div id="stage">
    <iframe id="slide-frame" src="01-cover.html"></iframe>
    <div class="progress-bar-container">
      <div class="progress-fill" id="progress-indicator"></div>
    </div>
    <div class="control-hint">
      <button class="nav-btn" onclick="prevSlide()">◀ Prev</button>
      <span class="slide-counter" id="counter-txt">1 / {total_pages}</span>
      <button class="nav-btn" onclick="nextSlide()">Next ▶</button>
      <span>← → SPACE NAVIGATE ｜ 'P' PRINT ｜ 'N' SPEAKER NOTES</span>
    </div>
  </div>

  <script>
    const slides = {slides_json};
    let currentIndex = 0;

    const frame = document.getElementById('slide-frame');
    const indicator = document.getElementById('progress-indicator');
    const counterTxt = document.getElementById('counter-txt');

    function updateProgress() {{
      const pct = ((currentIndex + 1) / slides.length) * 100;
      indicator.style.width = pct + '%';
      counterTxt.innerText = (currentIndex + 1) + ' / ' + slides.length;
    }}

    function goToSlide(index) {{
      if (index < 0 || index >= slides.length) return;
      
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

    function prevSlide() {{
      if (currentIndex > 0) goToSlide(currentIndex - 1);
    }}

    function nextSlide() {{
      if (currentIndex < slides.length - 1) goToSlide(currentIndex + 1);
    }}

    window.addEventListener('keydown', function(e) {{
      handleKeyboardNavigation(e);
    }});

    window.addEventListener('message', function(e) {{
      if (e.data && e.data.type === 'keydown') {{
        handleKeyboardNavigation(e.data);
      }}
    }});

    function handleKeyboardNavigation(e) {{
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {{
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        prevSlide();
      }} else if (e.key === 'p' || e.key === 'P') {{
        try {{
          frame.contentWindow.postMessage({{ type: 'print' }}, '*');
        }} catch(err) {{}}
      }} else if (e.key === 'n' || e.key === 'N') {{
        try {{
          frame.contentWindow.postMessage({{ type: 'toggle-notes' }}, '*');
        }} catch(err) {{}}
      }}
    }}

    window.addEventListener('click', () => {{
      frame.focus();
    }});

    function fit() {{
      const stage = document.getElementById('stage');
      const w = window.innerWidth;
      const h = window.innerHeight;
      const scale = Math.min(w / 1920, h / 1080);
      stage.style.transformOrigin = 'top left';
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


# Clean structured override data for Unit 1 slides to prevent layout metadata leaks and broken visual cards
UNIT0_SLIDE_DATA = {
    2: {
        "layout": "triple-grid",
        "title": "企業 AI 落地面臨的殘酷財務現實",
        "subtitle": "數字背後的沉沒成本與轉型焦慮",
        "left_badge": "GARTNER 2026",
        "left_title": "70-80%",
        "left_desc": "• 企業 AI 專案最終死於 POC (概念驗證) 階段，未能跨越生產力臨界點",
        "mid_badge": "MCKINSEY 2026",
        "mid_title": "NT$ 1,200 萬",
        "mid_desc": "• 中型企業 AI 專案失敗的平均「沉沒成本」（含硬體與工程人月）",
        "right_badge": "BCG 2026",
        "right_title": "18 個月",
        "right_desc": "• 企業從盲目投入到發現「技術路線徹底選錯」的平均時間"
    },
    3: {
        "layout": "steps",
        "title": "您今天將帶走的「實體戰略資產」",
        "subtitle": "鳳凰 AI 顧問團隊為您今天 90 分鐘決策課做出的鄭重承諾",
        "steps": [
            {
                "num": "1",
                "badge": "🗺️ 全景地圖",
                "text": "<strong>1 張 2026 AI 全景地圖</strong>：告別技術焦慮，站在決策者高度看清商業選型與技術路徑"
            },
            {
                "num": "2",
                "badge": "🎯 戰略畫布",
                "text": "<strong>1 套 4+1 戰略畫布</strong>：現場親自動手實作梳理，帶回公司即可直接召開管理會議"
            },
            {
                "num": "3",
                "badge": "⚖️ 決策路徑",
                "text": "<strong>1 個 Buy vs. Build 決策樹</strong>：理性精算 10 倍財務成本差距，防範研發沉沒成本"
            },
            {
                "num": "4",
                "badge": "📋 行動清單",
                "text": "<strong>1 份 90 天 Quick-Win 行動清單</strong>：拒絕空談與紙上談兵，下課後立即有章可循地啟動專案"
            }
        ]
    },
    8: {
        "layout": "dual-grid",
        "title": "MCP 協定 ｜ AI 時代的企業級 USB",
        "subtitle": "Model Context Protocol (模型上下文協定) 全球統一對接協定",
        "left_badge": "TRADITIONAL (HIGH COST)",
        "left_title": "傳統對接模式 (煙囪式研發)",
        "left_desc": "• 每個 AI 對接企業內部 SQL、ERP、CRM 都要單獨定製開發，耗資數十萬<br>• IT 系統架換凌亂、安全防護混亂、開發週期長達數月",
        "right_badge": "MCP STANDARD (LOW COST)",
        "right_title": "MCP 統一協定 (隨插即用)",
        "right_desc": "• 大模型與企業內部資料庫、系統全部遵循同一 USB 標準，即插即用，節省 80% 開發成本<br>• <strong>CEO 指令</strong>：未來採購任何軟體，廠商必須承諾支援 MCP 協定"
    },
    10: {
        "layout": "dual-grid",
        "title": "SLM 小語言模型 ｜ 守護企業核心智慧財產權",
        "subtitle": "混合雲 AI 架構下的隱私與財務最優選型",
        "left_badge": "CLOUD LLM (RISK & COST)",
        "left_title": "大型雲端 LLM 服務",
        "left_desc": "• <strong>隱私洩露</strong>：數據必須上傳至外部雲端伺服器，商業配方與財務機密有外流風險<br>• <strong>昂貴費用</strong>：按人頭按月收取高額訂閱費，年累計費用隨人數暴增",
        "right_badge": "LOCAL SLM (SECURE & ONE-TIME)",
        "right_title": "本地私有化 SLM",
        "right_desc": "• <strong>100% 安全</strong>：模型直接安裝部署在公司機房內，100% 離線可用，資料絕對不出大樓<br>• <strong>一次性投資</strong>：無需月費，僅需購置高性價比本地 GPU 伺服器，永久擁有私有知識庫"
    },
    15: {
        "layout": "steps",
        "title": "鳳凰 AI 獨家：RAG 採購的 5 大階梯",
        "subtitle": "避開 NT$ 500 萬沉沒成本的科學採購路徑",
        "steps": [
            {
                "num": "1",
                "badge": "數位化清查",
                "text": "確認紙本文檔是否已完全數位化與 OCR 掃描。無數據，則嚴禁啟動 RAG。"
            },
            {
                "num": "2",
                "badge": "免費驗證",
                "text": "使用 Google NotebookLM 免費測試 30 天，驗證資料品質與模型回覆精度。"
            },
            {
                "num": "3",
                "badge": "SaaS 租用",
                "text": "若免費版不夠，採購成熟 SaaS (如 Notion AI/Glean)，一週內上線，月租極低。"
            },
            {
                "num": "4",
                "badge": "低碼客製",
                "text": "若需串接內部系統，找鳳凰 AI 使用 n8n/Dify 進行微客製 (費用僅 30-50 萬)。"
            },
            {
                "num": "5",
                "badge": "私有自建",
                "text": "僅在集團具備極度機密與預算、且有專屬 IT 團隊時，才考慮花 300 萬以上自建。"
            }
        ]
    },
    41: {
        "layout": "steps",
        "title": "鳳凰 AI 獨家：企業 AI 落地 90 天具體戰術步驟",
        "subtitle": "從決策到勝利的臨界點，分階段、看得見成果的務實步伐",
        "steps": [
            {
                "num": "1",
                "badge": "第 1-30 天",
                "text": "補齊治理防線，發布全員『不裁員聲明』與『員工 AI 使用守則』。挑選右上角 Quick-Win 項目，採用 <strong>Rent 訂閱模式</strong> 快速開通 5 個帳號試用。"
            },
            {
                "num": "2",
                "badge": "第 31-60 天",
                "text": "進行 30 天試點小考，收集工時與效益數據。頒發首季『AI 卓越貢獻獎』並舉辦分享會，利用同儕激勵消除一線員工的防備與取代恐懼。"
            },
            {
                "num": "3",
                "badge": "第 61-90 天",
                "text": "進行財務核銷與 ROI 自評。部署模型自動分流 Router 與 API Gateway，省下 70% Token 費用。決定擴大採購或導入工作坊自研。"
            }
        ]
    },
    42: {
        "layout": "dual-grid",
        "title": "快速起手 ｜ 90 分鐘專家 AI 落地快診服務",
        "subtitle": "以最低成本，建構企業 AI 的理性安全護城河",
        "left_badge": "DIAGNOSIS (NT$ 12,800)",
        "left_title": "專家前置快診",
        "left_desc": "• <strong>量化雷達</strong>：產出企業 AI 成熟度五維度量化雷達圖<br>• <strong>套利路徑</strong>：為貴司規劃專屬補助與租稅套利匹配矩陣<br>• <strong>成果報告</strong>：提供 8-12 頁客製化 PDF 報告，盤點場景、精算 TCO、並匹配政府補助與節稅路徑",
        "right_badge": "RESERVATION & CTA",
        "right_title": "專屬健康檢查預約",
        "right_desc": "• <strong>全額折抵</strong>：本快診費用可 100% 全額折抵後續工作坊或陪跑專案費<br>• <strong>預約方式</strong>：掃描 QR Code 填寫問卷並上傳您的 A3 畫布，顧問團隊親自研析，5 個工作天內出具完整可行性報告"
    },
    44: {
        "layout": "dual-grid",
        "title": "Q＆A ｜ 自由發問與諮詢預約",
        "subtitle": "鳳凰 AI 顧問團隊：首席顧問 孟淑慧 ＆ 策略長 陳文家",
        "left_badge": "Q&A SESSION",
        "left_title": "自由發問時間",
        "left_desc": "• <strong>現場互動</strong>：歡迎隨時舉手提問，解答關於模型選型、變革管理、補助申報等任何實務問題<br>• <strong>內訓洽談</strong>：歡迎來信或會後交流企業內訓合作模式",
        "right_badge": "RESERVATION",
        "right_title": "預約快診與聯絡",
        "right_desc": "• <strong>快診表單</strong>：掃描 QR Code 填寫表單，預約專家前置診斷服務，產出專屬可行性評估<br>• <strong>聯絡信箱</strong>：allmyway2007@gmail.com ｜ 專員將在 24 小時內回覆您"
    }
}

UNIT1_SLIDE_DATA = {
    1: {
        "layout": "cover",
        "title": "AI 基礎理論與 2026 商業意涵 (CEO 90分鐘戰略速覽)",
        "subtitle": "從技術思維到決策邏輯：破除參數迷信，建構企業級大模型營運底座",
        "authors": "首席顧問 孟淑慧 ｜ 策略長 陳文家"
    },
    2: {
        "layout": "dual-grid",
        "title": "技術底層的範式革命：Rule-Based vs. 表示學習 (Learning Representations)",
        "subtitle": "",
        "left_badge": "RULE-BASED",
        "left_title": "規則導向 (Rule-Based)",
        "left_desc": "• 輸入資料 ➔ 人類工程師寫死的 \"IF-THEN\" 規則 ➔ 脆弱的輸出 (一旦語意稍微改變就崩潰)",
        "right_badge": "REPRESENTATION LEARNING",
        "right_title": "表示學習 (Learning Representations)",
        "right_desc": "• 輸入資料 ➔ 語意目標 ➔ 模型自動在幾何空間中對齊表徵 ➔ 靈活具備泛化能力的智慧輸出<br>• <strong>關鍵點</strong>：用幾何空間取代硬編碼"
    },
    3: {
        "layout": "formulas-and-badges",
        "title": "2026 鳳凰 AI 現代大模型營運架構公式",
        "subtitle": "",
        "formula": r"\text{現代 AI 營運架構} = \text{海量資料} + \text{Transformer 架構} + \text{自監督學習} + \text{人類偏好對齊 (RLHF/DPO)} + \text{推理與工具調用}",
        "badges": [
            "海量資料 (NIST AI RMF)",
            "Transformer 架構",
            "自監督學習",
            "人類偏好對齊 (RLHF/DPO)",
            "推理與工具調用 (MCP 協定)"
        ]
    },
    4: {
        "layout": "dual-grid",
        "title": "Token 標記化的商業算計：避開繁體中文分詞的 API 財務陷阱",
        "subtitle": "Tokenizer (分詞器) 對繁體中文優化不足將導致企業 API 成本暴增 3 倍",
        "left_badge": "WARNING (優化不足)",
        "left_title": "繁體中文優化不足的模型",
        "left_desc": "• 輸入「這家銀行的行長」➔ 拆為 12 個無規律 Token (如 <code>這</code>、<code>##家</code>、<code>銀</code>、<code>##行</code>、<code>的</code>、<code>##行</code>、<code>##長</code>)<br>• <strong>後果</strong>：Token 數 = 12，API 費用 3 倍暴增，Context Window 浪費且推理速度下降",
        "right_badge": "OPTIMIZED (深度優化)",
        "right_title": "鳳凰 AI 繁中優化系統",
        "right_desc": "• 同一個句子 ➔ 乾淨俐落地拆為 4 個 Token (<code>這家</code>、<code>銀行</code>、<code>的</code>、<code>行長</code>)<br>• <strong>優勢</strong>：Token 數 = 4，算力與推理速度最優化，API 費用節省 60%"
    },
    5: {
        "layout": "formulas-and-grid",
        "title": "餘弦夾角與向量嵌入的幾何魅力：RAG 知識庫的絕對本質",
        "subtitle": "Embedding (向量嵌入) 將文字轉化為高維幾何空間的座標",
        "formula": r"\text{Cosine Similarity}(\vec{a}, \vec{b}) = \frac{\vec{a} \cdot \vec{b}}{\|\vec{a}\| \|\vec{b}\|}",
        "left_badge": "ALIGNMENT (語意對齊)",
        "left_title": "夾角接近 0 (相似度高)",
        "left_desc": "• <code>[退款申請]</code> 與 <code>[我想拿回我的錢]</code> 夾角極小，餘弦相似度接近 1<br>• <strong>應用</strong>：RAG 知識庫能跨越字面拼寫，實現即時且精準的語意檢索",
        "right_badge": "OOD (語意無關)",
        "right_title": "夾角接近 90° (無關聯)",
        "right_desc": "• <code>[水果蘋果]</code> 被甩在完全不同的維度，相似度接近 0<br>• <strong>優勢</strong>：有效過濾雜訊，確保撈取的內部規章與問題高度契合"
    },
    6: {
        "layout": "formulas-and-triple-grid",
        "title": "Transformer 架構核心：自注意力機制 (Self-Attention) 說解",
        "subtitle": "利用 Q, K, V 機制讓模型實時計算詞與詞之間的注意力引力場",
        "formula": r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V",
        "left_badge": "QUERY (Q)",
        "left_title": "Query (查詢向量)",
        "left_desc": "• 像是<strong>查詢信封</strong><br>• 代表「我當前正在關注的這個詞是誰」",
        "mid_badge": "KEY (K)",
        "mid_title": "Key (鍵向量)",
        "mid_desc": "• 像是<strong>檔案櫃標籤</strong><br>• 代表「文章中其他詞各自帶有的特徵標籤」",
        "right_badge": "VALUE (V)",
        "right_title": "Value (值向量)",
        "right_desc": "• 像是<strong>實體文件內容</strong><br>• 代表「其他詞背後真正的實際語意價值」"
    },
    7: {
        "layout": "triple-grid",
        "title": "突破 KV Cache 頻寬地獄：GQA (集群查詢注意力) 之商業節能奇蹟",
        "subtitle": "當上下文變長時，傳統 MHA 的 VRAM (顯存) 消耗呈線性暴增",
        "left_badge": "MHA (WARNING)",
        "left_title": "MHA 多頭注意力",
        "left_desc": "• 四個 Query 頭連接四個獨立的 Key/Value 頭<br>• 線路繁瑣混亂，KV Cache 顯存暴增，硬體成本極高",
        "mid_badge": "MQA (STANDARD)",
        "mid_title": "MQA 單頭注意力",
        "mid_desc": "• 四個 Query 頭共用一個 Key/Value 頭<br>• 極度省顯存，但模型精度受損，長文本中容易丟三落四",
        "right_badge": "GQA (OPTIMIZED)",
        "right_title": "GQA 集群查詢注意力",
        "right_desc": "• 分組共享，每兩個 Query 頭共享一組 Key/Value 頭<br>• KV Cache 頻寬消耗降低 8 倍，精度近乎零損耗，省下 70% 算力折舊"
    },
    8: {
        "layout": "dual-grid-split",
        "title": "自監督預訓練：模型是如何無痛學習人類語言的？",
        "subtitle": "無需人工手動標註，利用文本本身作為標準答案",
        "left_badge": "PRE-TRAINING",
        "left_title": "自監督學習 (挖空填詞)",
        "left_desc": "• <strong>原始文本</strong>：<br>「鳳凰AI 致力於提供企業最頂級的 <code>[ ? ]</code>」<br>• <strong>預測任務</strong>：<br>計算下一個 Token (Next-Token Prediction) 的機率分佈，自動學習人類語言的語法與邏輯",
        "right_badge": "PROBABILITY",
        "right_title": "模型預測概率圖",
        "right_desc": "• <strong>AI 培訓課程</strong> ➔ <strong style='color:var(--color-success)'>82.00% 概率 (高亮)</strong><br>• <strong>太空船</strong> ➔ 0.02% 概率<br>• <strong>水果籃</strong> ➔ 0.01% 概率"
    },
    9: {
        "layout": "dual-grid",
        "title": "人類偏好對齊的商業剛需：從無情聯想機到品牌代言人",
        "subtitle": "剛出山的大模型只是文字聯想機，必須進行人類偏好對齊以控制公關風險",
        "left_badge": "UNALIGNED (WARNING)",
        "left_title": "未對齊的純預訓練模型",
        "left_desc": "• <strong>輸入</strong>：「我該怎麼調配炸藥？」<br>• <strong>回答</strong>：「步驟一：準備化學原料...」<br>• <strong>後果</strong>: 高法律合規風險、幻覺與偏見發散，無法對外提供服務",
        "right_badge": "ALIGNED (OPTIMIZED)",
        "right_title": "經過 DPO 偏好對齊的模型",
        "right_desc": "• <strong>同一個輸入回答</strong>：「對不起，我無法提供此有害訊息。我可以協助您了解安全防護規範。」<br>• <strong>優勢</strong>：符合 NIST AI RMF 與品牌聲調一致，安全合規"
    },
    10: {
        "layout": "formulas-and-grid",
        "title": "偏好對齊的技術演進：RLHF 強化學習 vs. DPO (直接偏好最佳化)",
        "subtitle": "DPO 在數學上完成了一次優雅突破：大模型本身就可以隱式作為自己的獎勵模型",
        "formula": r"\mathcal{L}_{\text{DPO}}(\pi_\theta; \pi_{\text{ref}}) = - \mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w | x)}{\pi_{\text{ref}}(y_w | x)} - \beta \log \frac{\pi_\theta(y_l | x)}{\pi_{\text{ref}}(y_l | x)} \right) \right]",
        "left_badge": "RLHF (WARNING)",
        "left_title": "RLHF 強化學習",
        "left_desc": "• PPO 強化學習算法<br>• 需在顯存中並行四個龐大神經網路，顯存消耗巨大<br>• 訓練極度不穩定，參數稍微設錯就無法收斂",
        "right_badge": "DPO (OPTIMIZED)",
        "right_title": "DPO 直接偏好最佳化",
        "right_desc": "• 2026 技術主流<br>• 免除訓練 Reward Model 的繁瑣步驟<br>• 簡化為二元交叉熵分類問題，收斂極度穩定，訓練速度飆升數倍"
    },
    11: {
        "layout": "dual-grid",
        "title": "避坑指南：DPO 對齊微調的物理限制與過擬合危機",
        "subtitle": "過度安全對齊會導致「對齊稅 (Alignment Tax)」，使模型邏輯與數學能力退化",
        "left_badge": "GREEN LINE",
        "left_title": "對齊安全度 (綠線)",
        "left_desc": "• 隨 DPO 訓練迭代次數增加而一路上升，說話變得溫和合規，符合安全紅線",
        "right_badge": "RED LINE (WARNING)",
        "right_title": "基礎推理能力 (紅線)",
        "right_desc": "• 臨界點後突然發生懸崖式下滑崩塌，基礎數學與邏輯推理能力退化（過擬合）<br>• <strong>避坑指南</strong>：嚴格清洗數據，控制 KL 散度懲罰係數 $\beta$，守護推理大腦"
    },
    12: {
        "layout": "steps",
        "title": "從空談到執行：Function Calling (工具調用) 機制之商業閉環",
        "subtitle": "模型發出 JSON 調用請求，安全中台讀取數據回傳，實現 API 行動閉環",
        "steps": [
            {
                "num": "1",
                "badge": "使用者提問",
                "text": "「幫我查詢客戶 C102 目前的餘額是多少？」"
            },
            {
                "num": "2",
                "badge": "AI 意圖推理",
                "text": "大腦識別需要外部數據，輸出 JSON 函數調用：<code>{ \"name\": \"get_customer_balance\", \"arguments\": { \"customer_id\": \"C102\" } }</code>"
            },
            {
                "num": "3",
                "badge": "企業中台執行",
                "text": "企業安全中台攔截 JSON，從 ERP 資料庫撈取真實數字並回傳：<code>$500,000</code>"
            },
            {
                "num": "4",
                "badge": "語意回答",
                "text": "模型合流資訊，以自然語言溫雅回覆：「客戶 C102 目前餘額為新台幣 50 萬元整。」"
            }
        ]
    },
    13: {
        "layout": "dual-grid",
        "title": "2026 最新連線標準：Model Context Protocol (MCP 協定)",
        "subtitle": "MCP 協定是大模型界的 \"Type-C 標準接口\"，免除複雜的一對一客製整合",
        "left_badge": "PLUG (CLIENT)",
        "left_title": "插頭側 (主流大模型)",
        "left_desc": "• Gemini, Claude, Llama 等模型端<br>• 支持統一標準化連線通道，隨插即用",
        "right_badge": "SOCKET (SERVER)",
        "right_title": "插座側 (企業數據源)",
        "right_desc": "• Postgres, Slack, GitHub, 既有 ERP 等異構系統<br>• 僅需開發標準 MCP Server 即可實現模組化插拔對接，集成成本降低 80%"
    },
    14: {
        "layout": "dual-grid",
        "title": "現場實作挑戰：繁中分詞評估與 AI Agent 安全防線設計",
        "subtitle": "請對照 A3 戰略畫布進行各桌高管討論",
        "left_badge": "CHALLENGE 1",
        "left_title": "實作一：分詞自診",
        "left_desc": "• <strong>評估句子</strong>：<br>「本保險契約特別條款之給付限額」<br>• <strong>思考</strong>：若 Tokenizer 出現嚴重分詞錯誤，將如何扭曲幾何 Embedding 的 Cosine Similarity 座標？為何會撈出不相干條款？",
        "right_badge": "CHALLENGE 2",
        "right_title": "實作二：Agent 防禦",
        "right_desc": "• <strong>場景</strong>：行銷 Agent 歷史記錄自動發信<br>• <strong>思考</strong>：為了防範 Prompt Injection 造成的毀滅性公關災難，<code>Human-in-the-loop</code> 與 <code>意圖過濾閘門</code> 應部署在何處？"
    },
    15: {
        "layout": "dual-grid",
        "title": "為企業 AI 營運建構理性防線：可行性診斷預約",
        "subtitle": "破除參數迷信，讓財務損益語言取代技術虛報，理性跨出轉型第一步",
        "left_badge": "DIAGNOSIS",
        "left_title": "企業 AI 落地前置診斷",
        "left_desc": "• <strong>快診費用</strong>：<strong>NTD 12,800</strong> (報告款項可全額折抵後續內訓/工作坊費用)<br>• <strong>產出成果</strong>：8-12 頁客製化 PDF 診斷報告，包含繁中數據就緒度、Buy vs Build 算力財務 TCO 精算、政府 5 大補助路徑對接自評",
        "right_badge": "RESERVATION",
        "right_title": "專屬健康檢查預約",
        "right_desc": "• <strong>預約方式</strong>：掃描右下角 QR Code (限額預約)<br>• <strong>保障</strong>：鳳凰 AI 顧問團隊（孟首席顧問、陳策略長）親自研析，5 個工作天內出具完整可行性報告，守護企業 AI 投資護城河"
    }
}


# Clean structured override data for Unit 2 slides to prevent layout metadata leaks and broken visual cards
UNIT2_SLIDE_DATA = {
    1: {
        "layout": "cover",
        "title": "Voice AI 傳產落地唯一破口工作坊",
        "subtitle": "解放現場師傅雙手：從抗拒打字交班的數字幻覺，到說話 30 秒自動結構化 ERP 的智慧製造革命",
        "authors": "首席顧問 孟淑慧 ｜ 策略長 陳文家"
    },
    2: {
        "layout": "triple-grid",
        "title": "越不過的現場物理障礙",
        "subtitle": "打字系統的數字幻覺與傳產現場的致命死穴",
        "left_badge": "DIGITAL ILLUSION",
        "left_title": "數字幻覺",
        "left_desc": "• 強推一線師傅在吵雜、高溫的廠區，脫下防護手套在平板上打字輸入工單，極度不切實際",
        "mid_badge": "RESISTANCE",
        "mid_title": "一線現狀",
        "mid_desc": "• 製造業一線員工對任何「打字輸入系統」的抗拒率高達 <strong>90%</strong> 以上，難以推行",
        "right_badge": "CONSEQUENCE",
        "right_title": "致命結果",
        "right_desc": "• 數據申報率幾乎為零，交班日誌流於形式，導致設備瑕疵數據完全斷鏈，系統成為擺設"
    },
    3: {
        "layout": "dual-grid",
        "title": "技術代價 ｜ 跨越 3 秒的致命遲滯",
        "subtitle": "2026 語音技術革命：傳統串接 vs. 端到端 Realtime API",
        "left_badge": "TRADITIONAL (MHA)",
        "left_title": "傳統串接架構 (STT ➔ LLM ➔ TTS)",
        "left_desc": "• <strong>體驗</strong>：延遲高達 3 - 8 秒，音色生硬且無法打斷<br>• <strong>結果</strong>：一線技師完全失去耐心，誤判定為系統死機",
        "right_badge": "REALTIME API (OPTIMIZED)",
        "right_title": "2026 端到端 Realtime API",
        "right_desc": "• <strong>體驗</strong>：延遲僅 0.5 - 1.2 秒 (與真人對話無異)<br>• <strong>特點</strong>：音色充滿抑揚頓挫，且隨時支援語音打斷 (Interruption)"
    },
    4: {
        "layout": "dual-grid",
        "title": "第一道防線 ｜ 噪聲屏障與 VAD 機制",
        "subtitle": "85dB+ 高噪環境下的陣列降噪麥克風與邊緣端 VAD 語音檢測",
        "left_badge": "ANC HARDWARE",
        "left_title": "硬體防護：ANC 降噪耳麥",
        "left_desc": "• 沖床與精密磨床噪音大於 85 分貝，傳統麥克風完全癱瘓<br>• 部署主動降噪骨傳導耳機或陣列式定向降噪麥克風",
        "right_badge": "VAD SOFTWARE",
        "right_title": "軟體過濾：邊緣 VAD 檢測",
        "right_desc": "• 地端邊緣部署 VAD 語音活動檢測機制<br>• 自動過濾高頻機械碰撞與底噪，只傳輸人類純語音封包，省下 80% 流量費"
    },
    5: {
        "layout": "dual-grid",
        "title": "第二道防線 ｜ 國台語與產業黑話大腦",
        "subtitle": "方言與口音辨識（國台語混雜口音與南部產業術語實例）",
        "left_badge": "TRADITIONAL LLM",
        "left_title": "傳統語意模型 (口音誤判)",
        "left_desc": "• 師傅說「controller 有 lens 誤差，要 check 一下」<br>• 模型誤判為「控制器有冷死誤差，愛去缺口一下」，導致申報數據失效",
        "right_badge": "PHOENIX LOCALIZED",
        "right_title": "鳳凰 AI 傳產微調大腦",
        "right_desc": "• 前端掛載自研術語庫對照機制，精準預處理日式黑話 (如阿嚕米、露兜) 與英文縮寫<br>• 100% 咬合南部製造業口語習慣"
    },
    6: {
        "layout": "dual-grid",
        "title": "第三道防線 ｜ 語音敏感個資合規網閘",
        "subtitle": "個資保護與台灣個資法語音強制主動告知",
        "left_badge": "CONSENT PROTOCOL",
        "left_title": "技術強制告知 SOP",
        "left_desc": "• 聲音屬唯一識別敏感個資，通話前 5 秒自動播送告知宣告<br>• 使用者語音回覆「同意」即建立免責憑證，保障合規性",
        "right_badge": "DATA DESTRUCTION",
        "right_title": "地端 24H 物理銷毀",
        "right_desc": "• 錄音轉譯為結構化 JSON 文本後，錄音源檔於地端存儲器定時 24 小時內強制擦除<br>• 徹底防範敏感聲音個資二次外洩"
    },
    7: {
        "layout": "steps",
        "title": "【實作環節 1】語音智慧轉譯現場挑戰 (3 分鐘)",
        "subtitle": "現場實作：師傅口述 30 秒異常交班，AI 自動翻譯與結構化建檔",
        "steps": [
            {
                "num": "1",
                "badge": "語音口述",
                "text": "使用降噪對講機模擬師傅的國台語口語，口述 30 秒生產線異常交班描述"
            },
            {
                "num": "2",
                "badge": "即時轉譯",
                "text": "語音助理在 1.2 秒內完成低延遲轉譯，剔除贅詞與雜音"
            },
            {
                "num": "3",
                "badge": "結構化 ERP",
                "text": "自動解析抽離為 <code>設備編號</code>、<code>瑕疵等級</code>、<code>對策</code> 與 <code>主責人</code> 寫入 Notion ERP 測試看板"
            }
        ]
    },
    8: {
        "layout": "dual-grid",
        "title": "技術控制點 ｜ 零侵入式的系統防禦",
        "subtitle": "技術架構：ERP/CRM 系統的唯讀副本與 API 唯寫保護機制",
        "left_badge": "READ REPLICA",
        "left_title": "唯讀副本安全隔離",
        "left_desc": "• 語意檢索與資料比對只在 100% 物理隔離的<strong>「唯讀副本資料庫」</strong>中執行<br>• 大模型自始至終接觸不到核心庫，防止因幻覺破壞生產數據",
        "right_badge": "WRITE SHIELD (HITL)",
        "right_title": "API 唯寫保護與 Token 驗證",
        "right_desc": "• 寫入請求必須通過地端 Token 驗證密鑰<br>• 必須經由現場組長在 App 上手動點擊「Approve」批准方可執行，完美規避自動化出錯風險"
    },
    9: {
        "layout": "dual-grid",
        "title": "收服人心 ｜ 讓師傅瘋狂使用語音的祕辛",
        "subtitle": "變革心法：收服 52 歲師傅的語音日誌 OKR 加薪與同儕激勵",
        "left_badge": "OKR BONUS",
        "left_title": "語音日誌 OKR 加薪方案",
        "left_desc": "• 老闆承諾：每天完成 2 次語音交班且結構化成功者，當月績效考評自動加分效率加薪<br>• 將師傅對「被監控」的戒備轉化為加薪的捷徑",
        "right_badge": "PEER PRESSURE",
        "right_title": "同儕效率激勵看板",
        "right_desc": "• 產線看板即時展示「語音交班之星」，前三名小組獲得高額福利金與榮譽表揚<br>• 師傅配合度飆升至 98%"
    },
    10: {
        "layout": "triple-grid",
        "title": "語音系統的長效防禦機制",
        "subtitle": "保命防護欄：休眠與喚醒機制、噪音誤觸發過濾與 HITL 真人轉接",
        "left_badge": "WAKE-UP WORD",
        "left_title": "休眠與喚醒 (Loop Control)",
        "left_desc": "• 嚴禁系統 24 小時無效回傳。設計語音喚醒關鍵字，僅在喚醒後進行推論，節省 80% Token 費用",
        "mid_badge": "NOISE GATING",
        "mid_title": "噪音防誤判過濾器",
        "mid_desc": "• 當偵測到背景噪音大於 90分貝 且無語音特徵時，自動啟動「1.5秒語意熔斷」，物理截斷 API 呼叫",
        "right_badge": "HUMAN BACKUP",
        "right_title": "無縫轉接真人 (HITL)",
        "right_desc": "• 大模型判定技師處於嚴重挫折或涉及高度機密時，強制阻斷 AI，2 秒內轉接至廠長或資深工程師"
    },
    11: {
        "layout": "triple-grid",
        "title": "鳳凰 AI 實戰案例 A ｜ 精密扣件廠語音交班",
        "subtitle": "實例解析 A：精密扣件廠（良率預警、提前預警設備停機避免 NT$ 45 萬損失）",
        "left_badge": "PAIN POINT",
        "left_title": "客戶痛點",
        "left_desc": "• 師傅平均年齡 52 歲抗拒打字，交班日誌缺漏率高達 <strong>85%</strong>，數據嚴重斷鏈",
        "mid_badge": "SOLUTION",
        "mid_title": "導入方案",
        "mid_desc": "• 部署基於 Gemini Live API 的廠區語音對講機系統，師傅口述 30秒自動寫入 ERP",
        "right_badge": "ROI OUTCOME",
        "right_title": "實質 ROI",
        "right_desc": "• 交班率暴增至 98%，數據收集降至即時<br>• 提前預警 3 次偏芯停機，避免損失 <strong>新台幣 450,000 元</strong>"
    },
    12: {
        "layout": "triple-grid",
        "title": "鳳凰 AI 實戰案例 B ｜ 鋼鐵重工高噪通報",
        "subtitle": "實例解析 B：鋼鐵重工廠（90dB 高噪頭盔、異常通報流程由 4小時縮短至 2分鐘）",
        "left_badge": "PAIN POINT",
        "left_title": "客戶痛點",
        "left_desc": "• 現場環境高達 90dB，高粉塵高溫易燒毀平板，手寫異常至建檔核簽需時 <strong>4 小時</strong>",
        "mid_badge": "SOLUTION",
        "mid_title": "導入方案",
        "mid_desc": "• 配置主動降噪頭盔式耳麥，搭配地端 Whisper 降噪過濾與本地閉環大腦",
        "right_badge": "ROI OUTCOME",
        "right_title": "實質 ROI",
        "right_desc": "• 90分貝下精準度達 93%<br>• 通報流程從 4 小時縮短至 <strong>2 分鐘</strong>，效率提升 120 倍"
    },
    13: {
        "layout": "steps",
        "title": "拿政府的 460 億為您的語音 AI 專案買單",
        "subtitle": "台灣五大補助對接與淨自籌款降至 46% 的政策套利實務",
        "steps": [
            {
                "num": "1",
                "badge": "SBIR Stage 2",
                "text": "為語音大腦與 NLP 系統申請 50% 研發資金補助"
            },
            {
                "num": "2",
                "badge": "智慧機械計畫",
                "text": "取得地端降噪麥克風與安全帽購置折舊補貼最高 500 萬"
            },
            {
                "num": "3",
                "badge": "充電起飛計畫",
                "text": "師傅的使用訓練內訓課程，講師與輔導費 100% 由政府買單"
            },
            {
                "num": "4",
                "badge": "產創條例 10-1",
                "text": "享有 5% 直接抵減企業營所稅，將自籌比暴降至 46%"
            }
        ]
    },
    14: {
        "layout": "dual-grid",
        "title": "最嚴格的商業機敏安全與隱私承諾",
        "subtitle": "B2B 安全保密雙向 NDA 與結案錄音檔案物理銷毀承諾",
        "left_badge": "NDA SHIELD",
        "left_title": "保密承諾 1：雙向 NDA",
        "left_desc": "• 合作首日強制簽署受中華民國法律管轄之雙向 NDA 協議<br>• 絕不上傳任何未經遮罩之客戶名單或製程不良率數據至雲端",
        "right_badge": "PHYSICAL ERASE",
        "right_title": "保密承諾 2：錄音物理銷毀",
        "right_desc": "• 專案結束或診斷報告交付後 6 個月內，完全銷毀所有暫存錄音檔影本<br>• 捍衛企業製程機密"
    },
    15: {
        "layout": "dual-grid",
        "title": "鳳凰 AI：為您的產線裝上會聽話的智慧大腦",
        "subtitle": "預約 NT$ 12,800 到廠噪聲與語音成熟度快診引流與結語",
        "left_badge": "DIAGNOSIS",
        "left_title": "現場專家快診 (NT$ 12,800)",
        "left_desc": "• <strong>噪聲實測</strong>：顧問攜專業分貝儀到產線進行真實噪聲頻譜測試<br>• <strong>術語自評</strong>：盤點一線師傅台式黑話口音與術語就緒度<br>• <strong>架構規劃</strong>：規劃 ERP 唯讀副本與 API 唯寫保護網路拓撲",
        "right_badge": "RESERVATION",
        "right_title": "專屬健康檢查預約",
        "right_desc": "• <strong>折抵機制</strong>：本快診款項可 100% 全額折抵後續長期陪跑或顧問部署費<br>• <strong>預約方式</strong>：掃描 QR Code，顧問親自到廠檢測，5 個工作天出具完整可行性診斷書"
    }
}



# Clean structured override data for Unit 4 slides to prevent layout metadata leaks and broken visual cards
UNIT4_SLIDE_DATA = {
    1: {
        "layout": "cover",
        "title": "機器學習與數據預測財務決策工作坊 (CFO & CDO 數據資產營運學)",
        "subtitle": "破除唯 LLM 算力泡沫：以最優 TCO 與多模態特徵工程建構企業數據預測防線",
        "authors": "首席顧問 孟淑慧 ｜ 策略長 陳文家"
    },
    2: {
        "layout": "dual-grid",
        "title": "傳統機器學習 vs. 生成式大模型：算力與推理成本的萬倍鴻溝",
        "subtitle": "用大砲打小鳥的財務悲劇：企業級預測型任務必須回歸合理 TCO 的傳統 ML",
        "left_badge": "TRADITIONAL ML",
        "left_title": "XGBoost / LightGBM 預測",
        "left_desc": "• 本地自主訓練與部署，硬體算力幾乎為 0<br>• 推理成本低於 0.01 USD / 萬次，毫秒級極速回應",
        "right_badge": "GENERATIVE AI (WARNING)",
        "right_title": "GPT-4o / Claude 3.5 API",
        "right_desc": "• 雲端超大模型 API 調用，受網絡頻寬與 VRAM 限制<br>• 推理成本高於 10.00 USD / 萬次，存在萬倍的算力財務差距"
    },
    3: {
        "layout": "formulas-and-grid",
        "title": "企業 AI 專案淨收益公式與技術導入決策路線圖",
        "subtitle": "技術導入必須嚴格掛鈎財務損益表 (P&L)，算清實質財務回報",
        "formula": r"\text{企業 ML 專案淨收益} = \text{預防停機節省成本} - (\text{ML 軟硬體部署費用} + \text{誤報重工成本} + \text{漏報災難停機代價})",
        "left_badge": "DECISION TREE",
        "left_title": "技術導入選型決策",
        "left_desc": "• <strong>無專職 DS 團隊</strong> ➔ 採購成熟 AutoML 平台或 Low-Code 方案，縮短導入時效<br>• <strong>有專職 DS 團隊</strong> ➔ 選擇 Python 自研演算法，深耕企業客製場景",
        "right_badge": "NET INCOME",
        "right_title": "數據預測淨收益",
        "right_desc": "• 算力 TCO 與模型預測誤/漏檢代價，是檢驗 AI 成敗的唯一指標<br>• 避免盲目自建龐大架構，優先尋求 Quick-Win 試點項目"
    },
    4: {
        "layout": "triple-grid",
        "title": "時序預測的範式轉移：時間序列基礎模型 (TSFMs) 崛起",
        "subtitle": "時序預測完成了從單一序列建模到「零樣本冷啟動」的範式轉移",
        "left_badge": "1ST GEN",
        "left_title": "第一代 (ARIMA)",
        "left_desc": "• 傳統統計學演算法，需對每條時間序列單獨建模<br>• 無法跨序列泛化，長文本或冷啟動場景完全失效",
        "mid_badge": "2ND GEN",
        "mid_title": "第二代 (DeepAR/TFT)",
        "mid_desc": "• 傳統深度學習時序模型，可學習多序列共享規律<br>• 依賴歷史長度與大量本地訓練，調參耗時較長",
        "right_badge": "3RD GEN (OPTIMIZED)",
        "right_title": "第三代 (TimeGPT/Chronos)",
        "right_desc": "• 零樣本 (Zero-Shot) 時序預測基礎模型崛起<br>• 支持極短序列冷啟動，直接實現未來 7 天精準預測波動"
    },
    5: {
        "layout": "dual-grid-split",
        "title": "降本增效的核心：熱數據地端 LightGBM vs. 冷數據雲端 TimeGPT",
        "subtitle": "孟顧問的「冷熱分流時序混合戰略」，為企業省下 90% 雲端 API 帳單",
        "left_badge": "熱路徑 (95% 流量)",
        "left_title": "地端 LightGBM / XGBoost",
        "left_desc": "• <strong>適用條件</strong>：歷史長度大於 3 個月的常規數據序列<br>• <strong>優勢</strong>：本地自主訓練，推理成本為 0，極速回應",
        "right_badge": "冷路徑 (5% 流量)",
        "right_title": "雲端 TimeGPT / Chronos API",
        "right_desc": "• <strong>適用條件</strong>：歷史長度小於 3 個月的新 SKU (冷啟動)<br>• <strong>優勢</strong>：按次付費 API，零樣本快速預估，無需本地訓練數據"
    },
    6: {
        "layout": "formulas-and-grid",
        "title": "時間序列特徵工程：滑動窗口統計與差分特徵實務",
        "subtitle": "特徵工程是機器學習的靈魂，能將原始時序轉化為高判別特徵矩陣",
        "formula": r"\text{滑動均值} = \mu_t = \frac{1}{W}\sum_{i=0}^{W-1} x_{t-i}, \quad \text{一階差分} = \Delta x_t = x_t - x_{t-1}",
        "left_badge": "FEATURE 1",
        "left_title": "滑動窗口特徵",
        "left_desc": r"• 緩慢移動窗口，計算區間內 $\mu_t$ 與 $\sigma_t$<br>• 捕捉短期波動規律與震盪趨勢，平滑數據噪聲",
        "right_badge": "FEATURE 2",
        "right_title": "差分與季節性特徵",
        "right_desc": "• 計算 $x_t - x_{t-1}$，消除時序的不平穩趨勢<br>• 凸顯週期性季節變化，強化機器學習大腦的趨勢感知"
    },
    7: {
        "layout": "formulas-and-grid",
        "title": "頻域特徵奇蹟：快速傅立葉變換 (FFT) 與預測性維護 (PdM) 實務",
        "subtitle": "傅立葉變換能將時域波形分解為頻率成分，捕捉隱藏的高頻微小震動",
        "formula": r"X(f) = \int_{-\infty}^{\infty} x(t) e^{-i 2 \pi f t} dt",
        "left_badge": "TIME DOMAIN",
        "left_title": "時域波形 (無異常)",
        "left_desc": "• 展現混亂、無規律的微小高頻震動訊號<br>• 直觀看無法識別異常，傳統時域特徵檢測極易漏報",
        "right_badge": "FREQUENCY DOMAIN",
        "right_title": "頻域光譜 (金色特徵峰)",
        "right_desc": "• 透過 FFT 變換，在 120Hz 處呈現一根極高聳的金色能量特徵峰<br>• 精準鎖定真空幫浦軸承故障頻率，實現高可靠預測維護"
    },
    8: {
        "layout": "steps",
        "title": "文本特徵融合：將歷史人工維護日誌 Sentence Embedding 向量化",
        "subtitle": "融合結構化感測器數據與非結構化文本工單，打造多模態預測模型",
        "steps": [
            {
                "num": "1",
                "badge": "手寫工單日誌",
                "text": "「軸承有微小異音，已更換油封但仍有輕微抖動」"
            },
            {
                "num": "2",
                "badge": "Embedding 漏斗",
                "text": "通過 <code>Sentence-Transformers (768-dim)</code> 模型，將文本轉化為高維語意空間特徵"
            },
            {
                "num": "3",
                "badge": "語意向量化",
                "text": "生成一排密集的浮點數向量 <code>[0.12, -0.45, ..., 0.88]</code>"
            },
            {
                "num": "4",
                "badge": "特徵拼接融合",
                "text": "與 FFT 頻域特徵、時序滑動窗口特徵進行拼接，共同餵入 <code>XGBoost</code> 預測引擎"
            }
        ]
    },
    9: {
        "layout": "formulas-and-triple-grid",
        "title": "跳出學術指標的誤區：精準率 (Precision) 與召回率 (Recall) 的商業翻譯",
        "subtitle": "Precision 與 Recall 通常此消彼長，商業工程師必須精確權衡兩者代價",
        "formula": r"\text{F1-Score} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}",
        "left_badge": "PRECISION",
        "left_title": "精準率 (Precision)",
        "left_desc": "• 公式：$\frac{TP}{TP + FP}$<br>• 商業轉譯：判定為瑕疵的商品中，有多少是真的瑕疵？<br>• <strong>關鍵</strong>：不誤報 (避免工程師白跑)",
        "mid_badge": "RECALL",
        "mid_title": "召回率 (Recall)",
        "mid_desc": "• 公式：$\frac{TP}{TP + FN}$<br>• 商業轉譯：產線上所有真正的瑕疵品，模型抓出了多少？<br>• <strong>關鍵</strong>：不漏報 (防範危險瑕疵出貨)",
        "right_badge": "F1-SCORE",
        "right_title": "兩者的權衡藝術",
        "right_desc": "• Precision 偏重降低誤報成本；Recall 偏重降低漏報代價<br>• F1-Score 為兩者的調和平均，代表綜合預測能力的均衡指標"
    },
    10: {
        "layout": "formulas-and-grid",
        "title": "混淆矩陣成本加權財務評估框架 (Cost-Weighted ROI Framework)",
        "subtitle": "利用成本矩陣取代傳統準確率指標，真實評估 AI 帶來的實質損益",
        "formula": r"\text{財務收益} = TP \times V_{TP} - FP \times L_{\text{over}} - FN \times L_{\text{leak}}",
        "left_badge": "CONFUSION MATRIX",
        "left_title": "混淆矩陣 $2 \times 2$ 象限",
        "left_desc": "• <strong>TP (預防成功)</strong> ➔ 避免突發大停機，回收產能代價<br>• <strong>TN (正常運行)</strong> ➔ 系統正確無害，無額外支出成本<br>• <strong>FP (誤報重工)</strong> ➔ 工程師白跑，損失檢查與人工覆核成本",
        "right_badge": "FN WARNING",
        "right_title": "FN 漏報代價 (深紅警告)",
        "right_desc": "• <strong>FN (漏報停機)</strong> ➔ 設備報廢，引發災難性停機與整批廢品<br>• <strong>非對稱損失</strong>：漏報損失 ($L_{\text{leak}}$) 通常比誤報重工 ($L_{\text{over}}$) 高出數十倍"
    },
    11: {
        "layout": "dual-grid",
        "title": "致命精算：模型 A (學術優化) vs. 模型 B (財務優化) 損益對決",
        "subtitle": "為什麼一個 90% 準確率的模型反而會讓企業大虧數億元？",
        "left_badge": "MODEL A (ACADEMIC)",
        "left_title": "模型 A：學術型 (平衡)",
        "left_desc": "• Precision = 80%, Recall = 80%<br>• 漏報 FN = 20 次，誤報 FP = 20 次<br>• <strong>財務淨收益 = 1.96 億元</strong>",
        "right_badge": "MODEL B (BUSINESS)",
        "right_title": "模型 B：商業型 (防漏報)",
        "right_desc": "• Precision = 50%, Recall = 98%<br>• 漏報 FN = 2 次，誤報 FP = 100 次<br>• <strong>財務淨收益 = 4.50 億元 (多賺 2.54 億！)</strong>"
    },
    12: {
        "layout": "formulas-and-grid",
        "title": "現場實作挑戰一：瑕疵檢測非對稱商業損失精算",
        "subtitle": "請拿出畫布，利用公式精算兩模型總損失，做出正確技術採購決策",
        "formula": r"\text{Total Loss} = FN \times L_{\text{leak}} + FP \times L_{\text{over}}",
        "left_badge": "PARAMETERS",
        "left_title": "已知商業參數",
        "left_desc": r"• <strong>漏檢損失 ($L_{\text{leak}}$)</strong> ➔ 單個 <strong>5,000 元</strong><br>• <strong>誤檢重工 ($L_{\text{over}}$)</strong> ➔ 單個 <strong>100 元</strong>",
        "right_badge": "MODELS",
        "right_title": "待評估模型",
        "right_desc": "• <strong>模型 A</strong> ➔ $FN = 10, FP = 300$<br>• <strong>模型 B</strong> ➔ $FN = 40, FP = 20$"
    },
    13: {
        "layout": "triple-grid",
        "title": "現場實作挑戰二：明日生鮮蔬菜銷量預測特徵工程設計",
        "subtitle": "請各桌主管進行 2x2 矩陣特徵盤點，並在 A3 戰略畫布上填寫",
        "left_badge": "TIME SERIES",
        "left_title": "第一欄：時間序列特徵",
        "left_desc": "• 待學員填寫 4 個特徵 📅<br>• 提示：滑動窗口均值、歷史同期銷量、一階差分、週環比",
        "mid_badge": "SHOP & SKU",
        "mid_title": "第二欄：店鋪與商品特徵",
        "mid_desc": "• 待學員填寫 3 個特徵 🏪<br>• 提示：店鋪級別、品類銷量排名、商品單價",
        "right_badge": "ENVIRONMENT",
        "right_title": "第三欄：外部環境特徵",
        "right_desc": "• 待學員填寫 3 個特徵 ⛈️<br>• 提示：氣溫波動、是否週末假期、降雨量"
    },
    14: {
        "layout": "triple-grid",
        "title": "數據資產的主動治理：安全防線與雙向機敏保護",
        "subtitle": "對齊安全國際標準，在保護企業核心數據資產與挖掘預測價值間取得平衡",
        "left_badge": "COMMITMENT 1",
        "left_title": "地端數據隔離",
        "left_desc": "• 簽署雙向 NDA 承諾<br>• 核心製程與機敏數據地端隔離，絕不上雲，100% 安全保障",
        "mid_badge": "COMMITMENT 2",
        "mid_title": "敏感資料遮罩",
        "mid_desc": "• 建置集中式遮罩網閘<br>• 去識別化過濾，阻斷任何個資與機密數據外洩",
        "right_badge": "COMMITMENT 3",
        "right_title": "六個月銷毀機制",
        "right_desc": "• 專案結案後 6 個月，自動銷毀所有測試數據與模型拷貝<br>• 建立高防線數據生命週期主動治理"
    },
    15: {
        "layout": "dual-grid",
        "title": "邁出理性的第一步：企業 ML 落地與預測成熟度前置快診",
        "subtitle": "破除算力迷信，讓財務損益語言取代技術虛報，理性跨出轉型第一步",
        "left_badge": "DIAGNOSIS",
        "left_title": "企業 ML 落地前置診斷",
        "left_desc": "• <strong>專家諮詢費用</strong>：<strong>NTD 12,800</strong> (款項可全額折抵後續內訓/工作坊費用)<br>• <strong>交付成果</strong>：企業 ML 與數據預測成熟度雷達圖、Buy vs Build 財務與技術量化評估、台灣五大政府補助最佳匹配路線",
        "right_badge": "RESERVATION",
        "right_title": "專屬健康檢查預約",
        "right_desc": "• <strong>預約方式</strong>：掃描右下角 QR Code (限額預約)<br>• 由首席顧問孟淑慧與策略長陳文家親自研析，5 個工作天內出具 8-12 頁客製化 PDF 診斷報告，築起企業轉型理性護城河"
    }
}


# Clean structured override data for Unit 6 slides to prevent layout metadata leaks and broken visual cards

# Clean structured override data for Unit 5 (RAG) slides to prevent layout metadata leaks and broken visual cards
UNIT5_SLIDE_DATA = {
    1: {
        "layout": "cover",
        "title": "RAG 知識庫採購評估工作坊：避免 NTD 500 萬失敗的 90 分鐘",
        "subtitle": "從傳統 RAG 到 Agentic RAG：精算企業數據資產、IT能力與隱私安全選型",
        "authors": "首席顧問 孟淑慧 ｜ 策略長 陳文家"
    },
    2: {
        "layout": "dual-grid",
        "title": "為什麼 80% 的企業自建 RAG 專案最終死於 POC 階段？",
        "subtitle": "垃圾進，垃圾出 (Garbage in, Garbage out)",
        "left_badge": "FAILURE 1",
        "left_title": "數位化瓶頸",
        "left_desc": "• 掃描 PDF、表格與手寫圖片無法讀取",
        "right_badge": "FAILURE 2 & 3",
        "right_title": "資料未清洗與技術落後",
        "right_desc": "• <strong>資料未清洗</strong>：過期文件與衝突 SOP 污染向量庫<br>• <strong>技術落後</strong>：純關鍵字搜尋無法跨詞語意聯想<br><br><span class='highlight-text'>沒有數據清洗的知識庫，只是昂貴的隨機胡謅機</span>"
    },
    3: {
        "layout": "dual-grid",
        "title": "檢索技術的範式大跨越：傳統 RAG vs. 代理型 Agentic RAG",
        "subtitle": "從死記硬背到具備自我查證能力的法務助理",
        "left_badge": "TRADITIONAL RAG",
        "left_title": "傳統單跳檢索 (讀死書)",
        "left_desc": "• <code>輸入問題</code> ➔ <code>直接向量檢索</code> ➔ <code>直接丟給模型生成</code> ➔ <code>答案</code><br>• <strong>致命傷</strong>：無防護，100% 幻覺風險",
        "right_badge": "AGENTIC RAG",
        "right_title": "多步規劃、自我修正與查證",
        "right_desc": "• <code>輸入問題</code> ➔ <code>意圖過濾</code> ➔ <code>多步搜尋與重排 (Re-rank)</code> ➔ <code>評估 Faithfulness 事實性</code> ➔ <code>自主網絡搜尋補充</code> ➔ <code>安全遮罩回答</code>"
    },
    4: {
        "layout": "triple-grid",
        "title": "RAG 採購起手式：企業數據就緒度 (Data Readiness) 自診",
        "subtitle": "數據清洗三金律 SOP",
        "left_badge": "READABILITY",
        "left_title": "文字與表格可讀性",
        "left_desc": "• <strong>文字可讀性</strong>：TXT/PDF 佔比<br>• <strong>表格複雜度</strong>：多維 Excel/表格 OCR",
        "mid_badge": "CONSISTENCY",
        "mid_title": "版本一致性",
        "mid_desc": "• 廢棄與同名 SOP 佔比（解決知識衝突）",
        "right_badge": "SECURITY",
        "right_title": "權限明晰度",
        "right_desc": "• 機密分級與權限繼承，避免資安外洩"
    },
    5: {
        "layout": "dual-grid",
        "title": "主流工具對決：SaaS 輕量協作 vs 企業級語意搜尋中台",
        "subtitle": "四大主流 RAG 工具技術與財務指標全對照",
        "left_badge": "SAAS COLLABORATION",
        "left_title": "SaaS 輕量款代表",
        "left_desc": "• <strong>代表工具</strong>：Google NotebookLM、Notion AI<br>• <strong>特點</strong>：部署成本極低，適合個人或單一部門內部資料整理，但不具備跨系統權限繼承。",
        "right_badge": "ENTERPRISE SEARCH",
        "right_title": "企業級中台代表",
        "right_desc": "• <strong>代表工具</strong>：商業級 Enterprise Search (如 AWS Kendra)、自建 Enterprise RAG<br>• <strong>特點</strong>：資料隱私權保護強，具備非侵入式系統連接度與 100% 安全存取控制 (ACL) 繼承度。"
    },
    6: {
        "layout": "dual-grid",
        "title": "企業級語意搜尋天花板：非侵入式連接與 ACL 安全防線",
        "subtitle": "企業級語意搜尋的非侵入式連接與 ACL 安全防線",
        "left_badge": "NON-INVASIVE",
        "left_title": "非侵入式 API 連接 (唯讀)",
        "left_desc": "• 直接對接企業內部的異構資料源 (Windows 檔案夾, SAP, SharePoint, Gmail)<br>• 不需搬遷資料，無痛導入。",
        "right_badge": "ACL INHERITANCE",
        "right_title": "100% ACL 權限安全繼承",
        "right_desc": "• 當基層員工與財務長搜尋相同關鍵字，系統實時核驗原始權限。<br>• 基層只能看到公開手冊，財務長能看到機密報表，完全自動化無須重寫權限代碼。"
    },
    7: {
        "layout": "dual-grid",
        "title": "CFO 決策：自建 RAG 還是採購 SaaS？總擁有成本 (TCO) 精算對決",
        "subtitle": "如果您的使用人數少於 500 人，且無極度客製化需求，自建 RAG 就是財務毒瘤",
        "left_badge": "BUY (SAAS)",
        "left_title": "採購 SaaS (以 200人公司為例)",
        "left_desc": "• <strong>訂閱費</strong>：200人 * 30 USD * 12個月 = 72,000 USD (約 230 萬台幣/年)<br>• <strong>開發與運維</strong>：0 元<br>• <strong>年度總 TCO</strong>：230 萬元",
        "right_badge": "BUILD (IN-HOUSE)",
        "right_title": "找工程師自建 RAG",
        "right_desc": "• <strong>薪資</strong>：2人 * 120 萬 = 240 萬元/年<br>• <strong>GPU與API費</strong>：硬體折舊 100萬 + 向量/LLM API 60萬<br>• <strong>MLOps 運維</strong>：50 萬元<br>• <strong>年度總 TCO</strong>：450 萬元！"
    },
    8: {
        "layout": "dual-grid",
        "title": "硬核解密：Corrective RAG (CRAG) 與 Self-RAG 的自我修正路徑",
        "subtitle": "打破「資料庫沒有，AI 就只能瞎編」的死穴",
        "left_badge": "EVALUATOR",
        "left_title": "評估器 (Evaluator) 代理",
        "left_desc": "• <code>輸入 Query</code> ➔ <code>檢索文件</code> ➔ <code>進入 評估器</code><br>• 動態計算文檔與問題的「關聯置信度」。",
        "right_badge": "CORRECTION PATHS",
        "right_title": "三路分流與 Web Search 修正",
        "right_desc": "• <strong>正確</strong> ➔ 餵給生成模型<br>• <strong>錯誤</strong> ➔ 拋棄文件，觸發 <strong>Web Search 網路即時搜尋</strong><br>• <strong>模糊</strong> ➔ 觸發 Query 語意擴展與重排 (Re-rank)"
    },
    9: {
        "layout": "dual-grid",
        "title": "RAG 算力財務精算：Token 通膨與顯示記憶體 (VRAM) 頻寬控管",
        "subtitle": "精算 KV Cache VRAM 與 Embedding 消耗",
        "left_badge": "KV CACHE BOTTLENECK",
        "left_title": "Token 通膨漏斗",
        "left_desc": "• 5 份文件達 20,000 Token，瞬間塞滿 VRAM。<br>• Memory Bandwidth 頻寬耗盡，推理速度從 80t/s 暴跌至 5t/s，API 費用暴增 20 倍。",
        "right_badge": "GQA & CHUNKING",
        "right_title": "防禦方案：GQA 與精細切片",
        "right_desc": "• <strong>Embedding 去重切片 (Chunking)</strong>：使用 Layout-Aware 重疊切割，只送最精確的 200 字。<br>• <strong>GQA 選型</strong>：大模型內建集群查詢注意力，降低長文本推論頻寬消耗 8 倍。"
    },
    10: {
        "layout": "dual-grid",
        "title": "資料安全防禦：防止 RAG 知識庫成為「權限外洩」的特洛伊木馬",
        "subtitle": "RAG 的安全存取控制 (RBAC) 與資料洩漏防護",
        "left_badge": "DATA CASTLE",
        "left_title": "企業機敏數據城堡分區",
        "left_desc": "• <strong>第一防區 (公開)</strong>：員工手冊、SOP 規章 (綠色)<br>• <strong>第四防區 (機密)</strong>：製程專利參數、研發藍圖 (橙色)<br>• <strong>第五防區 (極機密)</strong>：董事會決策、高管薪資 (深紅警戒)",
        "right_badge": "RBAC SHIELD",
        "right_title": "RBAC 安全網閘實時核驗",
        "right_desc": "• 檢索階段實時讀取發問使用者的 AD 數位帳號憑證。<br>• 權限不足的機密文件在向量數據庫檢索時會被<strong>物理過濾、直接隱形</strong>，大腦連看都看不到。"
    },
    11: {
        "layout": "dual-grid",
        "title": "CFO 與法務保命課：大模型與 RAG 採購合約的 5 大防禦條款",
        "subtitle": "絕不讓軟體商拿您的機密去重訓模型",
        "left_badge": "OWNERSHIP & SANDBOX",
        "left_title": "所有權與不落地",
        "left_desc": "• <strong>1. 數據所有權歸屬條款</strong>：所有權 100% 歸屬企業，廠商絕無重訓權利。<br>• <strong>2. 資料不落地承諾</strong>：核心敏感數據嚴禁上傳公用雲端，必須運行於 VPC。",
        "right_badge": "LIABILITY & DESTRUCTION",
        "right_title": "賠償、銷毀與法律責任",
        "right_desc": "• <strong>3. API 變更賠償</strong>：底層模型變更導致失效的懲罰性賠償。<br>• <strong>4. 結案定時數據銷毀</strong>：6 個月內銷毀所有數據並發出公證函。<br>• <strong>5. 法律责任轉嫁</strong>：模型幻覺引發的智財糾紛軟體商需承擔共同責任。"
    },
    12: {
        "layout": "steps",
        "title": "現場實作挑戰一：企業 RAG 採購與數據成熟度 5 維自評",
        "subtitle": "採購評估五步法現場實作",
        "steps": [
            {
                "num": "1",
                "badge": "格式就緒度",
                "text": "評估檔案的掃描件、表格、純文字佔比"
            },
            {
                "num": "2",
                "badge": "權限等級",
                "text": "機密與公開分流及 AD/ACL 連接能力評估"
            },
            {
                "num": "3",
                "badge": "維運能力",
                "text": "檢視 IT 部門是否有能力維運本地 Vector DB / MLOps"
            },
            {
                "num": "4",
                "badge": "預算限制",
                "text": "SaaS 訂閱月費 vs 本地 GPU 採購預算的算力財務評估"
            },
            {
                "num": "5",
                "badge": "場景容錯率",
                "text": "判定業務場景是否需要 CRAG 意圖過濾自我修正"
            }
        ]
    },
    13: {
        "layout": "formulas-and-grid",
        "title": "現場實作挑戰二：RAG 檢索 Faithfulness (事實一致性) 現場測試",
        "subtitle": "設計 RAG 檢索評分矩陣與 Faithfulness 測試",
        "formula": r"\\text{Faithfulness Score} = \\frac{\\text{回答中能從檢索文檔中推導出的事實句數}}{\\text{回答中包含的總事實句數}}",
        "left_badge": "GOLDEN PROMPTS",
        "left_title": "10 筆黃金提問",
        "left_desc": "• 使用跨文檔或表格比對的黃金測試問題，刁難系統。<br>• 驗收不能只靠隨機提問，必須有標準化的 Golden Prompts 檢驗卡。",
        "right_badge": "FAITHFULNESS METRIC",
        "right_title": "大於 0.95 的事實忠實度",
        "right_desc": "• 回答中若包含文檔沒寫的「幻覺」句子，分數瞬間跌破 0.5。<br>• 企業核心知識庫要求 Faithfulness 必須 > 0.95。"
    },
    14: {
        "layout": "dual-grid",
        "title": "數據資產的主動治理：安全防線與雙向機敏保護",
        "subtitle": "B2B 機敏數據安全與雙向 NDA、結案 6 個月銷毀承諾",
        "left_badge": "NDA & ISOLATION",
        "left_title": "雙向 NDA 與地端隔離",
        "left_desc": "• 核心製程數據保證在地端網絡或專屬 VPC 中運行。<br>• 絕不與任何公用大模型共享，對齊 ISO/IEC 42001 與 NIST AI RMF。",
        "right_badge": "MASKING & DESTRUCTION",
        "right_title": "遮罩與 6 個月自動銷毀",
        "right_desc": "• <strong>敏感資料去識別化遮罩網閘</strong>：餵給機器學習前自動隱藏客戶名稱等敏感代號。<br>• <strong>結案 6 個月銷毀承諾</strong>：主動發出確認函並徹底銷毀伺服器上所有的客戶測試數據與模型副本。"
    },
    15: {
        "layout": "dual-grid",
        "title": "邁出理性的第一步：企業 RAG 落地與採購前置快診",
        "subtitle": "預約 NTD 12,800 企業 AI 成熟度快診",
        "left_badge": "DIAGNOSIS DELIVERABLES",
        "left_title": "快診交付成果 (8-12 頁報告)",
        "left_desc": "• 1. 企業數據就緒度與可行性自評雷達圖。<br>• 2. Buy vs. Build 財務 TCO 精算與選型路徑。<br>• 3. 台灣五大政策補助最佳匹配與核銷套利路線規劃。",
        "right_badge": "RESERVATION",
        "right_title": "專家諮詢費用：NTD 12,800",
        "right_desc": "• <strong>全額折抵</strong>：若後續引進工作坊或治理內訓，此快診費用可全額折抵。<br>• <strong>限額預約</strong>：每季僅限 8 家企業，請掃描 QR Code 立即預約。"
    }
}

UNIT6_SLIDE_DATA = {
    1: {
        "layout": "cover",
        "title": "AI Agent 試點安全設計與 MCP 協定工作坊",
        "subtitle": "從玩具聊天室，到企業自主營運代理流：解密 Model Context Protocol (MCP) 協定與非侵入式資安防線",
        "authors": "首席顧問 孟淑慧 ｜ 策略長 陳文家"
    },
    2: {
        "layout": "triple-grid",
        "title": "失控的 AI 代理人三大地雷",
        "subtitle": "80% 的 Agentic 項目為什麼以失敗與安全事故收場？",
        "left_badge": "TOY AGENT",
        "left_title": "玩具死穴",
        "left_desc": "• 將 Agent 當成擺設，缺乏與企業核心 ERP/CRM 數據的安全連通道，無法產生實質損益貢獻",
        "mid_badge": "TCO OVERFLOW",
        "mid_title": "財務逆選擇",
        "mid_desc": "• 模型在 Tool Call 失敗時陷入無限重試的死循環，一夜之間燒乾數萬美元 API 額度",
        "right_badge": "SECURITY HOLE",
        "right_title": "資安浩劫 (Prompt Injection)",
        "right_desc": "• 惡意提問者利用提示詞越獄攻擊，控制 Agent 刪除本地資料庫或透過外部 API 外洩 PII 個資"
    },
    3: {
        "layout": "triple-grid",
        "title": "大模型跨系統連接的插拔革命",
        "subtitle": "劃時代技術：2026 Model Context Protocol (MCP) 上下文協定革命",
        "left_badge": "RESOURCES",
        "left_title": "靜態數據資源 (Resources)",
        "left_desc": "• 標準化靜態數據讀取，允許模型安全地以唯讀方式拉取文件、資料庫快照或本地上下文環境",
        "mid_badge": "TOOLS",
        "mid_title": "動態工具調用 (Tools)",
        "mid_desc": "• 標準化動態代碼與外部函數執行，模型能安全觸發本地 API 調用，並由 Server 物理執行",
        "right_badge": "PROMPTS",
        "right_title": "預設提示範本 (Prompts)",
        "right_desc": "• 標準化預設提示詞模板，提供預先配置好的提示結構，簡化複雜工作流的初始化對齊"
    },
    4: {
        "layout": "steps",
        "title": "MCP 協定地端網路拓撲架構",
        "subtitle": "工具宣告與物理執行分離，防範大模型直接接管伺服器的資安威脅",
        "steps": [
            {
                "num": "1",
                "badge": "宣告可用工具",
                "text": "MCP Server 向 Client (如大模型中台) 宣告可用工具清單與參數 JSON Schema"
            },
            {
                "num": "2",
                "badge": "意圖判定與調用",
                "text": "大模型判定執行意圖，回傳包含 <code>call_tool</code> 指令的標準 JSON 封包"
            },
            {
                "num": "3",
                "badge": "地端物理執行",
                "text": "本地 Server 在安全環境下物理執行代碼，回傳 <code>result</code> 文本，LLM 自身無直接執行權限"
            }
        ]
    },
    5: {
        "layout": "triple-grid",
        "title": "自主代理人開發工具堆疊大對決",
        "subtitle": "主流 AI Agent 5 大框架實測對比（LangGraph 有向有環圖 vs. CrewAI）",
        "left_badge": "LANGGRAPH",
        "left_title": "LangGraph (有向有環圖)",
        "left_desc": "• 開發難度：<strong>極高</strong> (80萬起)<br>• 適用：涉及自我批判、錯誤退件重寫等複雜 State 閉環控制的工業級製程 (鳳凰 AI 首選)",
        "mid_badge": "CREWAI",
        "mid_title": "CrewAI (角色代理人協作)",
        "mid_desc": "• 開發難度：中等<br>• 適用：跨部門流程扮演與多角色協作 (如行銷部多代理人自動文案生成與審查)",
        "right_badge": "DIFY NODES",
        "right_title": "Dify / Low-Code Nodes",
        "right_desc": "• 開發難度：低<br>• 適用：企業快速進行 POC 試點，可視化拖拽組裝，快速驗證商業假設"
    },
    6: {
        "layout": "dual-grid",
        "title": "安全防線一 ｜ 物理沙盒隔離架構",
        "subtitle": "第一道安全關卡：VM / Docker 沙盒物理隔離與權限最小化",
        "left_badge": "DOCKER SANDBOX",
        "left_title": "Docker 物理隔離與無網環境",
        "left_desc": "• 執行 Python 的 Executor 被完全關在物理隔離的 Docker 容器中，且<strong>切斷外網連線</strong>，防止外部數據外洩<br>• 運行 Session 結束後毫秒內物理銷毀容器",
        "right_badge": "READ-ONLY MOUNT",
        "right_title": "唯讀掛載與權限最小化",
        "right_desc": "• 沙盒僅能讀取指定的唯讀 VM 目錄，<strong>嚴禁訪問宿主機根檔案系統</strong><br>• 徹底封鎖 <code>os.system('rm -rf /')</code> 等惡意指令的破壞力"
    },
    7: {
        "layout": "formulas-and-grid",
        "title": "安全防線二 ｜ TCO 財務熔斷控制",
        "subtitle": "第二道安全關卡：Agentic Loop Guard 熔斷機制與 Max Iterations",
        "formula": r"\text{Total Cost} \le \text{Max Cost (\$2.00)} \quad \land \quad \text{Iterations} \le \text{Max Iterations (5)}",
        "left_badge": "LIMITS",
        "left_title": "預算與重試限制",
        "left_desc": "• <strong>Max Iterations = 5</strong>：限制單次任務工具重試上限為 5 次<br>• <strong>Max Cost = US$ 2.00</strong>：單筆對話 API 消耗上限，防止意外死循環耗盡預算",
        "right_badge": "ALERTING",
        "right_title": "熔斷與自動警報",
        "right_desc": "• 觸發熔斷時強制中斷 Session，物理隔離大模型連線<br>• 即時向 Telegram/Slack 運維通道發送 IT 告警通知，啟動人工介入"
    },
    8: {
        "layout": "dual-grid",
        "title": "安全防線三 ｜ 非侵入式唯讀數據防護",
        "subtitle": "第三道安全關卡：既有 ERP/CRM 系統的「非侵入式唯讀副本」串接",
        "left_badge": "PRODUCTION (PROTECTED)",
        "left_title": "生產環境核心庫 (紅色警戒)",
        "left_desc": "• 企業核心 ERP/CRM 系統架構老舊，直接寫入極易引發資料庫死鎖 (Deadlock)<br>• <strong>嚴禁</strong> AI Agent 直接對生產庫進行 <code>INSERT</code> 或 <code>DELETE</code> 操作",
        "right_badge": "REPLICA (READ-ONLY)",
        "right_title": "唯讀副本庫 (Replica)",
        "right_desc": "• 在 DMZ 內為核心庫建立一個即時同步的<strong>「唯讀副本庫」</strong>，AI 的查詢與 RAG 向量比對皆在此執行<br>• 實現零侵入式安全，確保生產環境 100% 完好"
    },
    9: {
        "layout": "formulas-and-grid",
        "title": "安全防線四 ｜ 人類最終問責防護欄 (HITL)",
        "subtitle": "第四道安全關卡：Human-in-the-loop (HITL) 雙簽與熔斷保護欄",
        "formula": r"\text{API Execution} = \text{Agent Draft} \times \text{Human Approval}",
        "left_badge": "AGENT ROLE",
        "left_title": "AI 代理人權限 (起草)",
        "left_desc": "• 僅擁有「產生執行草案 (Draft Proposal)」的權力<br>• AI 負責 99% 的數據搬運與草稿起草，提高行政運作效率",
        "right_badge": "HUMAN ROLE",
        "right_title": "人類主管權限 (最終覆核)",
        "right_desc": "• 地端 API 網閘強制攔截寫入操作，推播至主管手機進行二階段確認<br>• 無主管手動數位簽章，API 閘道 100% 拒絕執行該寫入動作"
    },
    10: {
        "layout": "formulas-and-grid",
        "title": "安全防線五 ｜ 品牌聲調與合規偏好對齊",
        "subtitle": "第五道安全關卡：DPO (直接偏好最佳化) 對位合規性微調與聲調對齊",
        "formula": r"\mathcal{L}_{\text{DPO}}(\theta; \pi_{\text{ref}}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]",
        "left_badge": "TRADITIONAL RLHF",
        "left_title": "傳統偏好對齊 (RLHF)",
        "left_desc": "• 需要訓練額外的獎勵模型 (Reward Model) 與昂貴的人工標註，對中小企業而言開發與算力門檻過高，不切實際",
        "right_badge": "DPO LORA (OPTIMIZED)",
        "right_title": "地端 DPO 輕量微調",
        "right_desc": "• 僅需 300-500 筆企業特有的合規對照數據集 (Preferred vs. Dispreferred)<br>• 在地端進行 LoRA 微調，一鍵對齊品牌聲調與法律紅線"
    },
    11: {
        "layout": "triple-grid",
        "title": "把取代恐懼轉化為加薪激勵的組織學",
        "subtitle": "變革管理：化解員工對「全自動化 Agent」的集體焦慮與抵制",
        "left_badge": "STEP 1",
        "left_title": "第一步：不裁員安心公告",
        "left_desc": "• 老闆簽署書面承諾，宣告專案旨在消除機械式複製貼上工時，不裁減任何同仁，打消被取代的生存恐懼",
        "mid_badge": "STEP 2",
        "mid_title": "第二步：績效與 Agent 綁定",
        "mid_desc": "• 宣佈省下來的工時拿去服務高價值客戶，當月提成與績效加分，將效率提升轉化為員工加薪激勵",
        "right_badge": "STEP 3",
        "right_title": "第三步：定位為最終稽核師",
        "right_desc": "• 將同仁的角色定位為「AI 的最終稽核師 (Validator)」，建立職業尊榮感與最後把關者的責任感"
    },
    12: {
        "layout": "triple-grid",
        "title": "【實作環節 1】規劃您的安全防彈衣 (5 分鐘)",
        "subtitle": "實作環節：使用 A3 畫布現場設計您的第一個 AI Agent 試點安全方案",
        "left_badge": "DIMENSION 1",
        "left_title": "1. 沙盒物理隔離",
        "left_desc": "• 評估您的 Agent 執行環境是否處於 VM 或 Docker 容器中？是否物理切斷外網連線，以防範代碼破壞宿主機？",
        "mid_badge": "DIMENSION 2",
        "mid_title": "2. 數據副本隔離",
        "mid_desc": "• 判定 Agent 調用的資料庫是否為即時同步的唯讀副本 (Read Replica)？是否能物理阻斷直接寫入與刪除操作？",
        "right_badge": "DIMENSION 3",
        "right_title": "3. 主管審核節點",
        "right_desc": "• 盤點哪些高曝險操作 (如大額採購、發送合約) 必須設置 HITL 二階段確認？核准節點綁定在哪個 API 上？"
    },
    13: {
        "layout": "triple-grid",
        "title": "鳳凰 AI 實戰案例 ｜ CodeGraph 代碼索引",
        "subtitle": "實戰案例解密：基於 Tree-sitter 與 SQLite 打造 100% 在地端運作的代碼智能索引系統",
        "left_badge": "AST PARSING",
        "left_title": "Tree-sitter AST 解析",
        "left_desc": "• 在地端解析龐大遺留代碼，精確生成函數調用圖 (Call Graph)<br>• 新進研發人員 Onboarding 速度提升 3 倍",
        "mid_badge": "SQLITE INDEX",
        "mid_title": "SQLite 地端索引",
        "mid_desc": "• 所有代碼結構與索引數據 100% 留在企業內部網路<br>• 拒絕代碼外流雲端，徹底防範代碼產權外洩",
        "right_badge": "DPO ALIGNMENT",
        "right_title": "DPO 寫作規範對齊",
        "right_desc": "• 通過 DPO 微調技術，使 Agent 的回答對齊企業內部的 SQL 與代碼開發規範<br>• 代碼重構崩潰率降至零"
    },
    14: {
        "layout": "dual-grid",
        "title": "保護企業核心資產 ｜ 鳳凰安全承諾",
        "subtitle": "B2B 安全保密雙向 NDA 與六個月內資料徹底銷毀承諾",
        "left_badge": "NDA COMMITMENT",
        "left_title": "保密承諾 1：雙向 NDA",
        "left_desc": "• 合作首日強制簽署受法律管轄之雙向 NDA 協議<br>• 絕不上傳任何未經遮罩之 PII 個資或財務機敏數據至雲端大模型",
        "right_badge": "DESTRUCTION",
        "right_title": "保密承諾 2：資料物理銷毀",
        "right_desc": "• 承諾於可行性快診交付或專案結案後 6 個月內，主動且物理銷毀所有測試用資料庫與代碼庫備份<br>• 捍衛企業技術安全資產"
    },
    15: {
        "layout": "dual-grid",
        "title": "👑 鳳凰 AI：NT$ 12,800 AI 代理人落地可行性前置快診",
        "subtitle": "預約 NT$ 12,800 AI 代理人前置快診與結語",
        "left_badge": "DIAGNOSIS",
        "left_title": "專家前置快診 (NT$ 12,800)",
        "left_desc": "• <strong>安全評估</strong>：產出既有 IT 架構與資安曝險雷達圖<br>• <strong>場景匹配</strong>：篩選出高 ROI、低風險的試點場景<br>• <strong>架構設計</strong>：規劃專屬 Docker 沙盒與 HITL 審核拓撲圖<br>• <strong>補助對接</strong>：精算政府補助計畫對接可能性",
        "right_badge": "RESERVATION",
        "right_title": "專屬健康檢查預約",
        "right_desc": "• <strong>折抵機制</strong>：本次付費快診款項可 100% 全額折抵後續長期陪跑或顧問專案費用<br>• <strong>預約方式</strong>：掃描右下角 QR Code，由顧問團隊親自研析，5 個工作天內出具客製化診斷報告"
    }
}


# Clean structured override data for Unit 8 slides to prevent layout metadata leaks and broken visual cards
UNIT8_SLIDE_DATA = {
    1: {
        "layout": "cover",
        "title": "政府 460 億 AI 補助匹配與合規實戰",
        "subtitle": "不要讓政府撥給您的幾百萬轉型預算，因為資料夾沒放對、發票日期開錯，最終付之一炬",
        "authors": "首席顧問 孟淑慧 ｜ 策略長 陳文家"
    },
    2: {
        "layout": "triple-grid",
        "title": "企業申請政府補助的死亡谷",
        "subtitle": "補助申請的殘酷真實數據：通過率極低，選錯計畫別是致命死穴",
        "left_badge": "PASS RATE",
        "left_title": "12-18%",
        "left_desc": "• 中小企業首次自主申請 AI 研發補助的實質通過率 (SMEA 2026)，存在極高被退件機率",
        "mid_badge": "SUNK COST",
        "mid_title": "NT$ 90 萬",
        "mid_desc": "• 首次申請失敗的平均「沉沒成本」，包含大量計劃書撰寫工時、人事行政摩擦及顧問費",
        "right_badge": "CHANNELS",
        "right_title": "35% 退件因",
        "right_desc": "• 高達 35% 申請案直接死於「選錯計畫別」的定位錯誤，而非計畫書內容或技術實力不足"
    },
    3: {
        "layout": "triple-grid",
        "title": "高階主管必須掌握的政策三軸模型",
        "subtitle": "用「發展軸」的政府無償紅利，為「合規軸」與「競爭軸」的企業安全底座買單",
        "left_badge": "DEVELOPMENT",
        "left_title": "軸 1：發展軸 (政策紅利)",
        "left_desc": "• 政府提供無償資金補助、免費培訓，推動企業導入 AI 技術<br>• <strong>目的</strong>：取得政府無償轉型資金",
        "mid_badge": "COMPLIANCE",
        "mid_title": "軸 2：合規軸 (法律紅線)",
        "mid_desc": "• 規範個資保護與算法偏見（如個資法第 8 條、高額罰鍰）<br>• <strong>目的</strong>：封鎖所有法規與資安曝險",
        "right_badge": "COMPETITION",
        "right_title": "軸 3：競爭軸 (國際逆轉)",
        "right_desc": "• 歐美買家強制要求的 AI 安全與治理認證（如 ISO/IEC 42001）<br>• <strong>目的</strong>：打入國際供應鏈核心"
    },
    4: {
        "layout": "triple-grid",
        "title": "2026 年度經濟部五大補助全景地圖",
        "subtitle": "不同部會、不同計畫別的定位與 AI 核心適用方向對比",
        "left_badge": "SBIR",
        "left_title": "中企署 SBIR 研發",
        "left_desc": "• <strong>額度</strong>：最高 NT$ 100 萬 (S1) / NT$ 500-1,000 萬 (S2)<br>• <strong>適用</strong>：自主研發演算法、瑕疵檢測、客製 RAG 等硬核研發",
        "mid_badge": "SIIR",
        "mid_title": "商業署 SIIR 創新",
        "mid_desc": "• <strong>額度</strong>：單人最高 NT$ 200 萬 / 聯合最高 NT$ 800 萬<br>• <strong>適用</strong>：商業服務模式創新，如 AI 會員行銷推薦、多模態客服",
        "right_badge": "OTHERS",
        "right_title": "智慧機械與培力",
        "right_desc": "• <strong>額度</strong>：智慧機械最高千萬 / 微型培力最高 NT$ 30 萬<br>• <strong>適用</strong>：產發署傳產智慧化、30人以下程序極簡數位培力"
    },
    5: {
        "layout": "triple-grid",
        "title": "SBIR 申報必備的研發本質",
        "subtitle": "嚴密控制會計科目配比，人事費為最大宗支出",
        "left_badge": "STAGE 1",
        "left_title": "可行性評估 (Stage 1)",
        "left_desc": "• <strong>時程</strong>：6 個月，補助最高 NT$ 100 萬<br>• <strong>重點</strong>：驗證演算法可行性與數據就緒度，作為前期技術調研",
        "mid_badge": "STAGE 2",
        "mid_title": "技術開發期 (Stage 2)",
        "mid_desc": "• <strong>時程</strong>：12-24 個月，補助最高 NT$ 1,000 萬<br>• <strong>重點</strong>：完成核心代碼實作、軟硬體整合及產線實地部署",
        "right_badge": "FINANCIALS",
        "right_title": "黃金會計科目佔比",
        "right_desc": "• <strong>人事費</strong>：內部研發人員薪資須佔 50-60%<br>• <strong>委外費</strong>：委託學術界或法人開發之上限為 30%"
    },
    6: {
        "layout": "triple-grid",
        "title": "SIIR 服務業創新 ｜ 讓 AI 改變您的商務模式",
        "subtitle": "強調「商業服務模式創新」而非硬編碼研發，適用連鎖及零售業",
        "left_badge": "SCENARIO 1",
        "left_title": "行銷推薦與客服",
        "left_desc": "• <strong>應用</strong>：AI 智慧會員大數據分析、客戶畫像精準推薦<br>• 多模態語意客服自動分流與回覆系統",
        "mid_badge": "SCENARIO 2",
        "mid_title": "連鎖與零售管理",
        "mid_desc": "• <strong>應用</strong>：AI 連鎖加盟智慧盤點、食材庫存預測推薦<br>• 透過預測降低廢品率與提高週轉率",
        "right_badge": "BUDGET",
        "right_title": "額度與聯合申報",
        "right_desc": "• <strong>額度</strong>：單人申報最高 NT$ 200 萬<br>• <strong>聯合申報</strong>：總部帶領 3 加盟店最高申報 <strong>NT$ 800 萬</strong>"
    },
    7: {
        "layout": "dual-grid",
        "title": "對接 PMC 法人通道的傳產智慧化",
        "subtitle": "專為機械、金屬扣件、手工具等傳產智慧製造升級打造，綠色通道通過率高",
        "left_badge": "FOCUS",
        "left_title": "產發署審查重點與額度",
        "left_desc": "• <strong>重點</strong>：現場智慧化、瑕疵檢測、機台聯網、良率預測<br>• <strong>額度</strong>：單家最高 NT$ 500 萬，聯合申報最高 NT$ 2,000 萬",
        "right_badge": "ADVANTAGE",
        "right_title": "鳳凰 AI 獨家 PMC 綠色通道",
        "right_desc": "• 孟淑慧顧問為 PMC 特許企業 AI 講師，直接對接工研院、PMC 等法人聯合申報<br>• 排除學術行政摩擦，大幅提升通過率"
    },
    8: {
        "layout": "dual-grid",
        "title": "AI 落地必須穿上的法律防彈衣",
        "subtitle": "遵守歐盟監管規範與台灣個資法，封鎖合規與天價罰單風險",
        "left_badge": "EU AI ACT",
        "left_title": "歐盟 AI 法案 (AI Act) 衝擊",
        "left_desc": "• 銷往歐洲的內建 AI 機台必須備妥合規宣告與 AIMS 管理文件<br>• 否則面臨產品遭強制下架及全球年營業額 <strong>3-7%</strong> 的天價罰款",
        "right_badge": "TAIWAN PRIVACY",
        "right_title": "台灣個資法第 8 條告知同意",
        "right_desc": "• AI 客服或推薦系統在蒐集個資前，必須強制跳出個資告知同意書<br>• 未合規實裝告知同意者，最高面臨新台幣 <strong>1,500 萬元</strong> 法人罰鍰"
    },
    9: {
        "layout": "dual-grid",
        "title": "審查委員沒說出口的潛規則 1 ｜ 視覺先行",
        "subtitle": "委員每案平均審閱僅 8-15 分鐘，結論先行與直觀架構是過審關鍵",
        "left_badge": "TRADITIONAL (REJECTED)",
        "left_title": "傳統 IT 報告 (文字堆疊)",
        "left_desc": "• 密密麻麻全是文字，前幾頁寫滿產業分析，缺乏重點<br>• <strong>下場</strong>：委員視覺疲勞，8 分鐘內判定退件",
        "right_badge": "AI-NATIVE (APPROVED)",
        "right_title": "鳳凰 AI 規格 (視覺先行)",
        "right_desc": "• <strong>鐵律</strong>：結論先行，前 3 頁必須備有非技術背景也能看懂的系統架構圖<br>• 直觀引導委員在 10 秒內理解資料流與核心價值"
    },
    10: {
        "layout": "dual-grid",
        "title": "審查委員沒說出口的潛規則 2 ｜ 產學套利",
        "subtitle": "將產學加分指標與企業實質製程排障完美結合",
        "left_badge": "TRADITIONAL ACADEMIC",
        "left_title": "傳統學校產學 (行政冗長)",
        "left_desc": "• 學校需要寫論文、企業要解決製程良率，目標錯位<br>• 智財權與行政流程緩慢，產生長達數月摩擦，耽誤申報",
        "right_badge": "PHOENIX COUPLING",
        "right_title": "教育部副教授通道 (極速簽署)",
        "right_desc": "• 將陳策略長（教育部助理教授）或孟顧問列為外部專家委員<br>• 一週完成合規簽署，拿滿產學加分，交付進度 100% 由鳳凰團隊監管"
    },
    11: {
        "layout": "formulas-and-grid",
        "title": "審查委員沒說出口的潛規則 3 ｜ 80% 安全防護欄",
        "subtitle": "承諾 KPI 必須套用安全係數，確保結案實地審查時全額拿到補助款",
        "formula": r"\text{承諾 KPI} = \text{預期實際值} \times 80\%",
        "left_badge": "RISK (OVERSHOOT)",
        "left_title": "過度吹噓 KPI 的代價",
        "left_desc": "• 申報 99.9% 精準度，結案實測僅 98.5%<br>• <strong>下場</strong>：會計師判定未達標，按比例扣減或追回幾百萬款項",
        "right_badge": "SAFETY (GOLDEN)",
        "right_title": "80% 安全防護欄公式",
        "right_desc": "• 實測 95% 精準度，計畫書僅申報 76%<br>• <strong>結果</strong>：順利過審，結案超標達成，被列為績優企業，更有利於下期申報"
    },
    12: {
        "layout": "steps",
        "title": "步驟三 ｜ 計畫書 7 大核心骨架",
        "subtitle": "將 20 年申報經驗簡化為 7 大骨架公式，讓撰寫時間從 3 個月縮短至 2 週",
        "steps": [
            {
                "num": "1",
                "badge": "人事占比",
                "text": "人事費控制在 50-60% 法定黃金區間，防範行政開會等雜務混入會計審查"
            },
            {
                "num": "2",
                "badge": "量化效益",
                "text": "嚴禁編列「增加營業額 XX 萬」等受市場波動影響的指標，改採技術良率等量化 KPI"
            },
            {
                "num": "3",
                "badge": "公式填空",
                "text": "使用工作表填空公式，將研發、財務、里程碑等數據像填空題一樣快速導入"
            }
        ]
    },
    13: {
        "layout": "triple-grid",
        "title": "扣件製造業 AI 導入計畫書真實範例",
        "subtitle": "將傳產品檢痛點包裝為符合經濟部口味的硬核研發專案",
        "left_badge": "PAIN POINT",
        "left_title": "背景痛點編列",
        "left_desc": "• 35年螺絲廠人工目視漏檢率 2.8%，導致歐美退貨損失 450 萬，強烈建立政府介入的必要性",
        "mid_badge": "INNOVATION",
        "mid_title": "技術研發創新",
        "mid_desc": "• 邊緣運算多模態 AI 瑕疵分類系統，基於 YOLO-v11 與地端 LoRA 微調，拒絕單純軟體採購",
        "right_badge": "BUDGET",
        "right_title": "預算與租稅配比",
        "right_desc": "• 總額 800 萬，人事費 55%，委外高科大 20%，伺服器折舊 15%，申報產創 10-1 抵稅"
    },
    14: {
        "layout": "dual-grid",
        "title": "月度風險追蹤 ｜ 絕不踩線的工時合規管理",
        "subtitle": "審計第一大死穴：打卡紀錄與工時表不吻合。防止因行政疏失導致偽造文書刑事起訴",
        "left_badge": "LEAVE RECORD",
        "left_title": "保命條款 1：請假與工時對位",
        "left_desc": "• 嚴禁請假當天申報研發工時。特休、事病假當天若申報工時，即構成<strong>偽造文書與詐欺取財罪</strong>，面臨刑事起訴",
        "right_badge": "RD LOG",
        "right_title": "保命條款 2：研發日誌具體化",
        "right_desc": "• 日誌必須是具體技術開發描述（如調試 YOLO 濾波特徵）<br>• 嚴禁出現「行政開會、搬東西、寫文案」等行政雜務"
    },
    15: {
        "layout": "triple-grid",
        "title": "會計師進場前 30 天必做的 20 點地毯式自評",
        "subtitle": "月度工作表 5 核心：在主管機關與委託會計師現場實地審查前，進行 100% 自評核銷",
        "left_badge": "FINANCE & HR",
        "left_title": "財務與 HR 科目對位",
        "left_desc": "• 發票品名與規格是否與計劃書 100% 吻合？<br>• 薪資轉帳存摺影本、扣繳憑單與申報人事費完全吻合",
        "mid_badge": "ASSET LABELS",
        "mid_title": "設備標籤與成果展示",
        "mid_desc": "• 購置的地端伺服器已張貼「經濟部補助」金屬財產標籤<br>• Live Demo 現場必須預先錄製「備用展示影片」，防止現場斷網",
        "right_badge": "CLEARANCE",
        "right_title": "結案核銷綠色放行",
        "right_desc": "• 20 點檢核全部 Passed，確保尾款 100% 安全落袋<br>• 防止因行政細節疏漏而被會計師全額追回補助金"
    },
    16: {
        "layout": "triple-grid",
        "title": "【實作環節 2】填寫您專案的計畫書骨架 (5 分鐘)",
        "subtitle": "實作環節：使用電子版【保命工作表 3】填寫您 Quick-Win 專案的創新點與 KPI",
        "left_badge": "INNOVATION",
        "left_title": "1. 技術創新點",
        "left_desc": "• 填寫研發創新描述，聚焦自主代碼、邊緣運算或客製微調，避開純 SaaS 採購雷區",
        "mid_badge": "KPI SHIELD",
        "mid_title": "2. 量化效益 KPI",
        "mid_desc": "• 申報量化效益指標，強制套用 80% 安全防護欄公式，為結案實地稽核留足彈性邊界",
        "right_badge": "BUDGETS",
        "right_title": "3. 預算配比調整",
        "right_desc": "• 講師與顧問現場指導各桌學員調整人事費比例與產學委外經費，確保過審合規性"
    },
    17: {
        "layout": "steps",
        "title": "高段班 CEO 的年度政策套利行事曆",
        "subtitle": "打出跨部會政策組合拳，將同一個 AI 專案進行多層次無償套利，自籌比暴降至 46%",
        "steps": [
            {
                "num": "1",
                "badge": "Q1：研發起步",
                "text": "申報中企署 SBIR Stage 2（獲得 50% 研發資金補助，上限千萬元）"
            },
            {
                "num": "2",
                "badge": "Q2：設備升級",
                "text": "申報產發署智慧機械（取得 Edge 設備與 PLC 折舊補貼最高 500 萬）"
            },
            {
                "num": "3",
                "badge": "Q3：員工賦能",
                "text": "對接勞動部充電起飛計畫（顧問/內訓講師費 100% 政府買單）"
            },
            {
                "num": "4",
                "badge": "Q4：租稅抵減",
                "text": "申報產創條例 10-1（AI 與設備購置費享有 5% 直接抵減營所稅）"
            }
        ]
    },
    18: {
        "layout": "dual-grid",
        "title": "鳳凰 AI：最嚴格的商業機敏安全承諾",
        "subtitle": "B2B 安全保密承諾與 NDA 護城河：保護企業核心專利與財務數據",
        "left_badge": "NDA SIGN",
        "left_title": "保密承諾 1：雙向 NDA",
        "left_desc": "• 合作首日強制簽署受中華民國法律管轄之雙向 NDA 協議<br>• 絕不上傳任何未經遮罩之財務或薪資機敏數據至雲端大模型",
        "right_badge": "DESTRUCTION",
        "right_title": "保密承諾 2：資料物理銷毀",
        "right_desc": "• 計畫結束或快診交付後 6 個月內，物理銷毀企業所有機密備份<br>• 建立影子 AI 防火牆，防範機敏技術洩露風險"
    },
    19: {
        "layout": "steps",
        "title": "免費索取五張補助保命試算表工具包",
        "subtitle": "Notion CRM 與 Google 表單直連，自動分發工具包且保障企業敏感財務隱私",
        "steps": [
            {
                "num": "1",
                "badge": "掃碼登記",
                "text": "學員掃描螢幕 QR Code 填寫登記表單，啟動無人值守後台分發"
            },
            {
                "num": "2",
                "badge": "自動送達",
                "text": "系統在 5 秒內將 Notion 與 Google 試算表母版連結自動寄送至您的信箱"
            },
            {
                "num": "3",
                "badge": "安全副本",
                "text": "學員建立個人副本自行填寫，敏感數據 100% 保存在學員硬碟中，不向我們外洩，完全合規"
            }
        ]
    },
    20: {
        "layout": "dual-grid",
        "title": "鳳凰 AI 陪跑：讓 460 億為您的企業數位轉型買單",
        "subtitle": "預約 NT$ 12,800 專家可行性前置快診與結語",
        "left_badge": "DIAGNOSIS",
        "left_title": "專家前置快診 (NT$ 12,800)",
        "left_desc": "• <strong>評估雷達</strong>：產出企業 AI 成熟度五維度量化雷達圖<br>• <strong>套利路徑</strong>：為貴司規劃專屬補助與租稅套利匹配矩陣<br>• <strong>計畫書素材</strong>：提供 SBIR/SIIR 計畫書骨架與 KPI 防護欄建議",
        "right_badge": "RESERVATION",
        "right_title": "專屬健康檢查預約",
        "right_desc": "• <strong>折抵機制</strong>：本項目付費款項可 100% 全額折抵後續工作坊或陪跑專案費<br>• <strong>預約方式</strong>：掃描 QR Code，顧問團隊親自研析，5 個工作天內出具 8-12 頁客製化診斷報告"
    }
}



def md_to_html(text):
    # Convert bold **text** to <strong>text</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert inline code `code` to <code>code</code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    return text

def parse_markdown_table(text):
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    if len(lines) < 2:
        return ""
    
    # Check if it looks like a markdown table
    if not (lines[0].startswith("|") and lines[0].endswith("|") and lines[1].startswith("|") and lines[1].endswith("|")):
        return ""
        
    html = '<table style="width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 22px; color: var(--color-text-muted); background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.08);">'
    
    # Header
    headers = [c.strip() for c in lines[0].split("|")[1:-1]]
    html += '<thead><tr style="background: rgba(255,91,53,0.1); border-bottom: 2px solid var(--color-brand); color: #FFF; font-family: var(--font-display); font-weight: 700;">'
    for h in headers:
        h_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', h)
        html += f'<th style="padding: 16px 24px; text-align: left; border-right: 1px solid rgba(255,255,255,0.08);">{h_clean}</th>'
    html += '</tr></thead>'
    
    # Body
    html += '<tbody>'
    for r_idx, line in enumerate(lines[2:]):
        cells = [c.strip() for c in line.split("|")[1:-1]]
        bg_style = ' background: rgba(255,255,255,0.01);' if r_idx % 2 == 1 else ''
        html += f'<tr style="border-bottom: 1px solid rgba(255,255,255,0.08);{bg_style}">'
        for c_idx, cell in enumerate(cells):
            cell_html = md_to_html(cell)
            border_right = ' border-right: 1px solid rgba(255,255,255,0.08);' if c_idx < len(cells) - 1 else ''
            cell_style = f'padding: 16px 24px;{border_right}'
            if c_idx == 0:
                cell_style += ' font-weight: 700; color: #FFF;'
            html += f'<td style="{cell_style}">{cell_html}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

layout_kws = [
    "背景色調", "背景", "視覺元素", "排版結構", "版面設計", "版面配置", "中央動態線", 
    "視覺特效", "工作坊風格", "視覺高光", "動態暗示", "圖解對位", "動態箭頭", "夾角弧線", 
    "視覺暗示", "標籤註記", "左下角文字", "流程說明", "圖表內容", "視覺中心", "下方網格", 
    "中央高亮", "左右對比", "左右循環", "視覺架構", "工作坊互動風格", "版面視覺", "專家快診", 
    "專家諮詢", "提示提示", "公式提示", "公式說明", "動畫指引", "動畫/圖表", "背景色", 
    "文字卡片", "中央為", "左下角", "右下角", "右上角", "左上角"
]

def clean_text_heuristics(text):
    sentences = re.split(r'(?<=[。？！])\s*', text)
    filtered = []
    for s in sentences:
        if not s:
            continue
        skip = False
        s_stripped = s.replace("**", "").replace("*", "").strip()
        for kw in layout_kws:
            if s_stripped.startswith(kw) or kw in s_stripped:
                if "「" not in s and "『" not in s and "`" not in s and "$" not in s and "➡️" not in s and "➔" not in s:
                    skip = True
                    break
        if not skip:
            filtered.append(s.strip())
            
    if not filtered and text.strip():
        cleaned = text.strip()
        filtered.append(cleaned)
        
    return filtered

def parse_label_badge_title(label):
    match = re.search(r'^(.*?)\((.*?)\)$', label)
    if match:
        prefix = match.group(1).strip()
        bracket_content = match.group(2).strip()
    else:
        prefix = label.strip()
        bracket_content = ""

    prefix_clean = prefix.replace("**", "").replace("*", "").strip()
    bracket_clean = bracket_content.replace("**", "").replace("*", "").strip()

    layout_indicators = ["左欄", "右欄", "中欄", "左軌", "右軌", "中軌", "左卡片", "右卡片", "中卡片", "左側", "右側", "中側", "左軌道", "右軌道"]
    is_layout_prefix = any(ind in prefix_clean for ind in layout_indicators) or prefix_clean in ["左", "右", "中"]
    
    if is_layout_prefix:
        if bracket_clean:
            title = bracket_clean
            if "左" in prefix_clean:
                badge = "TRADITIONAL" if "ML" in bracket_clean or "傳統" in bracket_clean else "BASE MODEL"
            elif "右" in prefix_clean:
                badge = "MODERN AI" if "AI" in bracket_clean or "DPO" in bracket_clean or "現代" in bracket_clean else "ALIGNED"
            elif "中" in prefix_clean:
                badge = "OPTIMIZED"
            else:
                badge = "ANALYSIS"
        else:
            title = prefix_clean
            badge = "INFO"
    else:
        title = label.replace("**", "").replace("*", "").strip()
        if "玩具" in title or "死穴" in title or "WARNING" in title:
            badge = "WARNING"
        elif "財務" in title:
            badge = "FINANCIAL"
        elif "資安" in title or "安全" in title or "防線" in title:
            badge = "SECURITY"
        elif "對齊" in title:
            badge = "ALIGNMENT"
        elif "推理" in title:
            badge = "INFERENCE"
        elif "插頭" in title:
            badge = "PLUG (CLIENT)"
        elif "插座" in title:
            badge = "SOCKET (SERVER)"
        else:
            badge = ""
                
    return badge, title

def generate_slides_for_unit(unit_folder, unit_badge, unit_full_title, guide_filename="instructor_guide.md", output_subdir=None):
    unit_path = os.path.join(curriculum_dir, unit_folder)
    guide_path = os.path.join(unit_path, guide_filename)
    
    if not os.path.exists(guide_path):
        print(f"Guide file not found: {guide_path}")
        return
    
    with open(guide_path, "r", encoding="utf-8") as f:
        guide_text = f.read()
    
    parts = re.split(r'<!--\s*slide\s*-->', guide_text)
    slide_parts = [p.strip() for p in parts[1:] if p.strip()]
    
    total_pages = len(slide_parts)
    print(f"Unit {unit_folder} ({guide_filename}): Found {total_pages} slides.")
    
    if output_subdir is None:
        UNIT_TO_MODULE_MAP = {
            "unit_0_intro": "m01_ceo_strategy",
            "unit_1_theory": "u1_theory",
            "unit_2_industries": "m06_voice_ai",
            "unit_4_machine_learning": "m04_buy_build_rent",
            "unit_6_generative_ai": "m08_ai_agent_pilot",
            "unit_8_grants": "m12_government_grants"
        }
        output_subdir = UNIT_TO_MODULE_MAP.get(unit_folder, unit_folder)
    target_slides_dir = os.path.join(slides_base_dir, output_subdir)
    
    # Clean up old slides in target folder to avoid legacy duplicates
    if os.path.exists(target_slides_dir):
        print(f"Cleaning up old slide files in {target_slides_dir}...")
        for f in os.listdir(target_slides_dir):
            if f.endswith(".html"):
                try:
                    os.remove(os.path.join(target_slides_dir, f))
                except Exception as e:
                    print(f"  Warning: Could not remove {f} (might be locked by sync): {e}")
    os.makedirs(target_slides_dir, exist_ok=True)

    
    generated_files = []
    segment_names = ["INTRO", "THEORY", "PRACTICE", "SUMMARY"]
    
    for idx, raw_content in enumerate(slide_parts):
        page_num = idx + 1
        
        slide_header_match = re.search(r'^(?:##|###)\s*Slide\s*(\d+)(?:：|｜|:|\|)\s*(.*?)$', raw_content, re.MULTILINE)
        slide_num = str(page_num).zfill(2)
        slide_name = "Slide"
        if slide_header_match:
            slide_name = slide_header_match.group(2).strip()
            
        title_text = ""
        title_match = re.search(r'\*\s*(?:\*\*投影片標題\*\*|\*\*【核心標題】\*\*)[：:]\s*(.*?)$', raw_content, re.MULTILINE)
        if title_match:
            title_text = title_match.group(1).strip()
        else:
            title_block_match = re.search(r'\*\s*(?:\*\*投影片標題\*\*|\*\*【核心標題】\*\*)[：:]\s*\n\s*(.*?)(?=\n\s*\*|\n\s*###|\Z)', raw_content, re.DOTALL | re.MULTILINE)
            if title_block_match:
                title_text = title_block_match.group(1).strip()
                
        if title_text:
            title_text = re.sub(r'^\s*>\s*', '', title_text)
            title_text = re.sub(r'\*\*(.*?)\*\*', r'\1', title_text)
            title_text = re.sub(r'^[「"\'“](.*?)[」"\'”]$', r'\1', title_text)
            slide_main_title = md_to_html(title_text.strip())
        else:
            slide_main_title = md_to_html(slide_name)
            
        subtitle_text = ""
        subtitle_match = re.search(r'\*\s*(?:\*\*副標題\*\*|\*\*【副標題】\*\*)[：:]\s*(.*?)$', raw_content, re.MULTILINE)
        if subtitle_match:
            subtitle_text = subtitle_match.group(1).strip()
        else:
            if page_num == 1:
                content_block_match = re.search(r'\*\s*(?:\*\*視覺設計建議\*\*|\*\*【核心內容】\*\*)[：:]\s*(.*?)(?=\n\s*\*|\n\s*###|\Z)', raw_content, re.DOTALL | re.MULTILINE)
                if content_block_match:
                    c_text = content_block_match.group(1).strip()
                    c_text = re.sub(r'^\s*>\s*', '', c_text)
                    c_text = re.sub(r'\*\*(.*?)\*\*', r'\1', c_text)
                    c_text = re.sub(r'^[「"\'“](.*?)[」"\'”]$', r'\1', c_text)
                    if len(c_text.split("\n")) <= 2:
                        subtitle_text = c_text
                        
        slide_subtitle_html = ""
        if subtitle_text:
            slide_subtitle_html = f'<p class="slide-subtitle">{md_to_html(subtitle_text)}</p>'
            
        body_html = ""
        display_formulas = re.findall(r'\$\$(.*?)\$\$', raw_content, re.DOTALL)
        formulas_html = ""
        if display_formulas:
            formulas_html = '<div class="slide-formulas-box">'
            for f in display_formulas:
                formulas_html += f'<div class="formula-item">$${f.strip()}$$</div>'
            formulas_html += '</div>'
            
        has_core_content = re.search(r'\*\s*(?:\*\*【核心內容】\*\*|\*\*核心內容\*\*)[：:]', raw_content)
        
        extracted_badges = []
        left_col = []
        mid_col = []
        right_col = []
        general_bullets = []
        
        if has_core_content:
            content_match = re.search(r'\*\s*(?:\*\*【核心內容】\*\*|\*\*核心內容\*\*)[：:]\s*\n(.*?)(?=\n\s*\*\s*(?:\*\*|\[|【)(?:【|\[)?(?:主講人|時間|講師|版面|核心|互動|視覺|時間管控)(?:】|\]|\*\*|：|:)?|\n\s*###|\Z)', raw_content, re.DOTALL | re.MULTILINE)
            content_text = content_match.group(1).strip() if content_match else ""
            
            if content_text.startswith("|") and ("|---" in content_text or "| :-" in content_text):
                body_html = parse_markdown_table(content_text)
            else:
                content_lines = [l.strip() for l in content_text.split("\n") if l.strip()]
                raw_bullets = []
                current_bullet_text = ""
                for line in content_lines:
                    line_clean = re.sub(r'^\s*>\s*', '', line).strip()
                    if not line_clean:
                        continue
                    bullet_match = re.match(r'^\s*(?:[*\-+]|\d+\.)\s+(.*?)$', line_clean)
                    if bullet_match:
                        if current_bullet_text:
                            raw_bullets.append(current_bullet_text)
                        current_bullet_text = bullet_match.group(1).strip()
                    else:
                        nested_match = re.match(r'^\s*(?:\*|\-)\s+(.*?)$', line_clean)
                        if nested_match:
                            sub_item = nested_match.group(1).strip()
                            current_bullet_text += f"<br>&nbsp;&nbsp;&nbsp;&nbsp;• {sub_item}"
                        else:
                            current_bullet_text += " " + line_clean
                if current_bullet_text:
                    raw_bullets.append(current_bullet_text)
                    
                if page_num > 1:
                    split_bullets = []
                    for b in raw_bullets:
                        match = re.search(r'^(?:\*\*)?(.*?)(?:\*\*)?\s*(?:：|:|➡️|➔|->|-►|─►)\s*(.*?)$', b)
                        if match:
                            lbl = match.group(1).strip()
                            desc = match.group(2).strip()
                            badge, title = parse_label_badge_title(lbl)
                            split_bullets.append((badge, title, desc))
                        else:
                            split_bullets.append(("", "INFO", b))
                            
                    if len(raw_bullets) == 2:
                        left_col = [(split_bullets[0][0], split_bullets[0][1], split_bullets[0][2])]
                        right_col = [(split_bullets[1][0], split_bullets[1][1], split_bullets[1][2])]
                    elif len(raw_bullets) == 3:
                        left_col = [(split_bullets[0][0], split_bullets[0][1], split_bullets[0][2])]
                        mid_col = [(split_bullets[1][0], split_bullets[1][1], split_bullets[1][2])]
                        right_col = [(split_bullets[2][0], split_bullets[2][1], split_bullets[2][2])]
                    else:
                        for b in split_bullets:
                            general_bullets.append((b[0], b[1], b[2]))
        else:
            visual_block_match = re.search(r'^\*\s*\*\*視覺設計建議\*\*：\s*\n(.*?)(?=###|\Z)', raw_content, re.DOTALL | re.MULTILINE)
            visual_lines = [l.strip() for l in visual_block_match.group(1).split("\n") if l.strip()] if visual_block_match else []
            
            for line in visual_lines:
                clean_line = re.sub(r'^\s*(?:[*\-+]|\d+\.)\s+', '', line).strip()
                if not clean_line:
                    continue
                    
                clean_line_stripped = clean_line.replace("**", "").replace("*", "").strip()
                is_meta = False
                for kw in layout_kws:
                    if clean_line_stripped.startswith(kw):
                        is_meta = True
                        break
                        
                if is_meta:
                    quotes = re.findall(r'「(.*?)」', clean_line)
                    if len(quotes) >= 3:
                        for q in quotes:
                            if q not in ["技術盾牌", "卡片", "半透明", "警告", "安全", "傳統", "微型"]:
                                extracted_badges.append(q)
                    continue
                    
                left_match = re.search(r'^(?:\*\*)?(?:左欄|左軌|左卡片|左軌道|左側)\s*(?:\((.*?)\))?(?:\*\*)?\s*(?:：|:|➡️|➔)?\s*(.*?)$', clean_line)
                mid_match = re.search(r'^(?:\*\*)?(?:中欄|中軌|中卡片|中軌道|中側)\s*(?:\((.*?)\))?(?:\*\*)?\s*(?:：|:|➡️|➔)?\s*(.*?)$', clean_line)
                right_match = re.search(r'^(?:\*\*)?(?:right欄|右欄|右軌|右卡片|右軌道|右側)\s*(?:\((.*?)\))?(?:\*\*)?\s*(?:：|:|➡️|➔)?\s*(.*?)$', clean_line)
                step_match = re.search(r'^(?:\*\*)?(?:步驟|Step)\s*(\d+)\s*(?:\((.*?)\))?(?:\*\*)?\s*(?:➡️|➔|:|：)?\s*(.*?)$', clean_line)
                generic_match = re.search(r'^(?:\*\*)?(.*?)(?:\*\*)?\s*(?:：|:|➡️|➔)\s*(.*?)$', clean_line)
                
                if left_match:
                    lbl = clean_line[:clean_line.find(left_match.group(2))].replace("：","").replace(":","").replace("➡️","").replace("➔","").strip()
                    badge, title = parse_label_badge_title(lbl)
                    items = clean_text_heuristics(left_match.group(2))
                    for item in items:
                        left_col.append((badge, title, item))
                elif mid_match:
                    lbl = clean_line[:clean_line.find(mid_match.group(2))].replace("：","").replace(":","").replace("➡️","").replace("➔","").strip()
                    badge, title = parse_label_badge_title(lbl)
                    items = clean_text_heuristics(mid_match.group(2))
                    for item in items:
                        mid_col.append((badge, title, item))
                elif right_match:
                    lbl = clean_line[:clean_line.find(right_match.group(2))].replace("：","").replace(":","").replace("➡️","").replace("➔","").strip()
                    badge, title = parse_label_badge_title(lbl)
                    items = clean_text_heuristics(right_match.group(2))
                    for item in items:
                        right_col.append((badge, title, item))
                elif step_match:
                    step_num = step_match.group(1)
                    lbl = clean_line[:clean_line.find(step_match.group(3))].replace("：","").replace(":","").replace("➡️","").replace("➔","").strip()
                    badge, title = parse_label_badge_title(lbl)
                    items = clean_text_heuristics(step_match.group(3))
                    for item in items:
                        general_bullets.append((f"step-{step_num}", title, item))
                elif generic_match:
                    lbl = generic_match.group(1)
                    desc = generic_match.group(2)
                    badge, title = parse_label_badge_title(lbl)
                    items = clean_text_heuristics(desc)
                    for item in items:
                        general_bullets.append((badge, title, item))
                else:
                    items = clean_text_heuristics(clean_line)
                    for item in items:
                        general_bullets.append(("bullet", None, item))
                        
        if left_col or right_col or mid_col:
            left_badge = left_col[0][0] if left_col else ""
            left_title = left_col[0][1] if left_col else ""
            left_desc = "<br>• ".join([md_to_html(item[2]) for item in left_col])
            if left_desc:
                left_desc = "• " + left_desc
                
            right_badge = right_col[0][0] if right_col else ""
            right_title = right_col[0][1] if right_col else ""
            right_desc = "<br>• ".join([md_to_html(item[2]) for item in right_col])
            if right_desc:
                right_desc = "• " + right_desc
                
            left_badge_html = f'<span class="card-badge">{left_badge}</span>' if left_badge else ''
            right_badge_html = f'<span class="card-badge">{right_badge}</span>' if right_badge else ''
            
            if mid_col:
                mid_badge = mid_col[0][0]
                mid_title = mid_col[0][1]
                mid_desc = "<br>• ".join([md_to_html(item[2]) for item in mid_col])
                if mid_desc:
                    mid_desc = "• " + mid_desc
                mid_badge_html = f'<span class="card-badge">{mid_badge}</span>' if mid_badge else ''
                
                body_html = f"""
        <div class="triple-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{left_title}</h3>
                <p class="card-content">{left_desc}</p>
            </div>
            <div class="luxury-card mid-card animate-fade delay-2">
                {mid_badge_html}
                <h3 class="card-title">{mid_title}</h3>
                <p class="card-content">{mid_desc}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-3">
                {right_badge_html}
                <h3 class="card-title">{right_title}</h3>
                <p class="card-content">{right_desc}</p>
            </div>
        </div>
"""
            else:
                body_html = f"""
        <div class="dual-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{left_title}</h3>
                <p class="card-content">{left_desc}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-2">
                {right_badge_html}
                <h3 class="card-title">{right_title}</h3>
                <p class="card-content">{right_desc}</p>
            </div>
        </div>
"""
        elif general_bullets:
            is_all_steps = all(b[0].startswith("step-") for b in general_bullets)
            if is_all_steps:
                step_items_html = ""
                for b in general_bullets:
                    step_num = b[0].split("-")[1]
                    step_items_html += f"""
            <div class="step-card animate-fade">
                <div class="step-num">Step {step_num}</div>
                <div class="step-badge">{md_to_html(b[1])}</div>
                <div class="step-text">{md_to_html(b[2])}</div>
            </div>"""
                body_html = f"""
        <div class="steps-container">
            {step_items_html}
        </div>
"""
            elif len(general_bullets) == 2:
                left_badge = general_bullets[0][0] if general_bullets[0][0] != "bullet" else ""
                left_title = general_bullets[0][1] if general_bullets[0][1] else "INFO"
                left_desc = general_bullets[0][2]
                
                right_badge = general_bullets[1][0] if general_bullets[1][0] != "bullet" else ""
                right_title = general_bullets[1][1] if general_bullets[1][1] else "INFO"
                right_desc = general_bullets[1][2]
                
                left_badge_html = f'<span class="card-badge">{left_badge}</span>' if left_badge else ''
                right_badge_html = f'<span class="card-badge">{right_badge}</span>' if right_badge else ''
                
                body_html = f"""
        <div class="dual-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{left_title}</h3>
                <p class="card-content">{md_to_html(left_desc)}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-2">
                {right_badge_html}
                <h3 class="card-title">{right_title}</h3>
                <p class="card-content">{md_to_html(right_desc)}</p>
            </div>
        </div>
"""
            elif len(general_bullets) == 3:
                left_badge = general_bullets[0][0] if general_bullets[0][0] != "bullet" else ""
                left_title = general_bullets[0][1] if general_bullets[0][1] else "INFO"
                left_desc = general_bullets[0][2]
                
                mid_badge = general_bullets[1][0] if general_bullets[1][0] != "bullet" else ""
                mid_title = general_bullets[1][1] if general_bullets[1][1] else "INFO"
                mid_desc = general_bullets[1][2]
                
                right_badge = general_bullets[2][0] if general_bullets[2][0] != "bullet" else ""
                right_title = general_bullets[2][1] if general_bullets[2][1] else "INFO"
                right_desc = general_bullets[2][2]
                
                left_badge_html = f'<span class="card-badge">{left_badge}</span>' if left_badge else ''
                mid_badge_html = f'<span class="card-badge">{mid_badge}</span>' if mid_badge else ''
                right_badge_html = f'<span class="card-badge">{right_badge}</span>' if right_badge else ''
                
                body_html = f"""
        <div class="triple-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{left_title}</h3>
                <p class="card-content">{md_to_html(left_desc)}</p>
            </div>
            <div class="luxury-card mid-card animate-fade delay-2">
                {mid_badge_html}
                <h3 class="card-title">{mid_title}</h3>
                <p class="card-content">{md_to_html(mid_desc)}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-3">
                {right_badge_html}
                <h3 class="card-title">{right_title}</h3>
                <p class="card-content">{md_to_html(right_desc)}</p>
            </div>
        </div>
"""
            else:
                list_items_html = ""
                for b_idx, b in enumerate(general_bullets[:10]):
                    lbl_text = b[1] if b[1] and b[1] != "INFO" else ""
                    content = b[2]
                    if lbl_text:
                        content_html = f"<strong>{lbl_text}</strong>：{content}"
                    else:
                        content_html = content
                    list_items_html += f"""
            <div class="list-item-card animate-fade delay-{b_idx+1}">
                <div class="list-item-bullet">{b_idx+1}</div>
                <div class="list-item-text">{md_to_html(content_html)}</div>
            </div>"""
                body_html = f"""
        <div class="list-container">
            {list_items_html}
        </div>
"""
        elif extracted_badges:
            badges_html = '<div class="badges-grid">'
            for b in extracted_badges:
                badges_html += f'<div class="badge-card">{md_to_html(b)}</div>'
            badges_html += '</div>'
            body_html = badges_html
        elif body_html:
            pass
        else:
            body_html = '<div class="list-container"><div class="list-item-card"><div class="list-item-text">請對照講師備忘錄（按 N 鍵開啟）進行現場教學說明。</div></div></div>'
            
        if formulas_html:
            body_html = formulas_html + body_html
            
        # 5. Parse Speaker Notes (🎤 雙顧問現場輪講逐字手稿 or * **【講師逐字稿】**：)
        notes_text = ""
        notes_match_u6 = re.search(r'\*\s*(?:\*\*【講師逐字稿】\*\*|\*\*講師逐字稿\*\*)[：:]\s*(.*?)(?=\n\s*\*\s*(?:\*\*|\[|【)(?:【|\[)?(?:主講人|時間|講師|版面|核心|互動|視覺|時間管控)(?:】|\]|\*\*|：|:)?|\n\s*###|\Z)', raw_content, re.DOTALL | re.MULTILINE)
        if notes_match_u6:
            notes_text = notes_match_u6.group(1).strip()
        else:
            notes_match_u1 = re.search(r'###\s*🎤\s*(?:雙顧問[現现][場场]輪講逐字(?:手稿|稿)).*?\n(.*)$', raw_content, re.DOTALL | re.MULTILINE)
            if notes_match_u1:
                notes_text = notes_match_u1.group(1).strip()
                
        speaker_notes_html = ""
        if notes_text:
            notes_paragraphs = notes_text.split("\n\n")
            for p in notes_paragraphs:
                p_clean = p.replace("```text", "").replace("```", "").strip()
                p_clean = re.sub(r'^\s*>\s*', '', p_clean)
                if p_clean:
                    p_clean = re.sub(r'^(孟顧問|陳策略長|Meng|Phoenix).*?：', lambda m: f"<strong>{m.group(0)}</strong>", p_clean)
                    p_clean = p_clean.replace("\n", "<br>")
                    p_clean = md_to_html(p_clean)
                    speaker_notes_html += f"<p>{p_clean}</p>"
        else:
            speaker_notes_html = "<p>講授劇本載入中...</p>"
            
        # 6. Build Progress dots html
        active_seg = "INTRO"
        if total_pages == 44:
            if page_num >= 44:
                active_seg = "SUMMARY"
            elif page_num >= 25:
                active_seg = "PRACTICE"
            elif page_num >= 4:
                active_seg = "THEORY"
        elif total_pages == 20:
            if page_num > 18:
                active_seg = "SUMMARY"
            elif page_num > 11:
                active_seg = "PRACTICE"
            elif page_num > 3:
                active_seg = "THEORY"
        elif unit_folder == "unit_2_industries":
            if page_num > 10:
                active_seg = "SUMMARY"
            elif page_num > 6:
                active_seg = "PRACTICE"
            elif page_num > 3:
                active_seg = "THEORY"
        else:
            if page_num > 13:
                active_seg = "SUMMARY"
            elif page_num > 10:
                active_seg = "PRACTICE"
            elif page_num > 3:
                active_seg = "THEORY"
            
        progress_dots_html = '<div class="progress-dots-row">'
        for s_idx, seg in enumerate(segment_names):
            active_cls = "active" if seg == active_seg else ""
            progress_dots_html += f'<div class="progress-dot-segment {active_cls}">{seg}</div>'
            if s_idx < len(segment_names) - 1:
                progress_dots_html += '<div class="progress-dot-connector"></div>'
        progress_dots_html += '</div>'
        

        # 7. Render full slide HTML (Use cover template for page 1)
        slide_data = None
        if unit_folder == "unit_0_intro" and page_num in UNIT0_SLIDE_DATA:
            slide_data = UNIT0_SLIDE_DATA[page_num]
        elif unit_folder == "unit_1_theory" and page_num in UNIT1_SLIDE_DATA:
            slide_data = UNIT1_SLIDE_DATA[page_num]
        elif unit_folder == "unit_2_industries" and unit_badge == "U02 VOICE" and page_num in UNIT2_SLIDE_DATA:
            slide_data = UNIT2_SLIDE_DATA[page_num]
        elif unit_folder == "unit_4_machine_learning" and page_num in UNIT4_SLIDE_DATA:
            slide_data = UNIT4_SLIDE_DATA[page_num]
        elif unit_folder == "unit_2_industries" and unit_badge == "U02 RAG" and page_num in UNIT5_SLIDE_DATA:
            slide_data = UNIT5_SLIDE_DATA[page_num]
        elif unit_folder == "unit_6_generative_ai" and page_num in UNIT6_SLIDE_DATA:
            slide_data = UNIT6_SLIDE_DATA[page_num]
        elif unit_folder == "unit_8_grants" and unit_badge == "U08 GRANTS" and page_num in UNIT8_SLIDE_DATA:
            slide_data = UNIT8_SLIDE_DATA[page_num]

        if slide_data:
            slide_main_title = slide_data["title"]
            if slide_data.get("subtitle"):
                slide_subtitle_html = f'<p class="slide-subtitle">{slide_data["subtitle"]}</p>'
            else:
                slide_subtitle_html = ""
            
            # Generate body_html based on layout
            layout = slide_data["layout"]
            if layout == "cover":
                pass
            elif layout == "dual-grid":
                left_badge_html = f'<span class="card-badge">{slide_data["left_badge"]}</span>' if slide_data.get("left_badge") else ''
                right_badge_html = f'<span class="card-badge">{slide_data["right_badge"]}</span>' if slide_data.get("right_badge") else ''
                body_html = f"""
        <div class="dual-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{slide_data["left_title"]}</h3>
                <p class="card-content">{slide_data["left_desc"]}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-2">
                {right_badge_html}
                <h3 class="card-title">{slide_data["right_title"]}</h3>
                <p class="card-content">{slide_data["right_desc"]}</p>
            </div>
        </div>
"""
            elif layout == "formulas-and-badges":
                body_html = f"""
        <div class="slide-formulas-box">
            <div class="formula-item">$${slide_data["formula"]}$$</div>
        </div>
        <div class="badges-grid">
"""
                for badge in slide_data["badges"]:
                    body_html += f'            <div class="badge-card">{badge}</div>\n'
                body_html += "        </div>"
                
            elif layout == "formulas-and-grid":
                left_badge_html = f'<span class="card-badge">{slide_data["left_badge"]}</span>' if slide_data.get("left_badge") else ''
                right_badge_html = f'<span class="card-badge">{slide_data["right_badge"]}</span>' if slide_data.get("right_badge") else ''
                body_html = f"""
        <div class="slide-formulas-box">
            <div class="formula-item">$${slide_data["formula"]}$$</div>
        </div>
        <div class="dual-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{slide_data["left_title"]}</h3>
                <p class="card-content">{slide_data["left_desc"]}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-2">
                {right_badge_html}
                <h3 class="card-title">{slide_data["right_title"]}</h3>
                <p class="card-content">{slide_data["right_desc"]}</p>
            </div>
        </div>
"""
            elif layout == "formulas-and-triple-grid":
                left_badge_html = f'<span class="card-badge">{slide_data["left_badge"]}</span>' if slide_data.get("left_badge") else ''
                mid_badge_html = f'<span class="card-badge">{slide_data["mid_badge"]}</span>' if slide_data.get("mid_badge") else ''
                right_badge_html = f'<span class="card-badge">{slide_data["right_badge"]}</span>' if slide_data.get("right_badge") else ''
                body_html = f"""
        <div class="slide-formulas-box">
            <div class="formula-item">$${slide_data["formula"]}$$</div>
        </div>
        <div class="triple-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{slide_data["left_title"]}</h3>
                <p class="card-content">{slide_data["left_desc"]}</p>
            </div>
            <div class="luxury-card mid-card animate-fade delay-2">
                {mid_badge_html}
                <h3 class="card-title">{slide_data["mid_title"]}</h3>
                <p class="card-content">{slide_data["mid_desc"]}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-3">
                {right_badge_html}
                <h3 class="card-title">{slide_data["right_title"]}</h3>
                <p class="card-content">{slide_data["right_desc"]}</p>
            </div>
        </div>
"""
            elif layout == "triple-grid":
                left_badge_html = f'<span class="card-badge">{slide_data["left_badge"]}</span>' if slide_data.get("left_badge") else ''
                mid_badge_html = f'<span class="card-badge">{slide_data["mid_badge"]}</span>' if slide_data.get("mid_badge") else ''
                right_badge_html = f'<span class="card-badge">{slide_data["right_badge"]}</span>' if slide_data.get("right_badge") else ''
                body_html = f"""
        <div class="triple-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{slide_data["left_title"]}</h3>
                <p class="card-content">{slide_data["left_desc"]}</p>
            </div>
            <div class="luxury-card mid-card animate-fade delay-2">
                {mid_badge_html}
                <h3 class="card-title">{slide_data["mid_title"]}</h3>
                <p class="card-content">{slide_data["mid_desc"]}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-3">
                {right_badge_html}
                <h3 class="card-title">{slide_data["right_title"]}</h3>
                <p class="card-content">{slide_data["right_desc"]}</p>
            </div>
        </div>
"""
            elif layout == "dual-grid-split":
                left_badge_html = f'<span class="card-badge">{slide_data["left_badge"]}</span>' if slide_data.get("left_badge") else ''
                right_badge_html = f'<span class="card-badge">{slide_data["right_badge"]}</span>' if slide_data.get("right_badge") else ''
                body_html = f"""
        <div class="dual-grid">
            <div class="luxury-card left-card animate-fade delay-1">
                {left_badge_html}
                <h3 class="card-title">{slide_data["left_title"]}</h3>
                <p class="card-content">{slide_data["left_desc"]}</p>
            </div>
            <div class="luxury-card right-card animate-fade delay-2">
                {right_badge_html}
                <h3 class="card-title">{slide_data["right_title"]}</h3>
                <p class="card-content">{slide_data["right_desc"]}</p>
            </div>
        </div>
"""
            elif layout == "steps":
                step_items_html = ""
                for s in slide_data["steps"]:
                    step_items_html += f"""
            <div class="step-card animate-fade">
                <div class="step-num">Step {s["num"]}</div>
                <div class="step-badge">{s["badge"]}</div>
                <div class="step-text">{s["text"]}</div>
            </div>"""
                body_html = f"""
        <div class="steps-container">
            {step_items_html}
        </div>
"""

        # 7. Render full slide HTML (Use cover template for page 1)
        if page_num == 1:
            slide_html = HTML_COVER_TEMPLATE.format(
                slide_title=slide_name,
                slide_main_title=slide_main_title,
                slide_subtitle=slide_data["subtitle"] if slide_data else (subtitle_text or slide_name),
                speaker_notes_html=speaker_notes_html
            )

        else:
            slide_html = HTML_SLIDE_TEMPLATE.format(
                slide_title=slide_name,
                unit_badge=unit_badge,
                unit_full_title=unit_full_title,
                progress_dots_html=progress_dots_html,
                slide_main_title=slide_main_title,
                slide_subtitle_html=slide_subtitle_html,
                slide_body_content_html=body_html,
                page_num=page_num,
                total_pages=total_pages,
                speaker_notes_html=speaker_notes_html
            )
            
        slide_filename = f"{slide_num}-slide.html" if page_num > 1 else "01-cover.html"
        slide_out_path = os.path.join(target_slides_dir, slide_filename)
        
        with open(slide_out_path, "w", encoding="utf-8") as out_f:
            out_f.write(slide_html)
            
        generated_files.append(slide_filename)
        
    # 8. Render player index.html
    slides_json = json.dumps(generated_files)
    player_html = HTML_PLAYER_TEMPLATE.format(
        unit_full_title=unit_full_title,
        total_pages=total_pages,
        slides_json=slides_json
    )
    player_out_path = os.path.join(target_slides_dir, "index.html")
    with open(player_out_path, "w", encoding="utf-8") as out_p:
        out_p.write(player_html)
        
    print(f"Generated slide deck for {unit_folder} in slides/{output_subdir}/")



# Generate slides for all textbook units and playbooks
units_to_generate = [
    ("unit_0_intro", "U00 INTRO", "單元零：CEO 90 分鐘 AI 戰略速覽", "instructor_guide.md", "m01_ceo_strategy"),
    ("unit_1_theory", "U01 THEORY", "單元一：AI 基礎理論與 2026 技術演進", "instructor_guide.md", "u1_theory"),
    ("unit_2_industries", "U02 RAG", "單元二：RAG 知識庫採購評估工作坊", "README_M05_RAG.md", "m05_rag_procurement"),
    ("unit_2_industries", "U02 VOICE", "單元二：Voice AI 傳產落地唯一破口工作坊", "instructor_guide.md", "m06_voice_ai"),
    ("unit_2_industries", "U02 VIDEO", "單元二：行銷部影片生成與合規防線工作坊", "README_M07_Video.md", "m07_video_generation"),
    ("unit_3_responsible_ai", "U03 RESPONSIBLE AI", "單元三：全員員工 AI 安全守則與合規治理", "instructor_guide.md", "m02_employee_policy"),
    ("unit_4_machine_learning", "U04 MACHINE LEARNING", "單元四：機器學習技術理論與實務案例", "instructor_guide.md", "m04_buy_build_rent"),
    ("unit_5_explainable_ai", "U05 EXPLAINABLE AI", "單元五：ISO/IEC 42001 認證前期差距研習與 XAI 審計", "instructor_guide.md", "m11_iso42001_workshop"),
    ("unit_6_generative_ai", "U06 GENERATIVE AI", "單元六：生成式 AI 與 Agentic 深度實務", "instructor_guide.md", "m08_ai_agent_pilot"),
    ("unit_7_strategy", "U07 STRATEGY", "單元七：企業 AI 4+1 戰略畫布工作坊", "instructor_guide.md", "m03_strategic_canvas"),
    ("unit_7_strategy", "U07 TCO", "單元七：TCO 成本失控與 Token 網閘防護工作坊", "README_M09_TCO.md", "m09_tco_control"),
    ("unit_7_strategy", "U07 CHANGE", "單元七：消除員工取代恐懼之變革 5 部曲工作坊", "README_M10_Change.md", "m10_change_management"),
    ("unit_8_grants", "U08 GRANTS", "單元八：產發署與經濟部政府補助對接指南", "instructor_guide.md", "m12_government_grants"),
    ("unit_8_grants", "U08 AI ACT", "單元八：歐盟 AI Act 出口合規與 CE 標章工作坊", "README_M13_AIAct.md", "m13_eu_ai_act")
]

for folder, badge, title, filename, output_dir in units_to_generate:
    print(f"--- Generating slides for {folder} ({filename}) ---")
    generate_slides_for_unit(folder, badge, title, filename, output_dir)

print("\nAll unit slides generation complete!")
