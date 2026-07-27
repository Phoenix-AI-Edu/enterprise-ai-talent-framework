# Enterprise RAG Foundation × 官網整合計畫

- 狀態：`phase1_implemented`（靜態骨架已落地；上站／PR 依官網流程）
- 日期：2026-07-27
- 官網 repo：`AI_Talent`（`enterprise-ai-talent-framework`）
- 產品 repo：`RAG_Bicycle`（`enterprise-rag-foundation` Private）
- 產品版本：Foundation **1.0.0** / tag `v1.0.0`
- enterprise_binding：`false`

## 1. 目標

在鳳凰 AI 官網建立 **可驗證的 RAG 產品／服務槽位**，讓訪客從診斷漏斗、旗艦系統、服務頁與交付檢查表理解「我們能交付什麼、不承諾什麼」，並導向評估／示範表單。

**不把** Foundation 執行時、客戶資料或後端塞進 GitHub Pages。

## 2. 契約來源（衝突時以此為準）

| 優先 | 文件 | 位置 |
|---|---|---|
| 1 | 能力／限制矩陣 | `RAG_Bicycle/docs/02_product/V1_1_0_CAPABILITY_LIMITATION_MATRIX.md` |
| 2 | 對外一句話／能力清單 | `RAG_Bicycle/docs/04_delivery/marketing/EXTERNAL_MESSAGING_V1.md` |
| 3 | 官網 11 section 文案 | `RAG_Bicycle/docs/04_delivery/marketing/WEBSITE_COPY_V1_1_0_ALIGNED.md` |
| 4 | 新企業 1 頁檢查表 | `RAG_Bicycle/docs/04_delivery/onboarding/ENTERPRISE_DELIVERY_CHECKLIST_1PAGE.md` |
| 5 | Experience 邊界 | `AI_Talent/docs/EXPERIENCE_BOUNDARY.md` |

## 3. 架構邊界

```text
AI_Talent（靜態）                RAG / Demo（獨立）
─────────────────              ──────────────────
services/*.html                enterprise-rag-foundation
experience/* 詳情頁            Private repo / 本機 Demo
solutions_data.js 卡片         不可嵌入 Pages 後端
contact.html 收 lead           不可上傳客戶 PDF 到官網
```

## 4. Phase 1 檔案清單（本輪）

| 檔案 | 動作 |
|---|---|
| `docs/RAG_FOUNDATION_SITE_INTEGRATION_PLAN.md` | 本規劃 |
| `services/enterprise-rag-foundation.html` | 服務落地頁（11 section） |
| `services/enterprise-delivery-checklist.html` | 新企業 1 頁檢查表（站內版） |
| `experience/enterprise-rag-foundation/index.html` | 體驗區詳情頁 |
| `experience/solutions_data.js` | 第 4 旗艦註冊 |
| `index.html` | 旗艦顯示 4 張；導覽可達服務頁 |
| `contact.html` | `rag_foundation_demo` / `rag_foundation_assessment` |
| `CHANGELOG.md` | 記錄上架 |

## 5. CTA 與 request_type

| 意圖 | request_type | 用途 |
|---|---|---|
| 10 分鐘示範 | `rag_foundation_demo` | 技術信任 |
| 30 分鐘評估 | `rag_foundation_assessment` | 顧問漏斗 |
| 檢查表 | 站內頁，無需 Form | 自助理解 |

UTM 建議：`utm_campaign=rag_foundation_v1`；`utm_content` 標 section。

## 6. 禁用宣稱（上站檢查）

- 零幻覺、保證 ROI、客戶已上線、資料一定不出域  
- 企業 SSO／DLP 已完成、丟檔即上線、60/100 放首頁主文案  
- 具名客戶 Logo／真實文件  

必須出現：synthetic／reference／非 production／不自動對外發送。

## 7. 驗收清單

- [x] 首頁旗艦區可見 RAG 卡（featured 最多 4；系統總覽全列）  
- [x] 服務頁文案對齊 CAP；有誠實邊界  
- [x] 檢查表頁可從服務頁到達  
- [x] contact 可預填 demo／assessment  
- [x] 無 Foundation 後端進主站  
- [ ] 瀏覽器人工 smoke（desktop／mobile）  
- [ ] 合併 main 並 GitHub Pages 部署驗證  
- [ ] 王傳訊確認 CTA 文案與是否調整定價區入口  

## 8. 後續 Phase（非本輪必做）

- Phase 2：診斷 Q2 結果導流、M05 落地頁橫幅  
- Phase 3：錄影 Demo 或預約本機 synthetic 示範  
- Phase 4：定價包裝（須王傳訊核准）  

## 9. 小 H 協作

本輪由整合者建立 Phase 1 骨架後，小 H 可依本計畫與 H-05 文案包微調視覺／SEO／上站；**不得**另寫超出矩陣的能力句。
