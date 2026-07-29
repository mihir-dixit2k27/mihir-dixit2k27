#!/usr/bin/env python3
"""
scripts/update_activity.py

Queries the GitHub Events API and Search API to compute contribution
metrics and refreshes two README.md blocks:
  - <!-- OSS_TABLE_START --> ... <!-- OSS_TABLE_END -->
  - <!-- METRICS_START --> ... <!-- METRICS_END -->

Usage:
    python scripts/update_activity.py

Environment variables:
    GITHUB_TOKEN     - Personal access token with public_repo scope
    GITHUB_USERNAME  - GitHub username (default: mihir-dixit2k27)
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

README_PATH = Path(__file__).parent.parent / "README.md"
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "mihir-dixit2k27")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Repos to track for the OSS dashboard (owner/repo format)
TRACKED_REPOS: list[tuple[str, str, str, str]] = [
    ("prometheus", "prometheus",       "Core · Query · API",       "Prometheus"),
    ("prometheus", "alertmanager",     "API · Silences · Routing", "Alertmanager"),
    ("grafana",    "loki",             "Ingestion · Query",        "Grafana Loki"),
    ("open-telemetry", "opentelemetry-go", "SDK · Collector",     "OpenTelemetry"),
    ("litmuschaos","litmus",           "Chaos Engine · Probes",    "LitmusChaos"),
    ("kgateway-dev","kgateway",        "Envoy · Control Plane",    "kgateway"),
    ("pipe-cd",    "pipecd",           "Deployment · CD",          "PipeCD"),
]


def gh_request(path: str) -> dict | list:
    """Make an authenticated GitHub API request."""
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    if GITHUB_TOKEN:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        print(f"[update_activity] HTTP {exc.code} for {url}")
        return {}
    except Exception as exc:  # noqa: BLE001
        print(f"[update_activity] Request failed for {url}: {exc}")
        return {}


def count_merged_prs(owner: str, repo: str) -> int:
    """Count merged PRs by the user in a given repo via Search API."""
    query = f"is:pr+is:merged+author:{GITHUB_USERNAME}+repo:{owner}/{repo}"
    result = gh_request(f"/search/issues?q={query}&per_page=1")
    time.sleep(0.5)  # Respect secondary rate limits
    if isinstance(result, dict):
        return result.get("total_count", 0)
    return 0


def build_oss_table() -> str:
    """Build the OSS contribution table markdown block."""
    rows: list[str] = []
    total_prs = 0

    for owner, repo, area, display_name in TRACKED_REPOS:
        pr_count = count_merged_prs(owner, repo)
        total_prs += pr_count
        count_display = f"{pr_count}+" if pr_count > 0 else "—"
        repo_url = f"https://github.com/{owner}/{repo}"
        rows.append(
            f"| [{display_name}]({repo_url}) | {owner.upper()} | {area} | "
            f"{count_display} | — | Active |"
        )

    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    table = "\n".join([
        "<!-- OSS_TABLE_START -->",
        "| Project | Org | Area | Merged PRs | Notable Impact | Status |",
        "|---------|-----|------|:----------:|----------------|--------|",
        *rows,
        "",
        f"<sub>Last updated: {updated_at} · Total merged PRs: {total_prs}+</sub>",
        "<!-- OSS_TABLE_END -->",
    ])
    return table, total_prs


def build_metrics_block(total_prs: int) -> str:
    """Build the engineering metrics block."""
    updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    return "\n".join([
        "<!-- METRICS_START -->",
        "| | |",
        "|---|---|",
        f"| **{total_prs}+** | Merged pull requests across CNCF projects |",
        "| **7** | OSS projects actively contributed to |",
        "| **3+** | Years writing production Go |",
        "| **1422** | Codeforces rating (Specialist) |",
        "| **8.63** | B.Tech CGPA, VIT Vellore |",
        "| **40% → <5%** | CI flakiness reduction at Motherson Group |",
        "| **50k/day** | Workflows processed by OpenFlow |",
        "",
        f"<sub>Last updated: {updated_at}</sub>",
        "<!-- METRICS_END -->",
    ])


def replace_block(content: str, start_marker: str, end_marker: str, replacement: str) -> str:
    """Replace a delimited block in readme content."""
    pattern = re.compile(
        rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}",
        re.DOTALL,
    )
    if not pattern.search(content):
        print(f"[update_activity] WARNING: markers {start_marker!r} not found.")
        return content
    return pattern.sub(replacement, content)


def main() -> None:
    oss_table, total_prs = build_oss_table()
    metrics_block = build_metrics_block(total_prs)

    content = README_PATH.read_text(encoding="utf-8")
    content = replace_block(content, "<!-- OSS_TABLE_START -->", "<!-- OSS_TABLE_END -->", oss_table)
    content = replace_block(content, "<!-- METRICS_START -->", "<!-- METRICS_END -->", metrics_block)

    README_PATH.write_text(content, encoding="utf-8")
    print(f"[update_activity] Done. Total merged PRs across tracked repos: {total_prs}+")


if __name__ == "__main__":
    main()
