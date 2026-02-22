"""
test_integration.py — End-to-end integration test for the Hermes Clew scan pipeline.

Runs scanner.run_scan() against test fixtures and verifies the full JSON
output structure matches PRD requirements (Section 13, 14).
"""

import os
import pytest
from scan.scanner import run_scan

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

# --- Required top-level keys ---

REQUIRED_TOP_KEYS = {
    "project_path",
    "scan_date",
    "file_count",
    "files_scanned",
    "skipped_files",
    "files_capped",
    "total_score",
    "rating",
    "breakdown",
    "categories",
}

REQUIRED_CATEGORIES = {
    "semantic_html",
    "form_accessibility",
    "aria",
    "structured_data",
    "content_in_html",
    "link_navigation",
}

REQUIRED_CATEGORY_KEYS = {"category", "passed", "total", "findings"}

VALID_RATINGS = {
    "Agent-Ready",
    "Partially Ready",
    "Agent-Challenged",
    "Agent-Invisible",
}


class TestFullPipeline:
    """Run the full scan against fixtures and verify output structure."""

    @pytest.fixture(autouse=True)
    def run_scan_once(self):
        """Run scan once and share result across all tests in this class."""
        self.result = run_scan(FIXTURES_DIR)

    def test_returns_dict(self):
        assert isinstance(self.result, dict)

    def test_has_all_top_level_keys(self):
        for key in REQUIRED_TOP_KEYS:
            assert key in self.result, f"Missing top-level key: {key}"

    def test_score_in_valid_range(self):
        score = self.result["total_score"]
        assert isinstance(score, int)
        assert 0 <= score <= 100

    def test_rating_is_valid(self):
        # Rating string should start with one of the valid prefixes
        rating = self.result["rating"]
        assert isinstance(rating, str)
        assert any(rating.startswith(r) for r in VALID_RATINGS), (
            f"Unexpected rating: {rating}"
        )

    def test_file_count_matches_files_scanned(self):
        assert self.result["file_count"] == len(self.result["files_scanned"])

    def test_file_count_positive(self):
        assert self.result["file_count"] > 0, "No files found in fixtures"

    def test_all_six_categories_present(self):
        categories = self.result["categories"]
        for cat in REQUIRED_CATEGORIES:
            assert cat in categories, f"Missing category: {cat}"

    def test_category_dict_structure(self):
        for cat_name, cat_data in self.result["categories"].items():
            for key in REQUIRED_CATEGORY_KEYS:
                assert key in cat_data, (
                    f"Category '{cat_name}' missing key: {key}"
                )

    def test_category_passed_lte_total(self):
        for cat_name, cat_data in self.result["categories"].items():
            assert cat_data["passed"] <= cat_data["total"], (
                f"Category '{cat_name}': passed ({cat_data['passed']}) > "
                f"total ({cat_data['total']})"
            )

    def test_findings_is_list(self):
        for cat_name, cat_data in self.result["categories"].items():
            assert isinstance(cat_data["findings"], list), (
                f"Category '{cat_name}': findings is not a list"
            )

    def test_each_finding_has_required_keys(self):
        for cat_name, cat_data in self.result["categories"].items():
            for i, finding in enumerate(cat_data["findings"]):
                assert "check" in finding, (
                    f"Category '{cat_name}' finding {i}: missing 'check'"
                )
                assert "passed" in finding, (
                    f"Category '{cat_name}' finding {i}: missing 'passed'"
                )
                assert "detail" in finding, (
                    f"Category '{cat_name}' finding {i}: missing 'detail'"
                )

    def test_breakdown_has_all_categories(self):
        breakdown = self.result["breakdown"]
        for cat in REQUIRED_CATEGORIES:
            assert cat in breakdown, f"Breakdown missing category: {cat}"

    def test_breakdown_values_structure(self):
        for cat_name, info in self.result["breakdown"].items():
            assert "earned" in info
            assert "max" in info
            assert "passed" in info
            assert "total" in info
            assert "status" in info

    def test_scan_date_is_iso_format(self):
        scan_date = self.result["scan_date"]
        assert isinstance(scan_date, str)
        assert len(scan_date) > 10, "scan_date too short for ISO format"

    def test_project_path_present(self):
        assert isinstance(self.result["project_path"], str)
        assert len(self.result["project_path"]) > 0

    def test_skipped_files_is_list(self):
        assert isinstance(self.result["skipped_files"], list)

    def test_files_capped_is_bool(self):
        assert isinstance(self.result["files_capped"], bool)


class TestScanFindsFixtureFiles:
    """Verify the scanner finds the expected fixture files."""

    @pytest.fixture(autouse=True)
    def run_scan_once(self):
        self.result = run_scan(FIXTURES_DIR)

    def test_finds_html_files(self):
        html_files = [f for f in self.result["files_scanned"] if f.endswith(".html")]
        assert len(html_files) > 0, "No HTML files found in fixtures"

    def test_finds_jsx_files(self):
        jsx_files = [f for f in self.result["files_scanned"] if f.endswith(".jsx")]
        assert len(jsx_files) > 0, "No JSX files found in fixtures"

    def test_expected_file_count(self):
        # 14 fixture files: 12 .html + 2 .jsx
        assert self.result["file_count"] == 14, (
            f"Expected 14 fixture files, got {self.result['file_count']}"
        )


class TestScoreReflectsFixtures:
    """Verify the score is reasonable given mix of good/bad fixtures."""

    @pytest.fixture(autouse=True)
    def run_scan_once(self):
        self.result = run_scan(FIXTURES_DIR)

    def test_score_not_zero(self):
        """Good fixtures should contribute some points."""
        assert self.result["total_score"] > 0

    def test_score_not_perfect(self):
        """Bad fixtures should prevent a perfect score."""
        assert self.result["total_score"] < 100

    def test_semantic_html_finds_issues(self):
        """bad_div_soup.html should produce findings."""
        cat = self.result["categories"]["semantic_html"]
        assert cat["total"] > 0
        assert len(cat["findings"]) > 0