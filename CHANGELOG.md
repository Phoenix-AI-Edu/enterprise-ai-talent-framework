# CHANGELOG: 2026 企業 AI 人才培育開源專案

本文件記錄「2026 企業 AI 人才培育開源專案」教材重構、自動化校對與開源工程的變更歷史。

---

## [Unreleased] - 2026-07-27

### Fixed
- **官網敘事一致性修正（EVT-194，2026-08-12，CEO 授權）**
  - 來源：雙主戰線草案審查（Social 發現官網與產品憲章/草案禁語衝突）
  - `experience/solutions_data.js`：AI 律師工作台 subtitle「期限不漏」→「期限紅線集中管理」；status「PoC Reference」→「Synthetic Demo」；maturity「Synthetic Reference」→「Synthetic Demo Ready」；compliance_note 自曝語句改為「展示採合成案件／流程；正式導入依客戶環境、權限與驗收規格完成。AI 草稿須經律師覆核；不宣稱勝訴率或零錯誤保證，不取代律師最終法律判斷。」
  - `experience/ledger-assist/index.html`＋`scripts/build_solution_pages_20260809.py`（生成腳本同步）：「自動核准依 GA、租戶與憑證類型分階段開放」→「自動化範圍與覆核政策於導入階段評估；正式覆核與匯出權限保留於事務所」（與人工覆核常數對齊）
  - 驗證：`node --check experience/solutions_data.js` PASS；公開頁無「期限不漏」「PoC Reference」「開放自動核准」殘留
  - 治理：Owner 裁決紀錄 → `Obsidian/00_Inbox/Phoenix-AI-Dual-Front-Strategy-REVIEW-2026-08-12.md`；同步狀態標 `sync_pending` 待 Obsidian CHANGELOG 回寫


### Fixed
- **修正全站分享圖 `assets/og-image.png` 中文亂碼（2026-08-10）**
  - 根因：8/5 SEO 統一時以 AI 生成品牌圖，AI 將繁體中文烤成亂碼：主標題「鳳凰」變「鳳龍」、tagline「企業 AI 落地・診斷・治理」變「企業 AI 癥応・診務・詰詛」、英文 Phoenix 被切斷。
  - 修法：保留左側金色鳳凰圖案，以微軟正黑體 + PIL 程式重繪右側文字區（鳳凰 AI 顧問 / Phoenix AI Consulting / 企業 AI 落地・診斷・治理）；背景依原圖漸層逐欄重建，無色塊接縫。
  - 驗證：vision 逐行文字正確、鳳凰完整、無殘留舊字、無色差（全站 og:image / twitter:image 共用此檔，一併修正）。

### Added
- **Enterprise RAG Foundation 官網上架（Phase 1）**
  - 規劃：`docs/RAG_FOUNDATION_SITE_INTEGRATION_PLAN.md`
  - 服務落地頁：`services/enterprise-rag-foundation.html`
  - 新企業交付檢查表：`services/enterprise-delivery-checklist.html`
  - 體驗詳情：`experience/enterprise-rag-foundation/index.html`
  - 旗艦註冊：`experience/solutions_data.js` 第 4 項
  - contact：`rag_foundation_demo` / `rag_foundation_assessment`
  - 首頁導覽「企業 RAG」；旗艦區顯示最多 4 卡；M05 導流至服務頁
- 文案與能力邊界對齊 Private 產品庫 Foundation **1.0.0**（synthetic；非客戶 production）

### Added
- **SEO meta 統一指向 03king.com（PR #7）**
  - 12 個公開頁面注入 canonical + og:url/og:image + twitter:card(summary_large_image)
  - 清除 phoenix-ai-edu.github.io 殘留引用 4 處（experience/phoenix-auditable-ai-workflow、services/enterprise-rag-foundation）
  - 新增 1200x630 品牌分享圖 `assets/og-image.png`（03king.com/assets/og-image.png）
  - 注入器置於 repo 外 `~/scripts/seo_meta_inject.py`（dry-run 先行、逐檔 .bak-seo 備份）

### Changed
- **DEC-021 套用**：服務名鎖定「**鳳凰企業 RAG Foundation 導入服務**」；移除 provisional；主 CTA 統一「預約 30 分鐘評估」；明確不公開標價；旗艦 pilot 指向 assessment。

### Notes
- 未將 RAG 執行時／後端／客戶資料納入本靜態站（符合 EXPERIENCE_BOUNDARY）

---

## [1.3.0] - 2026-05-31

### 🚀 新增 (Added)
- **「CodeGraph (Tree-sitter) 本地圖譜實戰教學案例」** (`curriculum/unit_6_generative_ai/curriculum_v2026.md`)：
  - 於單元六 MCP（Model Context Protocol）章節中新增 CodeGraph 本地優先代碼智慧圖譜實戰案例。
  - 解析 AI 開發代理面臨的 Token 暴燒與代碼安全痛點，引證 Tree-sitter AST 解析與 SQLite 本地圖譜的技術本質，並提供標準 JSON-RPC 通訊 Schema 及 CLI 部署 SOP，展示降低 90% 代碼探索成本的商業變革價值。
- **「本地技術除錯與開發備忘日誌」** (`internal_admin/09_dev_troubleshooting_log.md`)：
  - 專門為開發團隊與未來 AI 助手建立的高規格技術日誌範本。
  - 整理當前系統底層依賴基準，並錄入「LaTeX 數學定界符誤判預處理去噪」與「Slides 編譯相對路徑絕對化」兩大實戰 Bug 排障與防範因應記錄。

### ✏️ 修改 (Changed)
- **修正單元六教材代碼區塊語法衝突** (`curriculum/unit_6_generative_ai/curriculum_v2026.md`):
  - 移除 L139 冗餘的 python 代碼標記，使 LangGraph 狀態圖代碼區塊（L144-L277）完美閉環，徹底消除 H1 標題檢測誤判與 LaTeX 定界符不平衡的 18 個編譯 Error，成功實現單元六 Markdown Linter **100% 全數通過，0 錯誤**。

---

## [1.2.0] - 2026-05-21

### 🚀 新增 (Added)
- **「4+1 企業 AI 戰略畫布 Notion 互動模板規格指南」** (`curriculum/unit_7_strategy/notion_template_guide.md`)：
  - 依據「雙軌商業化」策略，將單元七「4張主表 + 1張總表」的 Markdown 版畫布全面升級為 Notion 資料庫架構。
  - **主表一（場景盤點 DB）**：設計含商業價值、數據就緒度與使用阻力三維加權的 Notion Formula 2.0 `ROI 綜合評估指數`公式，以及自動輸出 ⭐⭐⭐ 優先級決策的`導入優先級決策`公式。
  - **主表二（資料基礎與安全防線 DB）**：對應 ISO/IEC 42001 安全標準，設計技術路徑（Buy vs. Build）、大模型配置、DLP 防護、Prompt Injection 主動偵測，以及 Audit Trails 審計稽核的完整欄位。
  - **主表三（試點驗證與變革管理 DB）**：設計 Quick-Win KPI 量化欄位、多選式一線員工阻力識別欄位，以及對應「恐懼感化解策略」的心理學層面變革管理欄位。
  - **主表四（營運治理與 HITL 協作 DB）**：定義 Autonomous / Copilot / Validator 人機協作角色配置，設計單月 API 財務告警閾值欄位與 LLMOps 維運分工欄位。
  - **總表（企業 AI 一頁式總體戰略儀表板）**：提供 Notion Relation 資料庫聯結配置方法、Markdown 版會議直呈模板，以及 Miro 跨部門共創工作坊 3 步驟落地執行手冊。

### ✏️ 修改 (Changed)
- **入口官網首頁 B2B 商業化全面重塑** (`README.md`):
  - **語言風格精準化**：全面修正「硬核」、「全面揚棄」、「鐵律」等行銷煽情詞彙，替換為「核心知識模組」、「升級並對接」、「導入實務原則」等嚴謹的 B2B 管理顧問用語，全面提升企業決策層的信任感。
  - **數據引證補強**：融入 Gartner 2026 年最新報告（僅 27% 高階主管具備完整 AI 策略，僅 20% 員工達到 AI Readiness；2027 年缺乏以人為中心策略的企業恐失去 50% AI 人才）與 McKinsey 的 POC 失敗率統計，建立對企業採購方的公信力。
  - **三大 B2B 服務方案明確化**：
    - **方案 A（15 小時菁英培訓專班）**：完全對接「經濟部 115 年度企業專區 AI 人才培育輔導計畫」，輔助申請 15 ~ 30 萬元政府補助款。
    - **方案 B（企業 AI 一頁式戰略畫布工作坊）**：3 小時至 2 天半封閉式共創，交付 CEO 可直接呈報董事會的總體戰略藍圖，建議費用 5 ~ 20 萬元。
    - **方案 C（ISO/IEC 42001 合規前期輔導）**：針對金融、製造、醫療等高隱私合規行業，提供 NIST AI RMF Gap Analysis、DLP 標準流程建置與 LLM API 熔斷監控配置，每月費用 10 ~ 30 萬元。
  - **雙重 CTA 成交設計**：置入「免費索取 Notion 互動模板工具包」（行銷鉤子，換取 Email）與「預約免費 30 分鐘企業 AI 導入線上診斷諮詢」（限額 5 名/週）兩個強力成交入口。
  - **AI 自動維運說明移位**：將「Powered by AG-2.0」徽章與 Gemini + ANTIGRAVITY 2.0 雙 AI 聯動架構說明，從首頁主視覺移往底部「專案技術架構與 AI-Native 自動化維運」獨立章節，降低對 B2B 買家決策干擾，同時保留技術底氣的 Proof of Concept 展示。
- **單元七學習指引更新** (`curriculum/unit_7_strategy/README.md`):
  - 在核心教材跳轉連結下方，新增至 `notion_template_guide.md` Notion 互動模板規格指南的直接跳轉引導連結。

### 🔬 驗證 (Verified)
- 本地自動化 Markdown Linter 校對：`python scripts/validate_markdown.py` 執行結果 **16 個檔案全數通過，0 錯誤，0 警告**。
  - 驗證範圍涵蓋全新建立的 `notion_template_guide.md` 以及重構後的 `README.md`。

---

## [1.1.0] - 2026-05-21


### 🚀 新增 (Added)
- **單元一至單元七硬核教材長文編譯** (`curriculum/`):
  - **單元一 (AI 基礎理論)**：編譯千字講義，涵蓋 Transformer 自注意力、高維 Embedding、Tokenizer 與 DPO 數學本質。
  - **單元二 (10 大產業應用)**：拆解企業級 RAG、多模態生成、客服分流等 10 大實戰模組。
  - **單元三 (負責任的 AI 應用)**：依據 NIST AI RMF 與 ISO/IEC 42001 建立隱私遮罩、Guardrails 防護欄與審計日誌。
  - **單元四 (機器學習技術理論)**：完整梳理監督、非監督、強化學習與模型驗證指標，融入半導體與金融預警實務。
  - **單元五 (鑑別式 AI 與控制層)**：深入 ResNet、YOLO 卷積網路，解構混淆矩陣、IoU，並包含 Flask 門禁影像辨識路由實作。
  - **單元六 (生成式 AI 與多代理人系統)**：解碼 DPO 損失函數，建構 Planning/Execution/Review 的 Multiagent 協作工作流，並引進 2026 Model Context Protocol (MCP) 協定。
  - **單元七 (AI 導入與營運策略)**：重構 AI Operating Model 四大支柱，提供「4張主表 + 1張總表」整合規劃畫布包，並解析變革管理 (Change Management) 製造業瑕疵分類情境題。
- **自動化校對系統** (`scripts/validate_markdown.py`):
  - 建置本地 Python Linter，自動校對 H1 標題階層、LaTeX Delimiter (`$`, `$$`) 平衡性、以及專有名詞大小寫規範。
  - 成功過濾 inline/block code 反單引號，預防數學公式平衡性誤判。
- **CI/CD 自動化工作流** (`.github/workflows/lint.yml`):
  - 建立 GitHub Actions 工作流，在每次 Push 或 PR 時自動啟動 Python Container 執行 Linter 校對，確保開源教材 100% 零缺陷。
- **GitHub 遠端儲存庫推送**:
  - 配置 `git remote` 並成功推送 `main` 分支至 GitHub Organization 官方儲存庫：`https://github.com/Phoenix-AI-Edu/enterprise-ai-talent-framework`。
  - 使用 `git filter-branch` 重寫 commit 歷史，確保作者署名與 Email 統一為專案負責人 `陳文家 (鳳凰AI)` 及其官方帳戶 `allmyway2007@gmail.com`。

---

## [1.0.0] - 2026-05-21

### 🚀 新增 (Added)
- **專案規格書轉換**：將 Google Docs 格式的專案規劃規格書正式轉換為 Markdown 格式，並存入雲端同步根目錄下的 `README.md` 作為唯一信任源。
- **教材目錄結構初始化**：
  - 建立主教材目錄 `curriculum/`。
  - 依照規格書結構建立 7 個單元子目錄（`unit_1_theory` 到 `unit_7_strategy`）。
  - 在各單元下建置具備學習目標、核心知識模組、課後思考題的初始 `README.md` 教材模板。
- **版本變更記錄**：初始化專案根目錄的 `CHANGELOG.md`。

---

> [!NOTE]
> 本日誌將配合自動化 Markdown 校對與 GitHub CI 部署持續更新。

