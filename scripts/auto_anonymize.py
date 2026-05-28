#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
🦅 鳳凰 AI - B2B 簡報去識別化自動同步腳本 (Auto Anonymization Sync Engine)
-------------------------------------------------------------------------
作用：自動掃描 slides/ 下的各企業私有目錄，讀取其 anonymize_rules.json 規則，
      將 HTML 簡報徹底去識別化後，同步至公開的 curriculum/templates/ 對應目錄。
用法：在專案根目錄下執行：python scripts/auto_anonymize.py
"""

import os
import json
import codecs
import sys

# 強制將標準輸出重置為 UTF-8，防範 Windows 控制台 cp950 編碼報錯
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # 舊版本 Python 忽略

# 定義基礎路徑 (基於指令碼所在路徑的上一層)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLIDES_DIR = os.path.join(BASE_DIR, "slides")
TEMPLATES_DIR = os.path.join(BASE_DIR, "curriculum", "templates")

def load_rules(client_folder):
    """讀取企業專屬的去識別化規則"""
    rules_path = os.path.join(SLIDES_DIR, client_folder, "anonymize_rules.json")
    if not os.path.exists(rules_path):
        return None
    
    try:
        with codecs.open(rules_path, "r", "utf-8") as f:
            data = json.load(f)
            # 將規則排序，長度長的字詞排在前面，防止「短字詞覆蓋長字詞」的取代 Bug
            replacements = data.get("replacements", {})
            sorted_replacements = sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True)
            return sorted_replacements
    except Exception as e:
        print(f"❌ 讀取 {client_folder} 規則失敗: {str(e)}")
        return None

def anonymize_file(src_path, dest_path, replacements):
    """對單一檔案執行去識別化取代並儲存"""
    try:
        with codecs.open(src_path, "r", "utf-8") as f:
            content = f.read()
        
        # 執行取代
        replaced_count = 0
        for target, replacement in replacements:
            if target in content:
                content = content.replace(target, replacement)
                replaced_count += 1
                
        # 建立目的父目錄
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        with codecs.open(dest_path, "w", "utf-8") as f:
            f.write(content)
        return True, replaced_count
    except Exception as e:
        print(f"❌ 去識別化檔案失敗 {os.path.basename(src_path)}: {str(e)}")
        return False, 0

def run_sync():
    print("🦅 [Phoenix AI] 啟動 B2B 簡報去識別化同步引擎...")
    
    if not os.path.exists(SLIDES_DIR):
        print(f"⚠️ 找不到私有簡報目錄: {SLIDES_DIR}，請確認目錄結構。")
        return
        
    # 掃描 slides/ 下的所有子目錄
    client_folders = [f for f in os.listdir(SLIDES_DIR) if os.path.isdir(os.path.join(SLIDES_DIR, f))]
    
    if not client_folders:
        print("ℹ️ slides/ 目錄下目前沒有任何企業子目錄。")
        return

    synced_count = 0
    warning_count = 0

    for folder in client_folders:
        replacements = load_rules(folder)
        
        if not replacements:
            print(f"⚠️ [警告] 發現企業目錄 '{folder}'，但未配置 'anonymize_rules.json'，已跳過自動同步。")
            print(f"   👉 提示：請在 slides/{folder}/ 下建立 anonymize_rules.json 以啟用自動防禦機制。")
            warning_count += 1
            continue
            
        print(f"🔑 [解析] 載入 '{folder}' 去識別化規則，共計 {len(replacements)} 條取代限制...")
        
        # 掃描該企業目錄下的所有 HTML 簡報
        src_folder_path = os.path.join(SLIDES_DIR, folder)
        dest_folder_path = os.path.join(TEMPLATES_DIR, folder)
        
        files_to_sync = [f for f in os.listdir(src_folder_path) if f.endswith(".html")]
        
        for filename in files_to_sync:
            src_file = os.path.join(src_folder_path, filename)
            dest_file = os.path.join(dest_folder_path, filename)
            
            success, replaced_items = anonymize_file(src_file, dest_file, replacements)
            if success:
                synced_count += 1
                
        print(f"✅ [完成] '{folder}' 目錄下共 {len(files_to_sync)} 個簡報已安全同步至 curriculum/templates/{folder}/")

    print("\n------------------------------------------------")
    print(f"🎉 同步引擎執行結束！")
    print(f"   - 成功去識別化並同步: {synced_count} 個檔案")
    print(f"   - 未配置安全規則跳過: {warning_count} 個目錄")
    print("------------------------------------------------")

if __name__ == "__main__":
    run_sync()
