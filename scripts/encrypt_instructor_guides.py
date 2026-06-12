# -*- coding: utf-8 -*-
"""
encrypt_instructor_guides.py — 加密所有單元的講師手稿 (instructor_guide.md)
並生成密碼保護的 instructor_guide.html 網頁
========================================================================
[Confidential - Phoenix AI Internal Asset]
"""

import os
import sys
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Ensure UTF-8 output
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# Define default credentials
DEFAULT_USER = "phoenix_advisor"
DEFAULT_PASS = "phoenix_ai_2026"

# Derive AES-256 key from default credentials
key_material = f"{DEFAULT_USER}:{DEFAULT_PASS}".encode("utf-8")
AES_KEY = hashlib.sha256(key_material).digest()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} ｜ 講師幕後手冊</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.1.1/crypto-js.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <style>
        :root {{
            --bg-color: #070913;
            --primary-accent: #FF5B35;
            --secondary-accent: #00F2FE;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --glass-bg: rgba(255, 255, 255, 0.02);
            --glass-border: rgba(255, 255, 255, 0.1);
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-body);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow-x: hidden;
            position: relative;
        }}
        .grid-bg {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.01) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.01) 1px, transparent 1px);
            background-size: 80px 80px;
            z-index: 1;
        }}
        .glow-radial {{
            position: fixed;
            top: 50%; left: 50%;
            width: 800px; height: 800px;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.04) 0%, rgba(255, 91, 53, 0.02) 60%, transparent 100%);
            filter: blur(100px);
            z-index: 2;
            transform: translate(-50%, -50%);
            pointer-events: none;
        }}
        
        /* Login Box Styles */
        .login-container {{
            position: relative;
            z-index: 10;
            width: 440px;
            background: rgba(15, 23, 42, 0.65);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 40px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            display: block;
        }}
        .login-header {{
            text-align: center;
            margin-bottom: 35px;
        }}
        .login-logo {{
            font-family: var(--font-display);
            font-size: 32px;
            font-weight: 800;
            letter-spacing: 0.1em;
            background: linear-gradient(135deg, #FFF, var(--secondary-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
        }}
        .login-subtitle {{
            font-size: 14px;
            color: var(--text-muted);
            letter-spacing: 0.05em;
        }}
        .input-group {{
            margin-bottom: 20px;
            position: relative;
        }}
        .input-label {{
            display: block;
            font-size: 13px;
            font-weight: 600;
            color: var(--text-muted);
            margin-bottom: 8px;
            letter-spacing: 0.05em;
        }}
        .input-field {{
            width: 100%;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 14px 18px;
            font-family: var(--font-body);
            font-size: 15px;
            color: #FFF;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        .input-field:focus {{
            outline: none;
            border-color: var(--secondary-accent);
            background: rgba(0, 242, 254, 0.02);
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.1);
        }}
        .login-btn {{
            width: 100%;
            background: linear-gradient(135deg, var(--primary-accent), #FF8A00);
            border: none;
            border-radius: 12px;
            padding: 14px;
            font-family: var(--font-display);
            font-size: 16px;
            font-weight: 700;
            color: #FFF;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            margin-top: 10px;
            box-shadow: 0 4px 20px rgba(255, 91, 53, 0.2);
        }}
        .login-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(255, 91, 53, 0.35);
        }}
        .login-btn:active {{
            transform: translateY(0);
        }}
        .error-msg {{
            color: #EF4444;
            font-size: 13.5px;
            font-weight: 500;
            text-align: center;
            margin-top: 15px;
            display: none;
        }}
        
        /* Content Panel Styles */
        .content-container {{
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 1000px;
            padding: 60px 40px;
            display: none;
        }}
        .content-header {{
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 30px;
            margin-bottom: 40px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
        }}
        .content-title {{
            font-family: var(--font-display);
            font-size: 38px;
            font-weight: 800;
            background: linear-gradient(135deg, #FFF, #E2E8F0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .logout-btn {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            color: var(--text-muted);
            padding: 8px 16px;
            border-radius: 8px;
            font-family: var(--font-display);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .logout-btn:hover {{
            background: rgba(239, 68, 68, 0.1);
            border-color: rgba(239, 68, 68, 0.3);
            color: #EF4444;
        }}
        
        /* Premium Markdown Styles */
        .markdown-body {{
            line-height: 1.8;
            font-size: 17px;
            color: #E2E8F0;
        }}
        .markdown-body h1 {{
            font-family: var(--font-display);
            font-size: 32px;
            margin-bottom: 25px;
            color: #FFF;
        }}
        .markdown-body h2 {{
            font-family: var(--font-display);
            font-size: 26px;
            font-weight: 700;
            color: var(--secondary-accent);
            margin: 40px 0 20px 0;
            padding-bottom: 8px;
            border-bottom: 1px dashed rgba(255, 255, 255, 0.1);
        }}
        .markdown-body h3 {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 700;
            color: var(--primary-accent);
            margin: 30px 0 15px 0;
        }}
        .markdown-body p {{
            margin-bottom: 20px;
        }}
        .markdown-body ul, .markdown-body ol {{
            margin: 0 0 20px 25px;
        }}
        .markdown-body li {{
            margin-bottom: 8px;
        }}
        .markdown-body blockquote {{
            background: rgba(255, 255, 255, 0.015);
            border-left: 4px solid var(--secondary-accent);
            padding: 16px 24px;
            border-radius: 0 12px 12px 0;
            margin: 20px 0;
            color: #F8FAFC;
        }}
        .markdown-body blockquote strong {{
            color: var(--primary-accent);
        }}
        .markdown-body code {{
            background: rgba(255, 255, 255, 0.05);
            padding: 3px 6px;
            border-radius: 4px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 15px;
        }}
        .markdown-body pre {{
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid var(--glass-border);
            padding: 24px;
            border-radius: 12px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        .markdown-body pre code {{
            background: none;
            padding: 0;
            font-size: 14.5px;
            line-height: 1.6;
            color: #CBD5E1;
        }}
        .markdown-body table {{
            width: 100%;
            border-collapse: collapse;
            margin: 25px 0;
        }}
        .markdown-body th, .markdown-body td {{
            border: 1px solid var(--glass-border);
            padding: 14px 18px;
            text-align: left;
        }}
        .markdown-body th {{
            background: rgba(255, 255, 255, 0.03);
            font-family: var(--font-display);
            font-weight: 700;
            color: #FFF;
        }}
        .markdown-body tr:nth-child(even) {{
            background: rgba(255, 255, 255, 0.01);
        }}
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="glow-radial"></div>

    <!-- Login Form -->
    <div class="login-container" id="loginBox">
        <div class="login-header">
            <h1 class="login-logo">PHOENIX AI</h1>
            <p class="login-subtitle">講師幕後手冊安全防護網</p>
        </div>
        <div class="input-group">
            <label class="input-label" for="username">ADVISOR USERNAME</label>
            <input class="input-field" type="text" id="username" placeholder="請輸入顧問帳號" autocomplete="off">
        </div>
        <div class="input-group">
            <label class="input-label" for="password">ACCESS PASSWORD</label>
            <input class="input-field" type="password" id="password" placeholder="請輸入訪問密碼">
        </div>
        <button class="login-btn" onclick="handleLogin()">驗證並進入</button>
        <div class="error-msg" id="errorMsg">帳號或密碼錯誤！</div>
    </div>

    <!-- Main Content -->
    <div class="content-container" id="contentBox">
        <div class="content-header">
            <div>
                <h1 class="content-title">{title} 講師手稿</h1>
            </div>
            <button class="logout-btn" onclick="handleLogout()">登出手冊</button>
        </div>
        <div class="markdown-body" id="markdownContent"></div>
    </div>

    <script>
        const ciphertextB64 = "{ciphertext}";
        const ivHex = "{iv}";

        // Check for active session
        window.addEventListener('DOMContentLoaded', () => {{
            const savedKey = sessionStorage.getItem('phoenix_advisor_key');
            if (savedKey) {{
                if (decryptAndRender(savedKey)) {{
                    return;
                }}
                sessionStorage.removeItem('phoenix_advisor_key');
            }}
        }});

        function handleLogin() {{
            const user = document.getElementById('username').value.trim();
            const pass = document.getElementById('password').value.trim();
            
            if (!user || !pass) {{
                showError("帳號與密碼皆為必填！");
                return;
            }}

            const keyMaterial = user + ":" + pass;
            const keyHex = CryptoJS.SHA256(keyMaterial).toString();

            if (decryptAndRender(keyHex)) {{
                // Save session key
                sessionStorage.setItem('phoenix_advisor_key', keyHex);
            }} else {{
                showError("認證失敗！請確認您的顧問帳號與密碼是否正確。");
            }}
        }}

        function decryptAndRender(keyHex) {{
            try {{
                const keyBytes = CryptoJS.enc.Hex.parse(keyHex);
                const ivBytes = CryptoJS.enc.Hex.parse(ivHex);
                
                const decrypted = CryptoJS.AES.decrypt(
                    ciphertextB64,
                    keyBytes,
                    {{
                        iv: ivBytes,
                        mode: CryptoJS.mode.CBC,
                        padding: CryptoJS.pad.Pkcs7
                    }}
                );

                const plaintext = decrypted.toString(CryptoJS.enc.Utf8);
                if (plaintext && (plaintext.startsWith('# ') || plaintext.includes('Slide') || plaintext.includes('##'))) {{
                    // Render content
                    document.getElementById('loginBox').style.display = 'none';
                    document.getElementById('contentBox').style.display = 'block';
                    document.body.style.alignItems = 'flex-start'; // Allow natural scrolling
                    
                    // Render Markdown
                    document.getElementById('markdownContent').innerHTML = marked.parse(plaintext);
                    return true;
                }}
            }} catch (e) {{
                console.error("Decryption exception:", e);
            }}
            return false;
        }}

        function handleLogout() {{
            sessionStorage.removeItem('phoenix_advisor_key');
            location.reload();
        }}

        function showError(msg) {{
            const errorDiv = document.getElementById('errorMsg');
            errorDiv.innerHTML = msg;
            errorDiv.style.display = 'block';
            
            // Add error wiggle effect
            const loginBox = document.getElementById('loginBox');
            loginBox.style.animation = 'none';
            loginBox.offsetHeight; // Trigger reflow
            loginBox.style.animation = 'wiggle 0.3s ease-in-out';
        }}
    </script>
    <style>
        @keyframes wiggle {{
            0%, 100% {{ transform: translateX(0); }}
            25% {{ transform: translateX(-6px); }}
            75% {{ transform: translateX(6px); }}
        }}
    </style>
</body>
</html>
"""

def encrypt_guide(md_path, html_path):
    print(f"正在加密: {md_path}")
    with open(md_path, "r", encoding="utf-8") as f:
        plaintext = f.read()

    # Generate random IV (16 bytes)
    iv = os.urandom(16)
    
    # Pad plaintext using PKCS7
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode("utf-8")) + padder.finalize()
    
    # Encrypt using AES CBC
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Encode to Base64
    ciphertext_b64 = base64.b64encode(ciphertext).decode("utf-8")
    iv_hex = iv.hex()
    
    # Extract clean title from md_path
    dir_name = os.path.basename(os.path.dirname(md_path))
    # Parse title from folder name
    unit_map = {
        "unit_0_intro": "單元零 ｜ 高階主管 AI 落地速覽",
        "unit_1_theory": "單元一 ｜ AI 基礎理論與 2026 技術演進",
        "unit_2_industries": "單元二 ｜ 2026 企業級 AI 應用 7 大實戰模組",
        "unit_3_responsible_ai": "單元三 ｜ 負責任的 AI 應用 (Responsible AI)",
        "unit_4_machine_learning": "單元四 ｜ 中型企業機器學習實戰應用",
        "unit_5_explainable_ai": "單元五 ｜ AI 可解釋性與信任度評估",
        "unit_6_generative_ai": "單元六 ｜ 生成式 AI 與多代理人系統",
        "unit_7_strategy": "單元七 ｜ 企業 AI 導入、治理與營運策略",
        "unit_8_grants": "單元八 ｜ AI 與台灣產業政策對接"
    }
    title = unit_map.get(dir_name, "鳳凰 AI 講師手稿")
    
    # Format HTML
    html_content = HTML_TEMPLATE.format(
        title=title,
        ciphertext=ciphertext_b64,
        iv=iv_hex
    )
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"成功生成保護網頁: {html_path}")

def main():
    curriculum_dir = "curriculum"
    if not os.path.exists(curriculum_dir):
        print(f"找不到 {curriculum_dir} 目錄，請在專案根目錄執行此腳本。")
        sys.exit(1)
        
    guides_processed = 0
    for root, dirs, files in os.walk(curriculum_dir):
        for file in files:
            if file == "instructor_guide.md":
                md_path = os.path.join(root, file)
                html_path = os.path.join(root, "instructor_guide.html")
                encrypt_guide(md_path, html_path)
                guides_processed += 1
                
    print(f"加密任務完成！共處理 {guides_processed} 個單元手稿。")

if __name__ == "__main__":
    main()
