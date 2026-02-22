# AGENTS.md — Hermes Clew

## What This Project Is

Hermes Clew is a read-only developer tool that scans HTML, JSX, and TSX files in a repository and reports how well the application would perform in the agentic web — where AI agents, not humans, are the primary users of the internet.

## What This Project Does

- Scans HTML, JSX, and TSX source files for agent-readiness patterns
- Evaluates 6 categories: Semantic HTML, Form Accessibility, ARIA & Accessibility, Structured Data, Content in HTML, Link & Navigation Clarity
- Produces a machine-readable JSON report with raw findings
- Uses Claude (Anthropic) as a reasoning layer to interpret findings, catch false positives, and generate a plain-English report with an Agent Readiness Score (0-100)

## What This Project Does NOT Do

- Modify any files (read-only)
- Create merge requests
- Touch dependencies
- Store any data after scanning
- Access private repos or external services

## How to Use This Project

1. Ensure HTML/JSX/TSX files are in a GitLab repository
2. Trigger a scan via GitLab Duo Chat: "Scan this project"
3. Hermes Clew reads files, runs analysis, and posts a structured report

## Project Structure

- `scan/` — Python scan engine. Each `check_*.py` handles one category.
- `scan/scanner.py` — Entry point. Orchestrates checks, outputs JSON.
- `scan/report_prompt.py` — Builds the Claude reasoning prompt.
- `scan/file_finder.py` — Locates scannable files in the repo.
- `scan/scoring.py` — Applies category weights, computes total score.
- `tests/` — Unit tests and HTML/JSX fixtures.

## For AI Agents Interacting With This Repo

- The scan engine produces structured JSON output
- Report format is machine-readable markdown
- All files follow single-responsibility principle
- No side effects — every scan is stateless and independent

## Part of the Clew Suite

Hermes Clew is part of a collection of developer tools: Ariadne Clew, Janus Clew, Lumen Clew, Metis Clew, and Hermes Clew. Each serves a different aspect of code awareness.
