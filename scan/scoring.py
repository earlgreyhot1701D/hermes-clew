"""
scoring.py — Takes category result dicts, applies weights, returns total score.

This module knows NOTHING about HTML. It only knows weights and math.
"""

from typing import Dict

WEIGHTS = {
    "semantic_html": 25,
    "form_accessibility": 20,
    "aria": 15,
    "structured_data": 15,
    "content_in_html": 15,
    "link_navigation": 10,
}

SCORE_RANGES = {
    "agent_ready": (80, 100, "Agent-Ready — agents can navigate and interact with this app"),
    "partially_ready": (60, 79, "Partially Ready — agents can find content but struggle with interactions"),
    "agent_challenged": (40, 59, "Agent-Challenged — agents can see the page but can't do much with it"),
    "agent_invisible": (0, 39, "Agent-Invisible — agents bounce immediately"),
}


def calculate_total_score(category_results: Dict[str, Dict]) -> int:
    """Calculate weighted total score from category results.

    Each category: (passed / total) * weight_points.
    Categories with 0 total checks are skipped (don't penalize for N/A).
    """
    total = 0

    for category, result in category_results.items():
        if category not in WEIGHTS:
            continue

        max_points = WEIGHTS[category]
        passed = result.get("passed", 0)
        total_checks = result.get("total", 0)

        if total_checks == 0:
            continue

        category_score = (passed / total_checks) * max_points
        total += category_score

    return round(total)


def get_score_rating(score: int) -> str:
    """Return the human-readable rating for a given score."""
    for _key, (low, high, label) in SCORE_RANGES.items():
        if low <= score <= high:
            return label
    return "Unknown"


def get_category_breakdown(category_results: Dict[str, Dict]) -> Dict[str, Dict]:
    """Return per-category score breakdown for the report."""
    breakdown = {}

    for category, result in category_results.items():
        if category not in WEIGHTS:
            continue

        max_points = WEIGHTS[category]
        passed = result.get("passed", 0)
        total_checks = result.get("total", 0)

        if total_checks == 0:
            earned = 0
            status = "N/A"
        else:
            earned = round((passed / total_checks) * max_points)
            pct = (passed / total_checks) * 100
            if pct >= 80:
                status = "✅ Strong"
            elif pct >= 50:
                status = "⚠️ Needs Work"
            else:
                status = "❌ Weak"

        breakdown[category] = {
            "earned": earned,
            "max": max_points,
            "passed": passed,
            "total": total_checks,
            "status": status,
        }

    return breakdown
