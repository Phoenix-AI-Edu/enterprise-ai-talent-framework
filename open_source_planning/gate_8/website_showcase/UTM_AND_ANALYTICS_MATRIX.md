# UTM and Analytics Tracking Matrix (UTM與分析追蹤矩陣)

- **專案名稱**：`phoenix-auditable-ai-flow`
- **文件狀態**：**`W0/W1 DRAFT - READY FOR OWNER REVIEW`**
- **最新更新**：2026-07-13

本文件規範官網開源展示詳情頁面的商業轉換追蹤（UTM 參數）與 GA4 分析事件規格，確保行銷數據可被精確量測且符合隱私法規（不含個人識別資訊 PII）。

---

## 一、UTM 轉換追蹤規格 (UTM Specifications)

所有引導至 `contact.html` 的預約診斷 CTA 按鈕均須附加以下 UTM 參數，以便在 Google Forms 諮詢後台精確識別來源：

- **基本路徑**：`../../contact.html`
- **必填行銷參數**：
  - `request_type=auditable_ai_demo` (預約可稽核工作流演示與導入診斷)
  - `utm_source=site` (官網流量)
  - `utm_medium=open_source_showcase` (開源展示詳情頁)
  - `utm_campaign=phoenix_auditable_ai_flow` (開源專案活動名稱)
- **內容版面細分 (`utm_content`)**：
  - 首頁精選卡片連結：`utm_content=homepage_card`
  - 詳情頁 Hero 區按鈕：`utm_content=hero_cta`
  - 詳情頁開源與付費邊界區：`utm_content=service_boundary_cta`
  - 詳情頁底部頁尾按鈕：`utm_content=footer_cta`

---

## 二、GA4 站內分析事件定義 (GA4 Event Registry)

為監控漏斗轉換與使用者互動，我們在詳情頁面配置以下 GA4 自訂事件：

| 事件名稱 (Event Name) | 觸發時機 (Trigger) | 參數清單 (Parameters) | 說明 (Description) |
|---|---|---|---|
| `experience_solution_view` | 載入 `phoenix-auditable-ai-workflow` 詳情頁時。 | `solution_id="phoenix_auditable_ai_workflow"` | 衡量 Awareness 層級流量。 |
| `experience_cta_click` | 點擊任何前往 `contact.html` 的 Primary CTA 時。 | `solution_id`, `source_section` | 衡量 Intent 層級點擊。 |
| `experience_github_click` | 點擊前往 GitHub 專案的 Secondary CTA 時。 | `solution_id`, `source_section` | 衡量開源社群跳轉流量。 |
| `experience_release_click` | 點擊前往 v0.1.0 Release 頁面時。 | `solution_id`, `release_version="v0.1.0"` | 衡量技術信任點擊。 |
| `experience_video_progress` | 播放展示影片達 25%、50%、75%、100% 時。 | `solution_id`, `progress_percent` | 衡量 Interest 層級完播率。 |

---

## 三、隱私與安全性控制 (Privacy Guardrails)

- **PII 零收集原則**：所有 GA4 事件參數**嚴禁傳送**使用者的個人資料，包括姓名、Email、公司名稱或聯絡電話。所有表單實體輸入值均僅在 `contact.html` 內部傳送至 Google Forms 後台，不與 Analytics 共享。
- **測試數據過濾**：團隊進行 Pages 表單端到端測試時，提交的測試姓名必須包含特定識別碼 `[QA_TEST]`，以便在 Forms 後台進行數據分析時予以排除。
