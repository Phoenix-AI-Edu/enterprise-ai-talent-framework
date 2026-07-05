# Intake Form Specification
**Purpose:** Capture enough structured context from the client/system user to drive retrieval and draft generation for a diagnostic report.  
**Owner:** Phoenix consultant enters on behalf of the client during intake.  
**Storage:** Supabase Postgres table `intake_submissions`.

---

## Record Schema

| Field | Type | Required | Validation / Notes |
|------|------|----------|-------------------|
| id | uuid | yes | PK |
| created_at | timestamptz | yes | default now() |
| updated_at | timestamptz | yes | default now() |
| status | enum | yes | draft / submitted / in_review / approved / closed |
| client_name | text | yes | Legal entity name |
| client_industry | text | yes | Industry category for retrieval filtering |
| client_revenue_band | text | no | e.g., NT$500M–1B / US$1B–5B |
| problem_title | text | yes | Short descriptive title |
| problem_statement | text | yes | One-paragraph description of the actual operational or business problem |
| problem_type_tags | text[] | no | Controlled vocabulary: ai-adoption, supply-chain, decision-latency, governance, post-m&a, etc. |
| business_context | text | yes | What is the current situation, trigger event, and urgency? |
| stakeholders | jsonb | no | Array of {role, name_or_title, department, influence, position_on_issue} |
| constraints | text | no | Budget, timeline, regulatory, data-access, or political constraints |
| success_criteria | text | yes | How client will judge whether the diagnostic was useful |
| prior_attempts | text | no | What has been tried, what failed, what is still in place |
| data_availability | text | no | What internal data sources are available vs restricted |
| confidentiality_level | enum | yes | standard / sensitive / highly_confidential |
| assigned_consultant | text | no | Phoenix consultant responsible |
| intake_channel | text | no | email / meeting / form / referral |
| intake_version | int | yes | 1 on first save; incremented on resubmit |

---

## Minimal Completeness Rule

An intake is eligible for draft generation only when:
- problem_statement, business_context, success_criteria, and assigned_consultant are non-empty
- problem_type_tags has >=1 item
- confidentiality_level is set

---

## UI Flow

1. Consultant opens new intake.
2. System suggests problem_type_tags and prior analog cases based on partial input (auto-suggest, not auto-save).
3. Consultant confirms or overrides tags and links any known analog cases.
4. Consultant submits; system creates `intake_submissions` row and emits `intake_submitted` event.
5. If admin rules allow, draft generation starts immediately; otherwise waits for scheduler.

---

## Retrieval Hooks

- On submit, embed `problem_statement + business_context + problem_type_tags` to vector DB.
- Run similarity search over:
  - frameworks by domain and tag
  - anonymized prior cases by problem_type_tags and industry proximity
- Store matched framework ids and case ids on the intake record for audit trail.

---

## RLS / Privacy Notes

- Client-identifying fields must never be included in the embeddings stored externally if using shared vector infra.
- Prefer storing embeddings with only `problem_type_tags + industry_band + problem_statement` rather than full client-identifying fields.
