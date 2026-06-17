# -*- coding: utf-8 -*-
import os
import re
import json

def parse_front_matter(content):
    """
    Robust, dependency-free YAML front matter parser.
    Supports single keys and list keys (like pain_points, solutions, roi).
    """
    if not content.startswith("---"):
        return {}, content
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
        
    yaml_text = parts[1]
    body_text = parts[2].strip()
    
    metadata = {}
    lines = yaml_text.strip().split("\n")
    current_key = None
    current_list = []
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # If it's a list item under a key
        if line_stripped.startswith("-") and current_key:
            val = line_stripped[1:].strip()
            # Strip quotes if any
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            current_list.append(val)
            metadata[current_key] = current_list
            continue
            
        if ":" in line:
            # We found a key-value or key-list start
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            
            # Reset list collector
            current_list = []
            current_key = key
            
            if val:
                # Value is on the same line, e.g., title: Hello
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                metadata[key] = val
                current_key = None # Single value key
            else:
                # Value is empty, it's a list start
                metadata[key] = []
                current_list = metadata[key]
                
    return metadata, body_text

def compile_cases():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    markdown_dir = os.path.join(base_dir, "cases", "markdown")
    html_dir = os.path.join(base_dir, "cases", "html")
    json_path = os.path.join(base_dir, "cases", "cases.json")
    
    # Ensure directories exist
    os.makedirs(html_dir, exist_ok=True)
    
    if not os.path.exists(markdown_dir):
        print(f"Error: Markdown directory {markdown_dir} does not exist.")
        return
        
    cases_metadata = []
    md_files = [f for f in os.listdir(markdown_dir) if f.endswith(".md")]
    
    # Sort files to maintain consistent ordering
    md_files.sort()
    
    html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} ｜ 鳳凰 AI 企業案例庫</title>
    <!-- Premium Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800&family=Noto+Sans+TC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <!-- MathJax for rendering LaTeX formulas -->
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <!-- Marked.js Markdown Parser -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <!-- Mermaid.js for Diagrams -->
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        :root {{
            --bg-color: #070913;
            --primary-accent: #FF5B35;    /* Phoenix Orange */
            --secondary-accent: #00F2FE;  /* Vibrant Cyan */
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
            --glass-bg: rgba(255, 255, 255, 0.02);
            --glass-border: rgba(255, 255, 255, 0.08);
            --font-display: 'Outfit', 'Noto Sans TC', sans-serif;
            --font-body: 'Inter', 'Noto Sans TC', sans-serif;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-color);
            color: var(--text-main);
            font-family: var(--font-body);
            min-height: 100vh;
            overflow-x: hidden;
            position: relative;
            padding: 60px 20px;
            display: flex;
            justify-content: center;
        }}
        .grid-bg {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.01) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.01) 1px, transparent 1px);
            background-size: 80px 80px;
            z-index: 1;
            pointer-events: none;
        }}
        .glow-radial {{
            position: fixed;
            top: 50%; left: 50%;
            width: 900px; height: 900px;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.03) 0%, rgba(255, 91, 53, 0.015) 60%, transparent 100%);
            filter: blur(120px);
            z-index: 2;
            transform: translate(-50%, -50%);
            pointer-events: none;
        }}
        .container {{
            position: relative;
            z-index: 10;
            width: 100%;
            max-width: 1000px;
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 50px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.5);
        }}
        .back-link {{
            display: inline-flex;
            align-items: center;
            color: var(--secondary-accent);
            text-decoration: none;
            font-size: 15px;
            font-weight: 500;
            margin-bottom: 25px;
            transition: all 0.3s ease;
            gap: 8px;
        }}
        .back-link:hover {{
            color: var(--primary-accent);
            transform: translateX(-4px);
        }}
        .header-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 25px;
            margin-bottom: 40px;
        }}
        .logo-txt {{
            font-family: var(--font-display);
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.05em;
            background: linear-gradient(135deg, #FFF, var(--secondary-accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .badge {{
            background: rgba(255, 91, 53, 0.1);
            border: 1px solid rgba(255, 91, 53, 0.3);
            color: var(--primary-accent);
            font-size: 13px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 30px;
            letter-spacing: 0.5px;
        }}
        .markdown-body {{
            line-height: 1.8;
            font-size: 16px;
            color: #E2E8F0;
        }}
        .markdown-body h1 {{
            font-family: var(--font-display);
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 25px;
            background: linear-gradient(135deg, #FFF, #94A3B8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 15px;
        }}
        .markdown-body h2 {{
            font-family: var(--font-display);
            font-size: 22px;
            font-weight: 700;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #FFF;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .markdown-body h3 {{
            font-family: var(--font-display);
            font-size: 18px;
            font-weight: 600;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #FFF;
        }}
        .markdown-body p {{
            margin-bottom: 20px;
            color: #CBD5E1;
        }}
        .markdown-body ul, .markdown-body ol {{
            margin-bottom: 25px;
            padding-left: 24px;
        }}
        .markdown-body li {{
            margin-bottom: 10px;
            color: #CBD5E1;
        }}
        .markdown-body li strong {{
            color: #FFF;
        }}
        .markdown-body blockquote {{
            border-left: 4px solid var(--primary-accent);
            background: rgba(255, 91, 53, 0.03);
            padding: 16px 24px;
            margin: 25px 0;
            border-radius: 0 12px 12px 0;
        }}
        .markdown-body blockquote p {{
            margin-bottom: 0;
            font-style: italic;
        }}
        .markdown-body code {{
            font-family: 'Fira Code', 'Courier New', Courier, monospace;
            background: rgba(255, 255, 255, 0.06);
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 14.5px;
            color: var(--secondary-accent);
        }}
        .markdown-body pre {{
            background: rgba(10, 15, 30, 0.4);
            border: 1px solid var(--glass-border);
            padding: 24px;
            border-radius: 14px;
            overflow-x: auto;
            margin: 25px 0;
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
            margin: 30px 0;
        }}
        .markdown-body th, .markdown-body td {{
            border: 1px solid var(--glass-border);
            padding: 14px 18px;
            text-align: left;
            font-size: 15px;
        }}
        .markdown-body th {{
            background: rgba(255, 255, 255, 0.03);
            font-family: var(--font-display);
            font-weight: 700;
            color: #FFF;
        }}
        .markdown-body tr:nth-child(even) {{
            background: rgba(255, 255, 255, 0.005);
        }}
        .markdown-body hr {{
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            margin: 40px 0;
        }}
        
        /* Alert components from GitHub alerts */
        .markdown-body .alert {{
            border-left: 4px solid #1f6feb;
            background-color: rgba(31, 111, 235, 0.05);
            padding: 16px 20px;
            border-radius: 0 12px 12px 0;
            margin: 20px 0;
        }}
        .markdown-body .alert-title {{
            font-weight: 700;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* Mermaid styling */
        .mermaid {{
            background: rgba(10, 15, 30, 0.6) !important;
            border: 1px solid var(--glass-border) !important;
            padding: 20px !important;
            border-radius: 14px !important;
            margin: 25px 0 !important;
            display: flex;
            justify-content: center;
        }}
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="glow-radial"></div>

    <div class="container">
        <a href="../../index.html#cases" class="back-link">← 返回官網首頁案例庫</a>
        <div class="header-bar">
            <span class="logo-txt">🦅 PHOENIX AI 鳳凰顧問</span>
            <span class="badge">企業實戰示範報告</span>
        </div>
        
        <div class="markdown-body" id="content">
            <!-- Content will be rendered here -->
        </div>
    </div>

    <!-- Hidden Raw Markdown Data -->
    <script type="text/markdown" id="rawMarkdown">{markdown_content}</script>

    <script>
        // Set marked.js options
        marked.setOptions({{
            gfm: true,
            breaks: true,
            headerIds: true,
            mangle: false
        }});

        // Render Markdown
        const mdText = document.getElementById('rawMarkdown').textContent;
        const htmlContent = marked.parse(mdText);
        document.getElementById('content').innerHTML = htmlContent;

        // Extract and format Mermaid code blocks for Mermaid.js rendering
        const codeBlocks = document.querySelectorAll('code.language-mermaid');
        codeBlocks.forEach(codeBlock => {{
            const pre = codeBlock.parentElement;
            const mermaidDiv = document.createElement('div');
            mermaidDiv.className = 'mermaid';
            mermaidDiv.textContent = codeBlock.textContent.trim();
            pre.replaceWith(mermaidDiv);
        }});

        // Initialize and run Mermaid
        mermaid.initialize({{
            startOnLoad: false,
            theme: 'dark',
            securityLevel: 'loose',
            themeVariables: {{
                background: '#070913',
                primaryColor: '#1F4E78',
                secondaryColor: '#FF5B35',
                tertiaryColor: '#E8F8F5'
            }}
        }});
        mermaid.run();
    </script>
</body>
</html>
"""

    for filename in md_files:
        filepath = os.path.join(markdown_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        metadata, body_text = parse_front_matter(content)
        
        # Validate required metadata keys
        required_keys = ["id", "title", "industry", "industry_name", "tag", "scheme", "pain_points", "solutions", "roi"]
        missing_keys = [k for k in required_keys if k not in metadata]
        if missing_keys:
            print(f"Warning: File {filename} is missing metadata keys: {missing_keys}")
            continue
            
        # File name for the output HTML
        html_filename = filename.replace(".md", ".html")
        metadata["detail_url"] = f"./cases/html/{html_filename}"
        
        # Save metadata for cases.json
        cases_metadata.append(metadata)
        
        # Format HTML with single curly brace replacement to avoid CSS/JS brace issues
        # We replace {title} and {markdown_content} explicitly
        html_content = html_template.replace("{{", "{").replace("}}", "}").replace("{title}", metadata["title"]).replace("{markdown_content}", body_text)
        
        # Write HTML file
        html_path = os.path.join(html_dir, html_filename)
        with open(html_path, "w", encoding="utf-8") as out_f:
            out_f.write(html_content)
        print(f"Compiled: {filename} -> {html_filename}")
        
    # Sort metadata by case ID to keep order clean
    # PHX-CASE-2026-001, PHX-CASE-2026-002, etc.
    def sort_key(meta):
        case_id = meta.get("id", "")
        # Extract number at the end
        match = re.search(r'\d+$', case_id)
        if match:
            return int(match.group(0))
        return 9999
        
    cases_metadata.sort(key=sort_key)
    
    # Write JSON database
    with open(json_path, "w", encoding="utf-8") as json_f:
        json.dump(cases_metadata, json_f, ensure_ascii=False, indent=2)
    print(f"Generated cases index database: {json_path} (Total: {len(cases_metadata)} cases)")

    # Write JS database for file:// support without CORS blocks
    js_path = os.path.join(base_dir, "cases", "cases_data.js")
    with open(js_path, "w", encoding="utf-8") as js_f:
        js_data = json.dumps(cases_metadata, ensure_ascii=False, indent=2)
        js_f.write(f"const PHOENIX_CASES_DB = {js_data};\\n")
    print(f"Generated cases JS database: {js_path}")

if __name__ == "__main__":
    compile_cases()
