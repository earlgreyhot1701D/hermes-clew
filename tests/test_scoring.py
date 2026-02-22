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
        "semantic_html": {"passed": 3, "total": 6},     # 50% of 25 = 12.5
        "form_accessibility": {"passed": 0, "total": 5}, # 0% of 20 = 0
        "aria": {"passed": 2, "total": 4},               # 50% of 15 = 7.5
        "structured_data": {"passed": 1, "total": 4},    # 25% of 15 = 3.75
        "content_in_html": {"passed": 1, "total": 3},    # 33% of 15 = 5
        "link_navigation": {"passed": 3, "total": 3},    # 100% of 10 = 10
    }
    # earned = 38.75 out of applicable 100 → normalized = 39
    score = calculate_total_score(results)
    assert 35 <= score <= 42  # ~39


def test_empty_categories_skipped():
    """Categories with 0 total checks should not penalize — score normalizes to 100."""
    results = {
        "semantic_html": {"passed": 6, "total": 6},
        "form_accessibility": {"passed": 0, "total": 0},  # N/A
        "aria": {"passed": 4, "total": 4},
        "structured_data": {"passed": 0, "total": 0},     # N/A
        "content_in_html": {"passed": 3, "total": 3},
        "link_navigation": {"passed": 3, "total": 3},
    }
    # All applicable categories are perfect → normalized to 100
    assert calculate_total_score(results) == 100


def test_na_categories_normalize_to_100():
    """A JSX-only project scoring perfectly on applicable categories gets 100."""
    results = {
        "semantic_html": {"passed": 6, "total": 6},
        "form_accessibility": {"passed": 5, "total": 5},
        "aria": {"passed": 4, "total": 4},
        "structured_data": {"passed": 0, "total": 0},     # N/A (JSX-only)
        "content_in_html": {"passed": 0, "total": 0},     # N/A (JSX-only)
        "link_navigation": {"passed": 3, "total": 3},
    }
    assert calculate_total_score(results) == 100


def test_all_na_returns_zero():
    """If all categories are N/A, return 0."""
    results = {
        "semantic_html": {"passed": 0, "total": 0},
        "form_accessibility": {"passed": 0, "total": 0},
        "aria": {"passed": 0, "total": 0},
        "structured_data": {"passed": 0, "total": 0},
        "content_in_html": {"passed": 0, "total": 0},
        "link_navigation": {"passed": 0, "total": 0},
    }
    assert calculate_total_score(results) == 0


def test_score_rating():
    assert "Agent-Ready" in get_score_rating(90)
    assert "Partially Ready" in get_score_rating(70)
    assert "Agent-Challenged" in get_score_rating(50)
    assert "Agent-Invisible" in get_score_rating(20)


def test_score_rating_clamping():
    """Scores >100 or <0 should be clamped before lookup."""
    assert "Agent-Ready" in get_score_rating(150)
    assert "Agent-Invisible" in get_score_rating(-10)


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
