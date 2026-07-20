# HANDOFF → 小H（官網 Diagnostic Funnel HARD V1）

**日期：** 2026-07-20  
**Repo：** `Phoenix-AI-Edu/enterprise-ai-talent-framework`（本地 `C:\Users\m1016\Documents\AI_Talent`）  
**分支：** `feat/diagnostic-funnel-hard-v1`  
**基準：** 最新 `origin/main`  
**狀態：** 實作完成，待 commit／push／開 PR（依站內 push 政策由小H 執行）

## 做了什麼

1. 複製規格：`docs/WEBSITE_DIAGNOSTIC_FUNNEL_HARD_V1_HANDOFF.md`  
2. 重做 `index.html` `#diagnostic` 結果漏斗（最硬商業版）  
   - 成熟度帶：explore / start / execute / operate（5–8 / 9–12 / 13–16 / 17–20）  
   - 必選 next_step 1–5（無「不需要」）  
   - §5 預選演算法 + Q4=A 治理覆蓋  
   - 定稿免責／五段主推／兩段警告／五段感謝  
   - 內嵌聯絡表單 → **商業 Google Form**（與 contact 同端點）  
   - quiz payload 寫入需求說明隱藏欄  
3. `contact.html`：新增 kit / Capital Decision Sprint 需求類型；支援 quiz query 預填  
4. 測試紀錄：`docs/DIAGNOSTIC_FUNNEL_HARD_V1_T1_T13_TEST.md`

## 端點（已拍板）

- 主：結果頁 POST 商業 Form  
- 次：next_step=1 感謝區工具包 Form 連結  
- 備援：contact.html query 預填  

## 建議 git 指令（小H）

```bash
cd "C:/Users/m1016/Documents/AI_Talent"
git status
git add docs/WEBSITE_DIAGNOSTIC_FUNNEL_HARD_V1_HANDOFF.md \
        docs/DIAGNOSTIC_FUNNEL_HARD_V1_T1_T13_TEST.md \
        index.html contact.html HANDOFF_TO_XIAO_H.md
git commit -m "$(cat <<'EOF'
feat(diagnostic): hard commercial funnel on quiz result (v1)

Force next-step 1-5 selection with scoring-based preselect, full lead
payload into commercial Google Form, and contact.html quiz prefills.
EOF
)"
git push -u origin feat/diagnostic-funnel-hard-v1
gh pr create --base main --title "feat(diagnostic): HARD V1 commercial result funnel" --body "$(cat <<'EOF'
## Summary
- Rebuild `#diagnostic` result into mandatory 1–5 service funnel (no skip)
- Scoring bands + Q5/Q4 preselect algorithm per handoff
- Inline lead form → existing commercial Google Form with quiz payload
- contact.html accepts quiz query prefills; kit/sprint request types

## Spec
- docs/WEBSITE_DIAGNOSTIC_FUNNEL_HARD_V1_HANDOFF.md

## Test plan
- [x] T1–T13 matrix in docs/DIAGNOSTIC_FUNNEL_HARD_V1_T1_T13_TEST.md
- [ ] Manual browser pass on desktop + mobile
- [ ] One live Google Form test row (mark TEST)

## Notes
- Prices aligned with live site (12,800 / 29,800)
- Does not touch AI_Allocation_OS
EOF
)"
```

## 注意

- 先前 `codex/open-source-showcase` WIP 已 stash：`wip-before-diagnostic-funnel-hard-v1`  
  需要時：`git checkout codex/open-source-showcase && git stash pop`  
- 未改價位；未接 Kernel／Field  
- Production 驗證 URL：合併後 `…/enterprise-ai-talent-framework/#diagnostic`
