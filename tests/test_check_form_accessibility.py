"""Tests for scan.check_form_accessibility"""

from pathlib import Path
import pytest
from scan.check_form_accessibility import check_form_accessibility

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_form_passes():
    files = [FIXTURES / "good_form.html"]
    result = check_form_accessibility(files)

    assert result["category"] == "form_accessibility"
    assert result["total"] > 0
    assert result["passed"] >= 4  # labels, types, names, submit, required


def test_bad_form_fails():
    files = [FIXTURES / "bad_form.html"]
    result = check_form_accessibility(files)

    assert result["category"] == "form_accessibility"
    # Bad form should fail most checks
    assert result["passed"] <= 2


def test_no_forms_returns_zero_total():
    """Files with no form inputs should return 0 total (N/A)."""
    files = [FIXTURES / "good_links.html"]  # This file has no forms
    result = check_form_accessibility(files)

    assert result["total"] == 0


def test_empty_file(tmp_path):
    empty = tmp_path / "empty.html"
    empty.write_text("")
    result = check_form_accessibility([empty])

    assert result["category"] == "form_accessibility"
    assert result["total"] == 0


def test_findings_have_required_keys():
    files = [FIXTURES / "good_form.html"]
    result = check_form_accessibility(files)

    for finding in result["findings"]:
        assert "check" in finding
        assert "passed" in finding
        assert "detail" in finding


def test_jsx_htmlfor_recognized(tmp_path):
    """JSX htmlFor attribute should be recognized as a label association."""
    f = tmp_path / "form.jsx"
    f.write_text(
        '<form>\n'
        '  <label htmlFor="email">Email</label>\n'
        '  <input type="email" id="email" name="email" required />\n'
        '  <button type="submit">Submit</button>\n'
        '</form>\n'
    )
    result = check_form_accessibility([f])
    label_finding = [f for f in result["findings"] if f["check"] == "input_labels"]
    assert any(f["passed"] for f in label_finding), "htmlFor should be recognized as label"


def test_no_cross_file_wrapped_label(tmp_path):
    """A <label> in file A should not match an <input> in file B."""
    file_a = tmp_path / "a.html"
    file_a.write_text(
        '<form>\n'
        '  <label>Name\n'  # label opens in file A — no closing </label> with input
        '</form>\n'
    )
    file_b = tmp_path / "b.html"
    file_b.write_text(
        '<form>\n'
        '  <input type="text" name="user">\n'  # input in file B — no wrapping label
        '  </label>\n'
        '  <button type="submit">Go</button>\n'
        '</form>\n'
    )
    result = check_form_accessibility([file_a, file_b])
    label_finding = [f for f in result["findings"] if f["check"] == "input_labels"]
    # The input in file B has no label — should NOT be counted as labeled
    assert any(not f["passed"] for f in label_finding), "Cross-file label match should not happen"
