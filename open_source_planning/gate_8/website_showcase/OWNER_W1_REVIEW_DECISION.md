# Gate 8 W1 Owner Review Decision

- Review date: 2026-07-13
- Reviewer: Phoenix AI 專案決策者授權審查
- Executor: 小 G
- Decision: `CHANGES REQUIRED BEFORE W2`
- Scope: W0/W1 planning artifacts only

## Decision summary

商業漏斗、三系統能力鏈、Primary CTA 與 30 天轉換目標方向正確，可保留。W1 尚有公開事實、Schema 與文案精度缺口；這些缺口若直接進入 W2，會造成工具註冊驗證失敗及官網錯誤宣稱。因此 W2 暫不啟動，先完成本文件的一次性校正。

## Required corrections

### C-01 — Close the outdated single-administrator risk

Owner 已確認第二位 Organization administrator 建立完成。移除 W1 文件中「目前僅有一名管理員」及 30 天補件敘述，改為：

> 第二位 Organization administrator 已於 2026-07-13 建立；臨時單一管理員風險結案，後續納入定期權限檢查。

此事不代表第二位管理員已自動接受 Lead Maintainer、Release Manager 或 Security Maintainer 等公開專案角色。

### C-02 — Make the tool manifest pass the existing validator

`phoenix-auditable-ai-workflow.json` 的 `status` 目前為 `開源參考架構 v0.1.0`，不在既有 Schema enum，實測：

```text
status is not an approved public status
```

改為既有合法值 `公開沙盒示範`。版本資訊放入 `positioning`、頁面文案或未來擴充的版本欄位，不得繞過 validator。

完成後必須執行：

```powershell
python scripts\validate_tool_manifest.py open_source_planning\gate_8\website_showcase\phoenix-auditable-ai-workflow.json
```

預期結果：`Validated 1 tool manifest(s).`

### C-03 — Correct all GitHub evidence URLs

證據矩陣中的 `src/phoenix_flow/*` 路徑不存在。必須改用公開 Repo 的實際路徑：

- Policies：`src/phoenix_auditable_ai_flow/policies/`
- Workflow：`src/phoenix_auditable_ai_flow/workflow/orchestrator.py`
- Review：`src/phoenix_auditable_ai_flow/review/`
- Audit：`src/phoenix_auditable_ai_flow/audit/sqlite_repository.py`
- Mock model：`src/phoenix_auditable_ai_flow/providers/mock_model.py`
- Knowledge：`src/phoenix_auditable_ai_flow/providers/markdown_knowledge.py`

CI 證據不得只連到 Actions 首頁；應連到對應 commit `b9a04db2406c4d7a86ef2c2e7d6e55d625962c98` 的成功 run，並附註「v0.1.0 公開版目前 59 項自動化測試」，不得描述為生產安全認證。

### C-04 — Remove every tamper-proof claim

SQLite audit log 未做密碼學簽章、append-only storage 或 WORM，不能稱為：

- 抗篡改；
- 防篡改；
- 不可竄改；
- tamper-proof / immutable。

統一改為：

> 本機 SQLite 稽核事件紀錄，可依 request_id 查詢流程軌跡；不具密碼學不可竄改保證。

修正 `WIREFRAME_AND_CONTENT_SPEC.md`、`ASSET_PRODUCTION_LIST.md`、JSON 與所有規劃文件。

### C-05 — Accurately describe the model and knowledge providers

公開 v0.1.0 使用 `MockModelProvider` 與 Markdown 合成規章，不是正式 LLM model call，也不是「引用資料庫」。六階段應寫為：

`Input Policy → Markdown Knowledge → Mock Model → Output Policy → Human Review → SQLite Audit`

「模型推論」改為「Mock 回答生成」；「知識庫／引用資料庫」改為「Markdown 合成規章檢索與引用驗證」。

### C-06 — Correct HITL and insufficient-evidence behavior

不得宣稱所有「證據不足」都會送人工覆核。現有實作可直接回傳 `INSUFFICIENT_EVIDENCE`；政策衝突或特定輸出政策結果才會進入 `REVIEW_REQUIRED`。頁面文案、影片腳本及 JSON 必須反映此差異。

### C-07 — Restore the approved CTA hierarchy

詳情頁與商業漏斗：

1. Primary：`預約 AI 治理與導入診斷`
2. Secondary：`查看 GitHub 開源專案`
3. Tertiary：`查看 v0.1.0 Release 與測試證據`

工具 manifest 的 `primary_cta` 目前是「查看開源展示頁」，`secondary_cta` 才是預約診斷，與核准策略相反。工具卡若因導覽需要使用「查看詳情」，應由 `solutions_data.js` 的 `cta_text` 表達；manifest 的商業 CTA 仍須維持上述層級。

### C-08 — Correct catalog and contact paths

新詳情頁位於 `experience/phoenix-auditable-ai-workflow/`，從 `experience/index.html` 前往該頁應使用：

`./phoenix-auditable-ai-workflow/index.html`

不得使用會形成 `/experience/experience/` 的路徑。

`contact.html` 已能以 `request_type=diagnostic_demo` 選取診斷 Demo；只需新增 `utm_campaign=phoenix_auditable_ai_flow` 的 campaign mapping 或專屬頁面文案時才修改。不得為了形式重複改 Google Forms 欄位。

### C-09 — Correct ownership language

工具 manifest 的 `owner` 不應把網站執行者誤當成公開產品權利人。改為 `Phoenix AI` 或經 Owner 核准的公開 GitHub handle。文件的 `Executor` 繼續使用「小 G」。

### C-10 — Complete the missing page sections

Wireframe 必須補齊原任務書要求但目前未完整列出的：

- 三類買方入口：管理者、IT／CTO、顧問／培訓夥伴；
- 頁底商業 CTA；
- GitHub 與 v0.1.0 Release 的獨立 CTA；
- 三系統能力鏈區塊；
- SEO、Open Graph、canonical 與 `SoftwareSourceCode`／`Service` 分離的 structured data；
- 影片字幕或等價文字稿；
- 30 天 KPI 負責人與每週檢視頻率。

### C-11 — Fix JSON and copy defects

修正首頁卡片草稿中的 JSON 語法錯誤：

```text
"contact_label: "experience_solution_view"
```

以及 `ASSET_PRODUCTION_LIST.md` 的「Knowledge 檢檢」錯字。完成後將所有 JSON 以 parser 實際解析，不得只做目視檢查。

### C-12 — Correct the de-identification statement

本專案刻意保留 Phoenix 品牌、商標政策與商業 CTA，不可宣稱「完全去識別化」。正確表述為：

> 已移除私有 Repo、客戶資料、內部路徑與敏感資訊；Phoenix 品牌、商標政策與企業服務連結刻意保留。

## Resubmission evidence

小 G 補件時必須提供：

1. 12 項逐項完成對照；
2. manifest validator 成功輸出；
3. 所有 GitHub evidence URL 的 HTTP 200 或可讀證據；
4. 全目錄搜尋不存在「抗篡改／防篡改／不可竄改」的結果；
5. 更新後的 W1 Review Report；
6. 明確狀態 `READY FOR W1 RE-REVIEW`。

補件完成前，不得修改正式首頁、`solutions_data.js`、`contact.html` 或部署 GitHub Pages。
