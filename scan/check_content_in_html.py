"""
check_content_in_html.py — Category 5: Content in HTML (Weight: 15%) — LOW CONFIDENCE ⚠️

Checks whether HTML files contain actual content vs. being empty SPA shells.
This category is inherently unreliable without fetching the deployed URL.
Only safe, high-confidence checks are scored. Everything else is Claude advisory.

Detection: string matching for shell patterns, noscript, SSR markers.
"""

import re
from pathlib import Path
from typing import List, Dict

# Empty shell detection: <div id="root"></div> + script tags, little else
ROOT_DIV_PATTERN = re.compile(
    r'<div\b[^>]*id\s*=\s*["\'](root|app|__next)["\'][^>]*>\s*</div>',
    re.IGNORECASE,
)

# Noscript fallback
NOSCRIPT_PATTERN = re.compile(r"<noscript\b", re.IGNORECASE)

# SSR framework markers
SSR_MARKERS = [
    "__NEXT_DATA__",         # Next.js
    "__NUXT__",              # Nuxt
    "data-astro",            # Astro
    "data-reactroot",        # React SSR
    "data-server-rendered",  # Vue SSR
    "gatsby-focus-wrapper",  # Gatsby
]

# Meaningful text content: paragraphs, headings with text
MEANINGFUL_CONTENT_PATTERN = re.compile(
    r"<(p|h[1-6]|li|td|th|blockquote|figcaption|dt|dd)\b[^>]*>[^<]{10,}",
    re.IGNORECASE,
)

# Script-only pattern: body contains almost nothing but script tags
SCRIPT_TAG_PATTERN = re.compile(r"<script\b", re.IGNORECASE)


def _is_empty_shell(content: str) -> bool:
    """Heuristic: is this HTML file essentially an empty SPA shell?

    An empty shell has a root div, one or more script tags,
    and very little other content in the body.
    """
    if not ROOT_DIV_PATTERN.search(content):
        return False

    # Extract body content
    body_match = re.search(r"<body\b[^>]*>(.*)</body>", content, re.IGNORECASE | re.DOTALL)
    if not body_match:
        return False

    body = body_match.group(1)

    # Remove script tags and their content
    body_no_scripts = re.sub(r"<script\b[^>]*>.*?</script>", "", body, flags=re.IGNORECASE | re.DOTALL)
    # Remove HTML tags
    text_only = re.sub(r"<[^>]+>", "", body_no_scripts).strip()

    # If remaining text is very short, it's a shell
    return len(text_only) < 50


def check_content_in_html(files: List[Path]) -> Dict:
    """Run all Category 5 checks across the given files.

    Safe checks (scored):
    1. HTML files are NOT empty root shells
    2. <noscript> fallback present
    3. SSR framework markers present

    Claude advisory (NOT scored — mentioned in findings for context):
    - Whether meaningful text content appears in source
    """
    findings = []
    total_checks = 0
    passed_checks = 0

    html_files = [f for f in files if f.suffix.lower() == ".html"]

    if not html_files:
        return {
            "category": "content_in_html",
            "passed": 0,
            "total": 0,
            "findings": [{
                "check": "content_applicability",
                "passed": True,
                "detail": "No HTML files found. Content-in-HTML checks apply to HTML entry points, not JSX/TSX components.",
            }],
        }

    shell_files = []
    non_shell_files = []
    has_noscript = False
    has_ssr_markers = False
    ssr_marker_found = ""
    files_with_content = 0

    for filepath in html_files:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        fname = filepath.name

        # Check 1: Empty shell?
        if _is_empty_shell(content):
            shell_files.append(fname)
        else:
            non_shell_files.append(fname)

        # Check 2: Noscript
        if NOSCRIPT_PATTERN.search(content):
            has_noscript = True

        # Check 3: SSR markers
        for marker in SSR_MARKERS:
            if marker in content:
                has_ssr_markers = True
                ssr_marker_found = marker
                break

        # Advisory: meaningful content
        meaningful_matches = MEANINGFUL_CONTENT_PATTERN.findall(content)
        if len(meaningful_matches) >= 3:
            files_with_content += 1

    # --- Aggregate checks ---

    # Check 1: Not empty shells
    total_checks += 1
    if not shell_files:
        passed_checks += 1
        findings.append({
            "check": "not_empty_shell",
            "passed": True,
            "detail": f"All {len(html_files)} HTML files contain content beyond a bare root div.",
        })
    elif shell_files and non_shell_files:
        findings.append({
            "check": "not_empty_shell",
            "passed": False,
            "detail": f"{len(shell_files)} HTML file(s) are empty SPA shells ({', '.join(shell_files)}). Agents see only a blank div.",
        })
    else:
        findings.append({
            "check": "not_empty_shell",
            "passed": False,
            "detail": f"All {len(shell_files)} HTML files are empty SPA shells. Agents cannot read any content without JavaScript execution.",
        })

    # Check 2: Noscript fallback
    total_checks += 1
    if has_noscript:
        passed_checks += 1
        findings.append({
            "check": "noscript_fallback",
            "passed": True,
            "detail": "<noscript> fallback found — provides content for non-JS environments.",
        })
    else:
        findings.append({
            "check": "noscript_fallback",
            "passed": False,
            "detail": "No <noscript> fallback found. If JavaScript fails to load, agents see nothing.",
        })

    # Check 3: SSR framework markers
    total_checks += 1
    if has_ssr_markers:
        passed_checks += 1
        findings.append({
            "check": "ssr_markers",
            "passed": True,
            "detail": f"SSR framework marker found ({ssr_marker_found}). Content is likely server-rendered.",
        })
    else:
        findings.append({
            "check": "ssr_markers",
            "passed": False,
            "detail": "No SSR framework markers found (Next.js, Nuxt, Astro, etc.). Content may only be available after JavaScript execution.",
        })

    # Advisory (NOT scored — included for Claude reasoning context)
    if files_with_content > 0:
        findings.append({
            "check": "meaningful_content_advisory",
            "passed": True,
            "detail": f"[ADVISORY — not scored] {files_with_content} of {len(html_files)} HTML files contain meaningful text content in source.",
        })
    else:
        findings.append({
            "check": "meaningful_content_advisory",
            "passed": False,
            "detail": "[ADVISORY — not scored] Limited meaningful text content found in HTML source. Content may be loaded dynamically via JavaScript.",
        })

    return {
        "category": "content_in_html",
        "passed": passed_checks,
        "total": total_checks,
        "findings": findings,
    }
