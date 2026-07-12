# AI 解決方案體驗區 (AI Solutions Showcase) 規劃書

## 1. 核心策略：體驗區與主站解耦 (Decoupled Architecture)

為了保護 `AI_Talent` 既有的顧問平台銷售漏斗，我們不將互動型 AI 系統直接混入靜態的 `cases` 模組。
我們將採用 **「靜態入口導流，動態系統外部化部署」** 的策略。

```text
主站 (AI_Talent) --> /experience 靜態入口 --> 外部獨立的 Demo App 網址
```

---

## 2. 實作架構設計

我們在主站中僅建立一層極輕量的靜態目錄，**嚴禁放入任何後端程式碼、DB 或原始碼**。

```text
AI_Talent/
  experience/
    index.html                 # 體驗大廳首頁 (列出所有解決方案)
    solutions_data.js          # 資料模型 (定義卡片資訊與導流連結)
    central-kitchen-ai-agent/  # 第一個解決方案的獨立介紹頁 (Solution Page)
      index.html               # 放置痛點、解法、影片、架構圖
      assets/                  # 本機圖檔與影片素材
```

### 互動系統的外部部署
真正的系統 (如 FastAPI 引擎與 SQLite DB) 將獨立部署於外部平台：
- **示範網址**：`https://demo.ai-talent.example` (部署於 Cloud Run / Render 等)
- **銜接方式**：訪客在 `central-kitchen-ai-agent/index.html` 閱讀完產品簡介後，點擊「前往互動體驗」，才跳轉至外部的 Demo App。

### 商業層指標追蹤 (Business Metrics)
作為獲客漏斗的一環，`experience` 入口站必須設定分析與追蹤機制：
1. **訪客數 (Page Views)**：各解決方案的曝光流量。
2. **表單轉換率 (Lead Gen Rate)**：填寫信箱以獲取 Demo 密碼的比例。
3. **Demo 申請數**：跳轉至外部互動系統的點擊次數。
4. **預約諮詢數**：體驗完 Demo 後，回到主站填寫「預約顧問諮詢」的數量。

---

## 3. 中央廚房營運防護台：首發旗艦方案上架草案

作為 `/experience` 的第一個 Flagship Solution，其對外公開的描述將嚴格遵守「示範性質與去識別化」原則。

- **解決方案名稱**：中央廚房營運防護台
- **適用產業**：餐飲連鎖 / 中央廚房 / 零售連鎖
- **方案狀態**：公開沙盒示範（可申請操作 Demo）
- **展示重點**：
  - 門市查詢訂單與庫存
  - 高風險操作攔截與人工審核
  - 沙盒 ERP/POS payload 預覽
- **能力邊界**：LINE 流程屬 PoC 可配置項；正式 ERP/POS 寫入、SSO、地端部署與進階稽核皆屬導入階段評估。
- **🚫 避險文案規範**：
  - 絕不提及「已替某客戶省下多少成本」或「已上線某知名品牌」。
  - 絕不聲稱「已完成真實系統串接」；公開頁僅能描述 sandbox payload 預覽。

後續工具應依 [`experience/TOOL_PUBLISHING.md`](../experience/TOOL_PUBLISHING.md) 提交資料與經過發布檢核後，才可進入體驗區或首頁。

---

## 4. 階段性開發時程 (Execution Phases)

請嚴格遵循以下順序，切勿跳階執行，以確保平台穩定：

- **Phase A (現在)**：只產出這份規劃書與邊界定義。
- **Phase B**：產出 `AI_Talent` 移轉計畫書。
- **Phase C**：依照移轉計畫，將 `AI_Talent` 從 Google Drive 搬移至本機 `C:\Users\m1016\Documents\AI_Talent` 並建立 GitHub Private Repo。
- **Phase D**：在全新的本機 Repo 中，開始刻劃 `/experience` 的靜態入口頁面。
- **Phase E**：將中央廚房的行銷素材 (影片、截圖、文案) 放上 Solution Page，並串接外部 Demo 網址。
