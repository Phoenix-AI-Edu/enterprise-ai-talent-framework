# Wireframe and Content Specification (頁面線框圖與文案規格)

- **專案名稱**：`phoenix-auditable-ai-flow`
- **文件狀態**：**`W0/W1 DRAFT - READY FOR OWNER REVIEW`**
- **最新更新**：2026-07-13

本文件規範「Phoenix 可稽核 AI 工作流」官網第三張精選卡片文案以及獨立詳情頁的 Wireframe 與文案規格，提供桌面與 390px 手機排版對比。

---

## 一、首頁精選卡片文案與數據規格 (Homepage Registry JSON)

以下為預備寫入 `solutions_data.js` 的第三張卡片數據規格草稿：

```json
{
  "id": "phoenix_auditable_ai_workflow",
  "slug": "phoenix-auditable-ai-workflow",
  "title": "Phoenix 可稽核 AI 工作流",
  "short_title": "開源工作流",
  "subtitle": "把政策防護、引用證據、人工覆核與稽核紀錄組成可檢驗的企業 AI 參考架構",
  "status": "Open Source v0.1.0 / Local Reference",
  "maturity": "Open Source Reference",
  "access_type": "Public GitHub",
  "featured": true,
  "featured_order": 3,
  "category": ["AI 治理", "開源參考架構"],
  "industries": ["資訊與稽核", "高合規企業", "跨產業"],
  "page_variant": "governance-reference",
  "showcase_type": "open-source-showcase",
  "demo_duration": "60–90 秒",
  "highlights": [
    "Input & Output Policy 宣告式防護機制",
    "政策衝突攔截與人工審批 (HITL) 流程",
    "Markdown 引用驗證與本機 SQLite 稽核事件追溯"
  ],
  "sections": ["hero", "workflow-diagram", "evidence-grid", "service-boundary", "boundaries", "pilot-cta"],
  "compliance_note": "本機 Mock-first 參考架構；非生產環境認證。提供治理與技術安全底座示範。",
  "cta_text": "查看開源參考架構",
  "cta_href": "./experience/phoenix-auditable-ai-workflow/index.html",
  "catalog_cta_href": "./phoenix-auditable-ai-workflow/index.html",
  "pilot_program_text": "預約 AI 治理與導入診斷",
  "pilot_program_href": "./contact.html?request_type=diagnostic_demo&utm_source=site&utm_medium=open_source_showcase&utm_campaign=phoenix_auditable_ai_flow&utm_content=homepage_card",
  "catalog_pilot_program_href": "../contact.html?request_type=diagnostic_demo&utm_source=site&utm_medium=open_source_showcase&utm_campaign=phoenix_auditable_ai_flow&utm_content=systems_catalog",
  "primary_action": "pilot",
  "contact_category": "experience_cta",
  "contact_label": "experience_solution_view",
  "updated_at": "2026-07-13"
}
```

---

## 二、詳情頁獨立 Wireframe 排版 (390px 寬 vs 桌面版)

詳情頁路徑：`experience/phoenix-auditable-ai-workflow/index.html`

### 1. 頂部導航與 Hero 區 (Hero Section)
- **[桌面排版]**：左側大標題、副標題與 Primary CTA（預約診斷）/ Secondary CTA（前往 GitHub）；右側為 60–90 秒系統操作演示錄影。
- **[390px 手機排版]**：單欄垂直流。標題置頂，下方緊接操作錄影，接著是 Primary CTA，然後是 Secondary CTA。
- **文案**：
  - 主標題：`落實企業 AI 治理：從開源參考架構到可稽核決策證據鏈`
  - 副標題：`Phoenix 提供由顧問帶領的 AI 治理診斷。我們將政策防護、人工審查與可查詢的稽核事件紀錄結構化，協助您的技術與稽核團隊建立可驗證的工作流。`

### 2. 30 秒六階段工作流 (Workflow Section)
- **[桌面排版]**：橫向排列的 6 個步驟卡片（Input Policy → Knowledge Retrieval → Model Call → Output Policy → Human-in-the-loop → Audit Database），帶有向右的引導箭頭。
- **[390px 手機排版]**：垂直堆疊的步驟列表，箭頭改為向下引導。
- **文案**：
  1. 輸入政策核對 (核對合規邊界)
  2. Markdown 合成規章檢索 (取得政策依據)
  3. Mock 回答生成 (不連接正式 LLM)
  4. 輸出安全政策核對 (防止敏感溢出)
  5. 人工審查機制 (遇決策衝突時自動攔截)
  6. 本機 SQLite 稽核事件 (可依 request_id 查詢；不具不可竄改保證)

### 3. 可驗證技術證據網格 (Evidence Section)
- **[桌面排版]**：三欄網格展示：
  - 卡片 A：`59/59 自動化測試`（CI 綠色圖標，附 CI run 連結）
  - 卡片 B：`公開 GitHub 儲存庫`（v0.1.0 發布與程式碼，附 GitHub 連結）
  - 卡片 C：`開源治理與維護手冊`（GOVERNANCE / SECURITY 等管理文件連結）
- **[390px 手機排版]**：單欄垂直卡片列表，文字與圖標置中對齊。

### 4. 開源與付費服務邊界對照表 (Service Boundary Section)
- **[桌面排版]**：橫向兩欄式對照表（左欄「公開免費開源架構」、右欄「Phoenix 付費企業服務」）。
- **[390px 手機排版]**：雙卡片垂直對照。先顯示「公開免費開源架構」卡片，下方再顯示「Phoenix 付費企業服務」卡片，並以對比色彩突出付費諮詢的核心價值。
- **對照內容**：
  - *開源免費*：本機 Mock-first 參考架構、Policy/HITL 示範介面、合成 HR 測試案例、安裝與治理文件。
  - *Phoenix 付費服務*：企業問題與治理現況診斷、企業政策/資料與權限設計、場景選擇工作坊、正式系統整合與 SSO/RBAC/遮蔽評估、導入培訓與治理陪跑。

### 5. 限制聲明 (Compliance Limitations)
- **排版**：置於頁面最底部的灰色警示框（Alert Box）。
- **文案**：
  > 「本專案為本機 Mock-first 參考架構，採用虛構合成數據，非生產環境認證。正式導入仍需依據企業特定的資料結構、系統權限、資安防護與法規合規需求，進行個別顧問評估與客製設計。」

### 6. 三類買方入口 (Audience Paths)

- **管理者**：從治理責任、決策證據與 Pilot 路線切入，CTA 為預約導入診斷。
- **IT／CTO**：從 GitHub、v0.1.0 Release、測試與架構限制切入，CTA 為檢視程式碼後預約架構評估。
- **顧問／培訓夥伴**：從可重複的診斷與治理教學流程切入，CTA 為洽談企業內訓或共同交付。

### 7. 三系統能力鏈 (Portfolio Chain)

以 CSS 卡片呈現「中央廚房營運落地 → 顧問診斷交付 → 開源治理證據 → 診斷／Pilot／導入」，並明示為 Phoenix 能力組合，不宣稱三者已整合成正式生產平台。

### 8. 頁底商業 CTA (Footer Conversion)

- Primary：`預約 AI 治理與導入診斷`
- Secondary：`查看 GitHub 開源專案`
- Tertiary：`查看 v0.1.0 Release 與測試證據`

### 9. SEO、分享與可及性

- 設定 canonical、Open Graph 與實際頁面一致的 title／description。
- 以 `SoftwareSourceCode` 描述公開程式碼，以 `Service` 分開描述 Phoenix 付費服務。
- 影片必須提供字幕或等價文字稿；所有圖片提供 alt；鍵盤焦點清楚可見。

### 10. 商業追蹤責任

- KPI Owner：Phoenix AI Brand & Commercial Owner。
- 發布後每週檢視一次；第 30 天提出保留、改版或下架建議。
