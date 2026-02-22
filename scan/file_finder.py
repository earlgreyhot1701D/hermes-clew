"""
file_finder.py — Finds HTML, JSX, and TSX files in a repository.

Returns a list of Path objects. Does NOT read file contents.

Security: Rejects symlinks, path traversal (..), and files outside project root.
Respects v1.3 hard constraints: max 100 files, excluded directories, prioritized directories.
"""

from pathlib import Path
from typing import List

ALLOWED_EXTENSIONS = {".html", ".jsx", ".tsx"}

EXCLUDED_DIRS = {
    "node_modules",
    "dist",
    "build",
    ".next",
    "coverage",
    ".git",
}

# v1.3: Prioritized directories — files in these dirs are sorted first.
PRIORITY_DIRS = {"src", "app", "pages", "components"}

# v1.3: Hard constraints.
MAX_FILES = 100
MAX_FILE_SIZE_BYTES = 50 * 1024  # 50KB


def find_source_files(repo_path: str) -> List[Path]:
    """Find all scannable HTML/JSX/TSX files in the given repo path.

    Returns list of Path objects sorted by priority (src/app/pages/components first),
    capped at MAX_FILES. Skips symlinks, excluded dirs, oversized files, and
    paths containing '..'.
    """
    root = Path(repo_path).resolve()

    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid repository path: {repo_path}")

    priority_files = []
    other_files = []
    skipped = []

    for path in root.rglob("*"):
        # Security: skip non-files
        if not path.is_file():
            continue

        # Security: reject symlinks
        if path.is_symlink():
            skipped.append({"path": str(path), "reason": "symlink"})
            continue

        # Security: reject path traversal
        if ".." in path.parts:
            skipped.append({"path": str(path), "reason": "path_traversal"})
            continue

        # Security: reject files outside project root
        try:
            path.resolve().relative_to(root)
        except ValueError:
            skipped.append({"path": str(path), "reason": "outside_project_root"})
            continue

        # Filter: only allowed extensions
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        # Filter: skip excluded directories
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue

        # v1.3: skip oversized files
        try:
            if path.stat().st_size > MAX_FILE_SIZE_BYTES:
                skipped.append({"path": str(path), "reason": "exceeds_50kb"})
                continue
        except OSError:
            skipped.append({"path": str(path), "reason": "stat_error"})
            continue

        # Sort into priority vs other
        relative_parts = path.relative_to(root).parts
        if any(part in PRIORITY_DIRS for part in relative_parts):
            priority_files.append(path)
        else:
            other_files.append(path)

    # Priority dirs first, then others. Cap at MAX_FILES.
    all_files = priority_files + other_files

    if len(all_files) > MAX_FILES:
        skipped.append({
            "path": "multiple",
            "reason": f"file_limit_exceeded: {len(all_files)} found, capped at {MAX_FILES}",
        })

    return all_files[:MAX_FILES]
