# Hermes Clew

**Agent Readiness Scanner for the Agentic Web**

---

## The Problem

The web is about to get a second audience. AI agents — not just humans — are starting to browse, navigate, and interact with web applications. They book flights, fill out forms, extract data, and complete tasks on behalf of users.

But most web apps weren't built for them.

Vibecoded apps ship fast, but they ship with div-soup, missing labels, generic link text, and zero structured data. A human can squint past these issues. An AI agent can't. It sees a wall of `<div onclick="...">` and has no idea what's a button, what's a link, or what's a heading.

**The result:** agents fail silently. They can't navigate. They can't fill forms. They bounce. And the developer has no idea why — because the app looks fine to a human.

There's no tool that tells developers: *"Here's how an AI agent sees your app, and here's what to fix."*

## The Solution

Hermes Clew scans HTML, JSX, and TSX files in a GitLab repository and produces an **Agent Readiness Report** — a score from 0 to 100 that tells you exactly how well an AI agent can use your application, broken down across 6 categories, with plain-English explanations of what's working, what's broken, and what to fix first.

It lives inside GitLab Duo Chat. You talk to it, it scans, it reports. No frontend. No UI. No database.

> *"Awareness, not judgment."* — Hermes Clew explains problems like a knowledgeable colleague, not a compliance auditor.

**Part of the Clew suite:** Ariadne Clew | Janus Clew | Lumen Clew | Metis Clew | Hermes Clew

---

## How It Works

Hermes Clew uses a three-layer architecture:

1. **GitLab Duo Agent** (Interface) — Receives your request via Duo Chat, identifies files, triggers the scan, posts the report.
2. **Python Scan Engine** (Mechanical) — Finds HTML/JSX/TSX files, runs 6 category checks via pattern matching, produces raw JSON findings. No reasoning, no judgment — just facts.
3. **Claude Reasoning Layer** (Anthropic) — Receives raw findings, reasons about context and false positives, weighs severity, generates a plain-English report with an Agent Readiness Score (0-100).

---

## What It Checks

| Category | Weight | What Agents Need |
|----------|--------|-----------------|
| Semantic HTML | 25% | Standard HTML elements agents can identify by tag name |
| Form Accessibility | 20% | Labeled fields agents can identify and fill |
| ARIA & Accessibility | 15% | Role and state information for complex widgets |
| Structured Data | 15% | Machine-readable metadata (Schema.org, Open Graph) |
| Content in HTML | 15% | Content in initial HTML, not behind JavaScript |
| Link & Navigation | 10% | Predictable, descriptive navigation |

### Score Ranges

- **80-100:** Agent-Ready — agents can navigate and interact with this app
- **60-79:** Partially Ready — agents can find content but struggle with interactions
- **40-59:** Agent-Challenged — agents can see the page but can't do much
- **0-39:** Agent-Invisible — agents bounce immediately

---

## Quick Start

### Prerequisites

- Python 3.10+
- pytest (for running tests)
- GitLab account with access to the AI Hackathon group (for Duo Chat integration)

### Run the Scanner Locally

```bash
# Clone the repo
git clone <repo-url>
cd hermes-clew

# Run against a target repo
python -m scan.scanner /path/to/your/web-app

# Output: JSON with scores, findings, and category breakdowns
```

### Run Tests

```bash
pip install pytest
pytest tests/ -v
```

## CI → Duo workflow (Deterministic scan + LLM reasoning)

### 1) Run the deterministic scan in GitLab CI
Push any commit to trigger the pipeline.

In GitLab:
Build → Pipelines → latest pipeline → `hermes_clew_scan` job → Artifacts

Download:
`hermes_clew_scan_results.json`

### 2) Generate the final Agent Readiness Report in Duo
Open GitLab Duo Chat in this project and paste:

Hermes Clew: Use the following deterministic scan JSON as authoritative input.
Reduce false positives/negatives, prioritize fixes, and output the report in the strict Hermes Clew format.

SCAN JSON:
<paste contents of hermes_clew_scan_results.json here>
```

### Use via GitLab Duo Chat

1. Open GitLab Duo Chat in a project containing HTML/JSX/TSX files
2. Select the Hermes Clew agent
3. Say: "Scan this project"
4. Read the Agent Readiness Report

---

## Project Structure

```
hermes-clew/
├── AGENTS.md                          # Describes project to any AI agent
├── README.md                          # This file
├── LICENSE                            # MIT
├── .gitlab/
│   └── duo/
│       └── agent-config.yml           # GitLab Duo agent configuration
├── scan/
│   ├── __init__.py
│   ├── scanner.py                     # Entry point — orchestrates checks
│   ├── check_semantic_html.py         # Category 1 checks
│   ├── check_form_accessibility.py    # Category 2 checks
│   ├── check_aria.py                  # Category 3 checks
│   ├── check_structured_data.py       # Category 4 checks
│   ├── check_content_in_html.py       # Category 5 checks
│   ├── check_link_navigation.py       # Category 6 checks
│   ├── file_finder.py                 # Finds HTML/JSX/TSX files
│   ├── scoring.py                     # Applies weights, computes score
│   ├── report_prompt.py               # Builds Claude reasoning prompt
│   └── external_url.py               # STUB: Path B external scanning
├── tests/
│   ├── test_check_semantic_html.py
│   ├── test_check_form_accessibility.py
│   ├── test_check_aria.py
│   ├── test_check_structured_data.py
│   ├── test_check_content_in_html.py
│   ├── test_check_link_navigation.py
│   ├── test_file_finder.py
│   ├── test_scoring.py
│   ├── test_integration.py            # End-to-end pipeline test
│   └── fixtures/                      # Hand-written test HTML/JSX files
├── demo-app/                          # Sample app for scan demo (FreshCart)
│   ├── index.html                     # Landing page — mixed good/bad patterns
│   ├── login-form.html                # Form with accessibility gaps
│   └── Dashboard.jsx                  # React component — div-soup + good sections
└── docs/
    ├── PRD_HERMES_CLEW.md             # Product requirements document
    ├── ARCHITECTURE.md                # System architecture overview
    └── SPIKE_RESULTS.md               # Platform capability validation
```

---

## Design Philosophy

**Awareness, not judgment.** Hermes Clew explains problems like a knowledgeable colleague, not a compliance auditor. It tells you WHY an agent would struggle, not just WHAT is wrong.

**Agent-first.** This tool practices what it preaches. The codebase uses semantic file names, includes AGENTS.md, and produces machine-readable output.

**Read-only.** Hermes Clew never modifies files, never creates merge requests, never touches dependencies. It reads, reasons, and reports.

---

## Roadmap (Post-Hackathon)

- External URL scanning (GitHub repos, deployed URLs)
- MR-triggered scanning with report as MR comment
- Configurable score thresholds
- Historical score tracking across commits
- NLWeb and MCP compatibility checks
- Visual "human view vs agent view" comparison

---

## Hackathon

Built for the **GitLab Duo Agent Platform Challenge** (2026). Targets the Anthropic prize track.

- **Trigger:** User message in Duo Chat
- **Action:** Scans files, runs analysis, invokes Claude, posts report
- **Platform:** GitLab Duo Agent Platform
- **AI:** Anthropic Claude (via GitLab integration)

---

## License

MIT — see [LICENSE](LICENSE)

---

*Hermes Clew — Awareness, not judgment. Built for the agentic web.*
