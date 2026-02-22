"""Tests for scan.check_content_in_html"""

from pathlib import Path
import pytest
from scan.check_content_in_html import check_content_in_html

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_content_passes():
    files = [FIXTURES / "good_content.html"]
    result = check_content_in_html(files)

    assert result["category"] == "content_in_html"
    assert result["total"] == 3  # not_empty_shell, noscript, ssr_markers
    assert result["passed"] >= 2  # should pass shell + noscript + ssr


def test_bad_empty_shell_fails():
    files = [FIXTURES / "bad_empty_shell.html"]
    result = check_content_in_html(files)

    assert result["category"] == "content_in_html"
    assert result["total"] == 3

    # Should flag as empty shell
    shell_findings = [f for f in result["findings"] if f["check"] == "not_empty_shell" and not f["passed"]]
    assert len(shell_findings) > 0


def test_jsx_only_returns_na():
    files = [FIXTURES / "good_react_component.jsx"]
    result = check_content_in_html(files)

    assert result["total"] == 0


def test_empty_file(tmp_path):
    empty = tmp_path / "empty.html"
    empty.write_text("")
    result = check_content_in_html([empty])

    assert result["category"] == "content_in_html"


def test_advisory_findings_are_labeled():
    files = [FIXTURES / "good_content.html"]
    result = check_content_in_html(files)

    advisory = [f for f in result["findings"] if "ADVISORY" in f.get("detail", "")]
    assert len(advisory) > 0  # Should have at least one advisory finding
