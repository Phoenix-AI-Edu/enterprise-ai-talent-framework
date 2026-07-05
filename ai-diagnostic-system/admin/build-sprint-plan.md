# Build Sprint Plan — Diagnostic Work台 MVP
**Target:** In 4–6 weeks, deliver an internal consultant work台 that can produce the first paid diagnostic pilot with consultant sign-off.  
**Non-goals:** No SaaS, no multi-tenant auth, no agentic loop, no subscription management, no integrations.

---

## Week 1 — Foundation and Intake
**Goal:** Store problems and show them back; consultant can create and submit an intake record.

### Deliverables
- Supabase project configured with tables:
  - `intake_submissions` per `admin/intake-form-spec.md`
  - `reports` per `docs/report-output-schema.md`
  - `knowledge_assets` per `admin/knowledge-asset-schema.md`
- Intake form UI:
  - Fields from schema with client-side validation
  - Auto-suggest problem_type_tags based on partial input
  - Submit creates intake row and emits `intake_submitted`
- Intake list view (consultant only) showing status

### Acceptance
- 3 test intakes can be saved, retrieved, and listed
- Empty required fields block submission

---

## Week 2 — Knowledge Base and Retrieval
**Goal:** Upload internal assets and show analog matches for a problem.

### Deliverables
- Admin upload UI for framework/case assets with metadata tagging
- Embedding pipeline using one embed model → Supabase `pgvector`
- Similarity search API returning top 3–5 matches with source metadata
- Intake detail view shows matched assets after submission

### Acceptance
- Upload 5 frameworks and 3 cases; retrieval returns them with citations
- No client-identifying fields are embedded or exposed in results

---

## Week 3 — Diagnostic Draft Output
**Goal:** Generate a structured draft from intake + retrieved context.

### Deliverables
- LLM generation endpoint with retrieval context injected
- Output adheres to `docs/report-output-schema.md` section list for `draft` status
- Draft stored with `edit_state = ai_draft`

### Acceptance
- Run 3 problems from tests/test-problems.md
- Each draft contains: executive_summary, problem_decomposition, hypotheses, root_cause_map, risk_assessment
- Output includes citations to frameworks/cases used

---

## Week 4 — Consultant Editor and Report Composer
**Goal:** Consultant can review, edit, approve, and prepare a final report.

### Deliverables
- Report viewer with section-level edit controls:
  - section-level text replacement
  - accept/reject toggle per section
  - consultant notes field (internal only)
- Version increment on save
- Consultant sign-off block form
- Report status transitions: draft → consultant_review → client_review → signed → delivered

### Acceptance
- Consultant can edit and sign 1 draft in <=60 minutes for a familiar problem
- Final report shows clear `consultant_signed` attribution

---

## Week 5 — PDF Export and Beta Report Polish
**Goal:** Produce a PDF the client can take into a meeting.

### Deliverables
- Markdown → PDF export with:
  - Header: client_name, problem_title, classification, version
  - Footer: page number, confidentiality, consultant attribution
  - Consultant sign-off page
- Basic template styling; client name redaction if highly_confidential

### Acceptance
- 3 reports export to clean PDF without broken formatting
- PDF is accepted by Phoenix consultant as “meeting-ready”

---

## Week 6 — Write-Back, Hardening, Pilot Demo
**Goal:** Close the loop and show a credible first pilot experience.

### Deliverables
- Knowledge write-back form tied to report delivery
- Auto-embed new asset into vector index
- 10-problem batch run with scoring per problem (see Test Protocol)
- Bug fixes and stability pass
- Demo-ready consultation flow: intake → draft → consultant edit → PDF → write-back

### Acceptance
- 10 problem test set run with edit-time logs
- At least 1 report meets “meeting-ready” criteria
- Evaluation form can record 5-dimension score for each problem

---

## Test Protocol per Problem

After every run, record:

| Dimension | Scale | Definition |
|-----------|-------|------------|
| Diagnostic structural completeness | 1–5 | Does output cover required sections and causal reasoning? |
| Citation usefulness | 1–5 | Are retrieved references relevant and traceable? |
| Consultant edit time | minutes | Total time to finalize report |
| Meeting usability | yes/no | Can client use this in an internal meeting without Phoenix? |
| Asset reusability | yes/no | Did this generate >=1 reusable framework or pattern? |

Go/No-go check after 6 problems: if >=3 problems can convert to paid pilot or follow-on consulting, proceed; otherwise reassess value hypothesis.

---

## Not Doing This Sprint
- Subscription management, invoicing, multi-tenant auth
- Agentic loops or multi-step tool use
- Public API, SDK, integrations
- Real-time multi-user collaboration
- Complex inline commenting or rich-text editor
- Analytics dashboard

---

## Demo Conditions
To demonstrate pilot readiness:
1. Consultant creates intake from a real-scope problem
2. System generates draft with citations
3. Consultant edits and signs final report
4. Exported PDF is presenter-ready
5. Knowledge asset write-back completes
