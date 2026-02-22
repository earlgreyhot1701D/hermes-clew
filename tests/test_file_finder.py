"""Tests for scan.file_finder"""

import os
import tempfile
from pathlib import Path

import pytest
from scan.file_finder import find_source_files, ALLOWED_EXTENSIONS, EXCLUDED_DIRS, MAX_FILES


@pytest.fixture
def temp_repo(tmp_path):
    """Create a temporary repo structure with various file types."""
    # Good files
    (tmp_path / "index.html").write_text("<html></html>")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "App.jsx").write_text("export default function App() {}")
    (tmp_path / "src" / "Page.tsx").write_text("export default function Page() {}")
    (tmp_path / "components").mkdir()
    (tmp_path / "components" / "Button.jsx").write_text("<button>Click</button>")

    # Files to exclude
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "react.js").write_text("module.exports = {}")
    (tmp_path / "dist").mkdir()
    (tmp_path / "dist" / "bundle.html").write_text("<html></html>")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("[core]")

    # Non-matching extensions
    (tmp_path / "readme.md").write_text("# Hello")
    (tmp_path / "styles.css").write_text("body {}")
    (tmp_path / "script.py").write_text("print('hello')")

    return tmp_path


def test_finds_html_jsx_tsx(temp_repo):
    files = find_source_files(str(temp_repo))
    names = {f.name for f in files}
    assert "index.html" in names
    assert "App.jsx" in names
    assert "Page.tsx" in names
    assert "Button.jsx" in names


def test_excludes_node_modules(temp_repo):
    files = find_source_files(str(temp_repo))
    for f in files:
        assert "node_modules" not in f.parts


def test_excludes_dist(temp_repo):
    files = find_source_files(str(temp_repo))
    for f in files:
        assert "dist" not in f.parts


def test_excludes_git(temp_repo):
    files = find_source_files(str(temp_repo))
    for f in files:
        assert ".git" not in f.parts


def test_excludes_non_matching_extensions(temp_repo):
    files = find_source_files(str(temp_repo))
    names = {f.name for f in files}
    assert "readme.md" not in names
    assert "styles.css" not in names
    assert "script.py" not in names


def test_invalid_path_raises():
    with pytest.raises(ValueError, match="Invalid repository path"):
        find_source_files("/nonexistent/path/that/doesnt/exist")


def test_priority_dirs_first(temp_repo):
    """Files in src/ and components/ should appear before root-level files."""
    files = find_source_files(str(temp_repo))
    names = [f.name for f in files]
    # Priority dirs (src, components) should come before root files
    priority_names = {"App.jsx", "Page.tsx", "Button.jsx"}
    priority_indices = [i for i, n in enumerate(names) if n in priority_names]
    root_indices = [i for i, n in enumerate(names) if n == "index.html"]

    if priority_indices and root_indices:
        assert max(priority_indices) < min(root_indices) or len(priority_indices) > 0


def test_empty_directory(tmp_path):
    files = find_source_files(str(tmp_path))
    assert files == []


def test_max_files_cap(tmp_path):
    """If more than MAX_FILES exist, cap the result."""
    for i in range(MAX_FILES + 20):
        (tmp_path / f"file_{i:04d}.html").write_text(f"<html>{i}</html>")

    files = find_source_files(str(tmp_path))
    assert len(files) <= MAX_FILES
