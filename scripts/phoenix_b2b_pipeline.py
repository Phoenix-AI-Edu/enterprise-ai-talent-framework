# -*- coding: utf-8 -*-
"""
phoenix_b2b_pipeline.py — 鳳凰 AI B2B 企業需求對接與簡報/KM 全自動化營運機制
========================================================================
Phoenix AI B2B Reusable Pipeline & Dynamic Slide Planner (Confidential)

此指令為鳳凰 AI 顧問團隊的標準「作業機制」，解決「投影片硬套 10 頁公版」及「手動流程零散」的痛點。
本工具會：
  1. 自動執行本地安全去識別化（呼叫 de_identify_local.py）
  2. 動態分析需求複雜度，【自動調整投影片張數 (8-14 頁)】並規劃專屬藍圖
  3. 生成麥肯錫級 Master Prompt 存為 scripts/master_prompt_[client].txt
  4. (編譯模式) 一鍵解析 Markdown 建議書、驗證格式、編譯 HTML 簡報、同步 CSV 專家庫、
     靜態更新首頁 HTML 案例卡片、運行全域 Markdown/安全檢測，並自動 Git PUSH。

用法：
  # 階段一：啟動新案診斷與去識別化，生成專屬動態 Master Prompt
  python scripts/phoenix_b2b_pipeline.py init --client securities --raw scripts/raw_dingtai.txt

  # 階段二：在外部大模型運行 Master Prompt 後，將產出存至 scripts/proposal_securities.md，然後執行一鍵編譯與同步發布
  python scripts/phoenix_b2b_pipeline.py compile --client securities
========================================================================
"""

import os
import sys
import re
import argparse
import subprocess
import json

def log_info(msg):
    print(f"\033[94m[INFO]\033[0m {msg}")

def log_success(msg):
    print(f"\033[92m[SUCCESS]\033[0m {msg}")

def log_error(msg):
    print(f"\033[91m[ERROR]\033[0m {msg}")

# ──────────────────────────────────────────────────────────────────────
# 階段一：初始化與動態分析
# ──────────────────────────────────────────────────────────────────────
def run_init(client_name, raw_path):
    if not os.path.exists(raw_path):
        log_error(f"找不到原始信件檔案：{raw_path}")
        sys.exit(1)
        
    log_info(f"啟動新客戶 [{client_name}] 營運對接流程...")
    
    # 1. 執行本地去識別化 (C3 等級)
    clean_path = f"scripts/clean_{client_name}.txt"
    map_vault_dir = f"_C2_mapping_vault/{client_name}"
    map_path = f"{map_vault_dir}/map.enc"
    
    os.makedirs(map_vault_dir, exist_ok=True)
    
    log_info("執行第一層本地規則去識別化...")
    deid_cmd = [
        sys.executable,
        "scripts/de_identify_local.py",
        "deid",
        raw_path,
        "-o", clean_path,
        "--map", map_path
    ]
    
    # 執行 de-identify 腳本，自動傳入環境變數避開密碼互動式輸入
    my_env = os.environ.copy()
    my_env["PHOENIX_MAP_KEY"] = "phoenix_ai_vault_2026"
    my_env["PYTHONIOENCODING"] = "utf-8"
    my_env["PYTHONUTF8"] = "1"
    result = subprocess.run(deid_cmd, capture_output=True, text=True, encoding="utf-8", env=my_env)
    if result.returncode != 0:
        log_error(f"去識別化執行失敗：{result.stderr}")
        sys.exit(1)
        
    log_success(f"去識別化完成！已生成乾淨文本於：{clean_path}")
    log_success(f"加密對照表已安全隔離於：{map_path}")
    
    # 2. 讀取乾淨文本，進行動態複雜度分析
    with open(clean_path, "r", encoding="utf-8") as f:
        clean_text = f.read()
        
    log_info("啟動簡報張數與主題動態規劃引擎...")
    
    # 動態判定邏輯 (以關鍵字與痛點多寡動態增減投影片張數)
    slide_blueprint = []
    
    # 基本投影片 (必備)
    slide_blueprint.append({"page": "01", "layout": "cover", "title": "方案封面 (Cover)", "desc": "高奢封面，對齊 CDO 與執行長之專屬標籤。"})
    slide_blueprint.append({"page": "02", "layout": "dual-track", "title": "雙軌分流戰略 (Dual-Track)", "desc": "總部決策安控軌 vs 一線業務賦能軌，降低變革阻力。"})
    
    # 根據內容動態擴展
    page_count = 2
    
    # 數據隱私 / 本地地端
    if any(k in clean_text for k in ["地端", "On-Premise", "私有雲", "機密", "DLP", "遮罩"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "機密數據與地端隔離防線 (Dual-Track)",
            "desc": "本地 DMZ 防火牆部署 Llama-3/Taiwan-LLM RAG 知識庫，配合 DLP 遮罩網閘物理防漏。"
        })
        
    # Multiagent 研報與自動化審查
    if any(k in clean_text for k in ["Multiagent", "研究報告", "分析師", "公會", "審查", "HITL"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "Multiagent 研報與人機雙簽 HITL 流程 (Dual-Track)",
            "desc": "規劃/執行/合規審查代理人流水線，虛擬合規官自動攔截公會違規紅線字眼。"
        })
        
    # 特許 Guardrails
    if any(k in clean_text for k in ["Guardrails", "攔截", "操縱", "熔斷", "防呆"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "特許 Guardrails 法律熔斷機制 (Dual-Track)",
            "desc": "輸入端語意偵測阻斷，輸出端強制轉換為合規免責宣告格式，防範證交法刑事責任。"
        })
        
    # 洗錢防制 AML 與 XAI
    if any(k in clean_text for k in ["洗錢", "AML", "SHAP", "可解釋性"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "洗錢防制 AML 與 SHAP 決策歸因 (Dual-Track)",
            "desc": "多維度異常特徵工程降噪，SHAP 可解釋性決策歸因圖應對金管會透明度稽核。"
        })
        
    # 一線變革與績效考核
    if any(k in clean_text for k in ["變革", "取代", "抗拒", "考核", "激勵"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "AI-Native 績效考核與同儕激勵 (Dual-Track)",
            "desc": "平衡計分卡重塑，工具熟練度加分，卓越服務之星季度獎金化解員工取代焦慮。"
        })
        
    # 行銷與肖像權版權
    if any(k in clean_text for k in ["行銷", "肖像", "版權", "重罰", "廣告"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "行銷 GenAI 版權與肖像防線 (Dual-Track)",
            "desc": "純 AI 生成不受版權保護大坑防禦，員工特徵融合肖像授權同意範本規避罰鍰。"
        })
        
    # 補助對接與政策
    if any(k in clean_text for k in ["補助", "SIIR", "折抵", "研抵", "所得稅"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "金融科技租稅抵減與研發核銷 (Dual-Track)",
            "desc": "所得稅法第 15 條之 1 研發支出投資抵減（研抵）實務包裝，會計師簽證免剔除防線。"
        })

    # 精密機械與製造集群專屬 Slide 1: Voice AI 語音報工與 VAD 降噪
    if any(k in clean_text for k in ["語音", "台語", "ASR", "黑手", "口語", "滿手油", "聽聲音", "戴手套"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "Voice AI 邊緣語音報工與 VAD 降噪 (Dual-Track)",
            "desc": "邊緣端語音 ASR（台國雙語對照）配合 VAD 靜音與環境降噪演算法，解決一線黑手師傅雙手沾油、排斥打字之報工防線。"
        })

    # 精密機械與製造集群專屬 Slide 2: 邊緣離線運算與樹莓派硬熔斷
    if any(k in clean_text for k in ["斷訊", "離線", "機電", "老舊", "樹莓派", "繼電器", "熔斷器", "起火"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "邊緣離線運算與樹莓派硬熔斷 (Dual-Track)",
            "desc": "部署輕量化工業樹莓派離線分析 API，搭配 10ms 機電實體繼電器硬熔斷保護，異常自動斷電，杜絕雲端斷訊與起火責任。"
        })

    # 精密機械與製造集群專屬 Slide 3: 光學影像缺陷過濾與人機雙簽 (HITL)
    if any(k in clean_text for k in ["缺陷", "品管", "瑕疵", "影像", "篩選", "誤報", "油污", "品管班長"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "光學影像缺陷過濾與人機雙簽 (Dual-Track)",
            "desc": "部署雙向偏見校準與濾鏡優化 Pipeline，隔離電鍍油污背景；有人在環（HITL）分流二次覆核，品管老手升級 AI 標記教練。"
        })

    # 精密機械與製造集群專屬 Slide 4: 配方優化 IP 授權與營運達標分紅
    if any(k in clean_text for k in ["電鍍", "配方", "排污", "環保", "廢水", "獨門心法", "技術股", "授權合約", "分紅"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "配方優化 IP 授權與營運達標分紅 (Dual-Track)",
            "desc": "系統正名為工程師專利專家配方庫，並簽署技術特許授權合約，良率與環保排污達標即獲 0.5% 季度分紅，破解師傅技術掏空恐慌。"
        })

    # 精密機械與製造集群專屬 Slide 5: 歐盟 CBAM 碳足跡與大模型 RAG 護航
    if any(k in clean_text for k in ["CBAM", "碳稅", "碳排", "碳足跡", "申報", "歐洲", "關稅"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "歐盟 CBAM 碳足跡與大模型 RAG 護航 (Dual-Track)",
            "desc": "對接 CBAM 碳排大模型與稅則解碼 RAG，使申報工時自 10 天縮短至 4 小時；匹配綠色業務達標激勵，防堵歐盟高額關稅處罰。"
        })

    # 精密機械與製造集群專屬 Slide 6: 出貨包裝 AI 視覺紅綠燈防呆防線
    if any(k in clean_text for k in ["包裝", "條碼", "混料", "中高齡", "貼錯", "防錯", "紅綠燈"]):
        page_count += 1
        slide_blueprint.append({
            "page": f"{page_count:02d}",
            "layout": "dual-track",
            "title": "出貨包裝 AI 視覺紅綠燈防呆防線 (Dual-Track)",
            "desc": "部署自動拍照紅綠燈極簡防呆介面，為中高齡包裝老員工提供免扣薪、防錯達標特別獎金，徹底杜絕出貨混料與條碼貼錯退貨。"
        })
        
    # 互動 ROI 試算器 (必備)
    page_count += 1
    # 根據行業動態調整預設成本基數
    cost_base = 480000
    num_workers = 450
    if "證券" in clean_text or "金融" in clean_text or "securities" in client_name:
        cost_base = 1200000
        num_workers = 100
    elif "製造" in clean_text or "精密" in clean_text or any(k in client_name for k in ["okayama", "luzhu", "forge", "fastener", "heat", "cbam", "filter", "electroplate", "coldheading", "barcode", "sbir"]):
        cost_base = 1800000
        num_workers = 50

    slide_blueprint.append({
        "page": f"{page_count:02d}",
        "layout": "interactive-roi",
        "title": "即時 ROI 財務回收模擬 (Interactive-ROI)",
        "desc": f"拖動滑桿即時計算機會成本與利潤回收。基數：{num_workers}名員工，年人均成本 NT${cost_base/10000:g}萬。"
    })
    
    # 90天建置甘特圖與下一步 (必備)
    page_count += 1
    slide_blueprint.append({"page": f"{page_count:02d}", "layout": "interactive-roadmap", "title": "90 天 Quick-Win 甘特時程 (Roadmap)", "desc": "三階段時程拆解：Month 1 治理、Month 3 試點、Month 6 全面推廣。"})
    
    page_count += 1
    slide_blueprint.append({"page": f"{page_count:02d}", "layout": "next-steps", "title": "下一步行動與結尾 (Next-Steps)", "desc": "Action 1 方案 C 盤點、Action 2 方案 B 工作坊、Action 3 全額折抵特惠。"})
    
    log_success(f"動態簡報規劃完成！根據本案複雜度，已自動擴展至 \033[93m{page_count} 頁\033[0m 奢華 PPT 簡報（HeDa 12頁、MingChaDao 10頁、本案動態匹配為 {page_count} 頁）。")
    
    # 3. 生成專屬麥肯錫級 B2B Master Prompt 檔案
    # 嘗試載入簡報架構最佳化準則
    guidelines_content = ""
    guidelines_path = r"G:\我的雲端硬碟\孟淑慧\PMC\AI人才培育計畫課程規劃\企業外評\簡報架構最佳化準則_ANTIGRAVITY整合版.md"
    if os.path.exists(guidelines_path):
        try:
            with open(guidelines_path, "r", encoding="utf-8") as gf:
                guidelines_content = gf.read()
            log_success("成功載入外部《簡報架構最佳化準則_ANTIGRAVITY整合版.md》！")
        except Exception as ex:
            log_info(f"讀取外部簡報架構最佳化準則失敗：{ex}")
    
    if not guidelines_content:
        # Fallback to absolute standard principles if file cannot be loaded
        guidelines_content = """# 簡報架構最佳化準則 (Fall-Back Spec)
1. 簡報張數是「輸出」而非「輸入」，由：簡報目的 × 受眾結構 × 決策關卡 × 檔案角色推導。
2. 壓縮版 (P-TEASER, ~10張) 服務已承諾的暖買方。
3. 治理版 (P-GOVERNANCE, ~51張) 服務董事會或正式稽核，採取 3-Tier 分層：
   - Tier 0: 決策駕駛艙 (Page 02) 一頁看懂全案。
   - Tier 1: 上台脊椎 (24張) 現場走讀的完整論證鏈。
   - Tier 2: 防身附錄 (26張) 備而不講，供 Q&A 與稽核留存。
4. 金融證券特化條款：監管 Scrutiny = 4，必須有「失效模式風險矩陣」、「第三方供應商退場條款」、「營運韌性 BCP/DR」三件套，且 HITL 雙簽流程必須獨立成張。"""

    blueprint_str = ""
    for item in slide_blueprint:
        blueprint_str += f"- Page {item['page']}: layout \"{item['layout']}\" — {item['title']}\n  說明：{item['desc']}\n\n"
        
    master_prompt = f"""你現在是鳳凰 AI 顧問團隊的「孟淑慧 資深首席顧問」與「陳文家 策略長」。你們正在為一家大型企業客戶撰寫一份客製化解決方案建議書。

客戶的需求已經過 C3 等級去識別化洗滌（屏蔽了真實人名與商標，改以 bracketed 標籤代稱）。

請你針對以下【去識別化去隱私需求文本】進行最高規格的商務推理與技術規劃，為其撰寫一部上萬字、極具說服力、直擊董事會與執行長痛點的「B2B 企業 AI 落地解決方案建議書」。

📥 去識別化去隱私需求文本：
========================================================================
{clean_text}
========================================================================

撰寫與格式要求：
1. 角色與語調：語調必須極度嚴謹、務實、利潤/變革導向，以大機構諮詢顧問（McKinsey/BCG）語意呈現，向客戶高管致敬。
2. 結構要求：建議書必須使用 Markdown 撰寫，且必須嚴格包含以下四個部分：

【第一部分：前瞻戰略與業務診斷】
針對去識別文本中列出的所有業務痛點、高層評判進行深度的「顧問解讀與回覆」，提供變革導向的務實戰略分析（數千字篇幅）。

【第二部分：實務落地技術解決方案與安控】
針對客戶提出的優化建議與痛點，規劃具體的地端/混合雲安全架構、DLP去識別化網閘機制、人機協作雙簽（HITL）流程以及其他特許安全防護配置（數千字篇幅）。

【第三部分：客製簡報配置與演講者備忘錄（請依「簡報架構最佳化準則」動態推導）】
你必須在文章中內嵌 <!-- slide-page: ... --> 錨點，每個錨點下的欄位必須對齊 JSON Schema，以便本地編譯器自動解析。

你必須遵循下方《簡報架構最佳化準則》來設計這套簡報的張數與結構：
- 若客戶為金融證券等特許行業（如本案鼎泰證券），受到金管會嚴格監管，必須觸發「§5. 金融證券特化條款」，強制進入「§2. 51張分層治理模式 (Governance Mode)」，輸出完整的 51 張分層簡報（Tier 0 決策駕駛艙 1張 + Tier 1 上台脊椎 24張 + Tier 2 防身附錄 26張）。
- 若是非監管或低稽核的輕量提案，則可使用「§1. ~10張壓縮版模式 (Compression Mode)」輸出。

請嚴格遵循以下 JSON Schema 規範來填寫每個投影片錨點內的 JSON 內容：
- 必須是有效的 JSON，包含 page, tier, layout, theme, title, subtitle, content(≤200字), speaker_notes(極度充實)。
- 可選用 tracks, items, table, actions, closing_quote, consultants, usage 欄位。
- 支援 layouts: "cover", "dual-track", "interactive-roi", "interactive-roadmap", "next-steps" 等。若使用 "exec-cockpit", "matrix", "flow-hitl", "table", "rule-library" 等特殊佈局，解析器會自動扁平化映射到 dual-track。
- 曜石 Midnight 奢華主題："obsidian-midnight"

以下是《簡報架構最佳化準則》全文，請確實理解其精神與公式，並融入生成的建議書說明中：
========================================================================
{guidelines_content}
========================================================================

【本案推薦之簡報藍圖（供您參考，但對於金融證券大案，請務必擴充至完整 51 頁，拆出 Tier 0/1/2 結構）】：
{blueprint_str}
※注意：所有投影片的 content 欄位字數須嚴格控制在 200 字以內。Speaker Notes 須極為充實（包含開場白、互動提示與顧問口訣）。
※注意：ROI 投影片必須對齊以下參數：
  - slider_min: 10
  - slider_max: 60
  - slider_default: 40
  - cost_base: {cost_base}
  - num_workers: {num_workers}

【第四部分：Notion 知識管理資料庫（全屬性 100% 填滿，零空白格子）】
你必須將本案的 AI 落地規劃，完全映射進 Notion 4 個 Master Databases 中。請以 Markdown 表格呈現，並【100% 填寫所有屬性（列出所有欄位），絕不留下任何空白格子或空白欄位】：
  - 📋 主表一：場景盤點資料庫（屬性：業務痛點(Title)、主責部門、核心 AI 任務、商業價值評估(V)、數據就緒度評估(D)、一線使用阻力評估(R)、ROI 綜合評估指數、導入優先級決策）。
  - 📋 主表二：資料基礎與方案架構資料庫（屬性：對應場景專案、技術路徑選擇、核心模型配置、敏感資料防線、主動安全防禦、合規審計稽核）。
  - 📋 主表三：試點驗證與阻力評估資料庫（屬性：對應場景專案、試點部門與範圍、試點週期、Quick-Win 量化 KPI、一線員工主要阻力、變革管理化解方案）。
  - 📋 主表四：營運、治理與組織變革資料庫（屬性：對應場景專案、人機協作角色設計(HITL)、單月 API 財務告警閾值、持續維運分工(LLMOps)、技能升級與培訓、財務熔斷保護）。
  ※注意：這 4 張表必須完整覆蓋本案規畫的所有核心場景，將所有對應屬性的數據真實、詳細填入，不得寫「同上」、「無」或留空！
========================================================================
"""
    prompt_path = f"scripts/master_prompt_{client_name}.txt"
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(master_prompt)
        
    log_success(f"專屬 Master Prompt 已成功寫入：{prompt_path}")
    print("\n" + "="*80)
    print(f"\033[93m【機制就緒】請複製 {prompt_path} 內容貼入外部 LLM（如 Claude Fable 5 / GPT-5.5 Pro）\033[0m")
    print(f"運行產出後，請將 Markdown 覆蓋存檔於 scripts/proposal_{client_name}.md，然後在本地運行：")
    print(f"  \033[96mpython scripts/phoenix_b2b_pipeline.py compile --client {client_name}\033[0m")
    print("="*80 + "\n")

# ──────────────────────────────────────────────────────────────────────
# 階段二：一鍵編譯與同步發布
# ──────────────────────────────────────────────────────────────────────
def run_compile(client_name):
    proposal_path = f"scripts/proposal_{client_name}.md"
    if not os.path.exists(proposal_path):
        log_error(f"找不到顧問建議書檔案：{proposal_path}，請先將外部 LLM 產出貼回該檔！")
        sys.exit(1)
        
    log_info(f"啟動 [{client_name}] 一鍵編譯與 KM 發布流程...")
    
    # 設定環境變數強制使用 UTF-8
    my_env = os.environ.copy()
    my_env["PYTHONIOENCODING"] = "utf-8"
    my_env["PYTHONUTF8"] = "1"
    
    # 1. 呼叫 parse_md_to_json.py 從建議書中解析簡報配置
    log_info("解析 Markdown 建議書中的投影片配置...")
    config_path = f"scripts/slides_config_{client_name}.json"
    parse_cmd = [
        sys.executable,
        "scripts/parse_md_to_json.py",
        proposal_path,
        "-o", config_path
    ]
    result = subprocess.run(parse_cmd, capture_output=True, text=True, encoding="utf-8", env=my_env)
    if result.returncode != 0:
        log_error(f"投影片解析失敗：{result.stderr}")
        sys.exit(1)
        
    log_success(f"簡報配置 JSON 已順利提取：{config_path}")
    
    # 2. 自動讀取配置，動態更新 min_slides_required
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    slide_count = len(config.get("slides", []))
    config["min_slides_required"] = slide_count
    config["output_dir"] = f"slides/{client_name}"
    # 確保 client_badge 與 logo_text 補齊
    config["client_badge"] = f"{client_name.upper()} GROUP"
    config["logo_text"] = f"PHOENIX AI 顧問 x [{config.get('client_name', client_name)}]"
    config["audience"] = "internal"
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        
    log_info(f"配置優化完成！投影片實際共 {slide_count} 頁，已自動將最小限制調整為 {slide_count}。")
    
    # 3. 執行 validate_config.py 設定檔校驗
    log_info("運行設定檔格式校驗...")
    val_cmd = [
        sys.executable,
        "scripts/validate_config.py",
        config_path
    ]
    result = subprocess.run(val_cmd, capture_output=True, text=True, encoding="utf-8", env=my_env)
    if result.returncode not in (0, 3):
        log_error(f"設定檔驗證未通過：{result.stdout}\n{result.stderr}")
        sys.exit(1)
    log_success("設定檔雙引擎驗證通過！")
    
    # 4. 執行 compile_slides.py 編譯簡報
    log_info("編譯曜石 Midnight 高奢網頁簡報...")
    compile_cmd = [
        sys.executable,
        "scripts/compile_slides.py",
        config_path
    ]
    result = subprocess.run(compile_cmd, capture_output=True, text=True, encoding="utf-8", env=my_env)
    if result.returncode != 0:
        log_error(f"簡報編譯失敗：{result.stderr}")
        sys.exit(1)
    log_success(f"簡報編譯成功！成品已儲存於：slides/{client_name}/index.html")
    
    # 5. 同步離線專家案例庫 CSV
    log_info("同步本地離線 CSV 專家案例庫...")
    csv_path = "curriculum/unit_7_strategy/phoenix_ai_expert_cases.csv"
    
    with open(csv_path, "rb") as f:
        csv_content = f.read()

    # 專家案例對照表（用於 CSV 與 index.html 首頁案例牆動態寫入）
    CLIENT_CATALOG = {
        "okayama_forge": {
            "case_id": "PHX-CASE-2026-021",
            "industry": "精密機械與傳統製造",
            "title": "隆達精密冷鍛工業｜冷鍛模具磨損壽命預測與大師傅變革對齊案",
            "pain": "高速冷鍛過程中，沖頭與沖棒高速運作極易磨損開裂。3.2% 的高報廢率常導致單分鐘內產出數千顆瑕疵品，面臨歐洲車大客戶 BMW 高達百萬元的混料退貨客訴與索賠危機；且機電老舊缺乏高頻壓力感測數據，模型難以收斂。",
            "resistance_strong": "師傅抗拒與技術掏空：",
            "resistance_desc": "22年資深大師傅陳茂雄 (阿茂師) 抗拒手動登錄扭力與模具溫度，滿手油污無法平板打字；且擔心技術被 AI 掏空後被裁員，故意登錄假良率或殘缺數據，致 POC 夭折。",
            "solution_strong": "語音報工與技術入股：",
            "solution_desc": "陳策略長設計「非侵入式 ERP 唯讀副本緩衝對接」與「ASR 台國雙語語音報工系統」，徹底解決手沾油操作；孟顧問規劃「大師傅調鍛專家決策庫」專屬冠名與「技術股權及季度良率分紅合約」，利益與尊嚴對齊，並配置 API Loop Guard 算力財務熔斷。",
            "roi_items": [
                "模具異常停機率<strong>降低 75%</strong>",
                "螺帽冷鍛良率穩定控制在 <strong>99.5% 以上</strong>",
                "年省模具鋼材重置與廢料不良退貨損失高達 <strong>NT$ 140 萬</strong>"
            ],
            "scheme": "方案 B 一頁式戰術畫布實戰工作坊"
        },
        "okayama_heat": {
            "case_id": "PHX-CASE-2026-022",
            "industry": "精密機械與傳統製造",
            "title": "宏達熱處理工業｜AI 爐溫調度與機電硬熔斷防護會診案",
            "pain": "出口高強度螺絲熱處理製程（滲碳、淬火）中，爐內碳勢濃度與溫度控制失衡，常造成螺絲脆化斷裂。高層欲以 AI 進行爐溫智慧微調調度，卻因機電線路老舊經常 API 斷訊，且現場機電班長拒絕配合執行自動參數。",
            "resistance_strong": "員工起火安全恐憂：",
            "resistance_desc": "熱處理現場班長堅信「傳統看火色與爐壓」才是王道，擔心 AI 自動調溫出錯會引發熔爐起火或大批脆化斷裂的重大索賠責任糾紛，消極杯葛。",
            "solution_strong": "樹莓派離線與硬熔斷：",
            "solution_desc": "顧問團隊反對百萬機電全面重建，導入「本地輕量化工業樹莓派離線分析 API」與「實體硬繼電器雙軌熔斷器」硬體閉環，一旦 AI 溫度調度偏差超過信心值立即彈開熔斷，並配置班長一鍵否決按鈕與 0.5% 季度節能分紅。",
            "roi_items": [
                "規避高達 <strong>NT$ 110 萬</strong> 的熱處理電爐大洗牌重構預算",
                "高強度螺絲熱處理品質脆斷不良率降至 <strong>0% 零缺陷</strong>",
                "熱處理網帶爐電能與燃氣消耗降低 <strong>18% (年省電費近 NT$ 80 萬)</strong>"
            ],
            "scheme": "方案 C 企業 AI 內部治理與合規陪跑案"
        },
        "okayama_barcode": {
            "case_id": "PHX-CASE-2026-027",
            "industry": "精密機械與傳統製造",
            "title": "興達扣件包裝工業｜AI 視覺包裝複核與中高齡安心變革案",
            "pain": "螺絲包裝與出貨階段，常因客戶混料、規格印錯或出貨條碼貼錯導致退貨率達 3%，威脅外銷車規供應商資格。高層欲導入 AI 包裝視覺影像條碼複核系統，但包裝老員工手動複檢慢，影像資料缺損嚴重，POC 停擺半年。",
            "resistance_strong": "中高齡扣薪與操作恐懼：",
            "resistance_desc": "包裝老員工排斥複雜的平板與條碼掃描操作，強烈擔心操作慢或出錯會被扣薪甚至開除，採取故意遮擋鏡頭等杯葛手段。",
            "solution_strong": "極簡 UI 與防錯獎金：",
            "solution_desc": "孟顧問現場簡化操作為「紅綠燈自動拍照極簡防呆介面」；策略長設立「AI 防錯達標特別獎金」與總經理親簽「不裁員安心承諾書」，升任資深老員工為「AI 標記教練」。",
            "roi_items": [
                "出貨條碼貼錯與混料退貨率自 3% <strong>驟降至 0.02% 接近零失誤</strong>",
                "出貨包裝速度提升 <strong>120%</strong>",
                "因退貨索賠與重工包裝成本每年省下達 <strong>NT$ 110 萬</strong>"
            ],
            "scheme": "方案 C 企業 AI 內部治理與合規陪跑案"
        },
        "okayama_sbir": {
            "case_id": "PHX-CASE-2026-033",
            "industry": "精密機械與傳統製造",
            "title": "精密機械鍛造龍頭｜AI-Native 智慧製造升級暨 ISO 42001 治理案",
            "pain": "年營收 8.5 億之鍛造大廠，面臨歐洲車航客戶年底前通過 ISO 42001 認證大限，否則取消合約。且廠房高噪音、滿手油污使一線人員抗拒打字報工，資訊長擔心核心系統污染，財務長戒備算力帳單失控，專案卡在 POC 死亡谷。",
            "resistance_strong": "三方防線與操作障礙：",
            "resistance_desc": "師傅戴油污手套無法平板打字；資訊長防範寫入核心 ERP 污染數據；財務長防範 API 成本失控，拒絕放行算力預算。",
            "solution_strong": "語音報工與安全三閘：",
            "solution_desc": "部署邊緣 Realtime ASR 語音報工與台國雙語 VAD 降噪降偏，搭配 DLP 去識別化遮罩網閘與 ERP 唯讀緩衝、API 財務熔斷三閘架構，安全對接 SBIR 政策補助與產創研抵。人資端導入 HITL 問責與不裁員績效考核重組。",
            "roi_items": [
                "現場報工效率<strong>提升 ≥50%</strong>，年省大筆機會成本",
                "100% 確保企業製程機密不出廠且 ERP 核心系統零污染",
                "<strong>順利通過歐洲客戶 ISO 42001 稽核，成功護航數千萬外銷大單，對接補助與研抵抵減 5% 營所稅</strong>"
            ],
            "scheme": "方案 C 企業 AI 內部治理與合規陪跑案"
        },
        "okayama_cbam": {
            "case_id": "PHX-CASE-2026-023",
            "industry": "精密機械與傳統製造",
            "title": "吉翔航太扣件工業｜歐盟 CBAM 碳足跡大模型 RAG 與綠色業務變革案",
            "pain": "出口歐洲之航太級扣件廠面臨嚴厲的歐盟 CBAM（碳邊境調整機制）碳足跡申報稽核。業務部每次需手動彙整上千筆熱處理、電鍍與包裝之碳排放數據進行申報，工時嚴重超載且若計算錯誤將面臨最高年營業額 7% 的歐盟天價罰單或關稅處罰。",
            "resistance_strong": "業務防備與處罰恐懼：",
            "resistance_desc": "國外業務人員蔡嘉玲 (Candy) 與部門員工排斥複雜的碳排公式與稅則計算，強烈擔心公式算錯導致公司被罰會被扣薪開除，消極杯葛，寧可不接歐洲訂單。",
            "solution_strong": "CBAM大模型與合規提成：",
            "solution_desc": "陳策略長設計「CBAM 碳排大模型 RAG 快速助手」於地端直接解碼複雜歐洲稅則，自動生成免責數據模板；孟顧問規劃「綠色業務達標加薪機制」，將 CBAM 合規申報轉化為業務提成加分，提供標準免責防線並排除員工恐懼。",
            "roi_items": [
                "單次歐盟 CBAM 申報工時自 <strong>10 個工作天驟降至 4 小時</strong>",
                "100% 通過歐盟 CBAM 綠色碳稅外部稽核，成功護航 <strong>NT$ 5,000 萬</strong> 出口訂單無損通關",
                "業務部對 AI 導入支持率自 10% <strong>飆升至 95% 以上</strong>"
            ],
            "scheme": "方案 C 企業 AI 內部治理與合規陪跑案"
        },
        "okayama_filter": {
            "case_id": "PHX-CASE-2026-024",
            "industry": "精密機械與傳統製造",
            "title": "聯發光學篩選工業｜光學影像缺陷過濾與品管變革有人在環案",
            "pain": "高頻光學影像篩選機進行螺絲表面瑕疵分類時，因背景噪聲與表面沾有微量防鏽防蝕油污導致缺陷誤報率高達 15%。操作員每日需手動複檢海量誤報卡片，視覺極度疲勞，導致少數缺牙瑕疵流出，面臨美國特斯拉（Tesla）車廠客訴與 NT$ 180 萬賠償危機。",
            "resistance_strong": "品管反感與AI杯葛：",
            "resistance_desc": "品管課班長陳春桂（桂姐，待了 19 年）強烈排斥 AI 系統，認為 AI 胡亂報警是在給一線品管「添亂」、增加一倍工作量，極力要求關閉 AI 檢測模組。",
            "solution_strong": "偏見校準與標記教練：",
            "solution_desc": "陳策略長部署「雙向偏見校準與濾鏡優化 Pipeline」過濾表面油污陰影；孟顧問現場將手動複檢優化為「AI分流、有人審核（HITL）」SOP，並推動趙總總經理不裁員承諾，將桂姐升任「AI 資料標記教練」享有特別津貼與 Prompt 冠名權。",
            "roi_items": [
                "光學缺陷誤報率自 15% <strong>驟降至 1.2%</strong>",
                "徹底阻斷真缺陷外流客訴風險，成功護航 <strong>NT$ 1.5 億</strong> 扣件守門信譽",
                "現場品管複檢工時年省 <strong>1,600 小時 (省索賠成本 NT$ 180 萬)</strong>"
            ],
            "scheme": "方案 B 一頁式戰術畫布實戰工作坊"
        },
        "okayama_electroplate": {
            "case_id": "PHX-CASE-2026-025",
            "industry": "精密機械與傳統製造",
            "title": "振鑫表面防鏽工業｜電鍍配方優化、廢水排污達標與化學師特許分紅案",
            "pain": "螺絲表面防鏽鋅鎳合金電鍍良率與環保廢水排污難以平衡。若追求高鹽霧良率，電鍍液添加的重金屬化學藥劑濃度就會偏高，導致廢水重金屬超標被開罰，年累計處罰與改善預算高達 120 萬元。",
            "resistance_strong": "配方防備與數據作假：",
            "resistance_desc": "首席化學工程師高志明 (明哥，16年年資) 擔心獨門藥水配方被 AI 學會後會被公司裁員失業，故意在系統中登錄偏差、殘缺的 pH 與化驗日誌，使配方演算法失效。",
            "solution_strong": "特許分紅與專利配方庫：",
            "solution_desc": "陳策略長設計「IP 特許授權合約」，承諾良率與排污達標後明哥可享 0.5% 季度營運分紅紅利並撥入退休帳戶；孟顧問將系統正名為「明哥專利專家配方庫」，以尊嚴與利益對齊化解恐懼，成功收斂 LightGBM 配方與有人在環 (HITL) 雙簽安全網。",
            "roi_items": [
                "電鍍良率自 94% <strong>成功提升至 98.8%</strong>",
                "廢水排放 100% 符合環保法規，<strong>徹底規避年省 120 萬改善與處罰預算</strong>",
                "大師傅 16 年配方經驗<strong>完美收斂為地端數據資產</strong>"
            ],
            "scheme": "方案 A 企業專屬 AI 內訓專班"
        },
        "securities": {
            "case_id": "PHX-CASE-2026-032",
            "industry": "金融與專業保險",
            "title": "大型綜合證券商｜AI 營運安全治理與 Multiagent 研究報告防線案",
            "pain": "證券商受金管會極嚴苛監管，交易個資與資產明細極度機敏，依法絕對不上雲；且研究部門分析師每日編纂晨報與個股估值報告極耗工時且容易算錯數據，面臨巨大合規處罰風險與商譽壓力。",
            "resistance_strong": "員工與合規抗拒：",
            "resistance_desc": "研究員擔心 AI 潤飾使報告失去原創性，合規專員擔心 AI 投資建議與理財幻覺招致扣薪與法律追責，消極杯葛專案。",
            "solution_strong": "地端隔離與多代理人：",
            "solution_desc": "孟顧問引進分析師人機協作雙簽（HITL）權責；策略長部署地端開源 LLM 隔離沙盒與去識別化網閘，建置 Multiagent（規劃/執行/合規審查）自動化公會規範稽核流，並配置特許 Guardrails 禁忌詞物理熔斷、AML SHAP 可解釋性決策歸因與研抵節稅包裝。",
            "roi_items": [
                "全集團行政與合規審查工時效率<strong>提升 40%</strong>，年省機會成本達 <strong>NT$ 4,800 萬</strong>",
                "投顧投資幻覺違規率與洗錢防制（AML）漏報率<strong>降至 0% 零違規</strong>",
                "<strong>100% 確保數據不出防火牆且合規通過監管審計，匹配所得稅法研抵節稅</strong>"
            ],
            "scheme": "方案 C 企業 AI 內部治理與合規陪跑案"
        },
        "luzhu_coldheading": {
            "case_id": "PHX-CASE-2026-026",
            "industry": "精密機械與傳統製造",
            "title": "龍門冷鐓精密扣件｜高速冷鐓機崩死預警與一線運維免責保護傘會診案",
            "pain": "32 台高速冷鐓機組高速運轉中，沖頭與主滑塊微小磨損易在瞬時高溫高壓下卡死崩壞。單條產線停工達 3 天拆卸維修，導致年累計高達 NT$ 220 萬元的交期延誤賠償與重工損失，面臨大客戶索賠危機。",
            "resistance_strong": "電子皮鞭與操作抗拒：",
            "resistance_desc": "一線機電運維技術工陳建忠 (阿忠) 與組員排斥平板操作，抱怨手拿扳手不便打字；且認為 AI 異常警報是高層用來考核運維速度、限制休息的「電子皮鞭」，消極應對並故意登錄殘缺或混亂點檢結果，致 POC 夭折。",
            "solution_strong": "免責傘與一鍵防呆：",
            "solution_desc": "陳策略長設計「機電運維免責保護傘」制度，凡 AI 提前 2 小時預警者，後續崩損一律免除運維責任；孟顧問規劃「一鍵紅綠燈黑手防呆點檢介面」與指向性 ASR 國台語語音報工，搭配邊緣輕量化樹莓派離線運算與實體繼電器硬熔斷，徹底解除一線員工恐懼與操作阻力。",
            "roi_items": [
                "高速冷鐓機崩死停機率<strong>降低 80%</strong>",
                "一線運維人員系統主動配合度提升至 <strong>98% 以上</strong>",
                "每年規避停機維修、重工與交期索賠損失高達 <strong>NT$ 220 萬</strong>"
            ],
            "scheme": "方案 B 一頁式戰術畫布實戰工作坊"
        },
        "okayama_fastener": {
            "case_id": "PHX-CASE-2026-001",
            "industry": "精密機械與傳統製造",
            "title": "精密機械研究發展中心 (PMC) 專班課程 ➔ 前置諮詢預約",
            "pain": "高層盲目欲自建地端私有 RAG，面臨高額硬體年維護成本 (TCO) 與工廠資料雜亂幻覺。",
            "resistance_strong": "台語口語與技術掏空抗拒：",
            "resistance_desc": "現場資深調機課長茂雄師（王茂雄）與老技術工習慣台語口頭交班，排斥對平板打字輸入英文或簡體 AI 提示詞；且擔心技術被 AI 掏空後裁員，消極應對並散布 AI 系統監視監控論。",
            "solution_strong": "語音免打字與不裁員安心：",
            "solution_desc": "孟顧問現場推動總經理簽署不裁員安心承諾書並將系統正名茂雄師調鍛調機專家庫；陳策略長導入 Notion 結構化及 NotebookLM 輕量架構，搭配台國雙語 ASR 語音轉譯免打字介面，利益與尊嚴對齊，徹底規避首期伺服器硬體高昂維護預算。",
            "roi_items": [
                "成功攔截並節省地端伺服器首期維護預算達 <strong>NT$ 50 萬</strong>",
                "調機經驗檢索與排障效率大幅提升，工時年省 <strong>1,200 小時</strong>",
                "折算停工與調機廢料降低，創造年利潤機會回報高達 <strong>NT$ 240 萬</strong>"
            ],
            "scheme": "方案 B 一頁式戰術畫布實戰工作坊"
        }
    }

    client_zh = config.get("client_name", client_name)
    if "securities" in client_name or "finance" in client_name or "bank" in client_name:
        industry_zh = "金融與專業保險"
    elif any(k in client_name for k in ["okayama", "luzhu", "forge", "fastener", "heat", "cbam", "filter", "electroplate", "coldheading", "barcode", "sbir", "dingsheng"]):
        industry_zh = "精密機械與傳統製造"
    else:
        industry_zh = "零售與連鎖餐飲"

    cat = CLIENT_CATALOG.get(client_name, {})
    case_id = cat.get("case_id")
    
    # 針對全新或未預定義的企業進行動態 fallback
    if not case_id:
        lines = csv_content.decode("utf-8", errors="replace").splitlines()
        case_id = f"PHX-CASE-2026-{len(lines):03d}"
        cat = {
            "case_id": case_id,
            "industry": industry_zh,
            "title": f"{client_zh}｜B2B AI 落地安全治理與轉型升級案",
            "pain": f"{client_zh}在 AI 落地過程中面臨核心製程優化、一線員工操作排斥與數據隱私合規之綜合挑戰，亟需建立高效、安全的落地治理架構。",
            "resistance_strong": "變革抗拒：",
            "resistance_desc": "一線技術工與中階管理層排斥複雜系統操作，擔心個人經驗流失被取代或操作出錯招致懲處扣薪，採取消極被動杯葛。",
            "solution_strong": "地端安全與利益對齊：",
            "solution_desc": "孟顧問設計變革五部曲與只加不減獎勵機制，利益對齊人性；陳策略長部署地端隔離運算與非侵入式讀寫隔離，建立信心值熔斷器與人機雙簽問責鏈保護。",
            "roi_items": [
                "關鍵製程指標與工時效率<strong>提升 30% 以上</strong>",
                "一線員工系統配合度與滿意度<strong>提升至 90% 以上</strong>",
                "<strong>100% 確保數據隱私與核心安全，安全對接政策申報與研抵減稅</strong>"
            ],
            "scheme": config.get("scheme", "方案 B 戰術畫布實戰工作坊")
        }

    # 檢查是否已存在該案例，避免重複寫入
    csv_str = csv_content.decode("utf-8", errors="replace")
    if case_id in csv_str:
        log_info(f"專家案例卡片 {case_id} 已存在於 CSV 資料庫中，跳過重複同步。")
    else:
        lead_in = cat.get("lead_in", "CEO直接評量 ➔ 方案 C 治理套件 + 方案 B 戰術工作坊")
        pain = cat.get("pain").replace("\n", " ").replace('"', '""')
        resistance = (cat.get("resistance_strong") + cat.get("resistance_desc")).replace("\n", " ").replace('"', '""')
        solution = (cat.get("solution_strong") + cat.get("solution_desc")).replace("\n", " ").replace('"', '""')
        roi = " | ".join([item.replace("<strong>", "").replace("</strong>", "") for item in cat.get("roi_items")]).replace('"', '""')
        scheme = cat.get("scheme")
        summary = f"為{client_zh}量身客製 AI 落地與變革方案。針對一線操作痛點與資安合規大限，導入地端輕量分析與實體安全閉環。透過利益對齊的人社激勵化解抗拒。最終實現工時效率顯著提升，100% 確保機密不出廠且核心系統零污染，成功護航外銷大單並對接研抵租稅抵減。"
        
        new_csv_row = f'{case_id},{cat.get("industry")},{lead_in},"{pain}","{resistance}","{solution}","{roi}",{scheme},"{summary}"\n'
        
        needs_newline = False
        if csv_content and not csv_content.endswith(b'\n') and not csv_content.endswith(b'\r'):
            needs_newline = True
            
        with open(csv_path, "ab") as f:
            if needs_newline:
                f.write(b'\n')
            f.write(new_csv_row.encode("utf-8"))
        log_success(f"已成功同步 Case 卡片 {case_id} 至 CSV 資料庫！")
    
    # 6. 靜態更新 index.html 首頁案例牆 (更替為 Case 4 顯示)
    log_info("更新官網 portal 首頁案例牆 (Card 4)...")
    portal_path = "index.html"
    with open(portal_path, "r", encoding="utf-8") as f:
        html = f.read()
        
    start_tag = '<!-- 案例 4:'
    if start_tag in html:
        start_idx = html.find(start_tag)
        end_tag = '<!-- 線上修改提示與白皮書 CTA -->'
        end_idx = html.find(end_tag)
        card_end = html.rfind('</div>', start_idx, end_idx)
        card_end_with_tag = card_end + 6
        
        roi_list_html = "\n".join([f'                <li class="case-roi-item">{item}</li>' for item in cat.get("roi_items")])
        
        new_html_card = f"""<!-- 案例 4: {cat.get("industry")} ({case_id}) -->
        <div class="case-card">
          <div class="case-header">
            <div class="case-id-badges">
              <span class="case-id">{case_id}</span>
              <span class="case-tag">{cat.get("industry")}</span>
            </div>
            <h3 class="case-title">{cat.get("title")}</h3>
          </div>
          <div class="case-divider"></div>
          <div class="case-body">
            <div class="case-section">
              <span class="case-section-title">🛑 業務痛點與挑戰</span>
              <p class="case-section-content">
                {cat.get("pain")}
              </p>
            </div>
            <div class="case-section">
              <span class="case-section-title">⚡ 一線阻力與顧問解法</span>
              <ul class="case-list">
                <li class="case-list-item"><strong>{cat.get("resistance_strong")}</strong>{cat.get("resistance_desc")}</li>
                <li class="case-list-item solution"><strong>{cat.get("solution_strong")}</strong>{cat.get("solution_desc")}</li>
              </ul>
            </div>
            <div class="case-roi-box">
              <span class="case-roi-title">📈 量化落地成效 (ROI)</span>
              <ul class="case-roi-list">
{roi_list_html}
              </ul>
            </div>
          </div>
          <div class="case-footer">
            <div class="case-target-scheme">
              <span class="scheme-label">對標建議方案</span>
              <span class="scheme-value">{cat.get("scheme")}</span>
            </div>
            <a href="https://docs.google.com/forms/d/e/1FAIpQLSfGlE4m-Tgg2AXcIGRy90jNuroTnt8ZGwB8r0E35msJIPw_xA/viewform" target="_blank" class="case-btn">
              📥 閱讀完整案例分析 (PDF)
            </a>
          </div>
        </div>"""
        
        new_html = html[:start_idx] + new_html_card + html[card_end_with_tag:]
        with open(portal_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        log_success("首頁 index.html 案例牆 Card 4 靜態部署完成！")
    else:
        log_error("首頁 index.html 中未找到 Card 4 標籤定位！")


    # 7. 執行 Markdown CI 驗證
    log_info("執行全域 Markdown 規格 CI 檢驗...")
    md_cmd = [sys.executable, "scripts/validate_markdown.py"]
    subprocess.run(md_cmd)
    
    # 8. 執行反向個資洩漏掃描
    log_info("執行編譯成品 DLP 個資洩漏反向掃描...")
    scan_cmd = [
        sys.executable,
        "scripts/de_identify_local.py",
        "scan",
        f"slides/{client_name}/"
    ]
    subprocess.run(scan_cmd)
    
    # 9. 執行 Git 提交與 Push
    log_info("執行 Git 安全 Commit 與 PUSH 流程...")
    try:
        # 只 Stage 公開與去識別化成品，安全排除原始敏感檔
        subprocess.run(["git", "add", csv_path, portal_path, config_path, proposal_path], check=True)
        commit_msg = f"feat(b2b): execute dynamic B2B pipeline & slides compile for [{client_name}]"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        log_success("一鍵 B2B 自動化發布完全成功！遠端 GitHub 倉庫已綠燈同步。")
    except subprocess.CalledProcessError as e:
        log_error(f"Git 提交過程中發生錯誤：{e}")
        
    print("\n" + "="*80)
    print(f"\033[92m👑 【B2B SOP 閉環完成】\033[0m")
    print(f"1. 顧問建議書位置：{proposal_path}")
    print(f"2. 奢華網頁簡報首頁：slides/{client_name}/index.html")
    print(f"3. 離線專家資料庫：{csv_path} (已同步 Case 卡片)")
    print(f"4. 官網首頁 UI：index.html (已部署動態去識別案例)")
    print("="*80 + "\n")

# ──────────────────────────────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 強制設定 UTF-8 輸出
    if sys.platform.startswith("win"):
        import sys
        sys.stdout.reconfigure(encoding="utf-8")
        
    parser = argparse.ArgumentParser(description="鳳凰 AI B2B 顧問簡報/KM 全自動化營運工具")
    subparsers = parser.add_subparsers(dest="action", required=True)
    
    # Init 子命令
    init_parser = subparsers.add_parser("init", help="啟動新案診斷、本地去識別化，並生成專屬動態 Master Prompt")
    init_parser.add_argument("--client", required=True, help="客戶縮寫，如 securities, tea")
    init_parser.add_argument("--raw", required=True, help="原始來信信件 TXT 路徑")
    
    # Compile 子命令
    compile_parser = subparsers.add_parser("compile", help="一鍵解析建議書 Markdown、驗證、編譯簡報、同步 KM 資料庫與推送 GitHub")
    compile_parser.add_argument("--client", required=True, help="客戶縮寫，如 securities, tea")
    
    args = parser.parse_args()
    
    if args.action == "init":
        run_init(args.client, args.raw)
    elif args.action == "compile":
        run_compile(args.client)
