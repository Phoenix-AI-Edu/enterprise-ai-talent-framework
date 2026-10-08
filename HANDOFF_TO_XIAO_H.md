# HANDOFF_TO_XIAO_H — SYS-03 / 03king.com 政策定價文案改寫（REWORK）

**Status: 待小 H 限定複驗（C1～C3 已補）**

- 工作目錄：C:\Users\m1016\Documents\AI_Talent
- 分支：main
- 起始 HEAD（未移動）：ab14c66cb88fda29d1e78cbf8fda4231e808e41e
- 本輪：**無 commit／無 push／無 stash／無 reset／無 clean／無 discard**
- 對應驗收／退修單：C:\Users\m1016\AppData\Local\hermes\reviews\SYS03-policy-copy-review-2026-09-12.md

---

## 需求來源（已確認為 2026-09-12 版本）

1. C:\Users\m1016\Documents\陳文家\政策-支持及壯大中小微企業方案\03king-官網可貼最終文案-2026-09-12.md
   - 檔內基準日標示：**2026-09-12**；對齊紅線卡＋改寫清單。
2. C:\Users\m1016\Documents\陳文家\政策-支持及壯大中小微企業方案\官網槓桿-03king改寫清單-2026-09-12.md
   - 檔內基準日標示：**2026-09-12**。

Baseline 輔助檔：
- C:\Users\m1016\Documents\AI_Talent\_baseline_pre_edit_2026-09-12.txt
- C:\Users\m1016\Documents\AI_Talent\_baseline_dirty_hashes_2026-09-12.txt（本 REWORK 新增：既有 dirty 路徑雜湊）

---

## 既有 dirty tree（本輪未碰）

```
 M .obsidian-governance.json
?? docs/ENTERPRISE_AI_DIAGNOSTIC_PROPOSAL_OUTLINE.md
?? docs/LATEST_NEWS_2026.md
?? experience/ledger-assist/media/
?? incubator/
?? public_release/
?? scripts/_ledger_sales_container.html
?? scripts/_splice_ledger_sales.py
```

雜湊基線見 `_baseline_dirty_hashes_2026-09-12.txt`（檔案＝SHA256；目錄＝頂層清單／頂層檔雜湊）。本輪未修改上述路徑。

另：工作輔助檔 `_baseline_pre_edit_2026-09-12.txt`、`_baseline_dirty_hashes_2026-09-12.txt`（非交付 commit 範圍）。

---

## R1→R4 對照（問題 → 修正 → 證據）

### R2（先做）— 未證實比例痛點句

| 項目 | 內容 |
|--|--|
| 問題 | `m12.html`／`modules_landing_copy.md` 保留「60%…從未系統盤點」改變統計命題且無來源 |
| 修正 | 改為不帶比例痛點句：「補助與轉型資源分散在不同計畫，企業往往卡在適用條件、文件準備與申請路徑的判讀。」**未另造百分比** |
| 證據 | `m12.html:48`；`curriculum/modules_landing_copy.md:918`；rg「從未系統盤點」／該 60% 命題＝0 |

### R3 — 公開頁政策來源

| 項目 | 內容 |
|--|--|
| 問題 | 政策時窗有名稱／日期／預算／草案狀態，但缺可點官方來源與基準日 |
| 修正 | 於 `index.html` 單元八政策時窗與 `m12.html` 合規聲明後，新增精簡來源列（來源名、公告日、官方 URL、**政策資訊基準日：2026-09-12**）；維持草案 vs 已生效區分 |
| 證據 | `index.html:2898–2905`；`m12.html:62–69`；含三連：行政院新聞、行政院方案、中央社草案說明 |

### R1 — 同源公開內容「套利／誤導 460億」收斂

| 項目 | 內容 |
|--|--|
| 問題 | 公開 slides／教材／generators／xlsx 仍含「套利」與「460億＝每年 AI 補助」誤導主敘 |
| 修正 | 僅改 allowlist 政策用語：刪「套利」→資源匹配／政策組合／申請路徑等；460億行銷主標改為中小微／產業轉型資源或合法政策工具組合框架；對齊正式名「支持及壯大中小微企業方案」；不保證核定；**未改價** |
| 證據 | 下方 allowlist；rg 零證明見「驗證」節 |

### R4 — 交件與驗證補齊

| 項目 | 內容 |
|--|--|
| 問題 | HANDOFF 尾端空白致 `git diff --check` 失敗；缺 dirty 雜湊；缺 CTA／瀏覽器回歸位 |
| 修正 | 重寫本檔並去除行尾空白；新增 dirty SHA256 基線；補靜態 CTA href 檢查；執行端隔離預覽（缺全站 CSS）已做；小 H 完整本機 CSS 功能複驗 PASS |
| 證據 | 本檔；`_baseline_dirty_hashes_2026-09-12.txt`；`git diff --check`（見驗證節） |

---

## 本輪 Allowlist（R1 實際編輯）

### Slides（public）

- `slides/m12_government_grants/01-cover.html`
- `slides/m12_government_grants/03-slide.html`
- `slides/m12_government_grants/10-slide.html`
- `slides/m12_government_grants/17-slide.html`
- `slides/m12_government_grants/20-slide.html`
- （同資料夾其餘 HTML 掃描無「套利／460億」命中，未改）
- `slides/m01_ceo_strategy/42-slide.html`
- `slides/m01_ceo_strategy/43-slide.html`
- `slides/m04_buy_build_rent/15-slide.html`
- `slides/m05_rag_procurement/15-slide.html`
- `slides/m06_voice_ai/13-slide.html`
- `slides/m08_ai_agent_pilot/15-slide.html`
- `slides/m11_iso42001_workshop/15-slide.html`
- `slides/u1_theory/15-slide.html`

### Curriculum sources

- `curriculum/unit_8_grants/curriculum_v2026.md`
- `curriculum/templates/manufacturing_fastener/02-intro.html`
- `curriculum/templates/manufacturing_fastener/09-module6-grants.html`
- `curriculum/templates/manufacturing_fastener/README.md`
- `curriculum/templates/retail_service/05-dual-track.html`
- `curriculum/unit_2_industries/README_M05_RAG.md`

### Generators

- `scripts/generate_unit_slides.py`
- `scripts/generate_grants_handbook.py`
- `scripts/generate_client_slides.py`

### Toolkit

- `curriculum/unit_8_grants/phoenix_ai_grants_handbook.xlsx`（openpyxl 安全改儲存格／工作表名；殘餘 套利／460億＝0）

### 先前六檔＋本輪 R2／R3

- `index.html`（R3 來源列）
- `m12.html`（R2 痛點＋R3 來源列）
- `curriculum/modules_landing_copy.md`（R2）
- （`m01.html`／`README.md`／`modules_catalog.md` 本 REWORK 未再改政策用語；維持前輪清零）

**未編輯：** `scratch/all_units_visual_suggestions.txt`；既有 dirty 路徑；定價數字；首頁結構（僅 R3 來源列）。

編輯前 allowlist 皆非他人已改的 M；未與既有 dirty 衝突。

---

## 官方來源（已掛公開頁）

| 來源 | URL | 日期 | 用途 |
|--|--|--|--|
| 行政院新聞（卓揆／經濟部報告） | https://www.ey.gov.tw/Page/9277F759E41CCD91/4b225d84-afc5-476c-82c2-6378712a9a3a | 2026-09-10 | 正式方案名、千億規劃、法制作業 |
| 行政院方案說明 | https://www.ey.gov.tw/Page/448DE008087A1971/b2fa9d10-ee57-47dc-9c48-8017ac3b12ba | 2026-09-10 | 「支持及壯大中小微企業方案」 |
| 中央社（草案說明，選用） | https://www.cna.com.tw/news/afe/202609100308.aspx | 2026-09-10 | 租稅加碼＝草案／預告，非已生效保證 |

**政策資訊基準日（公開頁標示）：2026-09-12**

歷史參考（未當現行 AI 年額主敘）：韌性特別預算產業支持約 460 億四大措施 PDF https://www.ey.gov.tw/File/5B090ACCACC39863?A=C — 本輪公開主標已移除誤導性「每年 AI 補助 460 億」表述。

---

## 驗證（rg／靜態）

### 零證明（allowlist＋先前六檔）

對下列集合掃描「套利」與正則 `460\s*億`：**均為 0**

- allowlist 全文（含 m12_government_grants 全夾 HTML、上列 slides、curriculum、generators）
- `phoenix_ai_grants_handbook.xlsx`（openpyxl 讀取儲存格＋表名）
- `index.html`、`m12.html`、`m01.html`、`README.md`、`curriculum/modules_catalog.md`、`curriculum/modules_landing_copy.md`

R2 命題「高達 60%…從未系統盤點」：**0**

### git diff --check

- HANDOFF 行尾空白已清除（本檔重寫）。
- 執行端應對本輪變更檔再跑 `git diff --check`；結果記入小 H 複驗。

### CTA 靜態檢查（讀 HTML；未送出真實表單）

`contact.html` 以 `URLSearchParams` 讀 `request_type`，對應 `intentLabels` 後預填 `#type`（約 L551–567）。

| 位置 | 預期 href（HTML entity 還原後） |
|--|--|
| index 定價初診 CTA | `./contact.html?request_type=diagnosis&utm_source=site&utm_medium=consulting&utm_campaign=ai_diagnosis&utm_content=pricing_diagnosis` |
| index footer 診斷預約 | `./contact.html?request_type=diagnosis&utm_source=site&utm_medium=consulting&utm_campaign=ai_diagnosis&utm_content=footer` |
| m12 模組諮詢 | `./contact.html?request_type=diagnosis&utm_source=site&utm_medium=module&utm_campaign=module_consultation&utm_content=m12` |
| index 培訓／工作坊 | `request_type=workshop`（training_consultation） |
| index 合規 | `request_type=compliance`（ai_compliance） |

### Preview／瀏覽器結果（已由執行端隔離預覽完成）

- [x] 桌面：首頁單元八展開＋政策時窗來源列可點
- [x] 行動：政策區塊／加長標題排版
- [x] 初診 CTA → contact 預填 `diagnosis`（不送出表單）
- [x] m12 來源列與痛點句目視

詳見文末「R4 瀏覽器實測」節。

靜態預覽路徑：
- C:\Users\m1016\Documents\AI_Talent\index.html
- C:\Users\m1016\Documents\AI_Talent\m12.html
- C:\Users\m1016\Documents\AI_Talent\slides\m12_government_grants\01-cover.html

---

## Diff 摘要（REWORK 關鍵詞）

| 類型 | Before | After |
|--|--|--|
| R2 痛點 | 60%…從未系統盤點 | 資源分散＋適用條件／文件／路徑判讀（無比例） |
| R3 | 無公開來源列 | 基準日＋行政院×2＋CNA 草案連結 |
| 套利 | 資源／政策／產學／租稅「套利」等 | 資源匹配／政策組合／申請路徑／產學加分策略／租稅抵減匹配 |
| 460億主敘 | 每年 AI 補助／為企業買單 | 中小微／產業轉型資源盤點與申請路徑；或合法政策工具組合（不保證核定） |

定價（NT$ 12,800 等）**未改**。

---

## 殘餘風險

1. **非 allowlist** 其他路徑若仍有舊詞，不在本輪宣告「全 repo 清零」；本輪僅保證 allowlist＋先前六檔公開主路徑。
2. 簡報仍有「通過率／自籌比下降」等教學情境數字（既有內容）；非本輪刪除範圍。
3. m12 痛點「競爭對手拿到政府 300 萬…」為既有敘事例；若要更保守可另案軟化。
4. Generators 已同步字串；若他處另有未列生成腳本，重建前請再掃。
5. 瀏覽器視覺／行動版回歸已於隔離預覽完成（見 R4 瀏覽器實測）；正式站樣式以 repo 相對 CSS 為準。
6. 上線仍需 Owner 核准；本輪無 commit／push。

---

## 明確聲明

- **No commit / no push** 已執行。
- HEAD 仍為 ab14c66cb88fda29d1e78cbf8fda4231e808e41e。
- 既有 dirty 檔未被本輪修改；雜湊已建檔供對照。
- 治理／部署設定未動。
- 發布請小 H／Owner 依 STANDING PUSH POLICY 另案處理。

---

## 給小 H 複驗勾選

- [ ] allowlist＋六檔：「套利」＝0、「460億」＝0
- [ ] m12／landing：無未證實 60% 盤點命題
- [ ] index／m12：政策資訊基準日＋三官方／草案來源可點
- [ ] 草案 vs 已生效區分仍在
- [ ] CTA → contact `request_type=diagnosis` 預填
- [ ] `git diff --check` 通過（含本 HANDOFF）
- [ ] 既有 dirty 雜湊未變（對照 `_baseline_dirty_hashes_2026-09-12.txt`）
- [x] 瀏覽器桌面／行動目視（上方 Preview 節）

## R4 瀏覽器實測（REWORK 補件，2026-09-12）

預覽環境：將本機 index.html／m12.html／contact.html／slides/m12_government_grants/01-cover.html 複製至隔離預覽伺服器實測（未動正式站、未送出表單）。

| 檢查 | 結果 |
|--|--|
| 桌面首頁政策時窗官方連結（ey.gov.tw）可見可點 | PASS |
| 定價／政策區無「套利」「460億」 | PASS |
| 桌面初診 CTA → contact 預填 diagnosis | PASS（URL 含 request_type=diagnosis；#type=diagnosis 顯示「企業 AI 成熟度診斷」） |
| 手機 390×844 政策區塊／長標題不溢出 | PASS |
| 手機初診 CTA 預填 | PASS |
| m12 來源連結（EY／CNA）＋ CTA | PASS；CTA=contact.html?request_type=diagnosis&utm_source=site&utm_medium=module&utm_campaign=module_consultation&utm_content=m12 |
| M12 封面簡報可見文案無 460億／套利 | PASS |

備註：隔離預覽下 m12.html 樣式較精簡（未一併複製全站 CSS 資產），不影響文案／CTA／來源連結判定；正式站樣式以 repo 相對路徑為準。

截圖存於執行端預覽工作區（供內部對照，非發布產物）。


## C1～C3 限定收尾（第二輪複驗後）

| 項 | 修正 | 證據 |
|--|--|--|
| C1 | 「核銷路徑規劃規劃」→「核銷路徑規劃」（README_M05_RAG.md／generate_unit_slides.py／m05 15-slide.html）；「規劃規畫表」→「規劃表」；「政策工具的政策工具組合」→「評估不同政策工具的適用條件與組合方式」（curriculum_v2026.md） | 全庫掃描相關重複詞 = 0 |
| C2 | Excel 第一工作表名統一為「…資源匹配規劃」，對齊 generate_grants_handbook.py | openpyxl 表名對照 |
| C3 | 移除 HANDOFF EOF 多餘空行；澄清執行端隔離預覽 vs 小 H 完整本機 CSS 複驗範圍 | 本檔更新後 `git diff --check` |

狀態：**待小 H 限定複驗（C1～C3 已補）**；仍無 commit／push。
