# 鳳凰 AI 官網：第一波中央廚房行銷 Launch Readiness v0.2.0

> 狀態：Production Live  
> 日期：2026-07-06  
> 版本：v0.2.0

---

## 定位聲明

第一波對外素材全部維持 **Pilot-ready / Sandbox Preview** 定位，不宣稱已完成任何客戶真實後台串接。

---

## 已完成的

- 官網首頁 live：`https://phoenix-ai-edu.github.io/enterprise-ai-talent-framework/`
- 官網首頁已明確露出「中央廚房 AI 系統展示」主入口（`.hero-ctas` + `#flagship-system`）。
- 官方 landing page live：`/experience/central-kitchen-ai-agent/`
- GTM snippet 已載入於首頁與 central-kitchen page：`GTM-NB4699JG`
- GA4 direct sender 已於首頁載入：`G-MPT80VJN31`
- central-kitchen page 的 CTA 按鈕存在且可開啟 Google Form（`申請互動 Demo` / `預約顧問諮詢`）
- Google Form URL 實測回傳 HTTP 200：`https://docs.google.com/forms/d/e/1FAIpQLSfAUCKXkZB_ah0eOXX0Cr6EODIwQBp25LZZ1V3W_nSE8iqGrQ/viewform`
- privacy link 存在且可點擊（`/privacy.html`）
- experience portal 禁用字串掃描 clean（未發現真實客戶名稱、未驗證數字、ERP/POS 串接宣稱）

---

## 仍待確認

- GA4 自訂事件名稱尚未在 repo 層交叉驗證：已定義的事件名稱（如 `experience_demo_request_click`、`experience_contact_click`）必須在 GA4 UI 內對應建立，否則報表不會顯示。
- Analytics 事件追蹤：central-kitchen page 的事件發送程式碼已存在，但無法在這裡即時確認 GTM 容器內是否有對應 trigger。

---

## 阻塞點（Blocker）

> 無。以上「仍待確認」不阻擋第一波草稿發布，但會影響後續報表上線驗收。

---

## 結論（Verdict）

**可以進入第一波社交草稿 + 人工審稿發布。**  
官網、CTA、Form、GTM/GA4 與合規條件已滿足。
