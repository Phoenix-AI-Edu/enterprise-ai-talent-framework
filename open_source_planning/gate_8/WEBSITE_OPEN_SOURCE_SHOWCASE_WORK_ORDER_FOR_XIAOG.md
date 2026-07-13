# Phoenix 開源系統官網展示與商業轉換任務書

- 文件狀態：`APPROVED FOR PLANNING AND IMPLEMENTATION`
- Accountable Owner：Phoenix AI 專案決策者
- Executor：小 G
- Reviewer：官網整合負責人、商業內容審核人、發布核准人
- 建立日期：2026-07-13
- 執行範圍：`C:\Users\m1016\Documents\AI_Talent`
- 公開專案：<https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow>
- 首版 Release：<https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/releases/tag/v0.1.0>

## 1. 任務目標

將 **Phoenix Auditable AI Workflow** 製作成官網第三套旗艦 AI 系統展示，並與既有的：

1. 中央廚房營運防護台；
2. 企業問題診斷與決策交付工作台；
3. Phoenix Auditable AI Workflow 開源參考架構；

整合為一條一致的 Phoenix AI 能力敘事與商業漏斗，而不是三個互不相干的 Demo。

官網訪客必須能在 3 分鐘內理解：Phoenix 不只提供概念或模型呼叫，而是能把「營運場景、顧問診斷、治理控制與技術證據」組成可落地、可審閱、可進入付費 Pilot 的企業 AI 工作流。

本任務的商業目的為：

- 用公開程式碼與測試證據建立技術信任；
- 將 GitHub 技術流量導回 Phoenix 官網；
- 將官網決策者流量導向 Demo、企業診斷、內訓、Pilot 與客製導入；
- 保留 Phoenix 名稱、品牌與顧問服務的商業辨識度；
- 建立可持續量測、更新及交接的展示機制。

## 2. 不可更改的產品定位

### 2.1 三套系統的角色

| 系統 | 證明的能力 | 對應買方問題 | 商業承接 |
| --- | --- | --- | --- |
| 中央廚房營運防護台 | 一線營運事件、例外治理與人工決策閉環 | 「能不能落到真實營運流程？」 | 營運診斷、場景 Pilot、系統整合 |
| 企業問題診斷工作台 | 顧問主導的問題結構化、證據整理與決策交付 | 「能不能幫管理團隊把問題與責任說清楚？」 | 企業診斷、工作坊、顧問陪跑 |
| Phoenix Auditable AI Workflow | Policy-as-code、引用驗證、人工覆核與稽核軌跡的公開證據 | 「你們的安全與治理能力是否可被技術團隊檢驗？」 | AI 治理內訓、架構評估、客製導入與維護 |

統一主張：

> Phoenix AI 把企業問題做成可驗證、可人工決策、可留下證據的工作流；開源專案公開的是參考架構與工程證據，Phoenix 收費交付的是診斷、設計、導入、培訓與持續治理。

### 2.2 禁止定位

不得將本系統描述為：

- 自主 AI 顧問或取代顧問的 SaaS；
- 已通過法律、金融、ISO 或政府合規認證的產品；
- 可防止所有幻覺、攻擊或違規的安全產品；
- 不可竄改的正式稽核系統；
- 已在客戶正式生產環境創造成效的案例；
- 可提供投資、法律、醫療或其他專業個案建議的工具。

必須清楚標示：`Local / Mock-first reference architecture`、`Human-reviewed`、`Not production ready`，以及正式導入仍需依客戶資料、權限、資安與法規需求另行評估。

## 3. 官網資訊架構

### 3.1 首頁

在既有 `#flagship-system` 區塊加入第三張精選卡，不另建一套互相衝突的卡片機制。資料來源沿用：

- `experience/solutions_data.js`
- `experience/index.html`
- `experience/TOOL_PUBLISHING.md`

第三張卡片建議資料：

- `id`: `phoenix_auditable_ai_workflow`
- `slug`: `phoenix-auditable-ai-workflow`
- 標題：`Phoenix 可稽核 AI 工作流`
- 副標：`把政策防護、引用證據、人工覆核與稽核紀錄組成可檢驗的企業 AI 參考架構`
- 狀態：`Open Source v0.1.0 / Local Reference`
- 類別：`AI 治理`、`可稽核工作流`、`開源參考架構`
- 首要 CTA：`查看開源系統展示`
- 次要 CTA：`前往 GitHub`
- 商業 CTA：`預約 AI 治理與導入診斷`

### 3.2 獨立詳情頁

建立：

`experience/phoenix-auditable-ai-workflow/index.html`

頁面不可只是 GitHub README 的複製，必須依決策者閱讀順序呈現：

1. **Hero：** 企業風險與成果，不以技術名詞開場；
2. **30 秒理解：** Input Policy → Knowledge → Model → Output Policy → Human Review → Audit；
3. **可驗證證據：** 公開 Repo、v0.1.0 Release、59 項測試通過、公開治理文件；
4. **互動／錄影展示：** 問題輸入、政策衝突、送人工覆核、核准／拒絕、依 `request_id` 查詢稽核軌跡；
5. **開源與付費邊界：** 清楚說明免費取得什麼、Phoenix 收費交付什麼；
6. **三類買方入口：** 管理者、IT／CTO、顧問／培訓夥伴；
7. **商業 CTA：** 預約診斷與 Demo；
8. **限制聲明：** 本機、Mock-first、非生產環境認證。

### 3.3 三系統組合圖

在首頁或 AI 系統總覽增加一張「Phoenix 企業 AI 落地能力鏈」：

```text
營運場景證明（中央廚房）
        ↓
問題診斷與決策交付（顧問工作台）
        ↓
治理、人工覆核與技術證據（開源工作流）
        ↓
企業診斷 → 付費 Pilot → 客製導入 → 培訓／維護
```

圖上不得暗示三個系統已合併成同一個正式生產平台；應表述為 Phoenix 的「能力組合與導入方法」。

## 4. 開源與付費服務邊界

詳情頁必須包含下表，避免訪客只拿程式碼、不理解 Phoenix 的商業價值：

| 公開免費 | Phoenix 付費服務 |
| --- | --- |
| 本機 Mock-first 參考架構 | 企業問題與治理現況診斷 |
| Policy、HITL、Audit 的示範介面 | 客戶政策、資料與權限邊界設計 |
| 合成 HR 案例與測試 | 場景選擇、工作坊與 Pilot 成功指標 |
| 安裝、測試與治理文件 | SSO、RBAC、資料遮蔽、正式系統整合評估 |
| 社群 Issue 與版本 Release | 導入、培訓、驗收、維護與治理陪跑 |

不得在官網承諾免費架構諮詢、免費客製或開源版 SLA。第一波頁面不公開固定報價；以「預約診斷」承接需求，再依已核准的商業方案提案，且小 G 不得自行修改報價。

## 5. CTA 與轉換漏斗

### 5.1 固定連結

- GitHub：<https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow>
- Release：<https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/releases/tag/v0.1.0>
- 聯絡頁：`../../contact.html`

### 5.2 CTA 層級

1. Primary：`預約 AI 治理與導入診斷`
2. Secondary：`查看 GitHub 開源專案`
3. Tertiary：`查看 v0.1.0 Release 與測試證據`

不得只放 GitHub 按鈕。每個主要區塊都必須有一個回到 Phoenix 商業服務的合理下一步。

### 5.3 UTM 規格

聯絡 CTA 使用：

```text
../../contact.html?request_type=diagnostic_demo
&utm_source=site
&utm_medium=open_source_showcase
&utm_campaign=phoenix_auditable_ai_flow
&utm_content={hero|evidence|service_boundary|footer_cta}
```

GitHub 外連使用相同活動名稱，並以 `utm_medium=github_outbound`、不同 `utm_content` 區分來源。若 GitHub 不需接收 UTM，至少須由站內事件保存 CTA 位置。

### 5.4 contact.html 對齊

不得改壞現有 Google Forms 串接。小 G 應：

1. 新增或映射 `phoenix_auditable_ai_flow` 活動至既有 `diagnostic_demo` 類型；
2. 保留所有 UTM 欄位；
3. 以專用測試識別碼完成一次公開 Pages 端到端提交；
4. 在 Google Forms 後台確認資料與來源完整；
5. 測試完成後將測試資料標記為 QA，避免被當成業務名單。

## 6. 展示素材規格

至少交付：

- 一張三系統能力鏈圖；
- 一張六階段工作流圖；
- 4–6 張真實本機 Demo 截圖；
- 一支 60–90 秒無客戶資料的操作錄影或 MP4；
- GitHub、Release、測試狀態的文字證據；
- 桌面與 390px 手機版頁面截圖。

展示畫面必須使用公開 Repo、合成資料與 `.example` 網域，不得出現私有 Repo 路徑、真實客戶資料、內網 IP、API Key、個人信箱或開發環境使用者路徑。

不得把 Stars、下載量或客戶數寫成尚未發生的數字。59 項測試只可描述為「目前 v0.1.0 公開版的自動化測試」，不得推論為生產安全認證。

## 7. SEO 與分享預覽

詳情頁至少設定：

- title：`Phoenix 可稽核 AI 工作流｜企業 AI 治理開源參考架構`
- description：聚焦 Policy-as-code、人工覆核、引用證據與 Audit Trail；
- canonical URL；
- Open Graph title、description、image；
- 結構化資料：`SoftwareSourceCode` 與 Phoenix 顧問服務 `Service` 分開描述；
- 關鍵詞：企業 AI 治理、可稽核 AI 工作流、Human-in-the-loop、Policy-as-code、AI 導入診斷。

不得使用「保證合規」、「合規認證」或「零風險」作為 SEO 字詞。

## 8. Analytics 與商業 KPI

事件命名沿用既有 `experience_` 規格，且不得傳送姓名、Email、電話或公司名稱：

- `experience_solution_view`
- `experience_cta_click`
- `experience_demo_request_click`
- `experience_github_click`
- `experience_release_click`
- `experience_video_progress`（25／50／75／100）

事件參數最多保留：`solution_id`、`cta_type`、`source_section`、`release_version`、`target_type`。

發布後建立 30 天成效表，每週更新：

| 漏斗層級 | 指標 |
| --- | --- |
| Awareness | 詳情頁訪客、影片 50% 完播、GitHub 外連點擊 |
| Interest | 系統頁停留、Release 點擊、回訪率 |
| Intent | contact CTA 點擊、表單開始、表單成功提交 |
| Qualified | 符合目標企業／有決策問題／有時間表的線索 |
| Revenue | Demo、診斷案、Pilot 提案、簽約與預估管線金額 |

30 天最低商業驗證目標：3 筆合格詢問、2 場 Demo、1 份付費提案。若未達標，先檢討受眾、頁面訊息與 CTA，不得以虛構數字美化。

## 9. 分階段執行與停止條件

### W0 — 盤點與規格

交付：

- 現有首頁、`experience`、中央廚房、診斷工作台、contact 與 analytics 的影響清單；
- `experience/tools/phoenix-auditable-ai-workflow.json` 草稿；
- 頁面 wireframe、文案表、素材清單、UTM 矩陣。

停止條件：任何功能、測試、法律或客戶成效無法提出公開證據。

### W1 — 文案與視覺預覽

交付：首頁卡片預覽、詳情頁靜態預覽、三系統能力鏈、60–90 秒展示腳本。

核准：Owner 核准定位、CTA、限制聲明後才能實作。

### W2 — 分支實作

建立獨立分支，僅修改白名單檔案：

- `experience/solutions_data.js`
- `experience/tools/phoenix-auditable-ai-workflow.json`
- `experience/phoenix-auditable-ai-workflow/**`
- `contact.html`（僅必要的 request type／campaign 映射）
- 與該頁直接相關的共用樣式或驗證測試

不得順手格式化或改寫既有大檔案，不得碰使用者目前的其他未提交修改。

### W3 — 驗證

必須完成：

- `npm run validate:tools`；
- 所有內外連結檢查；
- GitHub Repo 與 v0.1.0 Release HTTP 200；
- Chrome 桌面及 390px 手機版檢查，無橫向溢位；
- 鍵盤操作、可見 focus、圖片 alt、對比與影片字幕／文字替代；
- CTA 與 GA4/GTM 事件不含 PII；
- contact Google Forms 端到端測試；
- 敏感字串與私有路徑掃描；
- 文案逐句對照公開證據。

任一假連結、未證實宣稱、表單失敗、手機版失真或私有資料洩漏均為 `HOLD`。

### W4 — Owner 預覽與發布

先提供預覽網址、變更摘要、截圖、測試報告與回滾 commit。Owner 明確核准後才可合併 `main` 與部署 GitHub Pages。

### W5 — 30 天商業追蹤

每週記錄流量、CTA、表單、Demo、提案與管線金額；只保存必要的彙總商業數據。第 30 天提出保留、改版或下架建議。

## 10. 驗收交付物

小 G 最終必須提交：

1. `WEBSITE_SHOWCASE_IMPLEMENTATION_PLAN.md`
2. `COPY_AND_CLAIMS_EVIDENCE_MATRIX.md`
3. `UTM_AND_ANALYTICS_MATRIX.md`
4. `experience/tools/phoenix-auditable-ai-workflow.json`
5. `experience/phoenix-auditable-ai-workflow/index.html` 與素材
6. 首頁及系統總覽第三張卡片
7. contact campaign 映射與端到端證據
8. `WEBSITE_SHOWCASE_VERIFICATION_REPORT.md`
9. 桌面／手機截圖、連結檢查、事件檢查與表單 QA 證據
10. `30_DAY_CONVERSION_SCORECARD.md`

## 11. 最終驗收標準

只有同時符合以下條件才能判定官網展示 `PASS`：

- 三套系統的定位一致且互相支援；
- 公開 Repo 與 v0.1.0 Release 可正常開啟；
- 開源免費內容與 Phoenix 付費服務邊界清楚；
- 至少一個商業 CTA 可成功送達既有 Google Forms 後台並保留 UTM；
- 所有外部宣稱可由公開證據支持；
- 無私有資料、Secrets、客戶資料或內部路徑；
- 手機、桌面、無障礙與分析事件驗證通過；
- Owner 已核准預覽與正式發布；
- 已指定 30 天 KPI 負責人與每週檢視節奏。

## 12. 小 G 回報格式

每一階段只回報：

- 本階段實際完成項目；
- 修改檔案與絕對路徑；
- 可重現的驗證命令與結果；
- 未完成、風險、需要 Owner 決策之處；
- 下一 Gate 建議；
- 明確狀態：`READY FOR REVIEW`、`HOLD` 或 `PASS`。

小 G 不得自行宣告 Owner 核准、不得代簽人類審查、不得自行部署、擴增商業名單或修改已核准報價。
