# AI_Talent 平台本機遷移計畫 (Migration Plan)

## 1. 遷移背景與核心原則
目前 `AI_Talent` 平台存放於 `G:\我的雲端硬碟\AI_Talent` (雲端同步目錄)。繼續在此開發將面臨檔案鎖死、Git 歷史損毀與效能低落等風險。

**本次遷移目標**：將開發主工作區安全轉移至本機磁碟。
**最高指導原則**：
- **唯一 Canonical Path**：未來所有的開發與平台維護，統一在 `C:\Users\m1016\Documents\AI_Talent` 進行，避免多個工作區並存造成混亂。
- **不盲目覆蓋**：遷移前必須進行 **Git Divergence Audit (差異稽核)**，根據 G 槽 Git 與 GitHub 的領先狀態，決定搬遷的決策樹路線。
- **資料保命第一**：在任何搬遷動作前，一律先產生 `.bundle` 完整備份。

---

## 2. Phase C-0.5：Git 差異稽核與保命備份 (Divergence Audit)

在進行任何搬遷或 `git commit` 之前，請在 PowerShell 執行以下動作：

### Step 1: 建立保命備份 (Git Bundle)
這能確保就算搬遷失敗，所有的分支與未 push 的 commits 都能完整救回。
```powershell
cd "G:\我的雲端硬碟\AI_Talent"
git bundle create "C:\Users\m1016\Documents\AI_Talent_git_backup.bundle" --all
```

### Step 2: 執行差異稽核 (Divergence Audit)
請執行以下指令來判斷 G 槽與 GitHub 遠端的差異：
```powershell
git status --short
git remote -v
git branch -vv
git log --oneline --decorate --graph --all -n 30
git log origin/main..HEAD --oneline
git stash list
```

---

## 3. 搬遷決策樹 (Migration Decision Tree)

根據上述稽核中 `git log origin/main..HEAD` 的結果，選擇對應的搬遷路線：

### 路線 A：G 槽 Git 領先 (有未 Push 的 Commits 或本地分支)
**適用條件**：`origin/main..HEAD` 有內容，或有重要 stash。
**策略**：完整搬遷本機，保留 `.git`。
1. 暫停 Google Drive 同步。
2. 使用 Robocopy (或 Copy-Item) 完整複製到本機：
   ```powershell
   robocopy "G:\我的雲端硬碟\AI_Talent" "C:\Users\m1016\Documents\AI_Talent" /E /XD "node_modules" ".venv"
   ```
3. 前往本機目錄 `C:\Users\m1016\Documents\AI_Talent`，檢查狀態後再將 commits push 至 GitHub。

### 路線 B：GitHub Git 最新，G 槽只是多出未追蹤素材
**適用條件**：`origin/main..HEAD` 無內容，且沒有重要的本地分支與 stash。
**策略**：GitHub Clean Clone + Overlay (覆蓋)。
1. 在本機直接 Clone 最乾淨的版本：
   ```powershell
   cd C:\Users\m1016\Documents
   git clone https://github.com/Phoenix-AI-Edu/enterprise-ai-talent-framework.git AI_Talent
   ```
2. 將 G 槽的靜態素材覆蓋過去，**但絕對排除 `.git`、DB 與快取**：
   ```powershell
   robocopy "G:\我的雲端硬碟\AI_Talent" "C:\Users\m1016\Documents\AI_Talent" /E /XD ".git" "node_modules" ".venv" /XF "*.db" ".env"
   ```

---

## 4. 特殊目錄獨立稽核

在 G 槽中，有兩個大型未追蹤目錄：
- `ai-diagnostic-system/`
- `ai-diagnostic-workbench/`

**嚴禁盲目整包 Commit**。在正式 Push 到遠端前，必須先進入這兩個目錄：
1. 檢查是否包含自己的 `.git` (若是，可能需要設為 submodule)。
2. 檢查是否包含巨大的模型檔案、快取或敏感的 `.env`。
3. 確認無誤或加入 `.gitignore` 後，才能分批加入主版本庫。

---

## 5. 舊版封存 (Legacy Archiving)

確認本機 `C:\Users\m1016\Documents\AI_Talent` 運作正常，且遠端 GitHub 備份完成後：
- 將原目錄更名：`Rename-Item -Path "G:\我的雲端硬碟\AI_Talent" -NewName "AI_Talent_Archive_Legacy"`
- 觀察 1~2 週，確定沒遺漏任何資源後，再考慮永久刪除舊目錄。
