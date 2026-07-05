# Knowledge Asset Write-Back Format
**Purpose:** After every delivered diagnostic, turn anonymized experience into reusable assets so the system improves over time.  
**Trigger:** When report status becomes `delivered` and client signs off.  
**Owner:** Phoenix consultant fills one record per delivered diagnostic.  
**Storage:** Supabase table `knowledge_assets`.

---

## Asset Record Schema

| Field | Type | Required | Notes |
|------|------|----------|-------|
| id | uuid | yes | PK |
| created_at | timestamptz | yes | |
| asset_type | enum | yes | case_record / framework_pattern / failure_mode / question_bank |
| source_intake_id | uuid | yes | FK to intake_submissions |
| source_report_id | uuid | yes | FK to report |
| problem_type_tags | text[] | yes | Controlled vocabulary |
| industry_context | text | no | Broad category, never specific company name |
| anonymized_context | text | yes | De-identified situation description |
| root_cause_structure | jsonb | no | Extracted reusable causal structure or taxonomy |
| framework_refs | uuid[] | no | Frameworks applied |
| hypothesis_patterns | jsonb | no | Reusable hypothesis templates for similar problems |
| option_patterns | jsonb | no | Reusable option building blocks |
| failure_signals | jsonb | no | Observable early signals for future detection |
| decision_trace | jsonb | no | What was decided, why, and by whom |
| outcome_notes | text | no | What happened after delivery; only known/verified facts |
| reusability_score | int | no | 1–5; 5 = expected to be reused in many future diagnostics |
| next_reuse_flag | bool | no | Mark for proactive injection into future RAG prompts |
| retention_review_date | date | no | Auto-set +6 months for review |
| legal_clearance | text | no | Any retention restriction or required deletion date |

---

## Write-Back Process

1. **Trigger:** Consultant marks report `delivered`.
2. **Form present:** Consultant is shown a write-back form with pre-populated fields from intake and report.
3. **De-identification check:** Form blocks any field that could re-identify the client; show warning if ambiguous.
4. **Submit:** Record saved to `knowledge_assets` with `asset_type` selected.
5. **Indexing:** Background job embeds new asset into vector index for future retrieval.
6. **Feedback loop:** If `reusability_score >= 4`, asset is queued for use in next N similar problems automatically.

---

## Reuse Rights

- Assets in this table are Phoenix property unless a client explicitly negotiated asset retention in their SOW.
- `legal_clearance` must be filled if client negotiated restrictions.
- If client requested deletion, set `retention_review_date` to past and queue delete job.

---

## Quality Covenants

- Do not write assets that require the original client name to be useful. If the lesson is client-specific and not generalizable, do not write it here.
- Always attach framework_refs when known; otherwise retrieval quality decays.
- Never include verbatim client internal documents unless they are already public frameworks.
