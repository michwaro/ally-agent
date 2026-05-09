# AGENTS.md — Ally: Community Voice & Accountability Agent

## Setup
- Python 3.11+: `pip install -e ".[dev]"`
- Copy `.env.example` to `.env`, set OPENAI_API_KEY (optional —
  deterministic mode works without it)
- Verify: `python -m ally --help`
- Serve: `ally serve` → open http://localhost:8765

## Sub-agents (orchestrator.py)
- **Intake** — validates submission, anonymizes metadata
- **Translator** — detects language, translates to English for analysis
- **Classifier** — maps to: rights violation | resource exploitation |
  broken commitment | conflict trigger
- **RightsMapper** — links to African Charter, UDHR, national
  constitutions in frameworks/
- **ReportGenerator** — assembles structured Markdown accountability
  brief from prior agent outputs

## Testing
- Run: `pytest -q`
- Mock all OpenAI and HTTP calls in tests
- orchestrate() must work without OPENAI_API_KEY (deterministic mode)

## Style
- Type hints on all functions
- No print() — use rich.console.Console in CLI, SSE events in server
- Event JSON shape is fixed — never add or remove fields
- Sub-agent names are fixed — never rename them

## Review guidelines
- Always show diff before applying multi-file changes
- Five agents always run in order — never reorder or skip
- web/index.html must remain a single file
- Anonymization happens in Intake before any content is read —
  this ordering is a hard security requirement