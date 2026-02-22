"""Tests for scan.report_prompt"""

from scan.report_prompt import build_reasoning_prompt


def test_build_prompt_renders_without_error():
    """Smoke test: build_reasoning_prompt should not raise with minimal input."""
    scan_result = {
        "total_score": 72,
        "file_count": 5,
        "categories": {
            "semantic_html": {
                "category": "semantic_html",
                "passed": 4,
                "total": 6,
                "findings": [
                    {"check": "nav_element", "passed": True, "detail": "Nav found."},
                ],
            },
            "form_accessibility": {
                "category": "form_accessibility",
                "passed": 0,
                "total": 0,
                "findings": [],
            },
            "aria": {
                "category": "aria",
                "passed": 3,
                "total": 4,
                "findings": [],
            },
            "structured_data": {
                "category": "structured_data",
                "passed": 2,
                "total": 4,
                "findings": [],
            },
            "content_in_html": {
                "category": "content_in_html",
                "passed": 2,
                "total": 3,
                "findings": [],
            },
            "link_navigation": {
                "category": "link_navigation",
                "passed": 3,
                "total": 3,
                "findings": [],
            },
        },
    }
    prompt = build_reasoning_prompt(scan_result, project_name="Test Project", scan_date="2026-01-01")
    assert isinstance(prompt, str)
    assert len(prompt) > 100


def test_prompt_contains_expected_sections():
    """The rendered prompt should include key report template sections."""
    scan_result = {
        "total_score": 50,
        "file_count": 3,
        "categories": {
            "semantic_html": {"category": "semantic_html", "passed": 3, "total": 6, "findings": []},
            "form_accessibility": {"category": "form_accessibility", "passed": 2, "total": 5, "findings": []},
            "aria": {"category": "aria", "passed": 1, "total": 4, "findings": []},
            "structured_data": {"category": "structured_data", "passed": 1, "total": 4, "findings": []},
            "content_in_html": {"category": "content_in_html", "passed": 1, "total": 3, "findings": []},
            "link_navigation": {"category": "link_navigation", "passed": 1, "total": 3, "findings": []},
        },
    }
    prompt = build_reasoning_prompt(scan_result, project_name="My App")
    assert "Agent Readiness Report" in prompt
    assert "Category" in prompt or "category" in prompt
    assert "What's Working" in prompt
    assert "My App" in prompt


def test_prompt_with_zero_score():
    """Prompt should render even with all-zero scores."""
    scan_result = {
        "total_score": 0,
        "file_count": 0,
        "categories": {
            "semantic_html": {"category": "semantic_html", "passed": 0, "total": 0, "findings": []},
            "form_accessibility": {"category": "form_accessibility", "passed": 0, "total": 0, "findings": []},
            "aria": {"category": "aria", "passed": 0, "total": 0, "findings": []},
            "structured_data": {"category": "structured_data", "passed": 0, "total": 0, "findings": []},
            "content_in_html": {"category": "content_in_html", "passed": 0, "total": 0, "findings": []},
            "link_navigation": {"category": "link_navigation", "passed": 0, "total": 0, "findings": []},
        },
    }
    prompt = build_reasoning_prompt(scan_result)
    assert isinstance(prompt, str)
    assert "0" in prompt
