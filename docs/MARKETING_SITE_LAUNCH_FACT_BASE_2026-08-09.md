---
title: 官網上架素材包：事實底稿（Ledger-Assist × AI Allocation OS）
author: Researcher（AI 產業研究員與技術分析師）
created_at: 2026-08-09
status: fact-base（待 CEO 核准後上架）
target_site: 03king.com（GitHub Pages 靜態站，AI_Talent repo）
related: MARKETING_SITE_LAUNCH_COPY_2026-08-09.md、Website-Integration-Matrix（SYS-04/SYS-05）
---

# 官網上架素材包：事實底稿

> **文件性質**：事實基礎文件（Fact Base），供鳳凰 AI 官網（03king.com，GitHub Pages 靜態站）上架兩套系統的行銷素材引用。
> **產出日期**：2026-08-09 ｜ **狀態**：待 CEO 核准後上架
> **事實來源**：僅以下 repo 商業／產品文件（本機路徑），本文件不新增任何未記載數字。
> **去識別化聲明**：本文件不含 PII、客戶真名、token、機密 URL；文件中的內部化名（Owner、獨立審查者等）一律以職稱稱之。

## 0. 通用規則

### 0.1 證據等級定義（E0–E3）

| 等級 | 定義 |
|---|---|
| E0 | 僅假設／規劃，無任何驗證證據 |
| E1 | 設計層證據：規格、架構、威脅模型、流程文件（Accepted） |
| E2 | 內部驗證證據：自動化測試通過、E2E、獨立 code review／驗收 |
| E3 | 真實世界證據：真實客戶、真實資料、付費交易、第三方稽核／認證 |

### 0.2 兩套系統的紅線（CEO 裁定，不可違反）

- **Ledger-Assist（SYS-05）**：對外只能用「Sandbox Demo／合成展示」話術（PC-07）；不得宣稱已上線真實客戶或處理真實帳務。部署模式＝每家事務所獨立私有部署，**非 SaaS**。
- **AI_Allocation_OS（SYS-04）**：商業定位是賣 **Capital Decision Sprint 顧問服務**；AI_Allocation_OS 是內部顧問工作台（工具層），**不是賣軟體**。

### 0.3 事實時效

本底稿事實以各來源文件標示日期為準（Ledger-Assist：2026-07-15 商業文件＋2026-08-02 產品憲章；AI_Allocation_OS：2026-07-14 commercial 文件＋2026-07-22 VERSION.md＋2026-08-09 凍結決策）。上架前若文件更新，須重新對照，本底稿不自動生效。

---

# 一、Ledger-Assist（會計事務所 AI 系統，SYS-05）

## 1. 產品定位一句話（對外可說版本）

> **Ledger-Assist 是「LINE 原生、每家會計師事務所獨立私有部署」的發票收件與檢核系統：使用者以 LINE 上傳發票，並在 LINE 內檢核、修正、確認；正式辨識、保存、覆核與稽核由該事務所控制的私有環境負責，不是集中式會計 SaaS。**
> （來源：產品憲章 §1 一句話定義，逐字引用）

補充定位語（憲章 §3.2 官方隱私說法，對外須用此版本）：
> 「憑證透過事務所核准的 LINE 通道傳輸；鳳凰 AI 不以集中式 SaaS 保存各事務所帳務，正式辨識、保存、覆核與稽核留在事務所控制的私有環境。」

## 2. 目標客戶與場景

| 項目 | 內容 | 來源 |
|---|---|---|
| 目標客戶 | 台灣會計師事務所／記帳士事務所 | 01 §1 |
| 客戶內角色 | tenant_admin（成員、預算、保留政策）；operator（上傳、編輯候選、送審）；reviewer（覆核核准／退件）；auditor（唯讀稽核與匯出驗證）；Pilot 另含兩位標註者＋資深會計師裁決 | 01 §2、06 §1 |
| 進入場景 | 設計夥伴 Pilot：1 家事務所；**DPA／用途與保存政策完成後才匯入真實資料**；Pilot 期間強制 MFA、自動核准關閉 | 01 §6、06 §1 |
| 核心使用情境 | LINE 上傳發票 → 收件與辨識候選 → LINE 內檢核／修正／確認 → 覆核核准 → 匯出；全程稽核 | 憲章 §3、01 §3 |
| 憑證支援範圍 | 電子發票 QR、傳統紙本票、POS、結構化檔；Pilot 擴充 PDF／低畫質 | 01 §4 |

## 3. 痛點 → AI 解決路徑（5 條）

| # | 痛點（文件事實） | AI 解決路徑（文件事實） | 來源 |
|---|---|---|---|
| 1 | 發票收件與登錄依賴人工，耗時且易錯 | LINE 上傳＋非同步辨識鏈（QR → browser OCR evidence → server OCR → 政策允許時 Terra）產出「可覆核候選」，人工覆核後才核准匯出 | 01 §3、02 §4 |
| 2 | 原始憑證散落、稽核鏈薄弱，事後無法舉證 | 原件強制進入物件儲存（商用稽核模式），含 SHA-256、版本、歷程、核准人；audit 採 hash chain＋S3 Object Lock（WORM）封存 | 01 §3、06 §1、05 §4 |
| 3 | 偽造／竄改憑證與惡意檔案風險 | quarantine → MIME 魔數 sniff → malware scan → accepted 後才進 OCR；SHA-256 不符拒絕處理；信任優先序：QR／結構化 > browser OCR > server OCR > Terra，高信任不被低信任靜默覆寫 | 02 §5、05 §2 |
| 4 | 事務所帳務資料外洩與隱私顧慮 | 每所獨立私有部署（資料權威留在事務所控制環境）；OIDC＋MFA、RBAC 職責分離、RLS 租戶隔離（僅限事務所內客戶／角色／案件）、log 禁原圖與完整統編 | 憲章 PC-03/04/08、05 §6 |
| 5 | 帳務錯誤與責任歸屬難以追查 | 全程 append-only audit trail、核准者紀錄、WORM checkpoint、匯出版本；刪除採 legal hold＋雙人／工單流程 | 05 §4/§7、06 §4 |

## 4. 核心能力清單（對外可說）

1. **LINE 原生主流程**：LINE 上傳發票為核心主流程；LINE 內檢核／修正／確認為核心體驗（LINE Flex／LIFF 回傳必要欄位）。（憲章 PC-01/02、§3）
2. **多來源憑證辨識候選**：電子發票 QR、傳統紙本、POS、結構化檔；AI 永遠產出「可覆核候選」，Pilot 期間自動核准完全關閉。（01 §1/§4）
3. **人機協作覆核與核准**：reviewer 覆核核准／退件；Pilot 下所有結果必須人工確認後方可核准／匯出 final。（01 §5）
4. **完整稽核與防竄改**：上傳 → quarantine → 辨識 → 覆核 → 匯出全程 audit；hash chain＋WORM checkpoint；transactional outbox 與冪等防重放。（05 §4/§5）
5. **資安基線**：OIDC＋MFA（Pilot 強制）、RBAC 分離、RLS、malware／MIME 檢查、KMS 加密、短 TTL signed URL、tenant rate limit、前端零 API key。（05）
6. **每所獨立私有部署**：container／Compose 交付（安裝、migration、升級、備份還原、監控與 Runbook）；部署於事務所主機、事務所 VM、客戶私有雲或客戶控制的機房環境。（憲章 §4.1）
7. **成本與用量可觀測**：每文件 usage ledger（OCR、AI、儲存、人工時間）；儀表板顯示修改率、成本與預算熔斷狀態；超限自動 `policy_blocked`，QR＋OCR＋人工路徑不受影響。（07 §5/§3）

## 5. 能力邊界（對外可說／不可說）

**可說**
- 目前產品階段：MVP／Phase B（本機）已完成規劃；Pilot 尚未開始（1 家設計夥伴招募中）。
- 合成資料 Sandbox Demo 可完整展示流程（見 §6）。
- 設計層能力（辨識、稽核、資安控制、SLO 目標）以已 Accepted 文件為基礎。
- 部署模式：每所獨立私有部署、一次性導入費用＋年度維護的商業模式。（憲章 §4.2）

**不可說**
- 已上線真實客戶、處理真實帳務、真實發票辨識成效。（紅線 PC-07）
- 自動核准已開放。（Pilot 自動核准關閉；GA 才逐租戶、分類型達標開放）
- 已取得合規認證／「符合個資法／稅法」。（06 §5：無專業審查證據前禁止）
- 台灣境內 AI 推論保證。（儲存區域 ≠ 推論區域；Terra 無台灣 residency，ADR-0007）
- 集中式雲端代管帳務／中央 SaaS。（憲章 PC-03）
- 特定準確率數字（如「全類型 99.5%」）。（Pilot ≥300 張僅驗工作流程，不得單獨宣稱）
- 以 2026-07-15 版「AWS Taipei 多租戶正式平台」架構為現況。（憲章 §7：有爭議／非現行授權）

## 6. Demo 導流建議（訪客體驗路徑）

1. **入口**：官網「體驗 Sandbox Demo」頁（合成資料，符合 PC-07 允許之「合成資料 Demo／不含正式客戶帳務的錄影與銷售展示」）；另提供合成展示影片下載。
2. **展示腳本**（合成資料）：LINE 上傳發票 → 自動產出辨識候選 → LINE 內檢核／修正／確認 → 覆核核准 → 匯出並檢視稽核軌跡。
3. **CTA 與轉換**：預約 1:1 線上展示 → 索取資料 → 若事務所有意願：DPA／用途與保存政策 → 設計夥伴 Pilot（1 家）洽談。
4. **限制**：不展示真實帳務；不提供公開自助試算；Demo 環境與正式私有部署完全隔離（資料、secret、身份、儲存）。
5. **待確認**：公開 Demo 頁 URL 與嵌入方式（文件未提供，由官網建置者提供）。

## 7. 證據等級評估

| 面向 | 等級 | 依據 | 備註 |
|---|---|---|---|
| 產品範圍／架構／威脅模型／保存／SLO 設計 | **E1** | 01/02/05/06/07 均為 Accepted 文件 | 設計層證據充分 |
| Phase B 本機驗證 | E2（**待確認**） | 05 §9 列出驗證清單（跨租戶、重放、hash 不符、audit 篡改偵測、未核准不可匯出、Terra `policy_blocked`） | 所提供文件未附執行結果 |
| 出廠定義證明 | E2（**待確認**） | 憲章 §6 六項出廠證明（獨立部署安裝／備份／還原／升級、LINE 全鏈、異常不丟單等） | 未見證明文件 |
| Pilot 真實客戶 | **E0** | 06 §1：DPA 完成前不得匯入真實客戶資料 | Pilot 尚未開始 |
| 合規／法律狀態 | **E0** | 06：provisional，需法律確認；行銷用語禁區待確認 | 不得對外宣稱合規 |
| **綜合** | **E1（E2／E3 待確認）** | | 對外話術僅可立足設計與合成展示 |

## 8. 對外禁語清單（不可出現在官網）

1. ❌「已服務／已上線真實客戶」「正在處理真實帳務」。
2. ❌「符合個資法／稅法」「已取得合規認證」。
3. ❌「集中式 SaaS／雲端代管帳務」。
4. ❌「資料完全不經任何外部服務」（LINE 是必要且明示的外部通道，憲章 §3.2）。
5. ❌「AI 自動核准／AI 直接入帳」。
6. ❌「辨識與推論均在台灣境內處理」（僅儲存於台灣可說）。
7. ❌「全類型辨識準確率 99.5%」等未經驗證數字。
8. ❌「99.9% 可用性 SLA」等 GA 目標當作現況（GA 前僅設計目標）。
9. ❌「已通過滲透測試」「Multi-AZ 營運中」（GA 規劃項目）。
10. ❌以「multi-tenant 平台」暗示 SaaS 商業模式。
11. ❌使用真實客戶發票、統編、PII 作展示素材。
12. ❌任何未經 Owner 核准的部署地點宣稱（AWS／Cloudflare 平面敘述以憲章 §7 裁定為準）。

---

# 二、AI_Allocation_OS（企業 AI 顧問決策工作台，SYS-04）

## 1. 產品定位一句話（對外可說版本）

> **「Phoenix AI Capital Decision Sprint」是一項 AI 投資決策支援顧問服務：依版本化規則、可追溯證據與預先定義的風險 gate，協助企業在有限資訊下，對 AI／流程改善投資做出一致且可稽核的決策。**
> （來源：OFFER_v1.1「解決的問題」與產品名稱，逐字引用）

補充定位語（工具層，對內用）：
> AI_Allocation_OS（Phoenix AI Opportunity Engine）是承載此服務的**內部顧問決策工作台**，對外不出售軟體授權。（來源：OFFER／README／VERSION.md）

## 2. 目標客戶與場景

| 項目 | 內容 | 來源 |
|---|---|---|
| 地區 | 台灣 | ICP |
| Primary ICP | 零售、電商及一般 B2C 服務業；流程＝客服案件分類／分流；**每月案件量 ≥ 1,000 件**；企業規模 50–1,000 人 | ICP |
| Baseline 要求 | 至少一項可量測指標：平均處理時間／首次回應時間／轉人工率；量測窗口 30–60 天；至少過去 6 個月聚合統計＋欄位字典 | ICP |
| 主要 buyer | COO、客服主管、數位轉型主管 | ICP |
| Economic buyer | COO、總經理、CFO | ICP |
| Conditional ICP | 金融、醫療、電信等受高度監管產業：須有具名 compliance／risk sponsor 且可完成資料治理審查；首個付費 Sprint 優先排除 | ICP |
| 進入場景 | 官網漏斗承接（表單）→ 診斷 → 合格買方確認 → Capital Decision Sprint 提案 | VERSION.md（官網漏斗承接已授權） |
| 服務時程 | kickoff、資料完整交付、決策者時間確認後 **10 個工作日內**完成；客戶資料延遲則順延，連續延遲 >5 個工作日可暫停 | OFFER |

## 3. 痛點 → AI 解決路徑（5 條）

| # | 痛點（文件事實） | 解決路徑（文件事實） | 來源 |
|---|---|---|---|
| 1 | AI 投資決策缺乏一致方法（Excel、內部委員會、外部顧問、SI、或無固定方法） | 以版本化規則＋預先定義風險 gate 的一致化評估流程取代隨機方法 | OFFER 解決的問題；Interview Guide Part A Q4 |
| 2 | 決策無可追溯證據，事後無法稽核／交代 | 產出 Decision Snapshot（T0/T1/T2）、Decision Delta、Assumption／Evidence Register、Decision Record（每案三軸決策與理由） | OFFER 交付物 |
| 3 | 決策僵持、拖沓（提議到決策耗時久） | 10 個工作日的 Sprint 會議制＋「具名 decision owner 確認收到」的完成定義，逼出決策節奏 | OFFER 時程與完成定義 |
| 4 | 評估被供應商或內部偏見綁架 | 三軸決策與 Funding Gate 機制；利益衝突聲明：Sprint 費用不因決策結果（Fund／Repair／Defer／Reject）改變，評分不以後續承接為條件 | OFFER 利益衝突聲明 |
| 5 | 缺乏可量測 baseline，無法判斷 AI 投入價值 | 以 30–60 天量測窗口與至少一項 KPI baseline（處理時間／首回應時間／轉人工率）作為評估前提，量不出就不做 | ICP Baseline 要求 |

## 4. 核心能力清單（對外可說）

1. **結構化決策評估**：最多篩選 5 個客服分類／分流候選 use case，深度 Underwriting 其中 3 個，產出 3 個三軸決策。（OFFER）
2. **風險 Gate 機制**：為最高優先或最具爭議的 1 個流程建立 Funding Gate／Foundation Repair Gate／Reassessment Gate（無適合撥款案子不強制產生）。（OFFER）
3. **可稽核決策紀錄**：Decision Snapshot（T0/T1/T2）、Decision Record、Assumption／Evidence Register、Committee Pack（PDF／HTML 版本化）、會議紀錄與 action log。（OFFER）
4. **可重現的計算原則**：計算負責「可重現的數字」，LLM 僅負責「抽取、解釋與草擬」，**LLM 不直接決定分數**。（README 核心原則）
5. **內部工作台工程基線**：Decision Kernel 2.1（版本化契約、雙族路由、黃金案例 oracle）＋ Concierge Workbench（Increment A/B 已完成並接受）。（VERSION.md／README）
6. **資料最小化**：僅收聚合流程量、工時與成本、KPI baseline、欄位字典、處理時間／轉人工率等 metadata；必要時 50–100 筆去識別樣本（需核准）；Benchmark opt-in 獨立選擇。（OFFER 資料條款）

## 5. 能力邊界（對外可說／不可說）

**可說**
- 賣的是 **Capital Decision Sprint 顧問服務**（客服分類／分流流程族群）。
- 定價（現行 v1.1 假設）：總價 NT$280,000（含稅），訂金 NT$80,000，尾款 NT$200,000（會議結束後 7 天內）。（OFFER；**為 v1 定價假設，將依市場反饋調整**）
- 服務不包含：實際 AI 系統開發、PoC 或導入執行（可另行報價）。（OFFER 不包含事項）
- 內部工程已通過自動化驗證（Kernel 2.1 Package 5：獨立審查＋CEO 接受）。（VERSION.md）
- 客戶須提供：3–5 個候選流程基本資料、決策人員名單與配合時間、必要歷史資料使用權限（去識別化後）。（OFFER）

**不可說**
- 販售 AI_Allocation_OS 軟體／平台授權，或提供線上自助軟體。
- 已有真實付費客戶／完成履約（VERSION.md：`EXECUTION_EVIDENCE_INCOMPLETE`，Gate A 未關）。
- 保證 ROI、投資成功或特定決策結果（OFFER 明列不包含）。
- 提供法律、財務、稅務、合規或證券投資專業意見（OFFER 免責聲明）。
- 已核准 SaaS／多租戶／雲端／LLM 決策／Continuous Optimizer／Portfolio Simulator（README：**尚未核准**）。
- 客服校準資料為「benchmark」或具外部效度（VERSION.md：`Synthetic, not benchmark`）。
- Field Edition 為企業 production-ready（README：受控版本，不代表 production-ready）。

## 6. Demo 導流建議（訪客體驗路徑）

1. **入口**：官網承接表單（CEO 已授權「官網漏斗承接與 48h 跟進」）＋診斷連結入口。（VERSION.md）
2. **內容**：免費決策診斷；去識別化的決策紀錄／Committee Pack 樣本展示（引用訪談或案例內容須匿名化並取得授權）。
3. **轉換路徑**：表單 → 資格確認（對照 ICP：台灣零售／電商／B2C 服務業、月案件 ≥1,000、可建 baseline）→ Capital Decision Sprint 提案（NT$280,000）。
4. **限制**：不提供線上自助軟體體驗；候選名單、錄音與 private 證據不公開（VERSION.md：private records 不屬於版本化公開資產）。
5. **待確認**：公開表單 URL、診斷連結 URL 與漏斗工具細節（屬內部營運文件，官網上架時由 CEO 指定公開版）。

## 7. 證據等級評估

| 面向 | 等級 | 依據 | 備註 |
|---|---|---|---|
| 工程驗證（Decision Kernel 2.1／Package 5） | **E2** | VERSION.md：PACKAGE_5_APPROVED、獨立審查、CEO 接受（2026-07-16）；自動化測試套件＋20 組 v2.1／12 組 v2.0 黃金案例 oracle＋B4 E2E＋pytest | 內部驗證充分；黃金案例為內部 oracle，非外部基準 |
| 客服校準資料 | **E1（非基準）** | customer-service calibration：`Synthetic, not benchmark` | 不可對外宣稱效能 |
| Field Edition | **E2 邊緣** | `CONTROLLED_RC_DELIVERABLE`（field-rc-2026.07.18） | 受控 RC 交付物，非 production-ready |
| 商業／市場驗證 | **E0** | `EXECUTION_EVIDENCE_INCOMPLETE`；Gate A open；無真實付費／履約證據 | 對外不得宣稱市場成果 |
| **綜合** | **工程 E2／商業 E0** | | 官網話術：講方法與流程，不講成績 |

## 8. 對外禁語清單（不可出現在官網）

1. ❌「購買 AI_Allocation_OS 軟體／平台授權」「SaaS 訂閱」。
2. ❌「已服務多家付費客戶」「已完成 N 次 Sprint 履約」（無證據）。
3. ❌「保證 ROI／投資成功／特定決策結果」。
4. ❌「提供法律、財務、稅務、合規或證券投資意見」。
5. ❌「AI 自動做決策／取代決策者」（最終決策權與責任在客戶）。
6. ❌「已核准 SaaS、多租戶、雲端、LLM 決策、Continuous Optimizer、Portfolio Simulator」。
7. ❌「客服校準資料為 benchmark／具外部效度」。
8. ❌「Field Edition 為 production-ready／企業正式版」。
9. ❌「官網可自助體驗決策引擎」。
10. ❌引用未匿名化授權的客戶／訪談內容、候選名單、錄音。
11. ❌「價格保證不變」（現行為 v1.1 定價假設，會調整）。
12. ❌把內部驗收（Gate A 門檻、合格買方人數等）當對外成果宣稱。

---

## 附錄：CEO 上架前裁量清單（待確認項）

1. Ledger-Assist Sandbox Demo 公開 URL／嵌入方式。
2. AOS 官網承接表單與診斷連結的公開版本。
3. 兩套系統上架後的首頁歸屬（同一網站兩個產品區）與品牌關係（Phoenix AI）。
4. AOS「三軸決策」三軸之具體維度（文件未明示，官網若需描述請先補文件）。
5. Ledger-Assist Phase B 本機驗證執行結果文件（若有，補上後可將 E2 待確認升為 E2）。
6. 官網文案若超出本底稿範圍（新增宣稱），一律先回補 repo 文件再上架。
