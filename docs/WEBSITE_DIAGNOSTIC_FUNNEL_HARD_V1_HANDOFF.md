# 官網「AI 成熟度快測」結果漏斗 — 最硬商業版（必選 1–5）

**文件 ID：** `WEBSITE-DIAG-FUNNEL-HARD-V1`  
**日期：** 2026-07-20  
**狀態：** `READY_FOR_WEBSITE_COLLABORATOR`  
**目標站點：** https://phoenix-ai-edu.github.io/enterprise-ai-talent-framework/  
**錨點：** `#diagnostic`（企業 AI 成熟度快速診斷器）  
**授權範圍：** **僅修改官網 repo**（`enterprise-ai-talent-framework` / GitHub Pages）。**禁止**修改 `AI_Allocation_OS` 的 Kernel、Workbench、Field RC。  
**產品裁決：** CEO／專案負責人  
**執行角色：** 官網協作者（前端／內容）  
**規格來源：** Phoenix 商業漏斗設計（對齊 Capital Decision Sprint 與官網既有定價）

---

## 1. 任務目標（DoD）

完成後，訪客行為必須符合：

1. 仍完成既有 **5 題 A–D** 成熟度快測（題幹可維持不動，除非實作需要小幅無語意變更）。
2. 顯示 **總分（5–20）**、**成熟度定位**、**主推說明**、**必備免責**。
3. 結果區提供 **五選一「下一步」**，且：
   - **必須選 1–5 之一才能送出**；
   - **沒有**「暫時不需要／只要存檔／略過」類選項；
   - 系統依演算法 **預選** 一項（使用者可改選）。
4. 送出時一併送出：分數、各題選項、預設推薦、使用者最終選擇、聯絡資料。
5. 依選擇顯示對應 **感謝文案**（或導向既有 contact／Google Form 並帶參數）。
6. 桌面與手機可完成全流程；未選下一步時送出被擋並有明確錯誤提示。

**非目標：**

- 不把 Decision Kernel／Field／Workbench 接到公開站。
- 不在結果頁宣稱「投資已核准」「保證 ROI」「自動 fund PoC」。
- 不刪除既有個資告知與隱私權連結。

---

## 2. 背景：兩套產品如何分工（給協作者）

| 層級 | 是什麼 | 本任務 |
|------|--------|--------|
| 官網 5 題快測 | 組織 AI **成熟度／商機預篩** | **要改** |
| 初診／快診／工作坊 | 官網既有顧問服務 | CTA 對齊 |
| Capital Decision Sprint | 付費後用 **Field RC** 做可稽核流程投資決策（另一工程庫） | **只在文案與選項 5 出現**；不實作診斷引擎 |

問卷 **不是** Allocation OS 的縮小版執行環境，只是漏斗前端。

---

## 3. 計分與標籤（保持與現站一致）

| 選項 | 分 |
|------|-----|
| A | 1 |
| B | 2 |
| C | 3 |
| D | 4 |

- `total_score` = Q1+Q2+Q3+Q4+Q5 ∈ **[5, 20]**
- `maturity_band`：

| 分數 | band 代碼 | 中文顯示 |
|------|-----------|----------|
| 5–8 | `explore` | 探索期 |
| 9–12 | `start` | 起步期 |
| 13–16 | `execute` | 推進期 |
| 17–20 | `operate` | 制度化期 |

五題維度（現站既有，供結果摘要可選顯示）：

1. 商業驅動與戰略對齊  
2. 數據基礎與技術可行性  
3. 組織與變革管理  
4. 風險安全與合規防線  
5. 專案執行力與預算決策  

---

## 4. 必選五項（固定；禁止增刪「離開」選項）

使用者 **必須** 且 **僅能** 選擇一項 `next_step`：

| 值 | 代碼 | 畫面標籤（請用此文案或語意等價、勿淡化） |
|----|------|------------------------------------------|
| `1` | `kit` | **索取 Notion＋Excel 工具包**，並依我的結果寄送對應文字指引 |
| `2` | `dx_lite` | **預約專家初診**（NT$12,800，可全額折抵後續方案） |
| `3` | `dx_90` | **預約 90 分鐘企業 AI 成熟度專家快診**（NT$29,800，可折抵工作坊） |
| `4` | `ws` | **洽詢戰略畫布／場景工作坊**（90 天路線圖與跨部門共識） |
| `5` | `sprint` | **洽詢 Capital Decision Sprint**（AI 預算／流程投資決策，可稽核決策包） |

**禁止新增：**

- 暫時不需要  
- 只要看結果不要聯絡  
- 略過／稍後再說  

**必選區上方固定提示：**

> 請選擇一項我們將為您安排的下一步（必選）。未選擇無法送出。  
> 每一項皆由鳳凰 AI 顧問團隊承接；我們不會在未確認範圍前逕行收費或進場。

**未選錯誤提示：**

> 請先勾選一項下一步服務（工具包／初診／快診／工作坊／Capital Decision Sprint）。

---

## 5. 預選演算法（`default_checked`）

使用者可改選；**預設必須依下列規則勾選一項**，降低空白送出。

### 5.1 特殊覆蓋（最高優先）

```
IF Q4 == "A" AND Q5 IN ("C", "D"):
    default_checked = 2   # dx_lite
    governance_warning = true
ELSE
    governance_warning = false
```

### 5.2 主表（無上列覆蓋時）

```
IF Q5 == "A":
    default_checked = 1   # kit

ELSE IF Q5 == "B":
    IF total_score <= 8:   default_checked = 1
    ELSE IF total_score <= 12: default_checked = 2
    ELSE: default_checked = 3

ELSE IF Q5 == "C":
    IF total_score <= 8:   default_checked = 2
    ELSE IF total_score <= 12: default_checked = 3
    ELSE: default_checked = 4   # 13–20 → ws

ELSE IF Q5 == "D":
    IF total_score <= 12:  default_checked = 3
    ELSE: default_checked = 5   # 13–20 → sprint
```

### 5.3 速查表

| Q5 \ 分數帶 | 5–8 explore | 9–12 start | 13–16 execute | 17–20 operate |
|-------------|-------------|------------|---------------|---------------|
| **A** | **1** | **1** | **1** | **1** |
| **B** | **1** | **2** | **3** | **3** |
| **C** | **2** | **3** | **4** | **4** |
| **D** | **3** | **3** | **5** | **5** |

（Q4=A 且 Q5=C/D 時整列改預選 **2**，並顯示治理提示。）

### 5.4 資料基礎提示旗標（不改預選，只加文案）

```
foundation_warning = (Q2 == "A" AND default_checked IN (3, 4, 5))
```

若使用者改選後 `next_step` 仍為 3/4/5 且 Q2=A，感謝前／主推區可持續顯示 foundation 提示。

### 5.5 主推文案塊對應

| default / 強調主推 | 文案塊 ID |
|--------------------|-----------|
| 1 | `P-KIT` |
| 2 | `P-DX-LITE` |
| 3 | `P-DX-90` |
| 4 | `P-WS` |
| 5 | `P-SPRINT` |

**顯示規則：** 結果頁「建議為您安排」區塊永遠依 **演算法 default** 顯示主推文案（即使使用者改選 radio，主推說明可維持 default，或改為隨 radio 即時切換——**建議：隨 radio 即時切換主推說明**，體驗較佳）。最低要求：載入時依 default 顯示正確主推。

---

## 6. 結果頁 UI 結構（建議 DOM 順序）

```
[A] 標題：您的企業 AI 成熟度快測結果
[B] 分數列：{total}/20 ｜ 定位：{中文 band}
[C] 免責聲明（固定，見 §7.1）
[D] 主推說明（P-* 文案，隨預選／選項）
[E] 可選：governance_warning / foundation_warning
[F] 必選區：下一步 1–5（radio，預選 default）
[G] 聯絡表單欄位
[H] 個資同意勾選 + 隱私權連結（沿用現站）
[I] 送出按鈕
[J] 送出後：感謝狀態或導向 thank-you / contact
```

**既有 CTA：**  
現站「搶先登記預約 90 分鐘…」等連結可保留為次要，但 **主路徑必須走必選 1–5 + 送出**，避免雙軌混亂。建議次要連結改為與選項 3 等價說明，或收進選項說明內。

---

## 7. 文案定稿（請直接使用）

### 7.1 免責（所有結果必顯示）

```
本結果依五個組織維度快速定位，供選擇後續服務參考。
不構成單一專案投資核准、ROI 保證或「必須導入 AI」之結論。
若需對特定流程做成可稽核的撥款／延後／拒絕決策，請選擇 Capital Decision Sprint。
```

### 7.2 主推文案塊

#### P-KIT

```
建議為您安排：① 工具包與文字指引

以您目前的預算節奏與準備度，最適合先建立內部共同語言與自助盤點，
避免條件未成熟就進入高成本 PoC。
請於下方確認選項 1，或改選付費診斷／工作坊／Capital Decision Sprint。
```

#### P-DX-LITE

```
建議為您安排：② 專家初診（NT$12,800，可全額折抵後續方案）

您已出現值得收斂的問題訊號，但範圍、時程或治理條件仍需對焦。
初診由顧問研析後交付精簡報告與路徑建議，並安排短視訊確認下一步。
請確認選項 2，或改選其他服務。
```

#### P-DX-90

```
建議為您安排：③ 90 分鐘成熟度專家快診（NT$29,800，可折抵工作坊）

您具備一定急迫或預算條件，適合用深度快診收斂優先場景、風險與 90 天方向。
請確認選項 3，或改選其他服務。
```

#### P-WS

```
建議為您安排：④ 戰略畫布／場景工作坊

您的執行與預算帶適合進入跨部門共識與 90 天路線圖。
工作坊產出董事會可用的優先級與路徑；若需對具體流程做成撥款級決策紀錄，
請改選 ⑤ Capital Decision Sprint。
請確認選項 4。
```

#### P-SPRINT

```
建議為您安排：⑤ Capital Decision Sprint（AI 資本決策）

您呈現較高急迫與預算條件，適合進入可追溯證據與風險閘門的資本決策流程，
產出委員會級決策包（Decision Snapshot／Committee Pack）。
結論可能是探索投入、基礎修復、延後或拒絕 AI——服務費用不因結論方向改變。
正式執行於範圍與資料條件確認後，由顧問以受控流程進行
（非本頁自動產出最終投資決定）。
請確認選項 5，或改選快診／工作坊若您尚未準備好決策會議。
```

### 7.3 附加提示

#### governance_warning（Q4=A 且 Q5∈{C,D}）

```
治理提示：您目前對生成式 AI 使用與合規防線偏弱。
我們建議先透過初診／快診對齊使用規範與風險底線，再擴大 PoC 或撥款決策，
以降低資安與個資暴露。
```

#### foundation_warning（Q2=A 且主推／選擇為 3/4/5）

```
資料基礎提示：核心資料偏離散時，後續正式診斷較常先指向「基礎修復／探索」，
而非直接 Fund PoC。這是為了降低失敗 PoC，不是拒絕服務。
```

### 7.4 感謝文案

| next_step | 標題 | 正文 |
|-----------|------|------|
| 1 | 已為您登記工具包 | 我們將於約定工作日內寄送 Notion＋Excel 工具包與對應文字指引。若需升級診斷，請來信或再次於網站預約。 |
| 2 | 已為您登記專家初診 | 我們將與您確認時段、請款方式與資料清單。初診費用 NT$12,800，可依官網規則全額折抵後續方案。 |
| 3 | 已為您登記 90 分鐘快診 | 我們將與您確認時段與請款方式。費用 NT$29,800，可依官網規則折抵工作坊。 |
| 4 | 已為您登記工作坊洽詢 | 我們將提供範圍說明、報價區間與可排檔期，再與您確認是否啟動。 |
| 5 | 已為您登記 Capital Decision Sprint 洽詢 | 我們將提供服務範圍、資料最小化清單、時程與訂金說明。確認後始進入受控診斷流程；本頁成熟度分數不作最終投資決定。 |

---

## 8. 聯絡表單欄位

### 8.1 使用者可見（建議）

| 欄位 | 必填 | 說明 |
|------|------|------|
| 公司名稱 | 是 | |
| 姓名 | 是 | |
| 角色 | 是 | 下拉：企業主/總經理、COO、CFO、CIO/IT、轉型/CDO、客服或營運主管、其他 |
| 工作 Email | 是 | 基本格式驗證 |
| 電話 | 是（最硬商業版） | |
| 個資同意 | 是 | 連結既有 `privacy.html` |
| next_step 1–5 | 是 | radio |

### 8.2 隱藏／一併送出欄位

| 欄位名 | 內容 |
|--------|------|
| `total_score` | 5–20 |
| `maturity_band` | explore\|start\|execute\|operate |
| `q1` … `q5` | A\|B\|C\|D |
| `primary_recommended` | 演算法 default 對應代碼 kit\|dx_lite\|dx_90\|ws\|sprint |
| `default_checked` | 1–5 |
| `next_step` | 使用者最終 1–5 |
| `foundation_warning` | true\|false |
| `governance_warning` | true\|false |
| `utm_source` | 若 URL 已有則保留 |
| `utm_medium` | |
| `utm_campaign` | |
| `utm_content` | 固定建議：`quiz_result_hard_v1` |

### 8.3 送出端點

協作者擇一實作（需與負責人確認現網慣例）：

**方案 A（建議，改動小）：**  
導向既有 `contact.html` 或 Google Form，以 query string / 隱藏欄帶上 §8.2。

**方案 B：**  
結果區內嵌表單 POST 至既有收集端；成功後同頁顯示 §7.4。

**無論 A/B：** 未選 1–5 或缺必填 → **不得送出**。

現有工具包 Google Form 可作為 `next_step=1` 的落地之一，但須仍記錄分數參數（可 mail 副本或 sheet 欄位）。

---

## 9. 前端校驗偽碼

```
function score(letter):
  return {A:1, B:2, C:3, D:4}[letter]

total = score(Q1)+score(Q2)+score(Q3)+score(Q4)+score(Q5)
band = total<=8 ? "explore" : total<=12 ? "start" : total<=16 ? "execute" : "operate"

if Q4=="A" and Q5 in ["C","D"]:
  default = 2
  governance_warning = true
else if Q5=="A":
  default = 1
else if Q5=="B":
  default = total<=8 ? 1 : total<=12 ? 2 : 3
else if Q5=="C":
  default = total<=8 ? 2 : total<=12 ? 3 : 4
else: # D
  default = total<=12 ? 3 : 5

preselect radio[default]
show copy for default (or live-update on radio change)

on Submit:
  if next_step not in [1,2,3,4,5]: show error; return
  if !company || !name || !role || !email || !phone: show error; return
  if !privacy_agreed: show error; return
  payload = { ...visible, ...hidden }
  send(payload)
  show thank-you for next_step
```

---

## 10. 實作工作拆解（給協作者的 checklist）

### Phase 0 — 開工前（30 分）

- [ ] 確認可寫入的官網 git repo 與部署方式（GitHub Pages）
- [ ] 確認表單最終端點（contact / Google Form / 其他）與誰收信
- [ ] 拉最新 `main`（或正式分支），開分支建議：`feat/diagnostic-funnel-hard-v1`
- [ ] 讀完本文件 §1–9，有衝突價位以 **官網現網標價** 為準並回報 CEO（勿默改 Sprint 定價文案中的服務定位）

### Phase 1 — 結果頁骨架

- [ ] 5 題完成後進入結果狀態（若現有已有計分 UI，在其上擴充）
- [ ] 顯示 total_score、maturity_band 中文
- [ ] 插入 §7.1 免責
- [ ] 插入主推區容器 + 5 個 radio + 提示句

### Phase 2 — 演算法與文案

- [ ] 實作 §5 預選邏輯
- [ ] 實作 P-* 五段文案與 warning 兩段
- [ ] （建議）radio change 時更新主推文案

### Phase 3 — 表單與送出

- [ ] 聯絡欄位 + 個資
- [ ] 隱藏欄位 payload
- [ ] 前端校驗（必選 1–5）
- [ ] 感謝文案 §7.4 或導頁帶參

### Phase 4 — 文案與 CTA 清理

- [ ] 避免結果頁多個互相矛盾的主 CTA
- [ ] 確認 Sprint 文案含「非正式自動投資決定」「費用不因結論改變」
- [ ] 隱私權連結仍可點

### Phase 5 — 測試與上線

- [ ] 執行 §11 測試矩陣
- [ ] PR 說明附：螢幕截圖（手機+桌面）、測試勾選表
- [ ] 合併後驗證 production URL `#diagnostic`
- [ ] 通知商業負責人：開始依 `next_step` 做 48h 跟進

---

## 11. 測試矩陣（上線前必過）

| # | 操作 | 期望 |
|---|------|------|
| T1 | 五題皆 A | score=5, band=探索期, 預選 **1**, 顯示 P-KIT |
| T2 | 五題皆 D | score=20, band=制度化期, 預選 **5**, 顯示 P-SPRINT |
| T3 | Q5=B, 其餘 C（估 total 約 14） | 預選 **3** |
| T4 | Q5=C, total 落在 13–16 | 預選 **4** |
| T5 | Q5=D, total≤12 | 預選 **3**（非 5） |
| T6 | Q4=A, Q5=D, 其餘任意使 total 中高 | 預選 **2**, 顯示 governance_warning |
| T7 | Q2=A, 預選為 5 | 顯示 foundation_warning |
| T8 | 不選 radio（若可清空）或強制無選 | 無法送出 + 錯誤文案 |
| T9 | 選 1 並送出 | payload next_step=1；感謝工具包 |
| T10 | 改選 5 後送出 | next_step=5；primary_recommended 仍為演算法值；default_was 可記錄 |
| T11 | 缺 email | 擋送出 |
| T12 | 手機寬度走完 | 可讀、可點、可送 |
| T13 | 免責與隱私連結 | 可見、可開 |

請將 T1–T13 結果貼在 PR 描述（PASS/FAIL）。

---

## 12. 商業端後續（非官網 repo，但需知會負責人）

上線後 **48 小時內** 跟進（由商業負責人，非前端）：

| next_step | 動作 |
|-----------|------|
| 1 | 寄工具包；弱意向標記 |
| 2–3 | 約時段 + 請款資訊 |
| 4 | 範圍與價帶一頁 |
| 5 | Sprint 說明 + 是否短約；**確認後才用 Field RC**（`AI_Allocation_OS` / field-rc） |

前端 **不實作** Field 連線。

---

## 13. 範圍外與禁止事項

- 修改 `AI_Allocation_OS` / Decision Kernel / Field Desktop Launcher  
- 公開站執行完整 DecisionInput 或顯示 fund_poc 為「已核准」  
- 新增「不需要任何服務」選項（本版明確禁止）  
- 刪除個資法第 8 條相關告知  
- 未經 CEO 同意改動 Sprint／初診／快診 **價格數字**（若現網價格與本文不一致：**以現網為準**，並在 PR 註記差異）

---

## 14. 交付物清單（協作者交回）

1. Git 分支／PR 連結  
2. Production 驗證 URL（含 `#diagnostic`）  
3. T1–T13 測試紀錄  
4. 表單實際收到的一筆 sample payload（可打碼 email）  
5. 已知限制（若有）

---

## 15. 聯絡與升級

| 問題類型 | 找誰 |
|----------|------|
| 價位／必選 1–5 是否放寬 | CEO／產品負責人 |
| Sprint 話術是否過界 | 產品負責人（對齊 Allocation OS 信任模型） |
| 表單收件、CRM | 商業負責人 |
| HTML/JS/CSS 實作 | 官網協作者（本文執行方） |

---

## 16. 一頁摘要（可印給協作者）

```
任務：成熟度 5 題結果頁 → 強制五選一服務漏斗（無「不需要」）
預選：看 Q5 + 總分；Q4=A 且急預算 → 預選初診
文案：免責 + 五段主推 + 兩段警告 + 五段感謝
送出：聯絡必填 + score/q1-5/next_step 等隱藏欄
禁止：接 Kernel、保證 ROI、略過選項
測完：T1–T13 全 PASS 再上 production
```

---

**文件結束。** 執行時以本檔為唯一實作規格；若與口頭說明衝突，以本檔 + CEO 書面裁決為準。
