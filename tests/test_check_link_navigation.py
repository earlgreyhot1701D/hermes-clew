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


def test_jsx_dynamic_href_recognized(tmp_path):
    """JSX href={variable} should be recognized as a valid href."""
    f = tmp_path / "links.jsx"
    f.write_text(
        '<nav>\n'
        '  <a href={item.url}>Product page</a>\n'
        '  <a href={`/orders/${order.id}`}>View order</a>\n'
        '</nav>\n'
    )
    result = check_link_navigation([f])
    href_findings = [f for f in result["findings"] if f["check"] == "link_has_href" and not f["passed"]]
    # Neither link should be flagged as missing href
    per_file = [f for f in href_findings if "file" in f]
    assert len(per_file) == 0, "JSX href={} should not be flagged as missing"


def test_substring_generic_link_text(tmp_path):
    """Generic text like 'Click Here for Details' should be caught by substring match."""
    f = tmp_path / "links.html"
    f.write_text(
        '<nav>\n'
        '  <a href="/a">Click Here for Details</a>\n'
        '  <a href="/b">Learn More About Pricing</a>\n'
        '  <a href="/c">Actual Descriptive Link</a>\n'
        '</nav>\n'
    )
    result = check_link_navigation([f])
    generic_per_file = [
        f for f in result["findings"]
        if f["check"] == "descriptive_link_text" and not f["passed"] and "file" in f
    ]
    assert len(generic_per_file) == 2, "Should catch 'Click Here for...' and 'Learn More About...'"
