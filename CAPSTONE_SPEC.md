# Capstone Spec — Ally: Community Voice & Accountability Agent

## Problem statement
In conflict-affected and marginalized communities across Africa, rights
violations go undocumented, broken government promises go unchallenged,
and community concerns go unheard — not because people don't want to
speak, but because there is no safe, accessible, or linguistically
inclusive way to do so. Existing accountability tools assume stable
internet, digital literacy, and identity exposure in contexts where
being identified can mean retaliation or displacement.

Ally is a multi-agent AI system built with OpenAI Codex that gives
communities a safe, anonymous, and multilingual way to document and
escalate accountability concerns. No account required. No identity
exposed. Works on minimal bandwidth.

Target users: community members in conflict-affected areas, CSOs,
human rights defenders, and facilitators operating in OSF geographies.

OSF tracks: Voice & Accountability (primary) + Peace & Community
(secondary)

## Acceptance criteria

### A. Multi-agent orchestrator
Five sub-agents run in this exact order, each emitting typed events:
1. **Intake** — validates the submission, cryptographically anonymizes
   identifying metadata before any content analysis begins
2. **Translator** — detects the submission language, translates to
   English for analysis (supports Arabic, French, Portuguese, Swahili,
   and local languages)
3. **Classifier** — maps the concern to an accountability category:
   rights violation, resource exploitation, broken commitment, or
   conflict trigger
4. **RightsMapper** — links the report to relevant legal frameworks:
   African Charter on Human and Peoples' Rights, UDHR, and applicable
   national constitutional provisions
5. **ReportGenerator** — assembles the four prior outputs into a
   structured Markdown brief a CSO or community leader can act on or
   submit to an oversight body

### B. Typed event shape (fixed — do not change)
```json
{
  "agent": "<one of the five names>",
  "status": "started | thinking | evidence | completed | failed",
  "message": "<short human string>",
  "evidence": ["<optional list of findings, clauses, categories>"],
  "ts": <unix epoch float>
}
```
Each agent emits at minimum: one `started`, one `evidence` with
concrete findings, one `completed` or `failed`.

### C. FastAPI server (exact paths)
- `POST /api/run-stream` — body `{report_text}`, returns
  `text/event-stream` of events. After ReportGenerator completes,
  sends `event: done` with `{"report": "<markdown string>"}`.
- `POST /api/upload-report` — multipart text or PDF upload, extracts
  plain text, returns `{"report_text": "<text>"}`.
- `GET /` — serves `web/index.html`.
- `GET /healthz` — returns `{"ok": true}`.
- CORS: allow `http://localhost:8765` and `http://127.0.0.1:8765`.

### D. Single-file web app at web/index.html
Sections in this order:
- `#hero` — display headline, tagline, animated 5-node agent preview
- `#problem` — three stat blocks with field-relevant numbers
- `#how` — three column cards mapping sub-agents to analysis steps
- `#console` — anonymous report submission form (textarea + optional
  file upload). Live agent graph (5 nodes: idle → active → done)
  driven by real SSE events. Scrolling event log. Live Markdown
  preview of the generated brief.
- `#built` — "Built with Codex IDE" with real prompt→diff cards
- `#run` — OS-specific setup instructions (macOS, Windows, Linux)
- `#next` — post-MVP roadmap pills

### E. Deterministic mode
When OPENAI_API_KEY is unset, all five sub-agents run in pure-Python
mode using heuristics and produce useful placeholder output. The demo
must run without an API key.

## Architecture
ally-agent/
├── CAPSTONE_SPEC.md
├── README.md
├── AGENTS.md
├── pyproject.toml
├── frameworks/           # African Charter + UDHR JSON
├── analysis/             # criteria.yaml
├── src/ally/
│   ├── init.py
│   ├── cli.py            # submit command + serve command
│   ├── orchestrator.py   # five sub-agents + Event dataclass +
│   │                     # orchestrate() generator
│   ├── server.py         # FastAPI + SSE streaming
│   └── loader.py         # text extraction from PDF or plain text
├── web/
│   └── index.html        # single-file editorial UI
└── tests/
├── test_orchestrator.py
└── test_server.py

## Tech stack
- Language: Python 3.11
- Libraries: openai, typer, rich, httpx, pypdf, fastapi,
  uvicorn[standard], python-multipart
- Codex surface: VS Code extension

## Task list
1. [ ] Refactor repo: rename package to ally, rebuild cli.py with
       submit + serve commands, update pyproject.toml
2. [ ] Build orchestrator.py: five sub-agents, typed Event dataclass,
       orchestrate() generator, deterministic mode without API key
3. [ ] Build server.py: FastAPI app with all endpoints, SSE streaming,
       report upload
4. [ ] Build web/index.html: editorial single-file UI with live agent
       graph driven by real SSE events, anonymous submission form
5. [ ] Tighten #built section: real prompt→diff cards from this build
6. [ ] Update README.md and AGENTS.md for submission
7. [ ] End-to-end demo: serve + browser run against a real sample
       community report

## Out of scope (MVP)
- SMS/USSD interface (post-MVP)
- Persistent report database (post-MVP)
- Multi-document pattern aggregation (post-MVP)
- Authentication for CSO dashboard (post-MVP)

## Reproducibility
A learner who pastes the prompts in order produces the same shape of
output. Deterministic mode produces useful output without OPENAI_API_KEY.

## Demo script (60 seconds)
1. "Rights violations in marginalized communities go undocumented
   because there's no safe way to report them. Ally changes that."
2. "A community member types a report — in any language, no account,
   no identity exposed — and hits Submit."
3. "Five agents run live: Intake anonymizes, Translator converts the
   language, Classifier categorizes the concern, RightsMapper links
   it to the African Charter, ReportGenerator writes the brief."
4. "Here's the accountability report it just produced — ready for a
   CSO to act on."
5. "Every part of this was built inside Codex IDE."
6. "Next: SMS/USSD input, pattern aggregation across reports,
   multi-country deployment."