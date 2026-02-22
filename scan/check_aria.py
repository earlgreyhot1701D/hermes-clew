"""
check_aria.py — Category 3: ARIA & Accessibility Attributes (Weight: 15%)

Checks for role attributes, aria-live regions, alt text, and aria-label on icon-only buttons.
Returns a dict with score, max, and detailed findings.

Detection: regex + string matching. NO AST parsing.
"""

import re
from pathlib import Path
from typing import List, Dict

# Custom interactive components with event handlers but no role
# Match: div/span with onClick/onPress but WITHOUT a role attribute
DIV_HANDLER_PATTERN = re.compile(
    r"<(div|span)\b([^>]*)(onClick|onclick|onPress)\s*=([^>]*)>",
    re.IGNORECASE | re.DOTALL,
)

ROLE_ATTR_PATTERN = re.compile(r'\brole\s*=\s*["\']', re.IGNORECASE)

# aria-live regions
ARIA_LIVE_PATTERN = re.compile(r'\baria-live\s*=\s*["\']', re.IGNORECASE)

# Images
IMG_PATTERN = re.compile(r"<img\b([^>]*)\/?>", re.IGNORECASE | re.DOTALL)
ALT_ATTR_PATTERN = re.compile(r'\balt\s*=\s*["\']', re.IGNORECASE)

# Icon-only buttons: buttons containing only SVG or <img> with no text content
# We detect buttons/elements that contain svg or img child but check for aria-label
BUTTON_WITH_SVG_PATTERN = re.compile(
    r"<button\b([^>]*)>(\s*<(?:svg|img)\b[^>]*>.*?)\s*</button>",
    re.IGNORECASE | re.DOTALL,
)

# Also catch div/span icon buttons
DIV_ICON_PATTERN = re.compile(
    r"<(div|span)\b([^>]*(?:onClick|onclick|onPress)[^>]*)>\s*<(?:svg|img)\b[^>]*>.*?</\1>",
    re.IGNORECASE | re.DOTALL,
)

ARIA_LABEL_PATTERN = re.compile(
    r'\baria-label\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)


def check_aria(files: List[Path]) -> Dict:
    """Run all Category 3 checks across the given files.

    Checks:
    1. Custom interactive components have role attribute
    2. Dynamic content areas have aria-live
    3. Images have alt text
    4. Icon-only buttons have aria-label
    """
    findings = []
    total_checks = 0
    passed_checks = 0

    custom_interactives_without_role = 0
    custom_interactives_total = 0
    has_aria_live = False
    images_total = 0
    images_with_alt = 0
    icon_buttons_total = 0
    icon_buttons_with_label = 0

    for filepath in files:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        fname = filepath.name

        # Check 1: Custom interactive divs/spans with handlers — do they have role?
        for match in DIV_HANDLER_PATTERN.finditer(content):
            custom_interactives_total += 1
            full_attrs = match.group(2) + match.group(4)
            if not ROLE_ATTR_PATTERN.search(full_attrs):
                custom_interactives_without_role += 1
                findings.append({
                    "check": "custom_widget_role",
                    "passed": False,
                    "detail": f"{fname}: <{match.group(1)}> with click handler lacks role attribute.",
                    "file": fname,
                })

        # Check 2: aria-live regions
        if ARIA_LIVE_PATTERN.search(content):
            has_aria_live = True

        # Check 3: Images with alt text
        for match in IMG_PATTERN.finditer(content):
            images_total += 1
            attrs = match.group(1)
            if ALT_ATTR_PATTERN.search(attrs):
                images_with_alt += 1
            else:
                findings.append({
                    "check": "image_alt_text",
                    "passed": False,
                    "detail": f"{fname}: <img> missing alt attribute.",
                    "file": fname,
                })

        # Check 4: Icon-only buttons with aria-label
        for match in BUTTON_WITH_SVG_PATTERN.finditer(content):
            icon_buttons_total += 1
            attrs = match.group(1)
            if ARIA_LABEL_PATTERN.search(attrs):
                icon_buttons_with_label += 1
            else:
                findings.append({
                    "check": "icon_button_label",
                    "passed": False,
                    "detail": f"{fname}: Icon-only <button> (contains SVG/img) lacks aria-label.",
                    "file": fname,
                })

        for match in DIV_ICON_PATTERN.finditer(content):
            icon_buttons_total += 1
            attrs = match.group(2)
            if ARIA_LABEL_PATTERN.search(attrs):
                icon_buttons_with_label += 1
            else:
                findings.append({
                    "check": "icon_button_label",
                    "passed": False,
                    "detail": f"{fname}: Icon-only <{match.group(1)}> with handler lacks aria-label.",
                    "file": fname,
                })

    # --- Aggregate checks ---

    # Check 1: Role attributes on custom interactives
    total_checks += 1
    if custom_interactives_total == 0:
        passed_checks += 1
        findings.append({
            "check": "custom_widget_role",
            "passed": True,
            "detail": "No custom interactive div/span widgets found (nothing to flag).",
        })
    elif custom_interactives_without_role == 0:
        passed_checks += 1
        findings.append({
            "check": "custom_widget_role",
            "passed": True,
            "detail": f"All {custom_interactives_total} custom interactive elements have role attributes.",
        })
    # else: individual file-level findings already appended above

    # Check 2: aria-live
    total_checks += 1
    if has_aria_live:
        passed_checks += 1
        findings.append({
            "check": "aria_live_regions",
            "passed": True,
            "detail": "aria-live regions found for dynamic content announcements.",
        })
    else:
        findings.append({
            "check": "aria_live_regions",
            "passed": False,
            "detail": "No aria-live regions found. Dynamic content updates may be invisible to agents.",
        })

    # Check 3: Image alt text
    total_checks += 1
    if images_total == 0:
        passed_checks += 1
        findings.append({
            "check": "image_alt_text",
            "passed": True,
            "detail": "No images found in scanned files (nothing to check).",
        })
    elif images_with_alt >= images_total:
        passed_checks += 1
        findings.append({
            "check": "image_alt_text",
            "passed": True,
            "detail": f"All {images_total} images have alt attributes.",
        })
    # else: individual file-level findings already appended above

    # Check 4: Icon-only button labels
    total_checks += 1
    if icon_buttons_total == 0:
        passed_checks += 1
        findings.append({
            "check": "icon_button_label",
            "passed": True,
            "detail": "No icon-only buttons found (nothing to check).",
        })
    elif icon_buttons_with_label >= icon_buttons_total:
        passed_checks += 1
        findings.append({
            "check": "icon_button_label",
            "passed": True,
            "detail": f"All {icon_buttons_total} icon-only buttons have aria-label.",
        })
    # else: individual file-level findings already appended above

    return {
        "category": "aria",
        "passed": passed_checks,
        "total": total_checks,
        "findings": findings,
    }
