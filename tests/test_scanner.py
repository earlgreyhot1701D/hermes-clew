"""Tests for scan.scanner CLI entry point"""

import json
import subprocess
import sys
import os

import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")


def test_main_invalid_path_exits_nonzero():
    """main() with an invalid path should write to stderr and exit non-zero."""
    result = subprocess.run(
        [sys.executable, "-m", "scan.scanner", "/nonexistent/path"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert result.stderr.strip() != ""


def test_main_no_args_exits_nonzero():
    """main() with no arguments should print usage to stderr."""
    result = subprocess.run(
        [sys.executable, "-m", "scan.scanner"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "Usage" in result.stderr


def test_main_valid_path_produces_json():
    """main() with a valid path should produce valid JSON to stdout."""
    result = subprocess.run(
        [sys.executable, "-m", "scan.scanner", FIXTURES_DIR],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "total_score" in data
    assert "categories" in data
    assert "skipped_files" in data
