# Website Showcase Implementation Plan (官網開源展示與落地規劃)

- **專案名稱**：`phoenix-auditable-ai-flow`
- **規劃狀態**：**`W1 PASS / W2 IMPLEMENTED / W3 TECHNICAL PASS`**
- **最新更新**：2026-07-13
- **Executor**：小 G

本規劃建立 Phoenix AI 官網第三套系統 —— **Phoenix Auditable AI Workflow** 的開源展示與商業化導入計畫。本規劃不修改任何正式生產代碼與頁面，所有變更將在分支驗收並獲得 Owner 授權後實作。

> 2026-07-13 更新：W2 已在 `codex/open-source-showcase` 分支完成，尚未合併 `main` 或部署 GitHub Pages。

---

## 一、商業漏斗與轉換路徑 (Conversion Funnel)

本展示的核心商業目標是將「公開程式碼與測試證據」轉化為「企業付費諮詢與 Pilot 合作」。官網將三套系統融合成一個完整的能力鏈敘事：

```text
中央廚房營運防護台 (營運場景證明)
          ↓
企業問題診斷工作台 (顧問診斷與決策交付)
          ↓
Phoenix Auditable AI Workflow (可檢驗的開源治理與技術證據參考架構)
          ↓
商業轉換漏斗：
[中央廚房營運落地]
  → [顧問診斷交付]
    → [開源治理證據建立信任]
      → [預約企業診斷] (Primary CTA)
        → [付費 Pilot] (Lite/Standard)
          → [客製系統導入／企業內訓／維護陪跑]
```

### 轉換指標設定 (30 天最低商業目標)
- **合格詢問 (Qualified Leads)**：至少 3 筆符合目標企業畫像且具備時間表之線索。
- **Demo 演示**：完成至少 2 場線上 Demo。
- **付費提案**：送出至少 1 份付費試點 (Paid Pilot) 提案。

---

## 二、官網受影響模組與影響分析 (Impact Analysis)

| 受影響模組 / 檔案 | 變更範疇與預期影響 | 防護控制措施 |
|---|---|---|
| **首頁及系統總覽**<br>`experience/index.html` | 在既有 `#flagship-system` 區塊中，於 `solutions_data.js` 加入第三張旗艦系統卡片。 | 不改動既有卡片渲染 HTML 架構，僅透過資料對接新增。 |
| **系統數據註冊**<br>`experience/solutions_data.js` | 註冊 `id: "phoenix_auditable_ai_workflow"` 資料結構與 UTM 參數。 | 保留原有兩套系統的數據與配置，僅追加第三個物件。 |
| **獨立詳情頁**<br>`experience/phoenix-auditable-ai-workflow/index.html` | 新增此詳情頁，以商業成果與可驗證證據為導向，展示 Policy-as-code 與 Audit trail 流程。 | 頁面資源完全隔離於獨立資料夾，不與既有詳情頁樣式衝突。 |
| **聯絡我們頁面**<br>`contact.html` | 新增 `phoenix_auditable_ai_flow` 至既有 `diagnostic_demo` 諮詢類型的 Campaign 映射。 | 不改動 Google Forms 實體欄位與串接，確保既有提交功能完好。 |
| **分析事件**<br>`analytics` | 註冊 GA4 站內事件監控，追蹤 GitHub 與聯絡 CTA 點擊。 | 禁止傳送任何個人隱私 PII（姓名、Email 等）至 Analytics。 |

---

## 三、變更邊界與安全防護 (Safety Guardrails)

- **非自主 AI 顧問**：官網所有文案必須強調「顧問主導、工具輔助」，不將系統定位為自主決策 SaaS。
- **無合規與法律保證**：明示為 `Local / Mock-first reference architecture`、`Not production ready`。嚴禁使用「保證合規」或「零風險」等字眼。
- **隔離測試**：在正式發布前，必須使用專用測試識別碼於 Pages 執行端到端表單提交，並在 Forms 後台標記測試數據為 `QA`，不污染真實業務名單。
