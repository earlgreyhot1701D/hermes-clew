"""
check_link_navigation.py — Category 6: Link & Navigation Clarity (Weight: 10%)

Checks for descriptive link text, proper href attributes, and consistent navigation structure.
Returns a dict with score, max, and detailed findings.

Detection: regex pattern matching on anchor tags and navigation elements.
"""

import re
from pathlib import Path
from typing import List, Dict

# Anchor tags
ANCHOR_PATTERN = re.compile(
    r"<a\b([^>]*)>(.*?)</a>",
    re.IGNORECASE | re.DOTALL,
)

# Generic/vague link text patterns (case-insensitive match against inner text)
GENERIC_LINK_TEXT = {
    "click here",
    "here",
    "learn more",
    "read more",
    "more",
    "link",
    "this",
    "go",
}

# href attribute
HREF_PATTERN = re.compile(r'\bhref\s*=\s*["\']([^"\']*)["\']', re.IGNORECASE)

# Anchor with onClick but no href (JS-only navigation)
ANCHOR_ONCLICK_NO_HREF = re.compile(
    r"<a\b(?![^>]*\bhref\s*=)[^>]*(onClick|onclick)\s*=",
    re.IGNORECASE,
)

# Navigation element with links
NAV_WITH_LINKS = re.compile(
    r"<nav\b[^>]*>.*?<a\b.*?</nav>",
    re.IGNORECASE | re.DOTALL,
)

# Non-functional hrefs
NONFUNCTIONAL_HREFS = {"#", "javascript:void(0)", "javascript:void(0);", "javascript:;"}


def _extract_text(html_fragment: str) -> str:
    """Strip HTML tags and get visible text."""
    text = re.sub(r"<[^>]+>", "", html_fragment)
    return text.strip()


def check_link_navigation(files: List[Path]) -> Dict:
    """Run all Category 6 checks across the given files.

    Checks:
    1. Links have descriptive text (not "click here", "learn more", etc.)
    2. Links have href attributes (not JS-only navigation)
    3. Navigation structure is consistent (<nav> with links)
    """
    findings = []
    total_checks = 0
    passed_checks = 0

    total_links = 0
    generic_text_links = 0
    links_without_href = 0
    links_with_nonfunctional_href = 0
    has_nav_with_links = False

    for filepath in files:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        fname = filepath.name

        # Check for <nav> containing links
        if NAV_WITH_LINKS.search(content):
            has_nav_with_links = True

        # Process each anchor tag
        for match in ANCHOR_PATTERN.finditer(content):
            total_links += 1
            attrs = match.group(1)
            inner_html = match.group(2)
            link_text = _extract_text(inner_html).lower()

            # Check 1: Generic link text
            if link_text in GENERIC_LINK_TEXT:
                generic_text_links += 1
                findings.append({
                    "check": "descriptive_link_text",
                    "passed": False,
                    "detail": f"{fname}: Link with generic text \"{link_text}\". Agents can't determine purpose.",
                    "file": fname,
                })

            # Check 2: href attribute
            href_match = HREF_PATTERN.search(attrs)
            if not href_match:
                links_without_href += 1
                findings.append({
                    "check": "link_has_href",
                    "passed": False,
                    "detail": f"{fname}: <a> tag without href attribute. Agents can't follow this link.",
                    "file": fname,
                })
            elif href_match.group(1).strip().lower() in NONFUNCTIONAL_HREFS:
                links_with_nonfunctional_href += 1
                findings.append({
                    "check": "link_has_href",
                    "passed": False,
                    "detail": f"{fname}: <a> tag with non-functional href=\"{href_match.group(1)}\". Agents treat this as a dead link.",
                    "file": fname,
                })

        # Also catch anchors with onClick but no href at all
        onclick_no_href = ANCHOR_ONCLICK_NO_HREF.findall(content)
        # These may overlap with the above; findings are deduplicated by Claude reasoning

    if total_links == 0:
        return {
            "category": "link_navigation",
            "passed": 0,
            "total": 0,
            "findings": [{
                "check": "links_present",
                "passed": True,
                "detail": "No anchor tags found in scanned files (nothing to check).",
            }],
        }

    # --- Aggregate checks ---

    # Check 1: Descriptive link text
    total_checks += 1
    if generic_text_links == 0:
        passed_checks += 1
        findings.append({
            "check": "descriptive_link_text",
            "passed": True,
            "detail": f"All {total_links} links have descriptive text.",
        })
    else:
        findings.append({
            "check": "descriptive_link_text",
            "passed": False,
            "detail": f"{generic_text_links} of {total_links} links use generic text (\"click here\", \"learn more\", etc.).",
        })

    # Check 2: Links have functional href
    total_checks += 1
    broken_links = links_without_href + links_with_nonfunctional_href
    if broken_links == 0:
        passed_checks += 1
        findings.append({
            "check": "link_has_href",
            "passed": True,
            "detail": f"All {total_links} links have functional href attributes.",
        })
    else:
        findings.append({
            "check": "link_has_href",
            "passed": False,
            "detail": f"{broken_links} of {total_links} links lack a functional href (missing or javascript:void).",
        })

    # Check 3: Navigation structure
    total_checks += 1
    if has_nav_with_links:
        passed_checks += 1
        findings.append({
            "check": "nav_structure",
            "passed": True,
            "detail": "Navigation uses <nav> element with links — consistent and agent-parseable.",
        })
    else:
        findings.append({
            "check": "nav_structure",
            "passed": False,
            "detail": "No <nav> element with links found. Navigation may be scattered in generic divs.",
        })

    return {
        "category": "link_navigation",
        "passed": passed_checks,
        "total": total_checks,
        "findings": findings,
    }
