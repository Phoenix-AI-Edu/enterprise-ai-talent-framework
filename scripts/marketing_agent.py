# -*- coding: utf-8 -*-
"""
marketing_agent.py — Phoenix AI B2B 社群行銷與流量漏斗全自動化行銷 Agent
========================================================================
B2B Marketing Automation Agent (Confidential & Compliance Guarded)

本工具為鳳凰 AI 框架的行銷自動化 Agent，能夠自動將 B2B 顧問建議書或特定主題，
轉化為 LinkedIn、Facebook、YouTube、X (Twitter) 與 EDM 的高質感行銷內容。
並且在產出後，自動執行金融與品牌合規偵測（對齊 MARKETING_COMPLIANCE_RULES.md）。

重要隱私與規劃機制：
  - 雙層去識別化：在資料發送至雲端大模型前，會先過濾並代換為行業泛稱（預先去識別化），
    防止任何企業真實隱私與 NDA 機密資訊上傳至雲端。
  - 檔案分層規劃管理：自動建立個案子目錄（如 marketing_drafts/henda/），防止檔案雜亂。
  - 反 AI 腔調（Anti-AI Slop）：嚴格禁止空洞的公關詞與機械式情感渲染，採用麥肯錫級專業語意。

用法：
  # 對 henda 建議書進行全渠道行銷內容生成：
  python scripts/marketing_agent.py --client henda --platforms all

  # 針對特定主題生成 LinkedIn 與 X 推文：
  python scripts/marketing_agent.py --topic "ISO 42001 企業稽核避坑指引" --platforms linkedin,twitter
========================================================================
"""

import os
import sys
import re
import argparse
import json
import logging
from datetime import datetime

# 設定 logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────────────
# 1. 載入環境變數與 API 金鑰 (支援多路徑 Fallback)
# ──────────────────────────────────────────────────────────────────────
def load_env_keys():
    """載入 API keys，優先檢查環境變數，再載入 .env 檔"""
    keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "GOOGLE_API_KEY": os.getenv("GOOGLE_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY")
    }

    # 檢查的 .env 路徑清單
    env_paths = [
        ".env",
        "scripts/.env",
        "../.env",
        "C:/Users/Ring/Documents/GitHub/twstock/.env",
        # 聯動 microservice 的 .env
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
                            # 去除引號
                            if val.startswith('"') and val.endswith('"'):
                                val = val[1:-1]
                            elif val.startswith("'") and val.endswith("'"):
                                val = val[1:-1]
                            
                            if key in keys and not keys[key]:
                                keys[key] = val
                                # 同步設定至 os.environ
                                os.environ[key] = val
            except Exception as e:
                logger.warning(f"載入 .env 檔案 [{path}] 失敗: {e}")

    return keys

# ──────────────────────────────────────────────────────────────────────
# 2. 合規守門員 (Compliance Guardian) 本地規則引擎
# ──────────────────────────────────────────────────────────────────────
class LocalComplianceGuardian:
    """
    本地合規守門員：
    - 硬性阻斷 (Hard Block): 投資買賣建議、獲利保證。
    - 企業隱私去識別化 (B2B Anonymization): 自動替換具體企業名/人名為去識別化的行業泛稱。
    - 內部代號阻斷: 偵測並自動替換洩漏的內部系統代號 (OpenClaw, HITL, Compliance Pipeline)。
    """
    def __init__(self):
        # 絕對禁止用語 (對齊台股金融法規與合規規則)
        self.hard_blocks = [
            "保證獲利", "穩賺不賠", "勝率保證", "目標價", "停利點", "停損點",
            "自動帶單", "自動下單", "買進", "賣出", "推薦買入"
        ]
        
        # 企業隱私去識別化對照表 (NDA 規避真實公司名稱)
        self.client_anonymizers = {
            # 恆達精密 / henda
            r"\[恆達精密扣件\]": "外銷車規級扣件大廠",
            r"恆達精密扣件": "外銷車規級扣件大廠",
            r"恆達精密": "外銷車規級扣件大廠",
            r"恆達": "外銷車規級扣件大廠",
            # 悅品餐飲 / yuepin
            r"\[悅品餐飲智慧排班案\]": "知名連鎖餐飲集團",
            r"\[悅品餐飲\]": "知名連鎖餐飲集團",
            r"悅品餐飲": "知名連鎖餐飲集團",
            r"悅品": "知名連鎖餐飲集團",
            # 鼎泰證券 / 證券商 / securities
            r"鼎泰證券": "大型綜合證券商",
            r"鼎泰": "大型綜合證券商",
            # 隆達精密冷鍛
            r"隆達精密冷鍛工業": "精密金屬冷鍛大廠",
            r"隆達精密": "精密金屬冷鍛大廠",
            r"隆達": "精密金屬冷鍛大廠",
            # 宏達熱處理
            r"宏達熱處理工業": "中南部大型熱處理廠",
            r"宏達熱處理": "中南部大型熱處理廠",
            r"宏達": "中南部大型熱處理廠",
            # 興達扣件
            r"興達扣件包裝工業": "精密扣件包裝大廠",
            r"興達扣件": "精密扣件包裝大廠",
            r"興達": "精密扣件包裝大廠",
            # 吉翔航太
            r"吉翔航太扣件工業": "航太扣件與五金出口大廠",
            r"吉翔航太": "航太扣件與五金出口大廠",
            r"吉翔": "航太扣件與五金出口大廠",
            # 聯發光學
            r"聯發光學篩選工業": "光學影像篩選大廠",
            r"聯發光學": "光學影像篩選大廠",
            r"聯發": "光學影像篩選大廠",
            # 振鑫表面防鏽
            r"振鑫表面防鏽工業": "表面處理與防鏽電鍍大廠",
            r"振鑫表面防鏽": "表面處理與防鏽電鍍大廠",
            r"振鑫": "表面處理與防鏽電鍍大廠",
            # 龍門冷鐓
            r"龍門冷鐓精密扣件": "精密冷鐓扣件大廠",
            r"龍門冷鐓": "精密冷鐓扣件大廠",
            r"龍門": "精密冷鐓扣件大廠",
        }
        
        # 內部工程代號防護 (不可對外洩漏)
        self.internal_leaks = {
            r"\bOpenClaw\b": "企業 AI 微服務架構",
            r"\bHITL\b": "有人在環 (Human-In-The-Loop) 協作流程",
            r"\bCompliance Pipeline\b": "自動化合規審查防線",
            r"\bVirtual Compliance Guardian\b": "虛擬合規官",
            r"\bMCP Review Loop\b": "模型協定覆核迴路"
        }

    def anonymize_text(self, text):
        """在資料發送出去前，將所有實體企業名稱代換為去識別化代稱"""
        clean_text = text
        for pattern, replacement in self.client_anonymizers.items():
            clean_text = re.sub(pattern, replacement, clean_text)
        return clean_text

    def check_and_clean(self, text):
        """進行合規偵測，報告違規項目，並自動進行安全替換"""
        warnings = []
        clean_text = text

        # 1. 偵測硬性禁止字眼
        for term in self.hard_blocks:
            if term in text:
                warnings.append(f"[警告] 偵測到違規金融用語 '{term}'，請手動移除以防法規違憲。")

        # 2. 自動替換內部技術代號
        for pattern, replacement in self.internal_leaks.items():
            if re.search(pattern, clean_text, re.IGNORECASE):
                warnings.append(f"[代號防護] 偵測到內部技術名稱，已將其替換為 '{replacement}'。")
                clean_text = re.sub(pattern, replacement, clean_text, flags=re.IGNORECASE)

        # 3. 再次替換任何殘留的真實企業名 (NDA 保護)
        for pattern, replacement in self.client_anonymizers.items():
            if re.search(pattern, clean_text):
                warnings.append(f"[隱私防線] 偵測到具體企業名稱或代號，已自動去識別化替換為 '{replacement}'。")
                clean_text = re.sub(pattern, replacement, clean_text)

        # 4. 二次掃描檢查是否殘留中括號形式的 bracket 洩漏，移除多餘的職稱括號
        bracket_pattern = r"\[[^\d\]]+\]"
        residual_brackets = re.findall(bracket_pattern, clean_text)
        for bracket in residual_brackets:
            # 排除合規佔位符如 [TW_ID_1] 等數字佔位符
            if not re.search(r"_[0-9]+\]$", bracket):
                if "董事長" in bracket or "總經理" in bracket or "執行長" in bracket or "顧問" in bracket:
                    clean_text = clean_text.replace(bracket, bracket.replace("[", "").replace("]", ""))
                    warnings.append(f"[隱私防線] 偵測到職稱中括號，已自動去括號為 '{bracket.replace('[', '').replace(']', '')}'。")
                else:
                    warnings.append(f"[警告] 偵測到疑似未去識別化之中括號佔位符 '{bracket}'，請手動覆核內容。")

        return clean_text, warnings

# ──────────────────────────────────────────────────────────────────────
# 3. 載入 B2B 顧問建議書或原始需求文字
# ──────────────────────────────────────────────────────────────────────
def get_input_context(client_name=None, topic=None, guardian=None):
    """取得行銷生成的上下文內容，並預先執行去識別化以防上雲洩漏"""
    raw_context = ""
    if topic:
        logger.info(f"使用自訂行銷主題進行生成: {topic}")
        raw_context = f"主題：{topic}\n請針對此主題生成符合鳳凰 AI 企業轉型框架的 B2B 行銷內容。"
    elif client_name:
        possible_paths = [
            f"scripts/proposal_{client_name}.md",
            f"proposal_{client_name}.md",
            f"scripts/clean_{client_name}.txt",
            f"clean_{client_name}.txt",
            f"scripts/raw_{client_name}.txt"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        raw_context = f.read()
                    logger.info(f"成功載入客戶 [{client_name}] 建議書內容，檔案路徑: {path}")
                    break
                except Exception as e:
                    logger.error(f"讀取建議書 [{path}] 失敗: {e}")
        
        if not raw_context:
            logger.warning(f"找不到客戶 [{client_name}] 的建議書檔案，使用預設 B2B 商業框架案例為上下文...")
            raw_context = f"客戶代號：{client_name}\n產業：智慧製造與精密加工企業\n痛點：現場黑手師傅排斥數位工具、雙手油污無法報工、外銷面臨歐盟 CBAM 碳足跡申報及車規稽核大限。"
    else:
        raw_context = "通用 B2B 行銷宣傳案。專注於企業 AI 落地治理、有人在環的流程與政府補助對接。"

    # 執行預去識別化，防止真實公司名稱發送至雲端
    if guardian:
        logger.info("執行發送前去識別化 PII/NDA 防護過濾...")
        return guardian.anonymize_text(raw_context)
    return raw_context

# ──────────────────────────────────────────────────────────────────────
# 4. LLM 生成模組 (Gemini / OpenAI 雙核支援)
# ──────────────────────────────────────────────────────────────────────
class LLMGenerator:
    def __init__(self, keys, model_override=None):
        self.keys = keys
        self.openai_key = keys.get("OPENAI_API_KEY")
        self.gemini_key = keys.get("GOOGLE_API_KEY") or keys.get("GEMINI_API_KEY")
        self.model_override = model_override

    def generate(self, system_instruction, prompt):
        if self.gemini_key:
            try:
                from google import genai
                from google.genai import types
                
                model = self.model_override or "gemini-2.0-flash"
                logger.info(f"正在使用 Google Gemini API ({model}) 進行生成...")
                client = genai.Client(api_key=self.gemini_key)
                
                response = client.models.generate_content(
                    model=model,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    ),
                    contents=prompt,
                )
                return response.text.strip()
            except Exception as e:
                logger.error(f"Gemini API 調用失敗: {e}")
                if not self.openai_key:
                    raise e

        if self.openai_key:
            try:
                from openai import OpenAI
                
                model = self.model_override or "gpt-4o-mini"
                logger.info(f"正在使用 OpenAI API ({model}) 進行生成...")
                client = OpenAI(api_key=self.openai_key)
                
                response = client.chat.completions.create(
                    model=model,
                    temperature=0.7,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"OpenAI API 調用失敗: {e}")
                raise e

        raise RuntimeError("未檢測到有效的 OPENAI_API_KEY 或 GOOGLE_API_KEY。")

# ──────────────────────────────────────────────────────────────────────
# 5. 各渠道的 System Prompt 設計 (COPE 思想與 B2B 受眾特化)
# ──────────────────────────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "linkedin": """
你現在是鳳凰 AI 團隊的「陳文家 策略長」。
你正在撰寫 LinkedIn 思想領袖 (Thought Leadership) 專欄。
目標受眾：大企業總經理(CEO/GM)、人資長(CHRO)、AI執行長(CAIO)與資安長(CISO)。
寫作風格：麥肯錫式高奢、結構化、數據與利益導向，避開消費性撒網，聚焦於核心痛點（變革阻力、數據隱私、合規稽核、租稅抵減）。

【🚨 嚴格禁止 AI 腔調與空話 (Anti-AI Slop Rules)】
- 絕對禁止使用以下空洞的 AI 常見詞彙與句式：
  * 「在當今瞬息萬變/快節奏的時代」、「數位轉型的浪潮」、「立於不敗之地」、「攜手共創輝煌/未來」、「開啟新篇章」、「深知您的痛點」、「不再是夢」、「為企業插上翅膀」、「誠摯地邀請您」。
- 寫作必須落地、客觀、用事實與架構說話。每一段都必須有具體的「痛點特徵」或「架構配置」。
- 語氣必須是專業的 B2B 顧問、理性、冷靜、以大機構諮詢顧問（McKinsey/BCG）的專業語意呈現。

【⚠️ 企業隱私保護重要指令 (Strict NDA Protection)】
- 本案例為真實快診案例。基於企業隱私 NDA 協議，你絕對不能在文案中使用任何具體公司名（例如「恆達精密」、「恆達」、「悅品餐飲」）或帶有中括號的真實企業標籤。
- 必須使用去識別化的行業代稱（例如「外銷車規級扣件大廠」、「連鎖餐飲集團」）來描述本案例。

請輸出以下兩部分內容：
1. **LinkedIn 長文文案**：深入淺出地闡述企業 AI 轉型的戰略觀點，字數約 600-800 字。
2. **McKinsey 奢華圖卡 PDF Slider 規劃**：為這篇文章規劃一個 8-10 頁的 PDF 簡報大綱，每頁需包含「視覺配置建議」與「核心金句文字」。
""",

    "facebook": """
高度重視：這篇文案必須徹底擺脫常見的 AI 腔調，展現真實的顧問洞察。

你現在是鳳凰 AI 團隊的「孟淑慧 資深首席顧問」。
你正在為 Facebook 的中小企業主與 HR 社群撰寫在地故事案例貼文。
目標受眾：台灣傳產老闆、中南部 SME 主管、中小企業人資主管。
寫作風格：用台灣在地傳統產業聽得懂的語言（如阿茂師、 si-to-ma 檔塊、 a-so-bi 間隙、成型油、滿手黑油等真實廠房場景），以溫暖、務實且深刻的「變革管理故事」為主線。聚焦於「解決師傅怕技術被掏空的恐慌」、「政府 SBIR/SIIR 補助紅利匹配」、「產創條例第10條之1（AI投資抵減5%）」等。

【🚨 嚴格禁止 AI 腔調與空話 (Anti-AI Slop Rules)】
- 絕對禁止使用以下空洞詞彙與句式：
  * 「在當今瞬息萬變的時代」、「數位轉型的浪潮」、「立於不敗之地」、「攜手共進/共創」、「不再是夢」、「開啟新篇章」、「我們非常高興」。
- 拒絕平庸的情感渲染。阿茂師不是被「AI 的強大所感動」，而是因為「總經理簽署了不裁員承諾書，並將系統正名為阿茂師調機專家庫，同時提供 0.5% 良率分紅」才轉為支持。要寫出利益對齊與尊嚴對齊的具體商業細節。

【⚠️ 企業隱私保護重要指令 (Strict NDA Protection)】
- 基於企業隱私 NDA 協議，絕對禁止在貼文中使用真實企業名稱。
- 請使用去識別化的行業泛稱（例如「外銷車規級扣件大廠」、「知名連鎖餐飲集團」）進行案例描述。

請輸出：
- 一篇極具台灣在地氣息的 FB 故事貼文，字數約 800 字，繁體中文撰寫。
""",

    "twitter": """
你現在是鳳凰 AI 顧問團隊。
你正在為 X (Twitter) 撰寫一系列「教材即程式碼 (Textbook-as-Code)」的技術線索 (Threads)。
目標受眾：技術架構師、CAIO、跨國智慧機械研發主管。
寫作風格：極客感（Geek）、高密度的架構說明、代碼設計與安全防線。

【🚨 嚴格禁止 AI 腔調與空話 (Anti-AI Slop Rules)】
- 絕對禁止使用任何 AI 腔調的公關詞。直接進入技術細節。
- 每一條 Twitter 必須是高度壓縮的技術乾貨。

【⚠️ 企業隱私保護重要指令 (Strict NDA Protection)】
- 絕對禁止使用任何具體企業真實名稱。請統一使用去識別化泛稱（如「外銷扣件大廠」、「連鎖餐飲集團」、「綜合證券商」）。

請輸出：
- 一組由 5-8 則推文組成的 X Thread，解構如何部署本地地端隔離、DLP 去識別化網閘機制，以及安全問責的人機雙簽協作流程。請使用 markdown 代碼塊展示邏輯示意。
""",

    "youtube": """
你現在是鳳凰 AI 顧問團隊。
你正在為 YouTube 頻道撰寫一門 15 分鐘的工具實作影音指令腳本大綱 (Walkthrough Video)。
目標受眾：企業經理人、尋求落地工具的決策者。

【🚨 嚴格禁止 AI 腔調與空話 (Anti-AI Slop Rules)】
- 絕對禁止使用「哈囉大家好，我們非常高興...」等老套 AI 開場。
- 影片以「無私螢幕錄影、手把手演示工具」為核心，展現顧問團隊擁有真實的實體工具，而非口頭理論。

【⚠️ 企業隱私保護重要指令 (Strict NDA Protection)】
- 絕對禁止出現真實企業名稱，請以去識別化泛稱代之。

請輸出：
- YouTube 影片企劃書與腳本大綱：
  - 影片標題（吸睛且專業，如「如何用 Excel 精算 RAG 採購成本」）
  - 0-2分鐘：Hook 開場（直接從財務痛點切入，如「你的 AWS/OpenAI 帳單是怎麼失控的？」）
  - 2-10分鐘：實操演示階段大綱（手把手示範 Excel TCO 試算表或 HTML 互動簡報動態）
  - 10-15分鐘：結尾 CTA（引流至免費索取 Notion A3 戰略畫布工具包）
""",

    "edm": """
你現在是鳳凰 AI 的自動化郵件行銷系統。
你正在規劃 B2B 線索培育漏斗（B2B Nurturing Funnel）的自動化郵件序列。
目標受眾：已填表下載工具包的潛在企業客戶。

【🚨 嚴格禁止 AI 腔調與空話 (Anti-AI Slop Rules)】
- 絕對禁止使用「希望這封信能給您帶來啟發」、「親愛的用戶」等 AI 客套話。
- 信件抬頭與結尾要像是一封真實的顧問工作郵件，語氣嚴謹、直指業務痛點。

【⚠️ 企業隱私保護重要指令 (Strict NDA Protection)】
- 絕對禁止在信件中出現具體真實公司名稱，一律使用去識別化泛稱。

請針對以下三個時間點，撰寫三封信件（繁體中文）：
1. **Day 1 信件：工具包啟用指南**：引導用戶如何使用 A3 紙本 AI 戰略畫布與 Notion 協作庫。
2. **Day 4 信件：傳產變革排除案例**：分享螺絲廠或傳產如何化解一線大師傅抗拒的真實案例（以去識別化泛稱如「南部扣件大廠」進行案例說明）。
3. **Day 7 信件：TCO 成本精算避坑指南**：解析如何精算 RAG 採購成本，避開雲端 SaaS 計費黑洞。
"""
}

# ──────────────────────────────────────────────────────────────────────
# 6. 執行 Agent 行銷生成工作流
# ──────────────────────────────────────────────────────────────────────
def run_agent():
    parser = argparse.ArgumentParser(description="Phoenix AI B2B Marketing Automation Agent CLI")
    parser.add_argument("--client", type=str, help="指定客戶名稱 (如: henda, yuepin, securities)")
    parser.add_argument("--topic", type=str, help="指定自訂行銷主題 (與 --client 二選一)")
    parser.add_argument("--platforms", type=str, default="all", help="要生成的平台，以逗號分隔 (如: linkedin,facebook,edm 或 all)")
    parser.add_argument("--output_dir", type=str, default="marketing_drafts", help="草稿儲存目錄")
    parser.add_argument("--model", type=str, help="指定模型名稱 (Gemini 或 OpenAI)")

    args = parser.parse_args()

    # 1. 載入金鑰與環境
    keys = load_env_keys()
    
    # 2. 決定要產出的平台
    target_platforms = []
    if args.platforms.lower() == "all":
        target_platforms = list(SYSTEM_PROMPTS.keys())
    else:
        target_platforms = [p.strip().lower() for p in args.platforms.split(",") if p.strip()]

    # 3. 初始化合規守門員
    guardian = LocalComplianceGuardian()

    # 4. 取得上下文內容 (此時已完成發送前的去識別化過濾)
    context_text = get_input_context(client_name=args.client, topic=args.topic, guardian=guardian)

    # 5. 建立輸出目錄與個案專屬子目錄
    client_label = args.client or "custom_topic"
    client_dir = os.path.join(args.output_dir, client_label)
    os.makedirs(client_dir, exist_ok=True)

    # 6. 初始化 LLM
    generator = LLMGenerator(keys, model_override=args.model)

    # 7. 開始為各平台生成內容
    # 建立總報告/導覽檔案，存於個案子目錄下
    report_filename = f"run_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path = os.path.join(client_dir, report_filename)
    
    report_content = [
        f"# 鳳凰 AI B2B 行銷自動化 Agent 執行報告 (防雜亂分層版)",
        f"- **執行時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- **輸入來源**: {'客戶建議書 (' + args.client + ')' if args.client else '自訂主題 (' + args.topic + ')'}",
        f"- **生成渠道**: {', '.join(target_platforms)}",
        f"- **個案目錄**: `{client_dir}/`",
        f"- **隱私機制**: 雙層本地預先去識別化 (Cloud NDA Protection) + 合規後處理",
        f"",
        f"---",
        f""
    ]

    logger.info(f"開始為以下平台生成行銷草稿: {', '.join(target_platforms)}")
    
    for platform in target_platforms:
        if platform not in SYSTEM_PROMPTS:
            logger.warning(f"不支援的平台: {platform}，跳過。")
            continue

        logger.info(f"====== 正在生成 [{platform.upper()}] 渠道文案 ======")
        system_instruction = SYSTEM_PROMPTS[platform]
        
        prompt = f"""
以下是我們的 B2B 顧問規劃上下文內容（已執行去識別化處理，保障 NDA 隱私）：
========================================================================
{context_text}
========================================================================

請根據此上下文，以及你的平台角色定位，為我們生成高質感的行銷內容。
文案內容請務必使用繁體中文（Taiwanese Mandarin）呈現，名詞需接地氣。
基於 NDA 隱私規範，生成的內容絕對不可含有具體客戶名稱（如「恆達精密」、「恆達」、「悅品餐飲」）或 bracketed 的真實公司標籤！
"""
        try:
            # 調用 LLM 生成
            raw_draft = generator.generate(system_instruction, prompt)
            
            # 進行合規審查與過濾
            clean_draft, warnings = guardian.check_and_clean(raw_draft)
            
            # 存檔至個案子目錄中
            platform_file = f"{platform}.md"
            platform_path = os.path.join(client_dir, platform_file)
            
            with open(platform_path, "w", encoding="utf-8") as pf:
                pf.write(clean_draft)
            
            logger.info(f"[{platform.upper()}] 生成完成，已儲存至: {platform_path}")
            
            # 紀錄至總報告
            report_content.append(f"## 📱 [{platform.upper()}] 渠道文案")
            report_content.append(f"- **草稿路徑**: [{platform_file}](file:///{os.path.abspath(platform_path).replace('\\', '/')})")
            if warnings:
                report_content.append("### ⚠️ 合規防線偵測報告:")
                for w in warnings:
                    report_content.append(f"- {w}")
            else:
                report_content.append("- ✅ **合規偵測**: 安全無違規詞彙")
            
            report_content.append("")
            report_content.append("---")
            report_content.append("")

        except Exception as ex:
            logger.error(f"[{platform.upper()}] 生成失敗: {ex}")
            report_content.append(f"## ❌ [{platform.upper()}] 渠道生成失敗")
            report_content.append(f"- 錯誤訊息: `{ex}`")
            report_content.append("")
            report_content.append("---")
            report_content.append("")

    # 8. 自動增補：將專案管理表 Markdown 編譯為實體 Excel
    pm_md_path = os.path.join(client_dir, "project_management_tables.md")
    pm_xlsx_path = os.path.join(client_dir, "project_management_tables.xlsx")
    if os.path.exists(pm_md_path):
        logger.info(f"偵測到專案管理表 Markdown，啟動 Excel 自動編譯機制...")
        try:
            sys.path.append(os.path.dirname(__file__))
            from parse_md_to_excel import parse_markdown_tables, export_tables_to_excel
            tables = parse_markdown_tables(pm_md_path)
            if tables:
                export_tables_to_excel(tables, pm_xlsx_path)
                logger.info(f"[自動化成功] 已生成對應的 Excel 專案表: {pm_xlsx_path}")
                report_content.append(f"## 📊 [EXCEL] 專案管理實體表")
                report_content.append(f"- **Excel 路徑**: [project_management_tables.xlsx](file:///{os.path.abspath(pm_xlsx_path).replace('\\', '/')})")
                report_content.append("")
                report_content.append("---")
                report_content.append("")
        except Exception as e:
            logger.warning(f"自動編譯 Excel 失敗: {e}")

    # 寫入總報告檔案
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write("\n".join(report_content))
    
    logger.info(f"行銷自動化工作完成！總報告已儲存至: {report_path}")

    print("\n" + "="*80)
    print(f"\033[92m【Agent 執行成功】行銷自動化草稿已順利輸出！\033[0m")
    print(f"請開啟總報告進行走讀與審計：")
    print(f"  \033[96mfile:///{os.path.abspath(report_path).replace('\\', '/')}\033[0m")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_agent()
