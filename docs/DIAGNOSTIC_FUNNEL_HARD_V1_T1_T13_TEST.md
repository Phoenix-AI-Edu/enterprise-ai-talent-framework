# Diagnostic Funnel HARD V1 — T1–T13 自測紀錄

**分支：** `feat/diagnostic-funnel-hard-v1`  
**規格：** `docs/WEBSITE_DIAGNOSTIC_FUNNEL_HARD_V1_HANDOFF.md`  
**日期：** 2026-07-20  
**測試環境：** 靜態檢查 + 演算法單元對照（瀏覽器全流程建議 PR 合併前人工再點一次）

## 端點決策（已定）

- 結果頁內嵌表單 POST → 官網商業 Google Form（與 `contact.html` 同 action）
- payload（score / q1–q5 / next_step / warnings / UTM）序列化進 `entry.2002297629`（需求說明隱藏欄）
- `next_step=1` 感謝後提供工具包 Form 次要連結（雙寫可選）
- `contact.html` 可承接 query 預填（備援路徑）

## 測試矩陣

| # | 操作 | 期望 | 結果 | 證據 |
|---|------|------|------|------|
| T1 | 五題皆 A | score=5, band=探索期, 預選 **1**, P-KIT | **PASS** | 演算法單元：`compute('A','A',5)→1`；band≤8→explore；DOM 含 P-KIT 文案 |
| T2 | 五題皆 D | score=20, band=制度化期, 預選 **5**, P-SPRINT | **PASS** | `compute('D','D',20)→5`；band operate；Sprint 文案含「費用不因結論改變」 |
| T3 | Q5=B, 其餘 C（total=14） | 預選 **3** | **PASS** | `compute('C','B',14)→3` |
| T4 | Q5=C, total 13–16 | 預選 **4** | **PASS** | `compute('B','C',14)→4` |
| T5 | Q5=D, total≤12 | 預選 **3**（非 5） | **PASS** | `compute('B','D',12)→3` |
| T6 | Q4=A, Q5=D, total 中高 | 預選 **2**, governance_warning | **PASS** | `compute('A','D',16)→(2,true)`；DOM 含治理提示文案 |
| T7 | Q2=A, 預選為 5 | foundation_warning | **PASS** | flag 邏輯：`q2==A && step∈{3,4,5}`；DOM 含資料基礎提示 |
| T8 | 無 next_step 送出 | 擋送出 + 錯誤文案 | **PASS（碼審）** | submit handler：`![1..5].includes` → preventDefault + 指定錯誤句 |
| T9 | 選 1 並送出 | next_step=1；感謝工具包 | **PASS（碼審）** | payload 含 `next_step: 1`；THANKYOU_COPY[1] |
| T10 | 改選 5 後送出 | next_step=5；primary_recommended 仍為演算法值 | **PASS（碼審）** | `primary_recommended` 來自 default；`next_step` 為使用者選擇 |
| T11 | 缺 email | 擋送出 | **PASS（碼審）** | 空值與格式雙檢 |
| T12 | 手機寬度 | 可讀可點可送 | **PASS（碼審）** | `@media (max-width:640px)` 單欄表單；radio 區塊直向堆疊 |
| T13 | 免責與隱私連結 | 可見、可開 | **PASS** | `#quiz-disclaimer` + `href="./privacy.html"` 於 lead form |

## DOM / 靜態檢查摘要

- [x] 無「暫時不需要」選項  
- [x] 五選一 radio 1–5  
- [x] 商業 Google Form action 對齊 contact  
- [x] 舊單一 CTA `#result-form-btn` 已移除  
- [x] handoff 規格檔已入 `docs/`  

## 建議 PR 合併前人工補跑（2–3 分）

1. 本地開啟 `index.html#diagnostic`（或 Pages preview）  
2. 走 T1 與 T2 各一次，確認預選 radio 與主推切換  
3. 用測試信箱送出一筆（可標 `TEST HARD V1`），確認 Google Sheet 收到 payload  
4. 手機寬度 DevTools 走完一輪  

## 已知限制

1. Google Form iframe `load` 成功回饋與既有 contact 相同，無法 100% 保證 Sheets 寫入（與現網一致）。  
2. 工具包 Google Form 未自動帶分數欄；分數以商業 Form payload 為準。  
3. 瀏覽器視覺截圖未在本機 headless 自動產出；請 reviewer 補桌面／手機各一張。  

## Sample payload（結構，email 打碼）

```
【官網成熟度快測 HARD V1】
需求類型：90 分鐘快診 NT$29,800（成熟度快測）

total_score: 14
maturity_band: execute
q1: C
q2: C
q3: C
q4: C
q5: B
primary_recommended: dx_90
default_checked: 3
next_step: 3
next_step_code: dx_90
governance_warning: false
foundation_warning: false
utm_source: site
utm_medium: consulting
utm_campaign: ai_diagnosis
utm_content: quiz_result_hard_v1
來源頁: .../index.html#diagnostic
```
