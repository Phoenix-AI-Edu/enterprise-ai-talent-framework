# -*- coding: utf-8 -*-
"""
generate_client_assets.py — 自動批量生成剩餘企業之專案管理表、A3 畫布、行銷文案，並自動編譯為 Excel 專案表
========================================================================
[Confidential - Phoenix AI Internal Asset]

本程式提供一鍵批次自動化生成所有剩餘客戶專案資產的功能：
1. 自動載入環境變數中的 Gemini 與 OpenAI API 金鑰。
2. 支援雙模型備份機制：優先使用 Gemini，遇到 429 速率限制時自動切換至 OpenAI gpt-4o-mini。
3. 增加延遲與重試機制，徹底規避 Cloud API 頻率限制。
4. 批次處理 11 個剩餘客戶案件。
5. 編譯為 5 個工作表之實體 Excel。
"""

import os
import sys
import re
import time
import subprocess
import logging
from datetime import datetime

# 設定 logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# 強制設定 UTF-8 輸出
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

# ──────────────────────────────────────────────────────────────────────
# 1. 載入 API Keys
# ──────────────────────────────────────────────────────────────────────
def load_env_keys():
    keys = {
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY")
    }
    env_paths = [
        ".env",
        "scripts/.env",
        "../.env",
        "C:/Users/Ring/Documents/GitHub/twstock/.env",
        "C:/Users/Ring/Documents/GitHub/twstock/ai_microservice_production/.env"
    ]
    for path in env_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            parts = line.split("=", 1)
                            key = parts[0].strip()
                            val = parts[1].strip()
                            if val.startswith('"') and val.endswith('"'):
                                val = val[1:-1]
                            elif val.startswith("'") and val.endswith("'"):
                                val = val[1:-1]
                            if key in keys and not keys[key]:
                                keys[key] = val
                                os.environ[key] = val
            except Exception as e:
                logger.warning(f"載入 .env 檔案 [{path}] 失敗: {e}")
    return keys

# ──────────────────────────────────────────────────────────────────────
# 2. 雙核生成模組 (Gemini 優先，OpenAI 備份，含退避重試)
# ──────────────────────────────────────────────────────────────────────
def generate_content_with_fallback(keys, system_instruction, prompt, retries=3):
    google_key = keys.get("GOOGLE_API_KEY") or keys.get("GEMINI_API_KEY")
    openai_key = keys.get("OPENAI_API_KEY")
    
    # 嘗試次數迴圈
    for attempt in range(1, retries + 1):
        # 1. 優先使用 Gemini
        if google_key:
            try:
                logger.info(f"  [推論] 嘗試使用 Gemini API...")
                from google import genai
                from google.genai import types
                
                client = genai.Client(api_key=google_key)
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.6,
                    ),
                    contents=prompt,
                )
                return response.text.strip()
            except Exception as e:
                logger.warning(f"  ⚠️ Gemini 調用異常 (第 {attempt} 次嘗試): {e}")
                # 若為 429 速率限制，則直接嘗試備用方案或等待
                
        # 2. 備份使用 OpenAI
        if openai_key:
            try:
                logger.info(f"  [推論] 切換使用 OpenAI API (gpt-4o-mini)...")
                from openai import OpenAI
                
                client = OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature=0.6,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.warning(f"  ⚠️ OpenAI 調用異常 (第 {attempt} 次嘗試): {e}")
                
        # 如果是最後一次嘗試依然失敗，拋出錯誤
        if attempt == retries:
            raise RuntimeError("Gemini 與 OpenAI 雙模型皆調用失敗或 API Key 未配置。")
            
        # 退避等待 15 秒再重試
        logger.info(f"  ⏳ 觸發 API 頻率保護，等待 15 秒後重試...")
        time.sleep(15)

# ──────────────────────────────────────────────────────────────────────
# 3. 專案管理表與 A3 畫布 Prompt 設計
# ──────────────────────────────────────────────────────────────────────
PROMPT_TEMPLATES = {
    "project_tables": {
        "system": """你現在是鳳凰 AI 顧問團隊的「孟淑慧 資深首席顧問」與「陳文家 策略長」。
你正在為客戶撰寫一套 Notion 對齊之專案管理資料庫。
寫作風格：麥肯錫式、嚴謹結構化、數據與變革對齊。

基於 NDA 隱私規範，生成的內容絕對不可含有具體客戶真實名稱，必須使用去識別化的行業代稱（例如「外銷車規級扣件大廠」、「連鎖餐飲集團」）進行去敏感替換。

請生成一個 Markdown 文件，標題為：# [Client_Name] AI 專案管理資料庫 (4+1 Notion-Aligned Databases)
內容必須嚴格包含以下四個主資料庫（以 Markdown 表格呈現，屬性必須 100% 完整填寫，絕不可有空白格或省略字眼）：

## 🗃️ 資料表一：企業 AI 場景盤點資料庫 (Scenario Inventory Database)
欄位：| 對應場景專案 | 業務痛點 | 主責部門 | 核心 AI 任務 | 商業價值 (V) | 數據就緒度 (D) | 一線阻力 (R) | ROI 綜合指數 | 導入優先級決策 |
（請根據客戶需求特徵，規劃 3-5 個場景）

## 🗃️ 資料表二：資料基礎與方案架構資料庫 (Data & Architecture Database)
欄位：| 對應場景專案 | 數據源與格式 | 數據清洗/處理技術 | 本地/地端硬體需求 | 外部 API/雲端服務 | 降級/災備模式 (DR) |

## 🗃️ 資料表三：試點驗證與阻力評估資料庫 (Pilot & Adoption Database)
欄位：| 對應場景專案 | 試點部門與核心人員 | 核心使用阻力分析 | 變革管理方案與激勵機制 | 試點期驗證指標 (90天) |

## 🗃️ 資料表四：營運、治理與組織變革資料庫 (Operations & Governance Database)
欄位：| 對應場景專案 | 運營維護責任人 | SLA 服務可用度要求 | 數據保護與安全稽核 (Audit) | 退場機制與數據可攜 (Exit) |

最後，請在文件尾端附上：
## 🎨 總表：企業 AI 一頁式總體戰略畫布 (A3 Strategy Canvas)
請在此處繪製一個精美的、以 ```text 包夾的 A3 戰略畫布 6 盒文字框格圖，對齊以下結構（請保持框線對齊，內容簡明扼要）：
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        【鳳凰 AI】[Client_Name_Anonymized]企業 AI 一頁式總體戰略畫布 (v2026)                    │
├────────────────────────────┬────────────────────────────┬─────────────────────────────┤
│ 1. 核心業務痛點與商用價值   │ 2. 技術架構與 Buy vs. Build│ 3. 資料資產與資安防線       │
│    (對應 主表一)            │    (對應 主表二)            │    (對應 主表二)            │
│    ...                     │    ...                     │    ...                      │
├────────────────────────────┼────────────────────────────┼─────────────────────────────┤
│ 4. 試點計畫與擴展時程       │ 5. 變革管理與人機協作比例  │ 6. 治理、合規與持續維運     │
│    (對應 主表三)            │    (對應 主表三 & 主表四)  │    (對應 主表四)            │
│    ...                     │    ...                     │    ...                      │
├────────────────────────────┴────────────────────────────┴─────────────────────────────┤
│ 🏆 終極戰略目標：...                                                                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
""",
        "prompt": """請閱讀以下去識別化診斷文本，為其量身客製生成專案管理資料庫 Markdown 文件。
========================================================================
{context}
========================================================================
請直接輸出 Markdown 內容，保持格式優美完整，不要包含 any 額外的對話說明。
"""
    },
    
    "a3_canvas": {
        "system": """你現在是鳳凰 AI 顧問團隊的「孟淑慧 資深首席顧問」與「陳文家 策略長」。
你正在撰寫一份高層決策專用的一頁式 AI 落地與合規戰略畫布 (A3 Strategy Canvas) 詳細說明書。
語氣必須極度嚴謹、務實、大機構諮詢顧問風格，對齊高層利益與變革痛點。

請生成一個 Markdown 文件，標題為：# [Client_Name] 一頁式 AI 落地與合規戰略畫布 (A3 Strategy Canvas)
文件必須嚴格包含以下結構：
## 🏗️ 一、 企業背景與核心業務挑戰 (Current Status & Challenges)
(包含 1. 企業背景 2. 特許監管大限與品質紅線 3. 一線變革痛點)

## 🔒 二、 核心 AI 解決方案架構 (Target AI Architecture)
(包含一個以 ```text 包夾的系統架構拓撲圖，並詳細解構部署策略與人機雙簽工作流)

## 🛡️ 三、 金融合規與資安防線 (Governance & Compliance)
(解構有人在環 (HITL) 決策簽章設計、DLP 個資網閘、以及 API 算力/Token 財務熔斷防線)

## 👥 四、 變革管理與員工賦能 (Change Management & Enablement)
(包含定位、激勵機制、變革心理化解方案與 KPI 指標重塑)

## 💸 五、 租稅折抵與財務 TCO 精算 (Tax Incentives & TCO)
(包含研發租稅抵減 15% 實務包裝申報指引，與 Buy vs. Build 3年期 TCO 評估)

## 📊 六、 [Client_Name_Anonymized] C-Suite 最終決策 (CEO Verdict)
(包含一個決策對照表格：
| 評估維度 | 一般技術廠商 / 外包 SI | **鳳凰 AI 金融落地框架** | 總經理/CEO 評語 |
)
""",
        "prompt": """請閱讀以下去識別化診斷文本，為其量身客製生成 A3 戰略畫布詳細說明書 Markdown 文件。
========================================================================
{context}
========================================================================
請直接輸出 Markdown 內容，保持格式優美完整，不要包含 any 額外的對話說明。
"""
    }
}

# ──────────────────────────────────────────────────────────────────────
# 4. 主執行程序
# ──────────────────────────────────────────────────────────────────────
def main():
    logger.info("啟動 PHOENIX AI 批量資產生成與編譯機制...")
    keys = load_env_keys()
    
    # 驗證金鑰配置
    if not (keys.get("GOOGLE_API_KEY") or keys.get("GEMINI_API_KEY") or keys.get("OPENAI_API_KEY")):
        logger.error("錯誤：未偵測到任何 API 金鑰，無法繼續生成！")
        sys.exit(1)
        
    # 待處理的 11 個企業客戶
    clients = [
        {"key": "dingsheng", "name": "鼎盛精密工業 (dingsheng)"},
        {"key": "luzhu_coldheading", "name": "龍門冷鐓精密扣件 (luzhu_coldheading)"},
        {"key": "mingchadao", "name": "明茶道 (mingchadao)"},
        {"key": "okayama_fastener", "name": "振豐精密 (okayama_fastener)"},
        {"key": "okayama_forge", "name": "隆達精密 (okayama_forge)"},
        {"key": "okayama_heat", "name": "宏達熱處理 (okayama_heat)"},
        {"key": "okayama_cbam", "name": "吉翔航太 (okayama_cbam)"},
        {"key": "okayama_filter", "name": "聯發光學 (okayama_filter)"},
        {"key": "okayama_electroplate", "name": "振鑫表面 (okayama_electroplate)"},
        {"key": "okayama_barcode", "name": "興達包裝 (okayama_barcode)"},
        {"key": "okayama_sbir", "name": "龍圖機械 (okayama_sbir)"}
    ]

    success_count = 0
    failure_count = 0
    
    my_env = os.environ.copy()
    my_env["PYTHONIOENCODING"] = "utf-8"
    my_env["PYTHONUTF8"] = "1"
    
    for idx, client in enumerate(clients, 1):
        logger.info(f"\n========================================================================")
        logger.info(f"🚀 [{idx}/{len(clients)}] 啟動企業：{client['name']}")
        logger.info(f"========================================================================")
        
        client_key = client["key"]
        client_dir = f"marketing_drafts/{client_key}"
        excel_path = os.path.join(client_dir, "project_management_tables.xlsx")
        pm_md_path = os.path.join(client_dir, "project_management_tables.md")
        
        if os.path.exists(excel_path) and os.path.exists(pm_md_path):
            logger.info(f"⏭️ 企業客戶 [{client_key}] 已有編譯完成的 Excel 與 Markdown 資產，自動跳過...")
            success_count += 1
            continue

        clean_path = f"scripts/clean_{client_key}.txt"
        if not os.path.exists(clean_path):
            clean_path = f"scripts/proposal_{client_key}.md"
            if not os.path.exists(clean_path):
                logger.error(f"❌ 找不到客戶去識別化文本，跳過：{client_key}")
                failure_count += 1
                continue
                
        with open(clean_path, "r", encoding="utf-8") as f:
            context_text = f.read()
            
        os.makedirs(client_dir, exist_ok=True)
        
        pm_md_path = os.path.join(client_dir, "project_management_tables.md")
        a3_md_path = os.path.join(client_dir, "a3_strategy_canvas.md")
        
        try:
            # Step A: 生成 project_management_tables.md
            logger.info(f"  [Step 1/4] 正在生成 Notion 4 大資料表...")
            pm_system = PROMPT_TEMPLATES["project_tables"]["system"].replace("[Client_Name]", client["name"])
            pm_prompt = PROMPT_TEMPLATES["project_tables"]["prompt"].format(context=context_text)
            pm_content = generate_content_with_fallback(keys, pm_system, pm_prompt)
            with open(pm_md_path, "w", encoding="utf-8") as f:
                f.write(pm_content)
            logger.info(f"  ✅ 專案管理資料庫生成成功：{pm_md_path}")
            
            # 延遲 3 秒以符合頻率限制
            time.sleep(3)
            
            # Step B: 生成 a3_strategy_canvas.md
            logger.info(f"  [Step 2/4] 正在生成 A3 戰略畫布...")
            a3_system = PROMPT_TEMPLATES["a3_canvas"]["system"].replace("[Client_Name]", client["name"]).replace("[Client_Name_Anonymized]", client["name"])
            a3_prompt = PROMPT_TEMPLATES["a3_canvas"]["prompt"].format(context=context_text)
            a3_content = generate_content_with_fallback(keys, a3_system, a3_prompt)
            with open(a3_md_path, "w", encoding="utf-8") as f:
                f.write(a3_content)
            logger.info(f"  ✅ A3 戰略畫布生成成功：{a3_md_path}")
            
            # 延遲 3 秒以符合頻率限制
            time.sleep(3)
            
            # Step C: 呼叫 marketing_agent.py 生成社交文案
            logger.info(f"  [Step 3/4] 正在執行行銷 Agent 自動化文案生成與合規過濾...")
            agent_cmd = [
                sys.executable,
                "scripts/marketing_agent.py",
                "--client", client_key,
                "--platforms", "all"
            ]
            result_agent = subprocess.run(agent_cmd, capture_output=True, text=True, encoding="utf-8", env=my_env)
            if result_agent.returncode == 0:
                logger.info(f"  ✅ 行銷文案與合規審核順利完成！")
            else:
                logger.warning(f"  ⚠️ 行銷 Agent 執行中發出警告：{result_agent.stderr or result_agent.stdout}")
            
            # Step D: 呼叫 parse_md_to_excel.py 編譯成實體 Excel
            logger.info(f"  [Step 4/4] 正在執行 Excel 編譯 (包含 5 大 Sheet & 樣式套用)...")
            excel_path = os.path.join(client_dir, "project_management_tables.xlsx")
            excel_cmd = [
                sys.executable,
                "scripts/parse_md_to_excel.py",
                "--markdown", pm_md_path,
                "--output", excel_path
            ]
            result_excel = subprocess.run(excel_cmd, capture_output=True, text=True, encoding="utf-8", env=my_env)
            if result_excel.returncode == 0:
                logger.info(f"  ✅ Excel 專案表編譯完成：{excel_path}")
            else:
                logger.error(f"  ❌ Excel 編譯失敗：{result_excel.stderr}")
                raise RuntimeError(result_excel.stderr)
                
            success_count += 1
            logger.info(f"🎉 企業客戶 [{client_key}] 的所有資產生成與編譯完成！")
            
            # 每處理完一家，延遲 5 秒防範全域 rate limit
            time.sleep(5)
            
        except Exception as ex:
            logger.error(f"❌ 企業客戶 [{client_key}] 處理失敗：{ex}")
            failure_count += 1
            
    logger.info(f"\n" + "="*80)
    logger.info(f"   📊 批量生成與編譯成果報告")
    logger.info(f"="*80)
    logger.info(f" 總處理企業：{len(clients)} 家")
    logger.info(f" 成功編譯：{success_count} 家")
    logger.info(f" 失敗數量：{failure_count} 家")
    logger.info(f"="*80 + "\n")

if __name__ == "__main__":
    main()
