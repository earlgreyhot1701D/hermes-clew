"""
check_semantic_html.py — Category 1: Semantic HTML (Weight: 25%)

Checks whether files use semantic HTML elements that agents can identify by tag name.
Returns a dict with score, max, and detailed findings.

Detection: regex + string matching. NO AST parsing. NO judgment (that's Claude's job).
"""

import re
from pathlib import Path
from typing import List, Dict

# Patterns for div/span with click handlers (anti-pattern)
DIV_CLICK_PATTERN = re.compile(
    r"<(div|span)\b[^>]*(onClick|onclick|onPress)\s*=",
    re.IGNORECASE,
)

# Semantic interactive elements
BUTTON_PATTERN = re.compile(r"<button\b", re.IGNORECASE)
ANCHOR_PATTERN = re.compile(r"<a\b", re.IGNORECASE)
INPUT_PATTERN = re.compile(r"<input\b", re.IGNORECASE)
SELECT_PATTERN = re.compile(r"<select\b", re.IGNORECASE)
TEXTAREA_PATTERN = re.compile(r"<textarea\b", re.IGNORECASE)

NAV_PATTERN = re.compile(r"<nav\b", re.IGNORECASE)
MAIN_PATTERN = re.compile(r"<main\b", re.IGNORECASE)
FORM_PATTERN = re.compile(r"<form\b", re.IGNORECASE)

# Heading hierarchy
HEADING_PATTERN = re.compile(r"<h([1-6])\b", re.IGNORECASE)

# List elements
LIST_PATTERN = re.compile(r"<(ul|ol)\b", re.IGNORECASE)
LIST_ITEM_PATTERN = re.compile(r"<li\b", re.IGNORECASE)


def check_semantic_html(files: List[Path]) -> Dict:
    """Run all Category 1 checks across the given files.

    Checks:
    1. Interactive elements use <button>, <a>, <input>, <select>, <textarea> (not div/span with onClick)
    2. Navigation uses <nav>
    3. Main content uses <main>
    4. Headers use <h1>-<h6> with proper hierarchy
    5. Lists use <ul>, <ol>, <li>
    6. Forms use <form>
    """
    findings = []
    total_checks = 0
    passed_checks = 0

    has_any_interactive = False
    has_any_nav = False
    has_any_main = False
    has_any_headings = False
    has_any_lists = False
    has_any_forms = False

    total_div_click_count = 0
    total_semantic_interactive_count = 0

    for filepath in files:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        fname = filepath.name

        # Check 1: Interactive elements — semantic vs div-click
        div_clicks = len(DIV_CLICK_PATTERN.findall(content))
        semantic_interactives = (
            len(BUTTON_PATTERN.findall(content))
            + len(ANCHOR_PATTERN.findall(content))
            + len(INPUT_PATTERN.findall(content))
            + len(SELECT_PATTERN.findall(content))
            + len(TEXTAREA_PATTERN.findall(content))
        )
        total_div_click_count += div_clicks
        total_semantic_interactive_count += semantic_interactives

        if div_clicks > 0:
            findings.append({
                "check": "semantic_interactive_elements",
                "passed": False,
                "detail": f"{fname}: Found {div_clicks} div/span with click handlers instead of semantic elements.",
                "file": fname,
            })

        # Check 2: Navigation
        if NAV_PATTERN.search(content):
            has_any_nav = True

        # Check 3: Main content
        if MAIN_PATTERN.search(content):
            has_any_main = True

        # Check 4: Heading hierarchy
        headings = [int(m) for m in HEADING_PATTERN.findall(content)]
        if headings:
            has_any_headings = True
            # Check for skipped levels
            for i in range(len(headings) - 1):
                if headings[i + 1] > headings[i] + 1:
                    findings.append({
                        "check": "heading_hierarchy",
                        "passed": False,
                        "detail": f"{fname}: Heading level skips from h{headings[i]} to h{headings[i+1]}.",
                        "file": fname,
                    })

        # Check 5: Lists
        if LIST_PATTERN.search(content) and LIST_ITEM_PATTERN.search(content):
            has_any_lists = True

        # Check 6: Forms
        if FORM_PATTERN.search(content):
            has_any_forms = True

        if semantic_interactives > 0:
            has_any_interactive = True

    # --- Aggregate checks ---

    # Check 1: Interactive elements
    total_checks += 1
    if has_any_interactive and total_div_click_count == 0:
        passed_checks += 1
        findings.append({
            "check": "semantic_interactive_elements",
            "passed": True,
            "detail": f"All interactive elements use semantic tags. {total_semantic_interactive_count} found.",
        })
    elif has_any_interactive and total_div_click_count > 0:
        # Partial: has semantic AND div-clicks
        findings.append({
            "check": "semantic_interactive_elements",
            "passed": False,
            "detail": f"Mixed: {total_semantic_interactive_count} semantic elements but also {total_div_click_count} div/span with click handlers.",
        })
    elif not has_any_interactive and total_div_click_count > 0:
        findings.append({
            "check": "semantic_interactive_elements",
            "passed": False,
            "detail": f"No semantic interactive elements found. {total_div_click_count} div/span with click handlers detected.",
        })
    # If no interactives at all, mark as N/A (pass — nothing to flag)
    elif not has_any_interactive and total_div_click_count == 0:
        passed_checks += 1
        findings.append({
            "check": "semantic_interactive_elements",
            "passed": True,
            "detail": "No interactive elements found in scanned files (nothing to flag).",
        })

    # Check 2: Navigation uses <nav>
    total_checks += 1
    if has_any_nav:
        passed_checks += 1
        findings.append({
            "check": "nav_element",
            "passed": True,
            "detail": "Navigation uses <nav> element.",
        })
    else:
        findings.append({
            "check": "nav_element",
            "passed": False,
            "detail": "No <nav> element found. Navigation may be inside generic divs.",
        })

    # Check 3: Main content uses <main>
    total_checks += 1
    if has_any_main:
        passed_checks += 1
        findings.append({
            "check": "main_element",
            "passed": True,
            "detail": "Page uses <main> element for primary content.",
        })
    else:
        findings.append({
            "check": "main_element",
            "passed": False,
            "detail": "No <main> element found. Agents may struggle to identify primary content area.",
        })

    # Check 4: Heading hierarchy
    total_checks += 1
    hierarchy_issues = [f for f in findings if f["check"] == "heading_hierarchy" and not f["passed"]]
    if has_any_headings and not hierarchy_issues:
        passed_checks += 1
        findings.append({
            "check": "heading_hierarchy",
            "passed": True,
            "detail": "Heading hierarchy is properly nested.",
        })
    elif not has_any_headings:
        findings.append({
            "check": "heading_hierarchy",
            "passed": False,
            "detail": "No heading elements (h1-h6) found. Agents use headings to understand content structure.",
        })

    # Check 5: Lists use semantic elements
    total_checks += 1
    if has_any_lists:
        passed_checks += 1
        findings.append({
            "check": "list_elements",
            "passed": True,
            "detail": "Lists use semantic <ul>/<ol>/<li> elements.",
        })
    else:
        findings.append({
            "check": "list_elements",
            "passed": False,
            "detail": "No semantic list elements found. Lists may be styled divs.",
        })

    # Check 6: Forms use <form>
    total_checks += 1
    if has_any_forms:
        passed_checks += 1
        findings.append({
            "check": "form_element",
            "passed": True,
            "detail": "Forms use <form> element wrapper.",
        })
    else:
        findings.append({
            "check": "form_element",
            "passed": False,
            "detail": "No <form> element found. Form inputs may not be grouped for agents.",
        })

    return {
        "category": "semantic_html",
        "passed": passed_checks,
        "total": total_checks,
        "findings": findings,
    }
