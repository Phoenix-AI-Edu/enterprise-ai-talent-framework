# Experience Portal 開工前 Go/No-Go Checklist

本文件定義了 `/experience` (AI 解決方案體驗區) 在正式動工前的「最後控制點」與「標準化實作流程」。這能確保程式開發不會產生資安漏洞、行銷災難，或破壞既有商業漏斗。

---

## 🛑 第一階段：開工前置盤點 (Pre-flight Checks)

在建立任何 HTML 或分支之前，必須完成以下稽核，且由相關負責人 (Owner) 簽核確認：

### D-1: Analytics Audit (數據追蹤稽核)
主站近期已有 GA4 / CTA event 的更新。在體驗區新增追蹤前，需確認：
- [ ] 盤點現有主站的 `dataLayer.push` 或 `gtag('event')` 命名規則與欄位結構。
- [ ] 定義體驗區的專屬事件名稱，需與主站對齊 (例如：`experience_solution_view`, `experience_demo_request_click`)。
- [ ] **資安紅線**：確認 Analytics Payload 中絕對不包含使用者的 PII (個人可識別資訊，如明碼 Email、真實姓名)。

### D-1.5: 跨部門素材去識別化審核 (De-identification Sign-off)
為確保首發「中央廚房 AI 營運助理」方案不洩漏商業機密，各產出物需由專責角色確認：
- [ ] **Researcher (研究員)**：審查產業描述、成效說法，確保外部事實不誇大。
- [ ] **Social / 行銷**：審查對外文案、截圖、Mockup，確認未洩漏真實客戶名稱、LINE ID 或機密資料。
- [ ] **BD (業務)**：審核表單欄位、CTA 動線、以及「個資蒐集同意文字」。
- [ ] **Developer (開發者)**：審核靜態資源的原始碼，確保未混入任何正式 API Key。

> **Go / No-Go 決策點**
> 只有上述 D-1 與 D-1.5 的核取方塊全數打勾，專案負責人才能授權進入 D0 開發。

---

## 🛠️ 第二階段：嚴謹的實作流程 (Execution Flow D0-D6)

取得授權後，開發人員應嚴格遵循以下順序施工：

### D0：隔離開發環境
- [ ] **建立專屬分支**：嚴禁在 `main` 直接施工，必須使用 `git checkout -b feature/experience-portal` 進行開發。

### D1：建立基礎架構
- [ ] 建立 `experience/` 目錄。
- [ ] 撰寫靜態的總覽大廳頁面 (`index.html`)。
- [ ] 建立包含治理欄位 (如 `maturity`, `complianceNote`) 的資料模型 (`solutions_data.js`)。

### D2：實作旗艦方案介紹頁
- [ ] 建立 `experience/central-kitchen-ai-agent/index.html`。
- [ ] 置入已通過 D-1.5 審核的去識別化文案與靜態 Mockup 截圖。

### D3：建立主站無害導流
- [ ] **首頁中段 Banner**：在快測與顧問方案之間插入「低干擾」Banner。
- [ ] **Footer 連結**：在頁尾區塊加入靜態入口。
- [ ] **禁止動作**：絕對**不更動 Navbar**，不搶奪主漏斗的權重。

### D4：安全的 CTA 實作
- [ ] 所有的「申請 Demo」按鈕，必須串接**真實有效**的表單連結，或直接導向主站既有的「預約諮詢」區塊。
- [ ] **禁止動作**：絕不使用 `https://forms.gle/YOUR_FORM_ID` 這種假網址上線。

### D5：埋設追蹤代碼
- [ ] 依據 D-1 盤點結果，植入標準化的事件追蹤程式碼。
- [ ] 再次確認沒有寫入任何 PII 個資。

### D6：本機全盤驗證
在 Commit 之前，於本機 (`localhost:8000`) 執行最終驗證：
- [ ] 檢查 RWD (響應式設計) 在手機與桌機的表現。
- [ ] 點擊所有 CTA，確認跳轉邏輯正確且無死結。
- [ ] 使用 `git diff` 審查所有變更，確保無敏感檔案被混入。
- [ ] 確認完成後，提交 PR (Pull Request) 合併回 `main`。
