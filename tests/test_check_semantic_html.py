"""Tests for scan.check_semantic_html"""

from pathlib import Path
import pytest
from scan.check_semantic_html import check_semantic_html

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_semantic_passes():
    files = [FIXTURES / "good_semantic.html"]
    result = check_semantic_html(files)

    assert result["category"] == "semantic_html"
    assert result["total"] > 0
    # Good file should pass most/all checks
    assert result["passed"] >= 4  # nav, main, headings, lists, form, interactives


def test_bad_div_soup_fails():
    files = [FIXTURES / "bad_div_soup.html"]
    result = check_semantic_html(files)

    assert result["category"] == "semantic_html"
    assert result["total"] > 0
    # Bad file should fail most checks
    assert result["passed"] <= 2

    # Should have findings about div-click handlers
    div_click_findings = [
        f for f in result["findings"]
        if f["check"] == "semantic_interactive_elements" and not f["passed"]
    ]
    assert len(div_click_findings) > 0


def test_good_react_component():
    files = [FIXTURES / "good_react_component.jsx"]
    result = check_semantic_html(files)
    assert result["passed"] >= 4


def test_bad_react_component():
    files = [FIXTURES / "bad_react_component.jsx"]
    result = check_semantic_html(files)
    assert result["passed"] <= 2


def test_empty_file(tmp_path):
    empty = tmp_path / "empty.html"
    empty.write_text("")
    result = check_semantic_html([empty])

    assert result["category"] == "semantic_html"
    assert result["total"] > 0


def test_findings_have_required_keys():
    files = [FIXTURES / "good_semantic.html"]
    result = check_semantic_html(files)

    for finding in result["findings"]:
        assert "check" in finding
        assert "passed" in finding
        assert "detail" in finding
