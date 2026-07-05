# Release Notes: v0.2.0 (Experience & Compliance Update)

## Overview
This release introduces the interactive AI Experience Portal, establishes a robust Pilot-ready framework for demonstrations, and completes a comprehensive de-identification and compliance audit of all case studies and metadata.

## Key Highlights

### 1. Experience Portal 上線
- 推出 `/experience/index.html` 體驗區總覽頁，整合各產業的 AI 互動展示入口。
- 提供一致的導覽列、返回動線與品牌視覺（鳳凰 AI 顧問）。

### 2. 中央廚房 Pilot-ready 方案頁
- 新增 `/experience/central-kitchen-ai-agent/index.html` 互動展示頁。
- 專為餐飲連鎖與中央廚房設計的 AI 營運助理情境，展示文字通報轉工單、戰情室監控與高風險決策阻斷（Human-in-the-loop）。
- 明確列出方案適合對象，提供「申請互動 Demo」與「預約顧問諮詢」行動呼籲。

### 3. R5 表單同意文案
- 所有體驗區、方案頁與首頁的表單入口（Google Form），皆已補上隱私權同意聲明文字。
- 點擊按鈕或送出表單前，明確告知使用者同意《個人資料保護與隱私權政策告知書》，連結至 `privacy.html`。

### 4. R2/R3 案例去識別化與宣稱清理
- 全面稽核 `cases.json`、`cases_data.js` 與所有 24 個 `cases/html/*.html` 及對應 Markdown。
- 已移除所有真實品牌名稱、地名組合。
- 移除所有具體未經驗證的節省百分比、金額與 ROI 宣稱，改以中性/定性描述（例如「大幅減少」、「有效降低」）。
- 落實「只展示 Payload Preview、不宣稱已完成真實系統串接」之原則。

### 5. Marketing Launch Kit
- 產出 `docs/MARKETING_LAUNCH_KIT.md` 推廣素材包。
- 包含 LinkedIn、Facebook、Threads 的社群貼文範本，3 分鐘 Demo 影片腳本，以及 BD 私訊模板與 One-pager 簡報大綱。
- 已內建 Sandbox Preview 定位與 Compliance 提醒，保護團隊發文安全。

### 6. Dead link 修復
- 修正了 16 個 Standalone HTML 案例頁面中錯誤的返回導覽連結（修正為指向 `../../index.html`），確保使用者體驗不斷鏈。

## 已知限制 (Known Limitations)
- **Interactive Demo 狀態**：目前的互動 Demo 仍為 Gated (需申請)、Sandbox、Pilot-ready 狀態。展示的 ERP/POS Payload 均為模擬資料預覽，未串接任何客戶之真實後台系統。
