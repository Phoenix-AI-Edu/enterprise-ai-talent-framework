# Website Showcase Verification Report

- Date: 2026-07-13
- Branch: `codex/open-source-showcase`
- Executor: Codex（網站實作與技術驗證）
- Planned website executor: 小 G
- Status: `W2 IMPLEMENTED / W3 TECHNICAL PASS / DEPLOYMENT PENDING OWNER APPROVAL`

## Implemented

- 官網首頁旗艦區由兩張擴充為三張系統卡。
- `experience` 系統總覽加入 Phoenix 可稽核 AI 工作流。
- 建立獨立詳情頁：`experience/phoenix-auditable-ai-workflow/index.html`。
- 建立正式工具 manifest 並通過既有 validator。
- 建立專屬 `auditable_ai_demo` 聯絡意圖與表單文案。
- 加入 Primary 商業 CTA、GitHub、Release、CI 與治理文件入口。
- 加入三系統能力鏈、六階段流程、互動導覽、開源／付費邊界與三類買方入口。
- 加入 canonical、Open Graph、`SoftwareSourceCode` 與 `Service` 結構化資料。
- 加入不含 PII 的 experience analytics 事件。

## Verification evidence

| Check | Result |
| --- | --- |
| Tool manifests | `Validated 2 tool manifest(s).` |
| System registry JavaScript | 3 systems loaded; new id present |
| HTML parsing | Homepage, catalog and detail page parsed successfully |
| Homepage rendering | 3 flagship cards; new detail link correct |
| Catalog rendering | 3 solution cards; new detail link correct |
| Guided demo | Next action changed content to Markdown knowledge step |
| Detail-page 390px check | no horizontal overflow; Primary CTA visible; 4 portfolio cards and 6 workflow steps present |
| Desktop detail check | no horizontal overflow; 6 campaign CTAs and 11 GitHub evidence links present |
| Detail-page link check | 18 unique links checked; 0 errors |
| Public evidence links | GitHub, Release, CI and governance URLs returned HTTP 200 |
| Contact intent | `auditable_ai_demo` selected; dedicated heading and submit copy rendered |
| Consent | not preselected |
| Browser console | 0 error or warning entries during contact verification |
| Private-reference scan | no private repository path, internal IP, API key or prohibited executor alias in new public files |

## Honest limitations

- No real Google Forms submission was performed in this round, avoiding production lead pollution. Existing form action and prior end-to-end integration remain unchanged.
- The W2 page uses an accessible interactive walkthrough instead of a new MP4. A marketing video may be added later after separate asset review.
- The page is not yet deployed. Owner preview approval is required before merging to `main` and publishing GitHub Pages.
- The public reference architecture remains local, Mock-first and not production certified.

## Deployment decision point

Recommended status: `READY FOR OWNER PREVIEW AND W4 DEPLOYMENT APPROVAL`.
