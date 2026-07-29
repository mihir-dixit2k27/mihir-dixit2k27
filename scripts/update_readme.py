#!/usr/bin/env python3
"""
scripts/update_readme.py

Master orchestration script. Calls all individual update modules in order:
  1. update_blog      — blog posts from RSS feed
  2. update_activity  — OSS PR counts and metrics

Designed to be idempotent. Each sub-script only writes to README.md if
the content it is responsible for has actually changed.

Usage:
    python scripts/update_readme.py

Environment variables:
    GITHUB_TOKEN     - Personal access token with public_repo scope
    GITHUB_USERNAME  - GitHub username (default: mihir-dixit2k27)
    BLOG_RSS_URL     - RSS/Atom feed URL for blog posts
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

# Ensure scripts/ is importable regardless of working directory
scripts_dir = Path(__file__).parent
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

MODULES_IN_ORDER = [
    "update_blog",
    "update_activity",
]


def run_all() -> None:
    print("[update_readme] Starting full README refresh...")
    for module_name in MODULES_IN_ORDER:
        print(f"\n[update_readme] Running {module_name}...")
        try:
            module = importlib.import_module(module_name)
            module.main()
        except Exception as exc:  # noqa: BLE001
            print(f"[update_readme] ERROR in {module_name}: {exc}")
            # Non-fatal: continue with other modules
    print("\n[update_readme] All modules complete.")


if __name__ == "__main__":
    run_all()
