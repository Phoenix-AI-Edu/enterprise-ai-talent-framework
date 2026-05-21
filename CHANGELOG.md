# CHANGELOG: 2026 企業 AI 人才培育開源專案

本文件記錄「2026 企業 AI 人才培育開源專案」教材重構、自動化校對與開源工程的變更歷史。

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

