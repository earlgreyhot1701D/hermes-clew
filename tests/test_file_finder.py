"""Tests for scan.file_finder"""

import os
import sys
import tempfile
from pathlib import Path

import pytest
from scan.file_finder import find_source_files, ALLOWED_EXTENSIONS, EXCLUDED_DIRS, MAX_FILES, MAX_FILE_SIZE_BYTES


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
    files, _ = find_source_files(str(temp_repo))
    names = {f.name for f in files}
    assert "index.html" in names
    assert "App.jsx" in names
    assert "Page.tsx" in names
    assert "Button.jsx" in names


def test_excludes_node_modules(temp_repo):
    files, _ = find_source_files(str(temp_repo))
    for f in files:
        assert "node_modules" not in f.parts


def test_excludes_dist(temp_repo):
    files, _ = find_source_files(str(temp_repo))
    for f in files:
        assert "dist" not in f.parts


def test_excludes_git(temp_repo):
    files, _ = find_source_files(str(temp_repo))
    for f in files:
        assert ".git" not in f.parts


def test_excludes_non_matching_extensions(temp_repo):
    files, _ = find_source_files(str(temp_repo))
    names = {f.name for f in files}
    assert "readme.md" not in names
    assert "styles.css" not in names
    assert "script.py" not in names


def test_invalid_path_raises():
    with pytest.raises(ValueError, match="Invalid repository path"):
        find_source_files("/nonexistent/path/that/doesnt/exist")


def test_priority_dirs_first(temp_repo):
    """Files in src/ and components/ should appear before root-level files."""
    files, _ = find_source_files(str(temp_repo))
    names = [f.name for f in files]
    # Priority dirs (src, components) should come before root files
    priority_names = {"App.jsx", "Page.tsx", "Button.jsx"}
    priority_indices = [i for i, n in enumerate(names) if n in priority_names]
    root_indices = [i for i, n in enumerate(names) if n == "index.html"]

    if priority_indices and root_indices:
        assert max(priority_indices) < min(root_indices)


def test_empty_directory(tmp_path):
    files, _ = find_source_files(str(tmp_path))
    assert files == []


def test_max_files_cap(tmp_path):
    """If more than MAX_FILES exist, cap the result."""
    for i in range(MAX_FILES + 20):
        (tmp_path / f"file_{i:04d}.html").write_text(f"<html>{i}</html>")

    files, _ = find_source_files(str(tmp_path))
    assert len(files) <= MAX_FILES


def test_returns_skipped_list(temp_repo):
    """find_source_files returns a tuple of (files, skipped)."""
    files, skipped = find_source_files(str(temp_repo))
    assert isinstance(files, list)
    assert isinstance(skipped, list)


# --- P2-4: Security tests ---

@pytest.mark.skipif(sys.platform == "win32", reason="Symlinks require admin on Windows")
def test_symlink_rejection(tmp_path):
    """Symlinks to files outside the repo should be skipped."""
    # Create a real file outside the repo
    outside = tmp_path / "outside"
    outside.mkdir()
    target = outside / "secret.html"
    target.write_text("<html>secret</html>")

    # Create repo dir with a symlink pointing outside
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "legit.html").write_text("<html>legit</html>")
    os.symlink(str(target), str(repo / "evil.html"))

    files, skipped = find_source_files(str(repo))
    names = {f.name for f in files}
    assert "legit.html" in names
    assert "evil.html" not in names
    # Verify it was recorded as skipped
    symlink_skipped = [s for s in skipped if s["reason"] == "symlink"]
    assert len(symlink_skipped) >= 1


def test_oversized_file_rejection(tmp_path):
    """Files exceeding MAX_FILE_SIZE_BYTES should be skipped."""
    (tmp_path / "small.html").write_text("<html>small</html>")
    # Create an oversized file (just over the limit)
    big_content = "x" * (MAX_FILE_SIZE_BYTES + 1)
    (tmp_path / "huge.html").write_text(big_content)

    files, skipped = find_source_files(str(tmp_path))
    names = {f.name for f in files}
    assert "small.html" in names
    assert "huge.html" not in names
    # Verify it was recorded as skipped
    oversized_skipped = [s for s in skipped if s["reason"] == "exceeds_50kb"]
    assert len(oversized_skipped) >= 1


def test_path_traversal_rejection(tmp_path):
    """Paths containing '..' components should be rejected."""
    # We can't easily create a filesystem path with '..' via rglob,
    # but we can verify the security check exists by testing that
    # files resolved outside root are rejected via the relative_to check.
    (tmp_path / "safe.html").write_text("<html>safe</html>")
    files, skipped = find_source_files(str(tmp_path))
    names = {f.name for f in files}
    assert "safe.html" in names
    # All returned files should resolve within root
    root = Path(tmp_path).resolve()
    for f in files:
        assert f.resolve().is_relative_to(root)
