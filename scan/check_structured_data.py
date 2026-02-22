"""
check_structured_data.py — Category 4: Structured Data (Weight: 15%)

Checks for Schema.org JSON-LD, Open Graph meta tags, title, and meta description.
Returns a dict with score, max, and detailed findings.

Detection: string search in HTML head sections.
"""

import re
from pathlib import Path
from typing import List, Dict

# Schema.org JSON-LD
JSONLD_PATTERN = re.compile(
    r'<script\b[^>]*type\s*=\s*["\']application/ld\+json["\'][^>]*>',
    re.IGNORECASE,
)

# Open Graph meta tags
OG_PATTERN = re.compile(
    r'<meta\b[^>]*property\s*=\s*["\']og:[^"\']+["\']',
    re.IGNORECASE,
)

# Title tag with content
TITLE_PATTERN = re.compile(
    r"<title\b[^>]*>(.+?)</title>",
    re.IGNORECASE | re.DOTALL,
)

# Meta description
META_DESC_PATTERN = re.compile(
    r'<meta\b[^>]*name\s*=\s*["\']description["\'][^>]*content\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)
# Also match reversed attribute order
META_DESC_PATTERN_ALT = re.compile(
    r'<meta\b[^>]*content\s*=\s*["\']([^"\']+)["\'][^>]*name\s*=\s*["\']description["\']',
    re.IGNORECASE,
)


def check_structured_data(files: List[Path]) -> Dict:
    """Run all Category 4 checks across the given files.

    Checks:
    1. Schema.org JSON-LD present
    2. Open Graph meta tags present
    3. Page has descriptive <title>
    4. Meta description present
    """
    findings = []
    total_checks = 0
    passed_checks = 0

    has_jsonld = False
    has_og_tags = False
    has_title = False
    has_meta_desc = False
    title_content = ""
    og_count = 0

    # Only check HTML files for structured data (JSX/TSX won't have <head> meta)
    html_files = [f for f in files if f.suffix.lower() == ".html"]

    if not html_files:
        # JSX/TSX only — structured data checks are not applicable
        return {
            "category": "structured_data",
            "passed": 0,
            "total": 0,
            "findings": [{
                "check": "structured_data_applicability",
                "passed": True,
                "detail": "No HTML files found. Structured data checks apply to HTML files with <head> sections. JSX/TSX components typically don't contain page-level metadata.",
            }],
        }

    for filepath in html_files:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        fname = filepath.name

        # Check 1: JSON-LD
        if JSONLD_PATTERN.search(content):
            has_jsonld = True

        # Check 2: OG tags
        og_matches = OG_PATTERN.findall(content)
        if og_matches:
            has_og_tags = True
            og_count += len(og_matches)

        # Check 3: Title
        title_match = TITLE_PATTERN.search(content)
        if title_match:
            title_text = title_match.group(1).strip()
            if title_text:
                has_title = True
                title_content = title_text

        # Check 4: Meta description
        if META_DESC_PATTERN.search(content) or META_DESC_PATTERN_ALT.search(content):
            has_meta_desc = True

    # --- Aggregate checks ---

    # Check 1: Schema.org JSON-LD
    total_checks += 1
    if has_jsonld:
        passed_checks += 1
        findings.append({
            "check": "schema_jsonld",
            "passed": True,
            "detail": "Schema.org JSON-LD structured data found.",
        })
    else:
        findings.append({
            "check": "schema_jsonld",
            "passed": False,
            "detail": "No Schema.org JSON-LD found. Adding structured data helps agents understand page content and purpose.",
        })

    # Check 2: Open Graph tags
    total_checks += 1
    if has_og_tags:
        passed_checks += 1
        findings.append({
            "check": "open_graph_tags",
            "passed": True,
            "detail": f"Open Graph meta tags found ({og_count} tags).",
        })
    else:
        findings.append({
            "check": "open_graph_tags",
            "passed": False,
            "detail": "No Open Graph meta tags found (og:title, og:description, etc.).",
        })

    # Check 3: Descriptive title
    total_checks += 1
    if has_title:
        passed_checks += 1
        findings.append({
            "check": "page_title",
            "passed": True,
            "detail": f"Descriptive <title> found: \"{title_content}\".",
        })
    else:
        findings.append({
            "check": "page_title",
            "passed": False,
            "detail": "No descriptive <title> found or title is empty.",
        })

    # Check 4: Meta description
    total_checks += 1
    if has_meta_desc:
        passed_checks += 1
        findings.append({
            "check": "meta_description",
            "passed": True,
            "detail": "Meta description tag found.",
        })
    else:
        findings.append({
            "check": "meta_description",
            "passed": False,
            "detail": "No <meta name=\"description\"> found. Agents use this to understand page purpose.",
        })

    return {
        "category": "structured_data",
        "passed": passed_checks,
        "total": total_checks,
        "findings": findings,
    }
