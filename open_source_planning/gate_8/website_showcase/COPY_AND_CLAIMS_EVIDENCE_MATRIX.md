# Copy and Claims Evidence Matrix (宣稱與公開證據對照矩陣)

- **專案名稱**：`phoenix-auditable-ai-flow`
- **文件狀態**：**`W0/W1 DRAFT - READY FOR OWNER REVIEW`**
- **最新更新**：2026-07-13

為確保官網開源展示之誠實性與透明度，所有對外文案宣稱之功能、測試及管理機制，均在此列出對應之公開 GitHub 儲存庫實體程式碼或文件證據連結。

---

## 宣稱與證據對照表 (Claims & Evidence Matrix)

| 官網宣稱內容 (Claim) | 公開證據類型 | GitHub 檔案 / Release 實體證據連結 (Evidence URL) |
|---|---|---|
| **開源專案版本**<br>已發布正式開源版本 v0.1.0。 | GitHub Release | [v0.1.0 Release](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/releases/tag/v0.1.0) |
| **自動化測試證明**<br>v0.1.0 公開版已通過 59 項整合、回歸與安全測試；此結果不等同生產安全認證。 | CI/CD 執行紀錄與代碼 | [tests/ 測試目錄](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/tree/v0.1.0/tests) 及 [v0.1.0 CI run](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/actions/runs/29232901901) |
| **Policy-as-Code**<br>系統提供輸入與輸出政策規則核對。 | 實體原始碼 | [policies/](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/tree/v0.1.0/src/phoenix_auditable_ai_flow/policies) |
| **人機協同 (HITL) 決策流程**<br>政策衝突或指定輸出政策結果可暫停並建立人工覆核；一般證據不足可直接回傳 `INSUFFICIENT_EVIDENCE`。 | 實體原始碼 | [workflow/orchestrator.py](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/v0.1.0/src/phoenix_auditable_ai_flow/workflow/orchestrator.py) 及 [review/](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/tree/v0.1.0/src/phoenix_auditable_ai_flow/review) |
| **本機稽核事件紀錄**<br>於本機 SQLite 記錄流程事件，可依 `request_id` 查詢；不具密碼學不可竄改保證。 | 實體原始碼 | [audit/sqlite_repository.py](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/v0.1.0/src/phoenix_auditable_ai_flow/audit/sqlite_repository.py) |
| **Mock-first 與合成知識邊界**<br>公開版使用 Mock Model 與 Markdown 合成 HR 規章，不連接正式 LLM 或客戶資料。 | 實體原始碼 | [mock_model.py](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/v0.1.0/src/phoenix_auditable_ai_flow/providers/mock_model.py) 及 [markdown_knowledge.py](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/v0.1.0/src/phoenix_auditable_ai_flow/providers/markdown_knowledge.py) |
| **企業專屬治理與商業限制**<br>明定開源與付費商業服務界限、禁止項目及支援政策。 | 治理文檔 | [ENTERPRISE.md](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/main/ENTERPRISE.md) |
| **安全性漏洞揭露原則**<br>已啟用安全通報與 Private Vulnerability Reporting。 | 安全文檔 | [SECURITY.md](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/main/SECURITY.md) |
| **開源治理模式與維護規範**<br>明定協作者守則、維護者流程與 release 檢核清單。 | 治理與運作手冊 | [GOVERNANCE.md](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/main/GOVERNANCE.md) / [MAINTAINERS.md](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/main/MAINTAINERS.md) / [RELEASE_CHECKLIST.md](https://github.com/Phoenix-AI-Edu/phoenix-auditable-ai-flow/blob/main/RELEASE_CHECKLIST.md) |
