"""Tests for scan.scoring"""

import pytest
from scan.scoring import calculate_total_score, get_score_rating, get_category_breakdown


def test_perfect_score():
    results = {
        "semantic_html": {"passed": 6, "total": 6},
        "form_accessibility": {"passed": 5, "total": 5},
        "aria": {"passed": 4, "total": 4},
        "structured_data": {"passed": 4, "total": 4},
        "content_in_html": {"passed": 3, "total": 3},
        "link_navigation": {"passed": 3, "total": 3},
    }
    assert calculate_total_score(results) == 100


def test_zero_score():
    results = {
        "semantic_html": {"passed": 0, "total": 6},
        "form_accessibility": {"passed": 0, "total": 5},
        "aria": {"passed": 0, "total": 4},
        "structured_data": {"passed": 0, "total": 4},
        "content_in_html": {"passed": 0, "total": 3},
        "link_navigation": {"passed": 0, "total": 3},
    }
    assert calculate_total_score(results) == 0


def test_partial_score():
    results = {
        "semantic_html": {"passed": 3, "total": 6},     # 12.5
        "form_accessibility": {"passed": 0, "total": 5}, # 0
        "aria": {"passed": 2, "total": 4},               # 7.5
        "structured_data": {"passed": 1, "total": 4},    # 3.75
        "content_in_html": {"passed": 1, "total": 3},    # 5
        "link_navigation": {"passed": 3, "total": 3},    # 10
    }
    score = calculate_total_score(results)
    assert 35 <= score <= 42  # ~38.75


def test_empty_categories_skipped():
    """Categories with 0 total checks should not penalize."""
    results = {
        "semantic_html": {"passed": 6, "total": 6},
        "form_accessibility": {"passed": 0, "total": 0},  # N/A
        "aria": {"passed": 4, "total": 4},
        "structured_data": {"passed": 0, "total": 0},     # N/A
        "content_in_html": {"passed": 3, "total": 3},
        "link_navigation": {"passed": 3, "total": 3},
    }
    # Should get 25 + 0 + 15 + 0 + 15 + 10 = 65
    assert calculate_total_score(results) == 65


def test_score_rating():
    assert "Agent-Ready" in get_score_rating(90)
    assert "Partially Ready" in get_score_rating(70)
    assert "Agent-Challenged" in get_score_rating(50)
    assert "Agent-Invisible" in get_score_rating(20)


def test_category_breakdown():
    results = {
        "semantic_html": {"passed": 6, "total": 6},
        "form_accessibility": {"passed": 0, "total": 5},
        "aria": {"passed": 4, "total": 4},
        "structured_data": {"passed": 2, "total": 4},
        "content_in_html": {"passed": 0, "total": 0},
        "link_navigation": {"passed": 3, "total": 3},
    }
    breakdown = get_category_breakdown(results)

    assert breakdown["semantic_html"]["status"] == "✅ Strong"
    assert breakdown["form_accessibility"]["status"] == "❌ Weak"
    assert breakdown["content_in_html"]["status"] == "N/A"
    assert breakdown["link_navigation"]["earned"] == 10
