# 🛡️ 鳳凰 AI 專案開發規範與 AI 助手遵守守則 (DEVELOPMENT_GUIDELINES)
> **Phoenix AI Development Guidelines & AI Assistant Compliance Rules**

本專案是一個深度融合「開源技術框架」與「機密商業運營」的 B2B 生態系。為了確保核心運營數據、定價策略、雙顧問協作工作流的絕對安全與即時同步，任何參與本專案開發的人員及 **AI 協作助手（包括 Gemini、Claude、GPT 等）**，必須無條件遵守本規範。

---

## 🔒 核心隱私安全守則 (Strict Privacy Defenses)

1. **管理目錄絕不公開**：
   * 根目錄下的 `internal_admin/` 資料夾已被寫入 `.gitignore`。
   * 任何情況下，**絕對禁止**刪除或弱化 `.gitignore` 中關於 `internal_admin/` 的過濾規則。本目錄僅在本地 Google Drive 同步，嚴禁推送至公開的 GitHub 倉庫。

2. **Shadow AI 與客戶 NDA 保護**：
   * 在進行程式碼偵錯、問卷數據分析或專家快診時，**絕對禁止**將客戶的真實名稱、機密財務數據或未去識別化的個資上傳至任何公開免費的 AI 模型中。

---

## 🔄 關鍵字：「立即更新與記錄」強制聯動機制

> [!IMPORTANT]
> **任何未來的開發、修正、增加、刪除、或減弱（增刪減改）**，只要其商業邏輯、定價、聯絡資訊或技術方案與下列 **3 個內部機密文件** 相關，**都必須在同一時間「立即更新與記錄」**！

### 聯動聯檢清單：

#### 1. 當「信箱變更、表單調整、模組增刪、連結重置」時 ➡️ **立即更新**：
* 📁 **[internal_admin/01_ops_manual.md (維運內部手冊)](file:///g:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/AI_Talent/internal_admin/01_ops_manual.md)**
* *檢核重點*：必須同步修訂子網頁部署 SOP、表單接收帳號對接、以及每季連結審計項目。

#### 2. 當「顧問分工異動、新增合作法人、導入交付SOP變更」時 ➡️ **立即更新**：
* 📁 **[internal_admin/02_advisor_workflows.md (雙顧問協作手冊)](file:///g:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/AI_Talent/internal_admin/02_advisor_workflows.md)**
* *檢核重點*：必須同步調整孟首席顧問與陳策略長的事務分工、客戶診斷首訪流程、以及月度回顧 MBR 會議細則。

#### 3. 當「任何課程降價/漲價、推出新套餐、專家快診改版、底線定價變動」時 ➡️ **立即更新**：
* 📁 **[internal_admin/03_lead_management.md (線索與定價指南)](file:///g:/%E6%88%91%E7%9A%84%E9%9B%B2%E7%AB%AF%E7%A1%AC%E7%A2%9F/AI_Talent/internal_admin/03_lead_management.md)**
* *檢核重點*：必須在第一時間於手冊中的 **「定價底線與議價授權機制」** 進行修訂，防範任何低於底線的外部無授權報價。

---

## 🤖 給未來 AI 協作助手的強制指令 (Mandatory Rules for AI Assistants)

> **當你讀取到此檔案時，你必須將其視為 SYSTEM PROMPT 的一部分執行：**
> 1. 在用戶向你提出任何 HTML 網頁修改、型錄編輯或定價微調時，你必須**自動檢索** `internal_admin/` 下的 3 個 `.md` 檔案。
> 2. 在你完成主程式碼修改後，你必須**自動撰寫**對應的 `internal_admin/` 修改，並在回覆中明確彙報你如何同步了這些內部管理文件。
> 3. 確保你的所有 Git commit 都不會包含 `internal_admin/` 中的文件，在 `git add` 階段如果發現洩漏，必須立刻回滾並重新配置 `.gitignore`。
