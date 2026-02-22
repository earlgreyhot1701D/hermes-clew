"""Tests for scan.check_aria"""

from pathlib import Path
import pytest
from scan.check_aria import check_aria

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_aria_passes():
    files = [FIXTURES / "good_aria.html"]
    result = check_aria(files)

    assert result["category"] == "aria"
    assert result["total"] > 0
    assert result["passed"] >= 3  # roles, aria-live, alt text, icon labels


def test_bad_aria_fails():
    files = [FIXTURES / "bad_aria.html"]
    result = check_aria(files)

    assert result["category"] == "aria"
    assert result["total"] > 0
    assert result["passed"] <= 1

    # Should flag missing alt text
    alt_findings = [f for f in result["findings"] if f["check"] == "image_alt_text" and not f["passed"]]
    assert len(alt_findings) > 0


def test_empty_file(tmp_path):
    empty = tmp_path / "empty.html"
    empty.write_text("")
    result = check_aria([empty])

    assert result["category"] == "aria"
    assert result["total"] == 4
    # Empty file: no custom widgets (pass), no aria-live (fail),
    # no images (pass), no icon buttons (pass) = 3/4
    assert result["passed"] == 3


def test_findings_have_required_keys():
    files = [FIXTURES / "good_aria.html"]
    result = check_aria(files)

    for finding in result["findings"]:
        assert "check" in finding
        assert "passed" in finding
        assert "detail" in finding
