# -*- coding: utf-8 -*-
"""
batch_init_okayama.py — 鳳凰 AI B2B 首期 Phase A (岡山精密製造集群) 批次去識別化與 Master Prompt 生成
========================================================================
This script batch-initializes the 9 Okayama/Luzhu precision manufacturing cases.
It executes `phoenix_b2b_pipeline.py init` on each case, generating clean text 
and dynamic McKinsey Master Prompts with manufacturing-optimized B2B slides.
========================================================================
"""

import os
import sys
import subprocess

# 強制設定 UTF-8 輸出，防範 Windows cp950 編碼異常
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def log_banner():
    print("="*80)
    print("   🏛️  PHOENIX AI B2B PIPELINE — BATCH INITIALIZATION (PHASE A / WEEK 1)  ")
    print("      Okayama & Luzhu Precision Manufacturing & Fastener Industry Cluster")
    print("="*80)

def main():
    log_banner()
    
    # 9 cases dictionary with client_key and raw_path
    cases = [
        {"key": "okayama_fastener", "path": "scripts/raw_okayama_fastener.txt", "name": "PHX-001 PMC 岡山扣件廠 (振豐精密)"},
        {"key": "okayama_forge", "path": "scripts/raw_okayama_forge.txt", "name": "PHX-021 冷鍛模具崩損岡山廠 (隆達精密)"},
        {"key": "okayama_heat", "path": "scripts/raw_okayama_heat.txt", "name": "PHX-022 高強度熱處理離線廠 (宏達熱處理)"},
        {"key": "okayama_cbam", "path": "scripts/raw_okayama_cbam.txt", "name": "PHX-023 航太扣件歐盟CBAM (吉翔航太)"},
        {"key": "okayama_filter", "path": "scripts/raw_okayama_filter.txt", "name": "PHX-024 影像篩選缺陷誤報 (聯發光學)"},
        {"key": "okayama_electroplate", "path": "scripts/raw_okayama_electroplate.txt", "name": "PHX-025 電鍍配方環保排污 (某電鍍加工廠)"},
        {"key": "luzhu_coldheading", "path": "scripts/raw_luzhu_coldheading.txt", "name": "PHX-026 路竹冷鐓停機預警 (龍門冷鐓)"},
        {"key": "okayama_barcode", "path": "scripts/raw_okayama_barcode.txt", "name": "PHX-027 條碼防錯中高齡安心 (興達包裝)"},
        {"key": "okayama_sbir", "path": "scripts/raw_okayama_sbir.txt", "name": "PHX-033 製造智慧防護SBIR (龍圖機械)"}
    ]
    
    success_count = 0
    failure_count = 0
    results = []
    
    my_env = os.environ.copy()
    my_env["PYTHONIOENCODING"] = "utf-8"
    my_env["PYTHONUTF8"] = "1"
    
    for idx, case in enumerate(cases, 1):
        print(f"\n🚀 [{idx}/9] 啟動 {case['name']}...")
        
        # Check raw file existence
        if not os.path.exists(case['path']):
            print(f"❌ [錯誤] 找不到原始諮詢檔案：{case['path']}")
            results.append({"name": case['name'], "status": "FAIL", "reason": "Raw file missing"})
            failure_count += 1
            continue
            
        cmd = [
            sys.executable,
            "scripts/phoenix_b2b_pipeline.py",
            "init",
            "--client", case['key'],
            "--raw", case['path']
        ]
        
        # Run subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=my_env)
        
        if result.returncode == 0:
            print(f"✅ [成功] {case['name']} 去識別化與 Master Prompt 生成順利完成！")
            # Parse produced slides count from stdout if possible
            slides_msg = "Dynamic match complete"
            for line in result.stdout.splitlines():
                if "動態簡報規劃完成！" in line:
                    slides_msg = line.strip()
                    print(f"   📊 {slides_msg}")
            
            clean_file = f"scripts/clean_{case['key']}.txt"
            prompt_file = f"scripts/master_prompt_{case['key']}.txt"
            
            results.append({
                "name": case['name'],
                "status": "SUCCESS",
                "clean": clean_file,
                "prompt": prompt_file,
                "details": slides_msg
            })
            success_count += 1
        else:
            print(f"❌ [失敗] {case['name']} 執行失敗！")
            print(f"   stderr: {result.stderr}")
            print(f"   stdout: {result.stdout}")
            results.append({"name": case['name'], "status": "FAIL", "reason": result.stderr or result.stdout})
            failure_count += 1
            
    print("\n" + "="*80)
    print("      📊首期 PHASE A 批次管線運行成果彙整報告")
    print("="*80)
    print(f" 總計案例：{len(cases)} 個")
    print(f" 成功數量：\033[92m{success_count}\033[0m 個")
    print(f" 失敗數量：\033[91m{failure_count}\033[0m 個")
    print("-"*80)
    
    for idx, r in enumerate(results, 1):
        if r['status'] == "SUCCESS":
            print(f" [{idx:02d}] \033[92m[SUCCESS]\033[0m {r['name']}")
            print(f"      ↳ 去敏感檔案：{r['clean']}")
            print(f"      ↳ 專屬 Prompt：{r['prompt']}")
        else:
            print(f" [{idx:02d}] \033[91m[FAIL]\033[0m {r['name']} — 原因：{r['reason']}")
            
    print("="*80)
    print(" 👑 【批次處理閉環】9 大精密製造去識別化與 Master Prompt 生成已全部就緒！")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
