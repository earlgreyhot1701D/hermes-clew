"""Tests for scan.check_link_navigation"""

from pathlib import Path
import pytest
from scan.check_link_navigation import check_link_navigation

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_links_pass():
    files = [FIXTURES / "good_links.html"]
    result = check_link_navigation(files)

    assert result["category"] == "link_navigation"
    assert result["total"] == 3  # descriptive text, href, nav structure
    assert result["passed"] == 3


def test_bad_links_fail():
    files = [FIXTURES / "bad_links.html"]
    result = check_link_navigation(files)

    assert result["category"] == "link_navigation"
    assert result["total"] == 3
    assert result["passed"] <= 1

    # Should flag generic link text
    generic_findings = [
        f for f in result["findings"]
        if f["check"] == "descriptive_link_text" and not f["passed"]
    ]
    assert len(generic_findings) > 0


def test_no_links_returns_na():
    """Files with no anchor tags should return 0 total."""
    files = [FIXTURES / "bad_empty_shell.html"]
    result = check_link_navigation(files)

    assert result["total"] == 0


def test_empty_file(tmp_path):
    empty = tmp_path / "empty.html"
    empty.write_text("")
    result = check_link_navigation([empty])

    assert result["category"] == "link_navigation"
    assert result["total"] == 0


def test_findings_have_required_keys():
    files = [FIXTURES / "good_links.html"]
    result = check_link_navigation(files)

    for finding in result["findings"]:
        assert "check" in finding
        assert "passed" in finding
        assert "detail" in finding
