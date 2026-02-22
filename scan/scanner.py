"""
scanner.py — ENTRY POINT. Orchestrates all 6 category checks and outputs JSON.

This file calls the check modules. It does NOT contain check logic.
One file, one job: orchestration.
"""

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from scan.file_finder import find_source_files, MAX_FILES
from scan.check_semantic_html import check_semantic_html
from scan.check_form_accessibility import check_form_accessibility
from scan.check_aria import check_aria
from scan.check_structured_data import check_structured_data
from scan.check_content_in_html import check_content_in_html
from scan.check_link_navigation import check_link_navigation
from scan.scoring import calculate_total_score, get_score_rating, get_category_breakdown

logger = logging.getLogger(__name__)


def run_scan(repo_path: str) -> dict:
    """Run the full Hermes Clew scan on a repository.

    Args:
        repo_path: Path to the repository root to scan.

    Returns:
        Dict with total_score, rating, file_count, categories, breakdown,
        skipped_files, and files_capped.
    """
    files, skipped = find_source_files(repo_path)

    logger.info("Files found: %d", len(files))
    if skipped:
        logger.info("Files skipped: %d", len(skipped))
        for entry in skipped:
            logger.debug("Skipped: %s — %s", entry["path"], entry["reason"])

    categories = {
        "semantic_html": check_semantic_html(files),
        "form_accessibility": check_form_accessibility(files),
        "aria": check_aria(files),
        "structured_data": check_structured_data(files),
        "content_in_html": check_content_in_html(files),
        "link_navigation": check_link_navigation(files),
    }

    total_score = calculate_total_score(categories)
    rating = get_score_rating(total_score)
    breakdown = get_category_breakdown(categories)

    for cat_name, info in breakdown.items():
        logger.info("Category %s: %d/%d", cat_name, info["earned"], info["max"])
    logger.info("Total score: %d — %s", total_score, rating)

    return {
        "project_path": str(repo_path),
        "scan_date": datetime.now(timezone.utc).isoformat(),
        "file_count": len(files),
        "files_scanned": [str(f.name) for f in files],
        "skipped_files": skipped,
        "files_capped": len(files) >= MAX_FILES and len(skipped) > 0,
        "total_score": total_score,
        "rating": rating,
        "breakdown": breakdown,
        "categories": categories,
    }


def main():
    """CLI entry point: python -m scan.scanner <repo_path>"""
    if len(sys.argv) != 2:
        print("Usage: python -m scan.scanner <repo_path>", file=sys.stderr)
        print("Example: python -m scan.scanner ./my-web-app", file=sys.stderr)
        sys.exit(1)

    repo_path = sys.argv[1]

    try:
        result = run_scan(repo_path)
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    # Output machine-readable JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
