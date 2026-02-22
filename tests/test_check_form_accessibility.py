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
