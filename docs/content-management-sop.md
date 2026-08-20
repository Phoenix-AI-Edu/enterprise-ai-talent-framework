# 03king.com 官網內容管理 SOP（內容發布與合規檢核）

| 項目 | 內容 |
|---|---|
| 文件版本 | 0.1（初稿） |
| 更新日期 | 2026-08-19 |
| 狀態 | **初稿 — 整合既有發布／禁語／合規規範；機密定價與顧問分工另見 `internal_admin/`（不公開）** |
| 適用對象 | 官網內容發布者、行銷／社群營運者（內部團隊） |
| 對應系統 | SYS-03 AI_Talent（03king.com 主官網，GitHub Pages custom domain） |
| 相關文件 | `DEVELOPMENT_GUIDELINES.md`、`docs/MARKETING_LAUNCH_KIT.md`、`docs/MARKETING_CAMPAIGN_UTM_MATRIX_v0.2.0.md` |

> **本 SOP 只講「官網內容怎麼發布、怎麼檢核」**。定價底線、顧問分工、線索管理屬機密，在 `internal_admin/`（本機 Google Drive 同步，**永不進 GitHub**），不在此重複。

---

## 1. 總覽

03king.com 是鳳凰 AI 的主官網，承載多系統的**合成展示與對外說明**（Ledger Assist、AI Allocation OS、AI 律師工作台、Enterprise RAG Foundation 等）。它是**內容源**，不是任何正式客戶資料的 data plane。

內容發布有兩條路：

1. **官網頁面**：`scripts/build_solution_pages_20260809.py` 生成器 → push `main` → GitHub Pages 直接 production。
2. **八平台社群**：LinkedIn／LINE／X／WeChat／FB／IG／Threads／YouTube，**手動發布**（不串 API），由 Owner 上傳後回填 publish-record。

---

## 2. 頁面生成（build_solution_pages）

### 用法

```bash
python scripts/build_solution_pages_20260809.py --target <target>
```

`--target` 限定生成單一 solution 頁，輸出到 `experience/<target>/index.html`。支援目標：`ledger`、`ai-allocation-os`、`ai-lawyer-workbench`。

### 生成後的必檢項目

| 檢核 | 要求 |
|---|---|
| canonical／OG／Twitter metadata | target 專屬，不繼承 central-kitchen metadata |
| 禁語 | 否定式一律改正向表述（見 §3） |
| 邊界卡（boundary） | 「現可驗證／Pilot 可配置／導入階段評估」三層如實呈現 |
| CTA | 對齊 §6 UTM 規範 |

---

## 3. 禁語檢核（否定式 → 正向表述）

官網文案**禁止否定式、自曝短板**。遇到「沒有／尚未／無」開頭的表述，改成「我們怎麼做／如何整合」的正向語感。

| 否定式（禁止） | 正向表述（改用） |
|---|---|
| 「沒有客戶」「尚未上線」 | 「我們怎麼做」「如何整合」 |
| 「不保證 ROI／SLA」 | （此類**保護性揭露須保留**，不屬禁語範疇，見 §4） |
| 把 AI 寫成「自動法律意見／取代律師」 | 「AI 輔助、律師簽核、引用可查」 |

> 注意區分：**禁語**（否定式自曝）要改；**保護性揭露**（不保證 ROI／SLA、不自動外送、零幻覺非保證）是保險絲，**不得刪除**。

---

## 4. 合規紅線（發布前必過）

| 紅線 | 要求 |
|---|---|
| 佔位符 | 發布前替換所有 `[聯絡人姓名]`／`[公司名稱]` 等，不得原樣發送 |
| 真實客戶 | **不得加入真實客戶名稱**（無具名上線實績） |
| 未驗證數據 | 不得加入未經驗證的百分比／金額／ROI |
| 串接宣稱 | 不得承諾已完成真實系統串接（維持 Pilot-ready／Sandbox 定位） |
| 結果保證 | 不宣稱勝訴率、零錯誤、期限絕不漏、省時比例 |

---

## 5. 發布流程

### 5.1 官網（GitHub Pages）

- `main` 直發：push `main` 即 production（GitHub Pages custom domain `03king.com`）。
- 發布前執行禁語檢核＋合規紅線掃描（§3、§4）。
- 變更後驗證：Chrome headless 截圖＋vision 檢核（中文無亂碼、無破版）。

### 5.2 八平台社群（手動發布）

| 平台 | 方式 |
|---|---|
| LinkedIn／X／WeChat／Threads | 手動貼文（不串 API） |
| LINE／FB／IG | 手動貼文＋圖卡 |
| YouTube | 手動上傳影片 |

- 由 **Owner 手動上傳**，發布後回填 publish-record（EVT-255 八平台發布包 71 檔）。
- 社群貼文**禁用 Markdown 表格**（LinkedIn／FB／IG／X 亂碼），用 `•` 或「標籤：說明」。

---

## 6. UTM 規範

- Primary CTA：導 landing page（`phoenix-ai-edu.github.io/...`），**不得在文宣中直接導 Google Form**。
- Secondary CTA：landing page 內才導 Google Form。
- UTM 三件套：`utm_source`（linkedin/facebook/threads/bd_dm）、`utm_medium`（social/direct/email/print）、`utm_campaign`（如 `v020_central_kitchen_ai`）。

---

## 7. 隱私與機密

| 規則 | 要求 |
|---|---|
| `internal_admin/` | 絕不公開（`.gitignore` 已鎖）；僅本機 Google Drive 同步，**嚴禁 push GitHub** |
| Shadow AI | 客戶真實名稱、機密財務、未去識別化個資，**不上傳任何公開免費 AI 模型** |
| 3 機密文件聯動 | 信箱／表單／模組／定價／顧問分工變更，**立即同步** `internal_admin/01_ops_manual.md`、`02_advisor_workflows.md`、`03_lead_management.md` |
| commit 防漏 | `git add` 階段若發現 `internal_admin/` 洩漏，立即回滾並重新配置 `.gitignore` |

---

## 8. 附錄：驗證狀態矩陣

| 章節 | 項目 | 狀態 | 備註 |
|---|---|---|---|
| §2 | 頁面生成器 | ✅ | build_solution_pages 已驗證（--target 限定） |
| §3 | 禁語檢核 | ✅ | 全素材禁語零命中（EVT-254） |
| §4 | 合規紅線 | ✅ | 佔位符／無未驗證數據已落實 |
| §5.1 | 官網發布 | ✅ | GitHub Pages main 直發已驗證 |
| §5.2 | 八平台手動發布 | 🟡 | 發布包備妥（EVT-255）；實際發布由 Owner 手動＋回填 record |
| §6 | UTM | ✅ | v0.2.0 UTM matrix 已定 |
| §7 | 隱私機密 | ✅ | internal_admin .gitignore 已鎖 |

---

*本 SOP 是內部營運文件，非法律意見；涉及補助、法規、個資、契約適用，以主管機關最新規範及 Owner 正式委任之合格專業人士意見為準。*
