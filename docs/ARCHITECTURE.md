# Hermes Clew — Architecture

Hermes Clew is a **hybrid “deterministic + LLM reasoning”** system for evaluating how navigable and understandable a web codebase is for AI agents.

The design intentionally separates **mechanical evidence collection** (repeatable, testable) from **interpretation and prioritization** (reasoning).

---

## Goals

- Produce a **deterministic scan** of HTML/JSX/TSX code for agent-readiness signals.
- Output a **structured JSON** artifact with findings and weighted scores.
- Use **LLM reasoning (GitLab Duo)** to:
  - reduce false positives/negatives,
  - prioritize fixes by impact,
  - explain *why* issues matter for agentic navigation,
  - produce a strict-format **Agent Readiness Report**.

---

## System Overview

```text
Developer pushes code
      |
      v
GitLab CI job: hermes_clew_scan
  - runs: python -m scan.scanner .
  - outputs: hermes_clew_scan_results.json (artifact)
      |
      v
Developer opens GitLab Duo Chat (Hermes Clew)
  - provides goal + scan JSON (authoritative input)
      |
      v
LLM reasoning layer (Duo / Claude)
  - interprets findings
  - prioritizes fixes
  - produces strict-format report
      |
      v
Hermes Clew — Agent Readiness Report (Markdown)
```

---

## Core Components

### 1) Deterministic Scan Engine (Python)

Location: `scan/`

Responsibilities:
- Discover relevant source files (`.html`, `.jsx`, `.tsx`) with safe filtering.
- Run 6 category checks (pattern-based, deterministic).
- Emit structured findings + computed scores.
- Produce stable output for CI artifacts and testing.

Primary entry point:
- `python -m scan.scanner <repo_path>`

Output:
- `hermes_clew_scan_results.json` (when run in CI)
- JSON structure includes `meta`, `overall`, and `categories`.

### 2) CI/CD Execution (Plan C)

Location: `.gitlab-ci.yml`

Responsibilities:
- Run unit tests.
- Run the deterministic scan job.
- Publish scan output as a downloadable **artifact**.

Why CI is critical:
- It provides a reliable execution environment on GitLab (no local setup required for judges).
- It creates an authoritative, repeatable input for the LLM reasoning layer.

### 3) LLM Reasoning Layer (GitLab Duo Agent + Flow)

Locations:
- `agents/` (agent configuration)
- `flows/` (flow configuration)

Responsibilities:
- Treat deterministic scan JSON as the **source of truth** when provided.
- Apply reasoning to:
  - interpret ambiguity,
  - identify likely false positives,
  - provide prioritized, actionable recommendations.
- Produce output in a strict report format (predictable for demos and judging).

Important constraint:
- Hermes Clew is **read-only**: it must not modify repository content.

---

## Scoring Model

Hermes Clew uses fixed weights (total 100):

| Category | Weight |
|---|---:|
| Semantic HTML | 25 |
| Form Accessibility | 20 |
| ARIA & Accessibility | 15 |
| Structured Data | 15 |
| Content in HTML | 15 |
| Link & Navigation | 10 |

The deterministic engine computes category points and a total score.
The LLM layer may *contextualize* results but should not invent evidence.

---

## Data Contracts

### Deterministic Output (JSON)
- Must be machine-readable.
- Must include per-category findings and score contributions.
- Must be suitable for CI artifacts and copy/paste into Duo chat.

### Final Output (Markdown Report)
- Must follow Hermes Clew’s strict report template.
- Must clearly state assessment mode:
  - **Structured Scan** (using JSON)
  - **Heuristic** (fallback when JSON isn’t available)

---

## Typical Workflow

1. **Push changes** → triggers GitLab pipeline.
2. Pipeline runs:
   - tests
   - deterministic scan job → produces `hermes_clew_scan_results.json` artifact
3. Open GitLab Duo Chat and request a report using the scan JSON.
4. Duo returns the strict-format **Agent Readiness Report**.
5. Iterate: fix issues → push → re-scan → updated report.

---

## Why This Architecture Wins (Hackathon Framing)

- **Deterministic grounding**: judges can verify evidence and repeat runs.
- **Agentic value**: LLM reasoning turns raw findings into prioritized action.
- **Trigger + action**: pipeline triggers on push; scan runs automatically; report can be generated quickly.
- **Safety**: read-only, no destructive actions, no “autofix” risks.

---

## Repository Map

```text
.
├── scan/                         # deterministic scan engine
├── tests/                        # unit tests + fixtures
├── agents/                       # Duo agent configuration
├── flows/                        # Duo flow configuration
├── .gitlab-ci.yml                # CI pipeline (tests + scan artifact)
└── docs/
    ├── PRD_HERMES_CLEW.md         # specification (source of truth)
    └── ARCHITECTURE.md            # this file
```
