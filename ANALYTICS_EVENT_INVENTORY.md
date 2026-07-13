# D-1 Analytics Audit — 事件命名盤點
_稽核日期：2026-07-05_  
_稽核範圍：`C:\Users\m1016\Documents\AI_Talent` 之主站與案例頁_  
_目標：作為 `/experience` 追蹤命名對齊依據_

---

## 1. 稽核發現摘要

| 項目 | 狀況 |
|------|------|
| 實際有埋追蹤邏輯的檔案 | 僅 `index.html` 一個主檔 |
| dataLayer.push 實作 | 僅 `index.html:4313` |
| gtag('event') 實作 | 僅 `index.html:4317`，做為 dual-track fallback |
| 案例子頁 | 仅載入 GTM snippet，無自訂事件 |
| m01~m13、privacy、curriculum | 無自訂 analytics 事件 |
| GTM ID | `GTM-NB4699JG` |
| GA4 Measurement ID | `G-MPT80VJN31` |
| 含 PII 欄位 | 已確認無 email、姓名、電話等明碼個資 |

---

## 2. ANALYTICS_EVENT_INVENTORY

### 事件：`case_cta_click`
- **事件名稱**：`case_cta_click`
- **優先級**：主站唯一自訂 analytics 事件
- **觸發機制**：全域 click 捕獲，`.case-card` 內的 `.case-btn-primary`、`.case-btn-secondary` 等 CTA
- **對應 dataLayer/gtag**：同名關鍵字均對應同一行為

| 來源標記 | 對應 event_label | 出現位置 |
|----------|------------------|----------|
| `data-ga="case_cta_primary"` | `case_cta_primary` | 卡片內 CTA 按鈕 |
| `data-ga="case_cta_secondary"` | `case_cta_secondary` | 卡片內次要 CTA |
| `data-ga="case_cta_sticky_detail"` | `case_cta_sticky_detail` | 右下 sticky |
| `data-ga="case_cta_sticky_diagnosis"` | `case_cta_sticky_diagnosis` | 右下 sticky |

#### 參數結構

```json
// dataLayer.push
{
  "event": "case_cta_click",
  "case_id": "ecommerce_01_guardrails",
  "case_title": "E-commerceGuardrails規劃策略報告",
  "cta_type": "case_cta_primary",
  "cta_href": "./index.html#pricing"
}

// gtag('event', ...)
window.gtag('event', 'case_cta_click', {
  "event_category": "case_cta",
  "event_label": "case_cta_primary",
  "case_id": "ecommerce_01_guardrails",
  "case_title": "E-commerce Guardrails規劃策略報告",
  "cta_type": "case_cta_primary",
  "cta_href": "./index.html#pricing" || absolute URL
})

// __sendGA4 Measurement Protocol
window.__sendGA4('case_cta_click', {
  case_id,
  case_title,
  cta_href
})
```

#### 行號與檔案

- `index.html:4313` `window.dataLayer.push(payload)`
- `index.html:4317` `window.gtag('event', ...)`
- `index.html:4331` `window.__sendGA4(...)`
- `index.html:4361` Measurement Protocol 組裝
- `index.html:4370` `window.__sendGA4 = sendGA4`

#### PII 檢查

| 參數 | 是否含 PII | 說明 |
|------|------------|------|
| case_id | 否 | 案例 ID，例：`medical_01_health_chat` |
| case_title | 否 | 產業＋場景描述，未含個資 |
| cta_type | 否 | 按鈕類型代稱 |
| cta_href | 否 | HTTP(S) 連結，不含明碼個資 |
| event_category | 否 | 固定字串 `case_cta` |
| event_label | 否 | 同上，按鈕種類代稱 |

---

## 3. experience 區命名建議

以下建議延續主站命名邏輯：底線命名、前置詞統一、語意明確。可將經驗域事件視為「新 prefix + 主站既有 suffix」的組合，避免重複船難。

### 3.1 可沿用主站邏輯的事件

建議保留相同行為定義，讓 GTM / Looker Studio 報表可直接跨區串接：

| experience 建議事件名稱 | 對應主站邏輯 | 建議 category | 建議 label |
|-------------------------|--------------|--------------|------------|
| `experience_solution_view` | page_view 增強版 | `experience` | `solution_id` |
| `experience_demo_request_click` | CTA 點擊 | `experience_cta` | `demo_primary` / `demo_secondary` |
| `experience_contact_click` | CTA 點擊 | `experience_cta` | `contact` |
| `experience_roi_view` | 區塊曝光 | `experience` | `roi_section` |

### 3.2 experience 專屬且必須新增的事件

| 建議事件名稱 | 觸發時機 | 建議 category | 建議 label |
|--------------|----------|--------------|------------|
| `experience_tab_switch` | 切換方案 tab | `experience` | `solution_id:tab_index` |
| `experience_scenario_view` | 點擊場景說明卡 | `experience` | `scenario_id` |
| `experience_kpi_toggle_view` | 展開/收合 KPI | `experience` | `kpi_topic` |
| `experience_tech_arch_toggle_view` | 展開技術架構 | `experience` | `arch_component` |
| `experience_cta_click` | 任一手動 CTA | `experience_cta` | `cta_type` |
| `experience_cookie_view` | 查看 cookie 治理說明 | `experience` | `compliance_note` |

### 3.3 experience 的參數規範（避免 PII）

experience 事件 **明令拒絕** 以下欄位：
- `email`、`phone`、`姓名`、`公司名稱`、`LINE_ID`、任何明碼個資

若必須追蹤表單意圖，只能使用：
- `form_id` / `form_type`
- `intent_level`：`high` / `medium` / `low`
- `source_section`：`hero` / `roi` / `footer`

---

## 4. 結論與建議

1. **主站命名極度精簡**：目前僅維護唯一事件 `case_cta_click`，GA4 `event_label` 多元化。
2. ** `/experience` 要延續 prefix：** 建議全部使用 `experience_` 開頭，並以 `experience_cta` 做為按鈕統一 category，與主站 `case_cta` 平行。
3. **experience 不能沿用 `case_cta_click`**：事件命名本身即帶有 domain，應另起 `experience_*` family，避免報表污染。
4. **參數避免過度膨脹**：主站僅帶 `case_id / case_title / cta_type / cta_href` 四欄；experience 建議控制在 **~5 欄以內**。
5. **安全底線**：主站目前 payload 無 PII；experience 承襲相同原則。

---

_止於盤點，未修改任何檔案。_

---

## 5. Phoenix Auditable AI Workflow 展示事件（2026-07-13）

詳情頁：`experience/phoenix-auditable-ai-workflow/index.html`

| 事件 | 用途 | 允許參數 |
| --- | --- | --- |
| `experience_solution_view` | 詳情頁曝光 | `solution_id`, `source_section` |
| `experience_demo_request_click` | 導入診斷／工作坊 CTA | `solution_id`, `source_section`, `target_type` |
| `experience_github_click` | GitHub 與治理文件外連 | `solution_id`, `source_section`, `target_type` |
| `experience_release_click` | Release 與 CI 證據外連 | `solution_id`, `source_section`, `release_version` |
| `experience_video_progress` | 互動導覽 0／25／50／75／100 進度 | `solution_id`, `source_section`, `progress_percent` |

本頁事件不傳送姓名、Email、電話、公司、問題內容或表單輸入值。
