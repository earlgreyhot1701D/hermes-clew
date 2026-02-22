"""
report_prompt.py — Builds the Claude reasoning prompt from raw scan JSON.

This module builds a prompt string. It does NOT call Claude.
The prompt is sent to Claude by the GitLab Duo agent layer (Layer 1).
"""

import json
from typing import Dict

REASONING_PROMPT_TEMPLATE = """You are the reasoning layer of Hermes Clew, an agent-readiness scanner.

You have received raw scan findings from a mechanical Python scanner. The scanner counts patterns — it does not understand context. Your job is to reason about these findings and produce a defensible, nuanced assessment.

## Project Summary
- **Project:** {project_name}
- **Files Scanned:** {file_count} HTML/JSX/TSX files
- **Raw Score:** {raw_score}/100

## Raw Findings
```json
{raw_findings_json}
```

## Category Breakdown
{category_breakdown}

## Your Tasks

1. REVIEW each category's findings for false positives. Common false positives:
   - React component libraries that use custom components (e.g., <Button>) that render to semantic HTML at build time
   - CSS-in-JS frameworks that produce div wrappers for styling but don't affect interactivity
   - Data visualization libraries that use many divs for chart containers
   - SPAs that use client-side routing (React Router, etc.) — href-less links may be intentional
   - JSX/TSX files are parsed heuristically, NOT via AST. Interpret JSX/TSX findings with extra context.

2. ASSESS severity. Not all failures are equal:
   - A missing <button> on a checkout CTA is critical
   - A missing alt on a decorative background is minor
   - Missing Schema.org on a personal portfolio is less urgent than on an e-commerce site

3. IDENTIFY the top 3 highest-impact fixes. Rank by: smallest code change that produces the biggest score improvement.

4. GENERATE the report using EXACTLY this markdown structure:

---

# Hermes Clew — Agent Readiness Report

**Project:** {project_name}
**Files Scanned:** {file_count} HTML/JSX/TSX files
**Scan Date:** {scan_date}

---

## Overall Score: [SCORE]/100 — [RATING]

| Category | Score | Status |
|----------|-------|--------|
| Semantic HTML | [earned]/25 | [status] |
| Form Accessibility | [earned]/20 | [status] |
| ARIA & Accessibility | [earned]/15 | [status] |
| Structured Data | [earned]/15 | [status] |
| Content in HTML | [earned]/15 | [status] |
| Link & Navigation | [earned]/10 | [status] |

[If you adjusted the raw score, explain why in one sentence here.]

---

## What's Working
[2-3 specific positives, referencing actual files/patterns from the findings]

## What Agents Struggle With
[Top 3 issues with WHY from the agent's perspective, and a concrete fix example for each]

## Suggested Fixes (Smallest Changes, Biggest Impact)
[Ranked by impact. Include estimated score improvement for each fix.]

---

*Hermes Clew — Awareness, not judgment. Built for the agentic web.*

---

5. If you adjust the raw score, explain why in one sentence.

## Tone
Friendly, educational, zero judgment. Like a knowledgeable colleague pointing things out over coffee. Use the phrase "awareness, not judgment" if it fits naturally. Never be preachy.

## Rules
- Do NOT reproduce source code from the scanned files in the report.
- Reference file names and describe patterns only.
- Keep fix suggestions to 1-3 lines of example code maximum (generic examples, not copied from their files).
- If Category 5 (Content in HTML) findings include [ADVISORY] items, mention them as context but do NOT include them in the score.
"""


def build_reasoning_prompt(
    scan_result: Dict,
    project_name: str = "Unknown Project",
    scan_date: str = "",
) -> str:
    """Build the Claude reasoning prompt from raw scan output.

    Args:
        scan_result: Output from scanner.run_scan()
        project_name: Name of the project being scanned
        scan_date: ISO date string of scan time

    Returns:
        Prompt string ready to send to Claude.
    """
    from scan.scoring import get_score_rating, get_category_breakdown

    raw_score = scan_result.get("total_score", 0)
    file_count = scan_result.get("file_count", 0)
    categories = scan_result.get("categories", {})

    # Build category breakdown text
    breakdown = get_category_breakdown(categories)
    breakdown_lines = []
    for cat_name, info in breakdown.items():
        display_name = cat_name.replace("_", " ").title()
        breakdown_lines.append(
            f"- **{display_name}:** {info['earned']}/{info['max']} — "
            f"{info['passed']}/{info['total']} checks passed — {info['status']}"
        )
    category_breakdown_text = "\n".join(breakdown_lines)

    # Build findings JSON (only the findings arrays, not full results)
    findings_for_prompt = {}
    for cat_name, cat_data in categories.items():
        findings_for_prompt[cat_name] = cat_data.get("findings", [])

    raw_findings_json = json.dumps(findings_for_prompt, indent=2)

    prompt = REASONING_PROMPT_TEMPLATE.format(
        project_name=project_name,
        file_count=file_count,
        raw_score=raw_score,
        raw_findings_json=raw_findings_json,
        category_breakdown=category_breakdown_text,
        scan_date=scan_date or "N/A",
    )

    return prompt
