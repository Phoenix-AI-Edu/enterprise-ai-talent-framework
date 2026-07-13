# Asset Production List (展示素材與影片生產清單)

- **專案名稱**：`phoenix-auditable-ai-flow`
- **文件狀態**：**`W0/W1 DRAFT - READY FOR OWNER REVIEW`**
- **最新更新**：2026-07-13

本清單列出官網第三張系統詳情頁所需的所有視覺素材、影片展示及規格說明，確保上線產物符合開源合規與去識別化安全標準。

---

## 視覺與影片素材清單 (Assets List)

### 1. 三系統落地能力鏈架構圖 (Three-System Architecture Diagram)
- **檔案類型**：SVG (向量圖，便於縮放與載入速度)。
- **寬高尺寸**：800 x 400 px。
- **內容規格**：展示由「中央廚房（場景落地）」→「顧問工作台（問題診斷）」→「Auditable AI Flow（技術與稽核證據底座）」組成的 Phoenix AI 落地方法論能力鏈，不得暗示為單一合併系統。

### 2. 六階段工作流圖 (Six-Step Workflow Diagram)
- **檔案類型**：SVG。
- **寬高尺寸**：1024 x 256 px。
- **內容規格**：以可及的 HTML／CSS 圖表呈現 Input Policy、Markdown Knowledge、Mock Model、Output Policy、HITL 人工判定與 SQLite 稽核事件紀錄；不得暗示外部 LLM 或正式資料庫整合。

### 3. 本地 Demo 執行截圖 (Local Rehearsal Screenshots)
- **檔案數量**：4-6 張。
- **檔案格式**：WebP (優化體積)。
- **截圖規格**：
  - `screenshot_01.webp`：展示輸入/輸出政策之設定檔與政策衝突警告。
  - `screenshot_02.webp`：展示當提問觸發人工審批時，操作台的審查等待狀態。
  - `screenshot_03.webp`：展示人工核准（Approve）與駁回（Reject）決策點。
  - `screenshot_04.webp`：展示依 `request_id` 查詢本機 SQLite 稽核事件與時間戳記，並標示不具密碼學不可竄改保證。
- **安全要求**：截圖中只使用合成 HR 資料與 `.example` 網域，禁止洩漏私有倉庫路徑、真實金鑰或開發路徑。

### 4. 60–90 秒操作錄影 (Demo Walkthrough Video)
- **檔案格式**：MP4 (H.264 / AAC, Web 優化)。
- **解析度**：1080p (1920 x 1080)。
- **時長**：75 秒。
- **腳本大綱**：
  - **00-15 秒**：顧問登入，輸入一個日常 HR 休假提問，展示政策快速核對與正常回答。
  - **15-40 秒**：輸入衝突差旅申報提問，畫面上彈出紅框政策衝突警告，系統自動進入等待人工審批狀態。
  - **40-60 秒**：顧問演示人工覆核操作，核准該提問，展示系統將答案釋出。
  - **60-75 秒**：依 `request_id` 檢視 SQLite 稽核事件，展示可查詢的流程軌跡與本機參考架構限制。

### W2 初版媒體決策

W2 首版以可鍵盤操作、含完整文字說明的「75 秒互動導覽」取代自動播放影片，原因為：

- 不需下載大型 MP4，改善手機載入；
- 不依賴聲音或動畫即可理解；
- 每一步能直接對照公開程式碼行為；
- 不會誤拍本機路徑或開發環境資訊。

MP4 保留為後續行銷素材，不是本次技術發布阻擋；製作時仍須遵守本清單的安全規格。

---

## 素材安全與合規查核要點 (Compliance & Security Checklist)
- [ ] 無真實客戶敏感資料與名稱。
- [ ] 無 `phoenix-ai-microservice` 私有開發目錄字樣。
- [ ] 無真實 email (`northstar.com`) 與內網 IP 洩漏。
- [ ] 影片完播率設定 GTM/GA4 事件追蹤點（25%, 50%, 75%, 100%）。
