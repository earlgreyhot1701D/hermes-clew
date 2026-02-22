"""
external_url.py — STUB: Path B External URL scanning.

Post-hackathon: Accept public GitHub URL or deployed URL as input.
Clone public repo to temp directory, scan, delete after report.
For deployed URLs: fetch rendered HTML, scan DOM output.
Security: Only public repos. Delete clone immediately after scan.
Never store cloned code. Never access private repos.
See PRD Section 20 for full specification.
"""


# STUB: Path B — External URL scanning
# Post-hackathon: Accept GitHub URL or deployed URL as input.
# Clone public repo to temp directory, scan, delete after report.
# For deployed URLs: fetch rendered HTML, scan DOM output.
# Security: Only public repos. Delete clone immediately after scan.
# Never store cloned code. Never access private repos.
# See PRD Section 20 for specification.
def scan_external_url(url: str) -> dict:
    raise NotImplementedError("Path B: External URL scanning — post-hackathon feature")
