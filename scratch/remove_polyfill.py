# -*- coding: utf-8 -*-
import os
import re

def clean_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Pattern to match: <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    # including potential line breaks or trailing whitespace
    pattern_html = r'<script\s+src="https://polyfill\.io/v3/polyfill\.min\.js\?features=es6"\s*></script>\s*'
    
    new_content = re.sub(pattern_html, '', content)
    
    if new_content != content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    return False

def clean_repository():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_count = 0
    
    # We will search in: cases, slides, curriculum, scripts
    target_dirs = ["cases", "slides", "curriculum", "scripts"]
    
    for target_dir in target_dirs:
        dir_path = os.path.join(base_dir, target_dir)
        if not os.path.exists(dir_path):
            continue
            
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(".html") or file.endswith(".py"):
                    filepath = os.path.join(root, file)
                    try:
                        if clean_file(filepath):
                            print(f"Cleaned polyfill.io from: {filepath}")
                            cleaned_count += 1
                    except Exception as e:
                        print(f"Error cleaning {filepath}: {e}")
                        
    print(f"Clean up complete! Cleaned {cleaned_count} files.")

if __name__ == "__main__":
    clean_repository()
