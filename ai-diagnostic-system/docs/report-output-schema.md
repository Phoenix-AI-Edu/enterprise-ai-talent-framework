# Report Output Schema
**Purpose:** Stable, schema-validated structure for diagnostic drafts and final consultant-signed reports.  
**Format targets:** Markdown source → rendered internal view → PDF export → presentation deck.  
**Audience:** Consultant editor → client executive.

---

## Top-Level Document Object

| Field | Type | Required | Notes |
|------|------|----------|-------|
| id | uuid | yes | Report instance |
| intake_id | uuid | yes | FK to intake_submissions |
| created_at | timestamptz | yes | |
| updated_at | timestamptz | yes | Bumped on each revision |
| version | int | yes | Starts at 1 |
| status | enum | yes | draft / consultant_review / client_review / signed / delivered |
| consultant_id | text | yes | Assigned Phoenix consultant |
| framework_refs | uuid[] | no | Linked framework assets used |
| case_refs | uuid[] | no | Linked anonymized case assets used |
| sections | jsonb | yes | Ordered section objects |
| metadata | jsonb | no | Client-requested tags, classification, confidentiality handling |

---

## Section Schema

Each section object:

| Field | Type | Required | Notes |
|------|------|----------|-------|
| section_key | enum | yes | executive_summary / problem_decomposition / hypotheses / root_cause_map / risk_assessment / options / decision_matrix / roadmap / appendices |
| title | text | yes | Human-readable heading |
| content | jsonb | yes | Rich structured content |
| citations | uuid[] | no | Framework/case ref ids used in this section |
| consultant_notes | text | no | Inline notes, not shown to client in draft view |
| edit_state | enum | yes | ai_draft / consultant_edited / accepted / rejected |
| revised_by | text | no | Consultant identifier |
| revised_at | timestamptz | no | |

---

## Required Sections per Status

| Status | Sections Required |
|--------|------------------|
| draft | executive_summary, problem_decomposition, hypotheses, root_cause_map, risk_assessment |
| consultant_review | All prior + options, decision_matrix |
| client_review | All prior + roadmap |
| signed / delivered | All sections + consultant_signature block |

---

## Content Shapes by section_key

- **executive_summary**: plain_text + bullets + decision_sentence
- **problem_decomposition**: list of {sub_problem, evidence, owner_or_source}
- **hypotheses**: list of {hypothesis, supporting_signals, testing_method, confidence}
- **root_cause_map**: adjacency list or hierarchy of {node, relation_to_parent, evidence_strength}
- **risk_assessment**: list of {risk, probability, impact, mitigation, owner}
- **options**: list of {option_name, description, tradeoffs, cost_band, timeline, dependencies}
- **decision_matrix**: table form with rows=options, cols=criteria, plus recommended_option and rationale
- **roadmap**: phases with {phase, actions, owners, metrics, timeline, dependencies}
- **appendices**: references, raw retrieval snippets, source list

---

## Consultant Sign-Off Block

Required fields at report finalization:
- consultant_name
- title
- signature_date
- attestation_text: "This report was produced using Phoenix’s diagnostic reasoning system; the final version is consultant-signed and represents Phoenix’s professional output."
- limitations: 1–3 bullets on what the report does/does not cover

---

## PDF Export Rules

- Header: client_name, problem_title, report_title, classification level, report date, version
- Footer: page number, confidentiality notice, consultant attribution
- Redact client_name in any appendix that includes raw retrieval snippets if confidentiality_level = highly_confidential

---

## Retrieval Citations

Every draft section must include citations when content was retrieved from:
- a framework asset → cite framework title + version
- an anonymized case → cite ANON-{case_id} only
- no external source → mark as consultant-authored

Citations are rendered as footnotes in PDF and as inline badges in internal view.
