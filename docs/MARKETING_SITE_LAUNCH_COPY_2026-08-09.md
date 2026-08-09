---
title: 官網上架素材包：對外行銷文案（Ledger-Assist × AI Allocation OS）
author: Social（首席社群營運官）
created_at: 2026-08-09
status: draft（待 CEO 落地）
target_site: 03king.com（GitHub Pages 靜態站，AI_Talent repo）
applies_to: experience/solutions_data.js、experience/<slug>/index.html（方案頁）、index.html #flagship-system
---

# 官網上架素材包：對外行銷文案

> 本文件提供兩套系統的官網上架素材：① `solutions_data.js` 卡片資料（可直接貼入）；② 方案頁五區塊文案（hero／痛點／方案／能力邊界／CTA，每區塊含標題與 2–4 句）；③ 對外合規聲明。
>
> 硬性合規已遵守：無虛構效益數字、無宣稱已上線真實客戶、無未經驗證成功案例。Ledger-Assist 僅以「Sandbox Demo／合成展示／預約體驗」對外定位；AI Allocation OS 定位為顧問服務（Capital Decision Sprint），不是賣軟體。
>
> 事實來源：`Ledger-Assist/docs/commercial/01-product-scope.md`、`Obsidian/10_Projects/Ledger-Assist-Product-Constitution.md`、`AI_Allocation_OS/commercial/OFFER_v1.1.md`、`AI_Allocation_OS/commercial/ICP_v1.1.md`。

---

## 系統 A：Ledger-Assist（會計事務所 AI 系統）

### A1. solutions_data.js 卡片資料（可直接貼入）

```js
{
  id: "ledger_assist",
  slug: "ledger-assist",
  title: "Ledger-Assist 發票收件與檢核系統",
  short_title: "憑證檢核系統",
  subtitle: "客戶 LINE 上傳發票、事務所 LINE 內檢核修正；每所獨立私有部署，正式憑證與稽核記錄留在事務所。",
  status: "Sandbox Demo",
  maturity: "Sandbox Demo Ready",
  access_type: "合成展示／預約體驗",
  featured: false,
  featured_order: 4,
  category: ["憑證檢核", "會計事務所"],
  industries: ["會計師事務所", "記帳士事務所", "稅務服務"],
  page_variant: "line-invoice-workflow",
  showcase_type: "synthetic-demo",
  demo_duration: "15 分鐘",
  highlights: [
    "客戶用 LINE 上傳發票，事務所在 LINE 內檢核、修正與確認",
    "AI 只產出可覆核候選，Pilot 期間不自動核准，人工確認後才匯出",
    "每家事務所獨立私有部署，正式憑證、覆核狀態與稽核記錄留在事務所控制環境"
  ],
  sections: ["line-flow", "review-workflow", "private-deployment", "boundaries", "pilot-cta"],
  compliance_note: "Sandbox Demo：展示使用合成資料，不含真實客戶憑證；正式部署為每家事務所獨立私有部署。",
  cta_text: "查看 Ledger-Assist 展示",
  cta_href: "./experience/ledger-assist/index.html",
  catalog_cta_href: "./ledger-assist/index.html",
  pilot_program_text: "預約 15 分鐘 Demo",
  pilot_program_href: "./contact.html?request_type=ledger_assist_demo&utm_source=site&utm_medium=ledger_assist&utm_campaign=ledger_assist_demo&utm_content=flagship",
  catalog_pilot_program_href: "../contact.html?request_type=ledger_assist_demo&utm_source=site&utm_medium=ledger_assist&utm_campaign=ledger_assist_demo&utm_content=systems_catalog",
  primary_action: "pilot",
  contact_category: "experience_cta",
  contact_label: "experience_solution_view",
  updated_at: "2026-08-09"
}
```

### A2. 方案頁區塊文案（對應 `experience/ledger-assist/index.html`）

**① Hero 區**
- hero-tag（眉題）：`Accounting · LINE Workflow`
- hero-title：**Ledger-Assist 發票收件與檢核系統**
- hero-desc：客戶用 LINE 上傳發票，系統完成收件、辨識與檢核候選；事務所人員在 LINE 內修正、確認，經人工覆核核准後才匯出。正式憑證、帳務結果與稽核記錄，全部留在每家事務所獨立私有部署的環境——不是集中式帳務 SaaS。

**② 痛點區（標題：為什麼事務所需要一套新的收件流程）**
- 客戶習慣用 LINE 傳發票：翻拍、截圖、PDF 夾雜，事務所逐張下載、整理、Key-in，旺季爆量時漏件與錯件的風險跟著上升。
- 憑證格式雜（電子發票 QR、傳統收據、POS 明細），直接讓 AI 自動入帳風險高；事務所不敢放手，卻也找不到折衷的檢核流程。
- 雲端 SaaS 集中保存客戶憑證，事務所對資料權威與稽核責任難以掌握；客戶資料外流的疑慮，往往成為導入的最大阻力。

**③ 方案區（標題：可驗證的收件 → 檢核 → 覆核閉環）**
- LINE 收件：客戶在 LINE 上傳發票即回覆收件確認；未完成綁定的使用者，系統不下載原圖、不 OCR、不建立案件。
- LINE 內檢核：AI 依 QR 與 OCR 產出辨識候選並附證據，事務所在 LINE 內檢核、修正、確認，不必另開工作台。
- 人工覆核與匯出：Pilot 期間自動核准關閉，每一筆都經人工確認後才匯出；全程留下可稽核軌跡，auditor 以唯讀身分稽核，不可改欄位或核准。
- 私有部署：每家事務所一套獨立部署（事務所主機、VM 或客戶私有雲），正式原圖、帳務草稿、覆核狀態與稽核 authority 留在事務所控制的環境。

**④ 能力邊界區（標題：能力邊界）**
- 現可驗證（Sandbox Demo）：以合成資料走完「LINE 上傳 → 收件確認 → QR／OCR 辨識候選 → LINE 內檢核修正 → 覆核 → 匯出預覽」完整流程。
- Pilot 可配置：1 家設計夥伴事務所；簽署 DPA 並確認用途與保存政策後才匯入真實資料；Pilot 強制 MFA（OIDC）。
- 導入階段評估：正式會計軟體／ERP adapter、本地模型、備份還原演練與 SLA 於導入階段另行評估。

**⑤ CTA 區（標題：預約 15 分鐘 Demo）**
- 用合成資料走完一次「客戶 LINE 上傳 → 事務所 LINE 檢核 → 覆核 → 匯出預覽」，先確認流程與資料邊界符合貴所要求，再談 DPA 與 Pilot 合作。導入與授權方式（一次性導入、每所授權、年度維護）於 Demo 後另行說明。

**（選用）適合對象區**
- 主要對象：台灣會計師事務所與記帳士事務所，客戶習慣以 LINE 傳遞發票，且希望正式帳務資料留在自己可控環境。
- 導入前提：願意先以合成資料驗證流程、簽署 DPA，並接受 Pilot 期間自動核准關閉、全程人工覆核。

### A3. 合規聲明（對外用，可置於頁尾與 CTA 下方）

本頁展示為合成資料 Sandbox Demo，不含任何真實客戶憑證。正式部署為每家事務所獨立私有部署：正式憑證、辨識結果、覆核狀態與稽核記錄均留在事務所控制的環境，鳳凰 AI 不以集中式 SaaS 保存各事務所帳務；Pilot 期間所有結果須經人工確認，系統不自動核准。

---

## 系統 B：AI Allocation OS（企業 AI 顧問決策工作台）

### B1. solutions_data.js 卡片資料（可直接貼入）

```js
{
  id: "ai_allocation_os",
  slug: "ai-allocation-os",
  title: "AI Allocation OS 企業 AI 投資決策工作台",
  short_title: "投資決策工作台",
  subtitle: "以 Capital Decision Sprint 顧問服務，把 AI 投資決策收成可稽核決策包：候選篩選、深度 Underwriting、風險 Gate 與決策紀錄，全程留痕。",
  status: "Consulting Offer｜開放預約",
  maturity: "Offer v1.1",
  access_type: "預約 Capital Decision Sprint",
  featured: false,
  featured_order: 5,
  category: ["AI 投資決策", "顧問服務"],
  industries: ["零售／電商", "B2C 服務業", "客服營運"],
  page_variant: "capital-decision",
  showcase_type: "decision-sprint",
  demo_duration: "30–45 分鐘",
  highlights: [
    "最多 5 個候選案篩選、3 個深度 Underwriting，每案產出三軸決策與理由",
    "Funding／Repair／Reassessment Gate 與 T0/T1/T2 決策快照，決策理由版本化留痕",
    "Committee Pack 與決策紀錄版本化交付；評分不因 Phoenix 是否承接後續實作而改變"
  ],
  sections: ["sprint-flow", "gate-model", "deliverables", "boundaries", "pilot-cta"],
  compliance_note: "顧問服務：提供決策支援與分析，不保證 ROI 或投資結果；案例均去識別化，最終決策權與責任由客戶承擔。",
  cta_text: "查看決策工作台",
  cta_href: "./experience/ai-allocation-os/index.html",
  catalog_cta_href: "./ai-allocation-os/index.html",
  pilot_program_text: "預約 30–45 分鐘說明",
  pilot_program_href: "./contact.html?request_type=capital_sprint_info&utm_source=site&utm_medium=ai_allocation_os&utm_campaign=capital_sprint&utm_content=flagship",
  catalog_pilot_program_href: "../contact.html?request_type=capital_sprint_info&utm_source=site&utm_medium=ai_allocation_os&utm_campaign=capital_sprint&utm_content=systems_catalog",
  primary_action: "pilot",
  contact_category: "experience_cta",
  contact_label: "experience_solution_view",
  updated_at: "2026-08-09"
}
```

### B2. 方案頁區塊文案（對應 `experience/ai-allocation-os/index.html`）

**① Hero 區**
- hero-tag（眉題）：`AI Investment Decision · Consulting Sprint`
- hero-title：**AI Allocation OS 企業 AI 投資決策工作台**
- hero-desc：AI 提案很多、預算有限——該投哪個、該修哪個、該延後哪個？我們以 Capital Decision Sprint 顧問服務，用版本化規則、可追溯證據與預先定義的風險 Gate，把決策過程收成可稽核的決策包。這是顧問服務，不是賣軟體：把「怎麼決定」變成可檢討、可重現的流程。

**② 痛點區（標題：AI 投資決策為何難以檢討）**
- AI 提案逐年增加，預算卻有限：Fund、Repair、Defer、Reject 的決定常靠會議感覺或老闆拍板，事後難以回溯當初的理由。
- 各提案用不同標準評估：理由沒有版本、沒有證據連結，幾個月後回頭看，已無法重現「當時為什麼這樣決定」。
- 評分容易受立場影響：提案方、供應商與決策者各有立場，缺少中立、且可留下紀錄的決策流程。
- 決策後缺乏追蹤設計：沒有 baseline 與 30／60／90 天回報機制，投入之後無法驗證當初假設是否成立。

**③ 方案區（標題：Capital Decision Sprint 內容）**
- 篩選與 Underwriting：最多 5 個候選 use case 篩選，其中 3 個深度 Underwriting，產出 3 份三軸決策（含理由）。
- Gate 控制：為最高優先或最具爭議的 1 個流程建立 Funding Gate、Foundation Repair Gate 或 Reassessment Gate；若無適合撥款案，不強制產生。
- 決策留痕：T0／T1／T2 Decision Snapshot 與 Decision Delta 記錄，決策理由版本化、可追溯。
- 正式會議與交付：一場 Capital Decision Sprint 會議，交付 Committee Pack、Decision Record、Assumption／Evidence Register、會議紀錄與下一步 action log。

**④ 能力邊界區（標題：能力邊界）**
- 本服務範圍：決策支援與分析（顧問 Sprint）；不包含實際 AI 系統開發、PoC 或導入執行，後續專案可另行報價。
- 不提供專業意見：法律、財務、稅務、合規或證券投資意見不在範圍內；不保證 ROI、投資成功或特定決策結果。
- 中立性：Sprint 費用不因最終決策為 Fund、Repair、Defer 或 Reject 而改變；Phoenix 若後續參與相關投標，須與本次決策紀錄分離並揭露。
- 資料最小化：僅收取聚合流程量、KPI baseline、欄位字典與處理 metadata；必要樣本為 50–100 筆去識別化資料且須先取得核准；匿名 benchmark 為獨立 opt-in，不同意不影響 Sprint。

**⑤ CTA 區（標題：預約 30–45 分鐘說明）**
- 用一個客服分類案例，示範「候選篩選 → Underwriting → 三軸決策 → Gate 產出」的完整流程，並說明所需資料、決策者參與與時程（正式 Sprint 於 kickoff 後 10 個工作日內完成）。先確認流程符合貴司決策文化，再進入正式 Sprint。

**（選用）適合對象區**
- 優先對象：台灣零售、電商與一般 B2C 服務業，客服案件分類／分流流程，每月案件量約 1,000 件以上，且 30–60 天內可建立或量測 baseline（如平均處理時間、首次回應時間、轉人工率）。
- 導入前提：具名 process owner 與 decision owner，願意提供可驗證的歷史聚合資料；受高度監管產業需另備具名 compliance／risk sponsor 並完成資料治理審查。

### B3. 合規聲明（對外用，可置於頁尾與 CTA 下方）

Capital Decision Sprint 為顧問服務，提供決策支援與分析，不構成法律、財務、稅務、合規或證券投資意見，亦不保證 ROI、投資成功或特定決策結果；最終決策權與責任由客戶自行承擔。網站與說明材料中的案例均經去識別化處理，不揭露客戶身分。

---

## 落地注意事項（CEO 落地時逐項確認）

1. **首頁精選上限**：`index.html` 的 #flagship-system 只渲染 `featured: true` 且依 `featured_order` 排序的前 3 筆（`slice(0, 3)`）。現有 3 套系統已佔滿，故兩套新系統預設 `featured: false`（系統總覽 `experience/index.html` 會自動全數顯示）。若要首頁輪替露出：將某套既有系統 `featured` 改為 `false`，再把新系統改為 `true`。
2. **方案頁檔案**：依 `experience/central-kitchen-ai-agent/index.html` 模板新增 `experience/ledger-assist/index.html` 與 `experience/ai-allocation-os/index.html`，將 A2／B2 各區塊文案填入對應 section；流程圖、summary box 與影片區可沿用模板結構（Ledger-Assist 尚無正式流程影片，可用靜態流程圖替代並註記「Demo 時提供操作畫面」）。
3. **contact.html**：`intentLabels` 需新增 `request_type` 對應標籤（`ledger_assist_demo`、`capital_sprint_info`），否則 CTA 連結會落入預設 intent。`cta_href`／`pilot_program_href` 為建議值，落地時依實際頁面路徑與 GA 參數慣例調整。
4. **版本參數**：`index.html` 與 `experience/index.html` 的 `solutions_data.js?v=` 需遞增版本（現為 `?v=20260713-5`）。
5. **隱私權連結**：方案頁 consent-text 依現行模板使用父層相對路徑（`../../privacy.html`），勿用 `./privacy.html`，避免 404。
6. **未公開事項**：AOS 報價（OFFER v1.1 為 pricing hypothesis）未寫入公開文案；若日後要公開報價，由 CEO 另行裁定。Ledger-Assist 未提「≥300 張驗證樣本」等內部驗證規劃，避免被解讀為成效承諾。
7. **PII 與去識別化**：本素材包不含 email、電話、LINE ID 或真實客戶名稱；上線前對 experience/ 全域再跑一次 PII 掃描（含既有頁面），確認無殘留。
