# Cases De-identification & Claim Risk Audit Report

## Executive Summary
本報告為 R2/R3 合規專案的第一階段盤點，旨在針對系統中現有的行銷案例進行風險分級與審查，確保行銷文案無潛在的真實客戶洩密（De-identification）或過度承諾（Claim）風險。

- **總案例數 (Total Cases)**: 24 筆
  - `cases.json` Active 案例: 8 筆
  - `cases/html/` Standalone (未被引用) 案例: 16 筆
- **整體風險統計 (Overall Risk)**:
  - **High (高風險)**: 15 筆
  - **Medium (中風險)**: 9 筆
  - **Low (低風險)**: 0 筆

## High-risk Remediation Queue
下列為 Overall Risk 評等為 High 的高風險案例，建議依循以下優先順序進行文案微調處理：

### 優先層級 1：涉及真實品牌與高度可識別特徵 (De-id & Brand Risk)
這部分案例含有強烈的品牌或地名標籤，極易被外界或同業識別，建議**立即進行去識別化**。
- **PHX-CASE-2026-027 (manufacturing_02_screw_packing.html)**: 興達扣件包裝工業｜AI 視覺包裝複核與中高齡安心變革案 (`both`) - De-identification: 「興達扣件包裝工業」 (真實品牌名)
- **finance_01_dingtai_ai.html**: 某證券公司｜AI 研究助理、合規二審與地端 RAG 部署案 (`cases/html`) - De-identification: 網址暗示 dingtai (鼎泰)
- **manufacturing_08_henda_ai.html**: 恆達精密扣件｜AI 語音報修、瑕疵分流與預測維護合規落地案 (`cases/html`) - De-identification: 「恆達精密扣件」 (真實品牌名)
- **manufacturing_10_okayama_fastener_ai.html**: 某精密扣件廠｜AI 資料治理、人機雙簽與調機知識傳承合規落地案 (`cases/html`) - De-identification: 網址暗示 okayama (岡山地名 + 扣件，極易識別)
- **retail_02_mingchadao_tea_ai.html**: 明茶道國際餐飲加盟集團｜連鎖茶飲 AI-Native 人力與原物料智能中台規劃案 (`cases/html`) - De-identification: 「明茶道國際餐飲加盟集團」 (真實品牌名)
- **retail_03_yuepin_ai.html**: 悅品餐飲暨連鎖零售集團｜AI-Native 門市營運與行銷合規中台規劃案 (`cases/html`) - De-identification: 「悅品餐飲暨連鎖零售集團」 (真實品牌名)

### 優先層級 2：涉及硬數字宣稱與過度承諾 (Claim Risk)
這部分案例使用了高度具體的倍數、金錢或成功率，若無嚴格驗證可能構成過度承諾，建議**轉換為質化或方向性描述**。
- **PHX-CASE-2026-001 (manufacturing_03_bicycle_rag.html)**: A 公司｜售後服務 PDF 檢索與 RAG 安全防幻覺工作流設計案 (`both`)
- **PHX-CASE-2026-002 (accounting_01_ledger.html)**: 會計事務所｜發票自動辨識與傳票登帳系統 AI 落地決策評估案 (`both`)
- **PHX-CASE-2026-003 (law_firm_01_contract.html)**: 律師事務所｜標準合約智慧審查與判例 RAG 檢索系統 AI 落地評估案 (`both`)
- **PHX-CASE-2026-004 (manufacturing_01_steel_defect.html)**: 中型鋼鐵製品廠｜AI 視覺檢測與一線變革管理案 (`both`)
- **PHX-CASE-2026-005 (medical_02_dental_clinic.html)**: 連鎖牙醫診所｜智能預約掛號與未到診預測系統 AI 落地評估案 (`both`)
- **PHX-CASE-2026-010 (medical_01_health_chat.html)**: 連鎖健康機構｜健檢 Line 諮詢 AI 隱私與雙簽防線 (`both`)
- **PHX-CASE-2026-012 (ecommerce_01_guardrails.html)**: 跨國電商集團｜多代理人客服越獄漏洞與折扣熔斷防禦 (`both`)
- **manufacturing_06_ai_visual_inspection.html**: 某精密沖壓零件廠｜AI 視覺檢測與 Mura 判定標準化案 (`cases/html`)
- **manufacturing_14_okayama_barcode.html**: 某螺絲包裝廠｜AI 條碼防錯、OCR 比對與合規雙簽落地案 (`cases/html`)

## Verification Notes
> **【合規與邊界稽核確認】**
> - [x] 確認本階段 **未修改** `cases.json` 任何資料。
> - [x] 確認本階段 **未修改** `cases/html/*.html` 任何原始檔。
> - [x] 確認本次專案僅新增盤點報告 `docs/CASES_DEIDENTIFICATION_AUDIT.md`，所有原始檔案維持原樣。

---

## 完整稽核結果列表 (Detailed Audit Table)

| Case ID / File | Source | Referenced by JSON | De-id Risk | Claim Risk | Overall Risk | Evidence & Suggested Rewrite |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| PHX-CASE-2026-001 (manufacturing_03_bicycle_rag.html) | `both` | Yes | Medium | High | **High** | **Evidence**:<br>De-identification: 「跨國自行車零件製造商 A 公司」<br>Claim: 「30 分鐘縮短至 1 分鐘」、「98% 以上」、「100% 規避」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 將「跨國自行車零件製造商 A 公司」改為「跨國自行車零組件大廠」<br>Claim: 將具體數字改為方向性描述，如「大幅縮減查閱時間」、「極大化檢索精準度」、「有效降低幻覺風險」 |
| PHX-CASE-2026-002 (accounting_01_ledger.html) | `both` | Yes | Low | High | **High** | **Evidence**:<br>Claim: 「縮短 80% 以上」、「正確率達 99.8%」、「釋放 40%」<br><br>**Suggested Rewrite Direction**:<br>Claim: 將「縮短 80% 以上」改為「顯著降低登帳工時」，「正確率達 99.8%」改為「維持極高登帳正確率」，「釋放 40%」改為「釋放部分重複性行政人力」 |
| PHX-CASE-2026-003 (law_firm_01_contract.html) | `both` | Yes | Low | High | **High** | **Evidence**:<br>Claim: 「初審效率提升 5 倍」、「數天縮短至數分鐘」、「100% 確保」<br><br>**Suggested Rewrite Direction**:<br>Claim: 將「提升 5 倍」改為「大幅提升初審效率」，「數天縮短至數分鐘」改為「檢索時間顯著下降」，「100% 確保」改為「確保高階律師覆核流程」 |
| PHX-CASE-2026-004 (manufacturing_01_steel_defect.html) | `both` | Yes | Medium | High | **High** | **Evidence**:<br>De-identification: 「南部中型鋼鐵製品廠」<br>Claim: 「8% 降至 0.5%」、「提升 150%」、「每年挽回損失達 NT$ 180 萬」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 改為「金屬製造業客戶」<br>Claim: 將數字改為「大幅降低漏檢率」、「顯著提升標記效率」、「有效減少退貨賠償與重工損失」 |
| PHX-CASE-2026-005 (medical_02_dental_clinic.html) | `both` | Yes | Low | High | **High** | **Evidence**:<br>Claim: 「降低 30% 以上」、「降低 80%」、「100% 規避」<br><br>**Suggested Rewrite Direction**:<br>Claim: 將數字改為「預期有效降低空置率」、「大幅減少重複確認工時」、「符合法規要求，規避風險」 |
| PHX-CASE-2026-010 (medical_01_health_chat.html) | `both` | Yes | Low | High | **High** | **Evidence**:<br>Claim: 「20 分鐘縮短至 3 分鐘」、「效率暴增 6 倍」、「50% 躍升至 94%」、「增加 35%」、「100% 規避」<br><br>**Suggested Rewrite Direction**:<br>Claim: 將具體倍數改為「作業時間大幅縮短」、「顯著提升滿意度與回診率」、「有效防範個資外洩」 |
| PHX-CASE-2026-012 (ecommerce_01_guardrails.html) | `both` | Yes | Low | High | **High** | **Evidence**:<br>Claim: 「降至 0.1% 以下」、「即時回覆率達 99%」、「年省夜間人力 NT$ 120 萬」<br><br>**Suggested Rewrite Direction**:<br>Claim: 建議將具體金額改為「有效節省夜間客服人力成本」，並將 99% 改為「維持極高客服回覆率」 |
| PHX-CASE-2026-027 (manufacturing_02_screw_packing.html) | `both` | Yes | High | High | **High** | **Evidence**:<br>De-identification: 「興達扣件包裝工業」 (真實品牌名)<br>Claim: 「3% 驟降至 0.02%」、「提升 120%」、「省下達 NT$ 110 萬」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 將「興達扣件包裝工業」改為「精密扣件包裝廠」<br>Claim: 將金錢改為「降低包裝重工與客訴索賠成本」，「提升120%」改為「顯著提升包裝速度」 |
| finance_01_dingtai_ai.html | `cases/html` | No | Medium | High | **High** | **Evidence**:<br>De-identification: 網址暗示 dingtai (鼎泰)<br>Claim: 「3 秒研究助理產出」、「15% 研發費用稅抵」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 確保網址與標題中無可識別證券商之拼音<br>Claim: 將 3 秒改為「極速產出合規話術」，稅抵部分可保留但避免承諾過度 |
| manufacturing_04_electroplate_ai.html | `cases/html` | No | Low | Medium | **Medium** | **Evidence**:<br>Claim: 「1.9 億年營收規模」<br><br>**Suggested Rewrite Direction**:<br>Claim: 若 1.9 億為真實客戶規模，建議改為「億元級年營收規模」以避免被推測 |
| manufacturing_05_sbir_ready_ai.html | `cases/html` | No | Low | Medium | **Medium** | **Evidence**:<br>Claim: 「8.5 億年營業額規模」<br><br>**Suggested Rewrite Direction**:<br>Claim: 改為「中大型扣件製造業」或「數億元級營收」 |
| manufacturing_06_ai_visual_inspection.html | `cases/html` | No | Low | High | **High** | **Evidence**:<br>Claim: 「漏檢率降低 85%」、「近 0 客訴退貨率」<br><br>**Suggested Rewrite Direction**:<br>Claim: 改為「有效降低漏檢率」、「大幅減少客訴退貨率」 |
| manufacturing_07_dingsheng_voice_ai.html | `cases/html` | No | Medium | Low | **Medium** | **Evidence**:<br>De-identification: 網址暗示 dingsheng (鼎盛)<br><br>**Suggested Rewrite Direction**:<br>De-identification: 建議修改檔案名稱，移除特定拼音暗示 |
| manufacturing_08_henda_ai.html | `cases/html` | No | High | High | **High** | **Evidence**:<br>De-identification: 「恆達精密扣件」 (真實品牌名)<br>Claim: 「85% 假警報濾除率」、「預防 75% 停機」、「4 小時 CBAM」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 將「恆達精密扣件」改為「知名車規扣件廠」<br>Claim: 將具體百分比與小時改為方向性描述（大幅濾除假警報、縮短申報工時） |
| manufacturing_09_luzhu_coldheading_ai.html | `cases/html` | No | Medium | Low | **Medium** | **Evidence**:<br>De-identification: 網址暗示 luzhu (路竹地名)<br><br>**Suggested Rewrite Direction**:<br>De-identification: 移除網址地名暗示，或確保內容無特定產區與產業組合 |
| manufacturing_10_okayama_fastener_ai.html | `cases/html` | No | Medium | High | **High** | **Evidence**:<br>De-identification: 網址暗示 okayama (岡山地名 + 扣件，極易識別)<br>Claim: 「每年新台幣 50 萬元維護成本」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 避免「岡山+扣件」的組合，淡化地名<br>Claim: 將「新台幣 50 萬元」改為「有效降低系統維護成本」 |
| manufacturing_11_okayama_forge_ai.html | `cases/html` | No | Medium | Medium | **Medium** | **Evidence**:<br>De-identification: okayama (岡山)<br>Claim: 「3.2% 模具報損率」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 避免「岡山」標籤<br>Claim: 建議將 3.2% 改為方向性數值 |
| manufacturing_12_okayama_sbir_ai.html | `cases/html` | No | Medium | Medium | **Medium** | **Evidence**:<br>De-identification: okayama (岡山)<br>Claim: 「近 100 萬 POC」、「千萬合約價值」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 避免「岡山」標籤<br>Claim: 可保留千萬合約，但注意過度承諾的風險 |
| manufacturing_13_okayama_heat_treatment.html | `cases/html` | No | Medium | Low | **Medium** | **Evidence**:<br>De-identification: okayama (岡山)<br><br>**Suggested Rewrite Direction**:<br>De-identification: 避免「岡山」標籤 |
| manufacturing_14_okayama_barcode.html | `cases/html` | No | Medium | High | **High** | **Evidence**:<br>De-identification: okayama (岡山)<br>Claim: 「3.2% 退貨率」、「110 萬每年損失」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 避免「岡山」標籤<br>Claim: 將 110 萬改為「顯著降低退貨損失成本」 |
| manufacturing_15_okayama_cbam.html | `cases/html` | No | Medium | Medium | **Medium** | **Evidence**:<br>De-identification: okayama (岡山)<br>Claim: 「10 天申報工時」、「7% 罰款上限」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 避免「岡山」標籤<br>Claim: 法定 7% 可保留，10 天縮短建議改為「大幅縮短申報時程」 |
| manufacturing_16_okayama_filter.html | `cases/html` | No | Medium | Medium | **Medium** | **Evidence**:<br>De-identification: okayama (岡山)<br>Claim: 「15% 誤報率」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 避免「岡山」標籤<br>Claim: 改為「大幅降低檢測誤判率」 |
| retail_02_mingchadao_tea_ai.html | `cases/html` | No | High | Medium | **High** | **Evidence**:<br>De-identification: 「明茶道國際餐飲加盟集團」 (真實品牌名)<br>Claim: 「450+ 加盟店」 (易辨識)<br><br>**Suggested Rewrite Direction**:<br>De-identification: 將「明茶道」改為「知名連鎖茶飲集團」<br>Claim: 將 450+ 加盟店改為「數百家分店規模」 |
| retail_03_yuepin_ai.html | `cases/html` | No | High | High | **High** | **Evidence**:<br>De-identification: 「悅品餐飲暨連鎖零售集團」 (真實品牌名)<br>Claim: 「提升 20%」、「縮短 3 天」、「5-10% 人力下降」<br><br>**Suggested Rewrite Direction**:<br>De-identification: 改為「大型餐飲連鎖集團」<br>Claim: 將數字改為「顯著提升收銀效率」、「有效縮短培訓週期」 |