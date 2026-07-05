# AI Problem-Solving System — Architecture Options for CEO Decision
> Enterprise AI consulting context. Constraint: web-based MVP first, cost-effective/low-code preferred, GitHub Pages-compatible where possible, solo-founder feasible.

---

## Option A — Static + No-Code RAG (Quickest MVP)
**Goal:** Get bookable, auditable AI problem-solving in front of clients inside 4–6 weeks.

### Core Features
- **Problem intake form** → stores request in a structured schema
- **RAG over uploaded docs / slides / case studies** → pulls relevant past solutions
- **Structured solution proposal page** → scoped approach, timeline, engagement model
- **Read-only admin/editor** → upload & curate knowledge base
- **GitHub Pages hosting** → zero hosting cost, CDN-backed

### Tech Stack
| Layer | Choice | Rationale |
|---|---|---|
| Frontend | Astro/Next.js static site or plain HTML + htmx | Can host on GitHub Pages; very low maintenance |
| Auth | None or cloudflare-turnstile / simple link | MVP doesn’t need org auth yet |
| Backend | Supabase Edge Functions or Vercel Edge API routes | Lightweight server-side, generous free tiers |
| Database | Supabase Postgres | Stores problems, solutions, embeddings metadata |
| Embeddings/Vector DB | Supabase pgvector | No separate infra; managed tonight |
| LLM | OpenRouter or OpenAI-compatible API | Call GPT-4o or Claude via single unified endpoint |
| Embed model | text-embedding-3-small / Voyage | Cheap, high quality |
| File storage | Supabase Storage or GitHub LFS | PDF/slide support |
| CI/Deploy | GitHub Actions → GitHub Pages / Vercel preview | Auto-deploy on push |

### Hosting Cost Estimate
- **GitHub Pages:** ~$0
- **Supabase Free Tier** (500MB DB, 1GB storage, 2M Edge Function invocations): ~$0
- **LLM API:** ~$50–400/month depending on volume (token-based)
- **Domain + email:** ~$15/year
- **Total MVP:** ~$50–400/month

### Data Flow
1. Client submits problem via web form
2. Edge function persists problem + runs embedding
3. Vector search over knowledge base → retrieves matching solutions / case studies
4. LLM composes a structured proposal referencing retrieved context
5. Proposal saved to DB and shown to client
6. Admin iterates on proposal (auto-save)

### AI/LLM Integration Points
- **Embedding step** at ingestion time
- **Retrieval step** in Edge Function (pgvector similarity search)
- **Generation step** using retrieved context as system prompt + user problem
- **Post-processing** for structured formatting (JSON schema or Zod-like constraints)

### Time-to-MVP
- **4–6 weeks** with solo founder part-time
- Week 1–2: Data model + embeddings pipeline + upload UI
- Week 3: Retrieval + LLM generation
- Week 4: Proposal UI + basic styling
- Week 5–6: Logo swap, deploys, 10 real problems tested

### Pros
- Cheapest path, free hosting
- Fastest to real user feedback
- SQL + pgvector familiar territory; low ops
- GitHub Pages → enterprise clients see polished public URL

### Cons
- Limited by free-tier burst/cold-starts
- No complex multi-agent orchestration yet
- Fine-tuning or eval loops are manual

---

## Option B — React App + Managed RAG Backend (Most Polished)
**Goal:** Scalable, client-facing SaaS feel with auth, usage tracking, and collaborators.

### Core Features
- Everything in Option A plus:
- **Multi-user auth** (clients, consultants, admins)
- **Subscription/usage tracking** per client
- **Collaborative proposal editing**
- **Scheduled follow-up emails / briefings**
- **Analytics dashboard** (most requested problem types, delivery accuracy)

### Tech Stack
| Layer | Choice | Rationale |
|---|---|---|
| Frontend | Next.js 14 App Router + shadcn/ui | Fast UI; built-in auth, API routes, server components |
| Auth | Clerk / Supabase Auth | Social + SSO, enterprise-ready |
| Database | Supabase Postgres | Same as A; connections durable |
| Vector DB | Pinecone or Weaviate Cloud | Managed; stronger filtering + metadata |
| Backend | Supabase Edge Functions or Next.js route handlers | Slightly more control than A |
| Blob storage | Supabase Storage / S3 | PDFs, PPTs, case studies |
| LLM | OpenRouter (multi-model router) | Switch providers by task |
| Eval pipeline | LangSmith / Braintrust | Track quality over time |
| Hosting | Vercel Pro + Supabase Pro | SLA-backed |

### Hosting Cost Estimate
- **Vercel Pro:** $20/seats/month
- **Supabase Pro:** $25–80/month depending on DB size
- **Pinecone Starter:** $70/month (or free dev)
- **LLM API:** $200–2000/month based on volume
- **Clerk / Auth:** $0–99/month
- **Total MVP:** ~$300–3000/month

### Data Flow
Same retrieval-augmented flow as Option A, with added:
- Auth gating before problem access
- Usage events streamed to analytics warehouse
- Proposal history → periodic export for governance

### AI/LLM Integration Points
- Same as Option A plus:
- **LLM-as-judge eval loop** when client rates proposal
- **Adapter layer** swapping models by task (routing via OpenRouter)
- **Prompt registry** in DB for governance

### Time-to-MVP
- **8–12 weeks** solo founder, or 4–6 weeks with 1 dev
- Week 1–3: Auth + user layers + multi-tenant data model
- Week 4–6: RAG backend + Pinecone pipeline
- Week 7–8: Dashboard + analytics + proposal flows
- Week 9–12: Polish, pilot with 3 clients

### Pros
- Professional SaaS → faster enterprise sales
- Auth + usage metrics = natural upsell hooks
- Weaviate/Pinecone metadata filtering helps quality
- Faster iteration once components exist

### Cons
- >10x cost bump vs static option
- More surface area to secure and maintain
- Founder time cost higher

---

## Option C — Agentic Workflow Platform (Highest ROI Long-term)
**Goal:** Multi-step reasoning workflows with tool use, memory, and GitHub integration.

### Core Features
- Everything in Options A/B plus:
- **Agentic solver pipeline:** decomposes problems → researches → drafts solutions → self-critiques → refines
- **Tool use** (web search, code execution, schema queries)
- **Session memory** per client / problem type
- **GitHub integration:** proposals push to client repos as issues/docs
- **Evaluation harness:** automated nightly benchmark on past problems

### Tech Stack
| Layer | Choice | Rationale |
|---|---|---|
| Frontend | Next.js 14 + shadcn/ui | Same as B |
| Auth | Clerk or GitHub Apps OAuth | Deepens GitHub linkage |
| Backend | LangGraph / CrewAI on FastAPI | Agent orchestration; retry + loops |
| Vector DB | Weaviate Cloud or pgvector | Same as A/B |
| Memory | Redis + Postgres + file-based checkpoints | Short + long-term memory |
| Exec env | Modal / E2B sandboxes | Secure code execution, evaluation |
| LLM | OpenRouter with fallback routing | Multi-model redundancy |
| Eval | Braintrust / LangSmith + custom CI | Nightly quality regression |
| Hosting | Modal + Vercel + Supabase | Agent infra independent |

### Hosting Cost Estimate
- **Vercel / Supabase:** $80–150/month
- **Modal compute:** $50–500/month based on agents run
- **Redis / checkpoints:** $20–100/month
- **Eval + logs:** $50–200/month
- **LLM API:** $400–5000/month (agents use 5–20x tokens per task)
- **Total MVP:** ~$600–6000/month

### Data Flow
1. Problem submitted → schema validated
2. Agent decomposes problem into research questions
3. Sub-agents run in parallel: search knowledge base, fetch web context, simulate code/SQL/strategy
4. Results written to memory store + proposal draft
5. Critic agent rates draft; if below threshold, triggers refinement loop
6. Final proposal + reasoning trace given to client
7. Session archived for later eval
8. Optionally pushed to GitHub via GitHub App

### AI/LLM Integration Points
- **Orchestrator** with structured prompt templates + tool schemas
- **ReAct/Plan-and-Execute** patterns via LangGraph
- **Tool API** surfaces: web search, GitHub API, SQL execution, schema inspection
- **Memory layer** across problems and personas
- **Eval harness** auto-generates grading rubrics nightly

### Time-to-MVP
- **12–20 weeks** (strong solo dev) or 8–14 with 2 devs
- Week 1–3: Frontend + auth + storage + basic RAG
- Week 4–6: Agent runtime + tool registry + sandboxing
- Week 7–9: Memory + multi-step evaluator
- Week 10–12: Evaluator harness + admin
- Week 13–20: GitHub integration + client pilots

### Pros
- Strong loop between quality and volume — more problems → better memory → better solutions
- Natural upsell: agent oversight, SLAs, benchmarking
- Differentiator against pure-RAG competitors
- Long-term automation: can solve 80% of consult intake without human

### Cons
- High token spend; need guardrails (budget cap, retry, fallback)
- Complexity debt; needs monitoring + observability early
- Longer path to revenue; need pilot revenue by week 8–10

---

## Comparison Matrix

| Dimension | A: Static + No-Code RAG | B: React + Managed RAG | C: Agentic Workflow |
|---|---|---|---|
| **Time-to-$1 revenue** | 4–6 weeks | 8–12 weeks | 12–20 weeks |
| **MVP Cost/mo** | $50–400 | $300–3000 | $600–6000 |
| **Enterprise Ready** | Medium | High | High+ |
| **Solo-founder feasible** | ✅ Yes | ⚠️ Harder | ❌ Needs 1–2 devs |
| **Client WOW factor** | Medium | High | Highest |
| **Ongoing token cost** | Low–Med | Medium | High |
| **Ops complexity** | Low | Medium | High |
| **GitHub Pages friendly** | ✅ Native | ⚠️ Partial (Vercel) | ❌ Modal/Sandbox heavy |
| **Scalability ceiling** | Medium | High | Very High |

---

## CEO Recommendation

**Build A first.**
Ship in 4–6 weeks, spend <$500/month, collect real client feedback, charge pilot fees immediately.

Then:
1. If you land >3 pilots in first 2 months: fast-track **Option B** to invoice / usage meter.
2. If problems are repeatable with high ROI: invest in **Option C** agent layer once B is live.

This staged approach avoids burning capital on infrastructure before product-market fit is proven.
