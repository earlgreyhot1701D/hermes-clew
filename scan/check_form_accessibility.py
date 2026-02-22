"""
check_form_accessibility.py — Category 2: Form Accessibility (Weight: 20%)

Checks whether form elements are properly labeled and identifiable by agents.
Returns a dict with score, max, and detailed findings.

Detection: regex + string matching. NO AST parsing.
"""

import re
from pathlib import Path
from typing import List, Dict

# Find all input elements (self-closing or not)
INPUT_PATTERN = re.compile(
    r"<input\b([^>]*)\/?>",
    re.IGNORECASE | re.DOTALL,
)

TEXTAREA_PATTERN = re.compile(
    r"<textarea\b([^>]*)>",
    re.IGNORECASE | re.DOTALL,
)

SELECT_PATTERN = re.compile(
    r"<select\b([^>]*)>",
    re.IGNORECASE | re.DOTALL,
)

# Label patterns (matches both HTML for= and JSX htmlFor=)
LABEL_FOR_PATTERN = re.compile(
    r'<label\b[^>]*\b(?:html[Ff]or|for)\s*=\s*["\']([^"\']+)["\']',
    re.IGNORECASE,
)

# Wrapping label: <label>...<input>...</label>
LABEL_WRAP_PATTERN = re.compile(
    r"<label\b[^>]*>.*?<(input|textarea|select)\b.*?</label>",
    re.IGNORECASE | re.DOTALL,
)

# Attribute extraction helpers
def _get_attr(attrs_str: str, attr_name: str) -> str | None:
    """Extract an attribute value from an element's attribute string."""
    match = re.search(
        rf'\b{attr_name}\s*=\s*["\']([^"\']*)["\']',
        attrs_str,
        re.IGNORECASE,
    )
    return match.group(1) if match else None


def _has_attr(attrs_str: str, attr_name: str) -> bool:
    """Check if an attribute exists (even without a value)."""
    return bool(re.search(rf"\b{attr_name}\b", attrs_str, re.IGNORECASE))


# Submit button patterns
SUBMIT_BUTTON_PATTERN = re.compile(
    r'<button\b[^>]*\btype\s*=\s*["\']submit["\']',
    re.IGNORECASE,
)

INPUT_SUBMIT_PATTERN = re.compile(
    r'<input\b[^>]*\btype\s*=\s*["\']submit["\']',
    re.IGNORECASE,
)

# A <button> without an explicit type defaults to submit inside a form
BUTTON_DEFAULT_SUBMIT = re.compile(
    r"<button\b(?![^>]*\btype\s*=)",
    re.IGNORECASE,
)

# Hidden/submit/button inputs we should skip when checking labels
SKIP_INPUT_TYPES = {"hidden", "submit", "button", "reset", "image"}


def check_form_accessibility(files: List[Path]) -> Dict:
    """Run all Category 2 checks across the given files.

    Checks:
    1. Every <input> has an associated <label> (via for/id or wrapping)
    2. Inputs have type attribute
    3. Inputs have name attribute
    4. Submit buttons exist and are identifiable
    5. Required fields are marked with required or aria-required
    """
    findings = []
    total_checks = 0
    passed_checks = 0

    all_inputs_count = 0
    labeled_inputs = 0
    typed_inputs = 0
    named_inputs = 0
    inputs_with_required_attr = 0
    inputs_needing_required = 0  # inputs that have required or aria-required

    has_any_form_inputs = False
    has_submit_mechanism = False
    total_wrapped_count = 0

    for filepath in files:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        fname = filepath.name

        # Collect all label[for] ids in this file
        label_for_ids = set(LABEL_FOR_PATTERN.findall(content))

        # Find wrapping labels per-file (avoid cross-file false positives)
        total_wrapped_count += len(LABEL_WRAP_PATTERN.findall(content))

        # Check submit mechanisms
        if (SUBMIT_BUTTON_PATTERN.search(content)
                or INPUT_SUBMIT_PATTERN.search(content)
                or BUTTON_DEFAULT_SUBMIT.search(content)):
            has_submit_mechanism = True

        # Process each <input>
        for match in INPUT_PATTERN.finditer(content):
            attrs = match.group(1)
            input_type = _get_attr(attrs, "type") or "text"

            # Skip hidden/submit/button/reset/image — not user-fillable
            if input_type.lower() in SKIP_INPUT_TYPES:
                continue

            has_any_form_inputs = True
            all_inputs_count += 1

            # Check: has type attribute?
            if _has_attr(attrs, "type"):
                typed_inputs += 1

            # Check: has name attribute?
            if _has_attr(attrs, "name"):
                named_inputs += 1

            # Check: has associated label?
            input_id = _get_attr(attrs, "id")
            if input_id and input_id in label_for_ids:
                labeled_inputs += 1
            elif _has_attr(attrs, "aria-label") or _has_attr(attrs, "aria-labelledby"):
                labeled_inputs += 1
            # Note: wrapping labels are harder to match per-input with regex,
            # we count them as a bulk check below.

            # Check: required marking
            if _has_attr(attrs, "required") or _has_attr(attrs, "aria-required"):
                inputs_with_required_attr += 1

        # Process <textarea>
        for match in TEXTAREA_PATTERN.finditer(content):
            attrs = match.group(1)
            has_any_form_inputs = True
            all_inputs_count += 1
            # name check
            if _has_attr(attrs, "name"):
                named_inputs += 1
            typed_inputs += 1  # textarea is inherently typed
            # label check
            input_id = _get_attr(attrs, "id")
            if input_id and input_id in label_for_ids:
                labeled_inputs += 1
            elif _has_attr(attrs, "aria-label") or _has_attr(attrs, "aria-labelledby"):
                labeled_inputs += 1

            if _has_attr(attrs, "required") or _has_attr(attrs, "aria-required"):
                inputs_with_required_attr += 1

        # Process <select>
        for match in SELECT_PATTERN.finditer(content):
            attrs = match.group(1)
            has_any_form_inputs = True
            all_inputs_count += 1
            if _has_attr(attrs, "name"):
                named_inputs += 1
            typed_inputs += 1  # select is inherently typed
            input_id = _get_attr(attrs, "id")
            if input_id and input_id in label_for_ids:
                labeled_inputs += 1
            elif _has_attr(attrs, "aria-label") or _has_attr(attrs, "aria-labelledby"):
                labeled_inputs += 1

            if _has_attr(attrs, "required") or _has_attr(attrs, "aria-required"):
                inputs_with_required_attr += 1

    # Don't double-count: wrapped labels supplement for/id labels
    remaining_unlabeled = all_inputs_count - labeled_inputs
    if remaining_unlabeled > 0 and total_wrapped_count > 0:
        additionally_labeled = min(remaining_unlabeled, total_wrapped_count)
        labeled_inputs += additionally_labeled

    # --- Aggregate checks ---

    if not has_any_form_inputs:
        # No form inputs found — all checks pass trivially
        return {
            "category": "form_accessibility",
            "passed": 0,
            "total": 0,
            "findings": [{
                "check": "form_inputs_present",
                "passed": True,
                "detail": "No form input elements found in scanned files (nothing to check).",
            }],
        }

    # Check 1: Labels
    total_checks += 1
    if all_inputs_count > 0 and labeled_inputs >= all_inputs_count:
        passed_checks += 1
        findings.append({
            "check": "input_labels",
            "passed": True,
            "detail": f"All {all_inputs_count} input elements have associated labels.",
        })
    else:
        unlabeled = all_inputs_count - labeled_inputs
        findings.append({
            "check": "input_labels",
            "passed": False,
            "detail": f"{unlabeled} of {all_inputs_count} inputs lack an associated <label> (via for/id, wrapping, or aria-label).",
        })

    # Check 2: Type attributes
    total_checks += 1
    if typed_inputs >= all_inputs_count:
        passed_checks += 1
        findings.append({
            "check": "input_types",
            "passed": True,
            "detail": f"All {all_inputs_count} inputs have explicit type attributes.",
        })
    else:
        untyped = all_inputs_count - typed_inputs
        findings.append({
            "check": "input_types",
            "passed": False,
            "detail": f"{untyped} of {all_inputs_count} inputs are missing a type attribute (defaults to 'text').",
        })

    # Check 3: Name attributes
    total_checks += 1
    if named_inputs >= all_inputs_count:
        passed_checks += 1
        findings.append({
            "check": "input_names",
            "passed": True,
            "detail": f"All {all_inputs_count} inputs have name attributes.",
        })
    else:
        unnamed = all_inputs_count - named_inputs
        findings.append({
            "check": "input_names",
            "passed": False,
            "detail": f"{unnamed} of {all_inputs_count} inputs are missing a name attribute. Agents use name to identify fields.",
        })

    # Check 4: Submit mechanism
    total_checks += 1
    if has_submit_mechanism:
        passed_checks += 1
        findings.append({
            "check": "submit_button",
            "passed": True,
            "detail": "Identifiable submit mechanism found (button[type=submit] or input[type=submit]).",
        })
    else:
        findings.append({
            "check": "submit_button",
            "passed": False,
            "detail": "No identifiable submit button found. Agents need <button type='submit'> or <input type='submit'>.",
        })

    # Check 5: Required fields marked
    total_checks += 1
    if inputs_with_required_attr > 0:
        passed_checks += 1
        findings.append({
            "check": "required_fields",
            "passed": True,
            "detail": f"{inputs_with_required_attr} inputs marked as required (via required or aria-required).",
        })
    else:
        findings.append({
            "check": "required_fields",
            "passed": False,
            "detail": "No inputs are marked with required or aria-required. Agents can't determine which fields are mandatory.",
        })

    return {
        "category": "form_accessibility",
        "passed": passed_checks,
        "total": total_checks,
        "findings": findings,
    }
