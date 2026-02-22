"""Tests for scan.check_structured_data"""

from pathlib import Path
import pytest
from scan.check_structured_data import check_structured_data

FIXTURES = Path(__file__).parent / "fixtures"


def test_good_structured_data_passes():
    files = [FIXTURES / "good_structured_data.html"]
    result = check_structured_data(files)

    assert result["category"] == "structured_data"
    assert result["total"] == 4  # jsonld, og, title, meta desc
    assert result["passed"] == 4


def test_bad_no_metadata_fails():
    files = [FIXTURES / "bad_no_metadata.html"]
    result = check_structured_data(files)

    assert result["category"] == "structured_data"
    assert result["total"] == 4
    assert result["passed"] == 0


def test_jsx_only_returns_na():
    """JSX-only files should return 0 total (structured data is N/A)."""
    files = [FIXTURES / "good_react_component.jsx"]
    result = check_structured_data(files)

    assert result["total"] == 0


def test_empty_file(tmp_path):
    empty = tmp_path / "empty.html"
    empty.write_text("")
    result = check_structured_data([empty])

    assert result["category"] == "structured_data"
    assert result["passed"] == 0


def test_findings_have_required_keys():
    files = [FIXTURES / "good_structured_data.html"]
    result = check_structured_data(files)

    for finding in result["findings"]:
        assert "check" in finding
        assert "passed" in finding
        assert "detail" in finding
