"""
report_prompt.py — Builds the Claude reasoning prompt from raw scan JSON.

This module builds a prompt string. It does NOT call Claude.
The prompt is sent to Claude by the GitLab Duo agent layer (Layer 1)
when the user pastes deterministic scan JSON into Duo Chat.

The report format here MUST match the format in agents/agent.yml exactly.
If you change one, change both.
"""

import json
from typing import Dict

REASONING_PROMPT_TEMPLATE = """You are the reasoning layer of Hermes Clew, an agent-readiness scanner.

You have received raw scan findings from a mechanical Python scanner. The scanner
counts patterns — it does not understand context. Your job is to reason about
these findings and produce a defensible, nuanced assessment.

PHILOSOPHY: "Awareness, not judgment." Explain problems like a knowledgeable
colleague pointing things out over coffee. Tell developers WHY an agent would
struggle, not just WHAT is wrong. Suggest the minimal fix. Never be preachy.

## Project Summary
- **Project:** {project_name}
- **Files Scanned:** {file_count} HTML/JSX/TSX files
- **Raw Score:** {raw_score}/100
- **Assessment Mode:** Deterministic Scan + Claude Reasoning
- **Confidence:** High

## Raw Findings
```json
{raw_findings_json}
```

## Category Breakdown
{category_breakdown}

## Your Tasks

1. REVIEW each category's findings for false positives. Common false positives:
   - React component libraries using custom components (e.g., <Button>) that
     render to semantic HTML at build time — don't flag as div-soup
   - CSS-in-JS frameworks producing div wrappers for styling, not interactivity
   - Data visualization libraries (D3, Recharts) using many divs for chart
     containers — these aren't interactive elements
   - SPAs using client-side routing (React Router, Next.js Link) — href-less
     links may be intentional
   - JSX/TSX files are parsed heuristically, NOT via AST. Interpret JSX/TSX
     findings with extra caution.
   When you suspect a false positive, note it in the report rather than
   silently adjusting the score.

2. ASSESS severity. Not all failures are equal:
   - A missing <button> on a checkout CTA is CRITICAL
   - A missing alt on a decorative background image is MINOR
   - Missing Schema.org on a personal portfolio is LESS URGENT than on e-commerce
   - A form without labels on a login page is CRITICAL (agents fill forms constantly)
   - Missing aria-live on a static section is MINOR

3. IDENTIFY the top 3 highest-impact fixes. Rank by: smallest code change
   that produces the biggest score improvement.

4. If you adjust the raw score, explain why in ONE sentence. Otherwise use
   the raw score as-is.

5. GENERATE the report using EXACTLY this markdown structure (do not deviate):

---

# Hermes Clew — Agent Readiness Report

**Project:** {project_name}
**Files Scanned:** {file_count} HTML/JSX/TSX files
**Scan Date:** {scan_date}
**Assessment Mode:** Deterministic Scan + Claude Reasoning
**Confidence:** High

---

## Overall Score: [SCORE]/100 — [RATING]

Use these EXACT rating labels:
- 80-100: Agent-Ready
- 60-79: Partially Ready
- 40-59: Agent-Challenged
- 0-39: Agent-Invisible

| Category | Score | Status | Notes |
|----------|------:|--------|-------|
| Semantic HTML | [earned]/25 | [status] | [brief note] |
| Form Accessibility | [earned]/20 | [status] | [brief note] |
| ARIA & Accessibility | [earned]/15 | [status] | [brief note] |
| Structured Data | [earned]/15 | [status] | [brief note] |
| Content in HTML | [earned]/15 | [status] | [brief note] |
| Link & Navigation | [earned]/10 | [status] | [brief note] |

Use these status labels:
- 80-100% of category points earned: ✅ Strong
- 50-79%: ⚠️ Needs Work
- 0-49%: ❌ Weak

[If you adjusted the raw score, explain why in one sentence here.]

---

## What's Working
[2-3 specific positives, referencing actual file names and patterns from the findings]

## What Agents Struggle With
[Top 3 issues. For each: what's wrong, WHY an agent struggles with it,
and a 1-3 line generic fix example. Include estimated score improvement.]

## Suggested Fixes (Smallest Changes, Biggest Impact)
[Ranked by impact. Include effort estimate and score improvement for each.]

---

## Confidence Notes
[Any limitations, false positive suspicions, or caveats about the assessment]

---

*Hermes Clew — Awareness, not judgment. Built for the agentic web.*

## Rules
- The category scores from the deterministic scan are AUTHORITATIVE. Use them.
- Do NOT reproduce source code from the scanned files in the report.
- Reference file names and describe patterns only.
- Keep fix suggestions to 1-3 lines of GENERIC example code (not copied from their files).
- If Category 5 (Content in HTML) findings include [ADVISORY] items, mention them
  as context but do NOT include them in the score.
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