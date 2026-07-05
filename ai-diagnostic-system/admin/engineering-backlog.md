# Engineering Backlog — Diagnostic Work台 MVP
**Target:** Build the minimum billable diagnostic work台 in 4–6 weeks.  
**North Star:** Enable the first paid pilot engagement, with consultant sign-off as the formal deliverable.

---

## Assumptions
- **Product form:** Consultant accelerator, not a self-service SaaS in M1–M2.
- **Primary user:** Phoenix consultant producing a client-facing diagnostic report.
- **Secondary user:** Design partner client, who only sees intake prompt and final report.

---

## P0 — Must Have for First Paid Pilot

1. **Problem intake capture**
   - Collect: problem statement, business context, stakeholders, constraints, success criteria.
   - Input: structured web form with validation.
   - Storage: Supabase Postgres.

2. **Knowledge base ingestion and management**
   - Upload/internalize: frameworks, case artifacts, prior reports, output templates.
   - Admin UI for upload and metadata tagging (problem domain, industry, framework used).

3. **RAG retrieval with visible citations**
   - Retrieve relevant framework passages and analog cases.
   - Expose source references in the diagnostic draft; no black-box answers.

4. **Structured diagnostic draft generation**
   - Output fields: problem decomposition, hypotheses, root-cause candidates, risks, options, next questions.
   - Enforce a stable schema so reports are predictable.

5. **Consultant editor and annotation layer**
   - Allow inline edits, comments, acceptance/rejection flags on each draft section.
   - Preserve original AI draft vs final consultant version.

6. **Report composer and export**
   - Generate a final Markdown/PDF report with consultant sign-off section.
   - Include executive summary, detailed diagnosis, roadmap, risks, appendices.

7. **Knowledge asset write-back**
   - After delivery, extract anonymized case metadata and reusable patterns into an asset record.
   - Fields: problem type, industry, frameworks used, outcome notes, next-reuse flag.

---

## P1 — Do After First Pilot Revenue

- Consultant dashboard: problem list, status, time spent, client status.
- Version history and diff view for drafts and final reports.
- Client feedback capture form (structured, post-delivery).
- Report template polish and basic styling system.

---

## Not Now — Defer Until PMF Signals

- Subscription management, invoicing, multi-tenant auth.
- Agentic multi-step solver with tool use.
- Native integrations to client tools.
- Public API / SDK / marketplace.
- Full analytics product suite.

---

## Success Criteria (Gate)

1. Consultant frontend diagnostic time reduced by >=30% versus prior manual process.
2. Client takes the report into an internal meeting without Phoenix staff present.
3. >=3 of the first 10 real problems convert to paid pilots or follow-on consulting.

If all three are true by pilot 3, invest in P1 and B/C architecture upgrade.
