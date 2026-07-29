# docs/setup.md
# Setup & Automation Guide

This document explains how to configure the automation workflows in this repository
so that the dynamic sections of `README.md` update automatically.

---

## Prerequisites

- A GitHub account with a **special repository** named exactly after your username
  (`mihir-dixit2k27/mihir-dixit2k27`). GitHub renders the `README.md` of this
  repository on your profile page.
- Python 3.10+ (for local testing of scripts).

---

## Repository Variables

Go to **Settings → Secrets and variables → Actions → Variables** and add:

| Variable | Value |
|----------|-------|
| `GITHUB_USERNAME` | `mihir-dixit2k27` |
| `BLOG_RSS_URL` | `https://mihirdixit.dev/blog/rss.xml` |

The `GITHUB_TOKEN` secret is automatically available to all workflows — no manual
configuration needed.

---

## Workflow Schedule

| Workflow | File | Trigger |
|----------|------|---------|
| Update blog posts | `update-blog.yml` | Daily at 06:00 UTC |
| Update activity / metrics | `update-activity.yml` | Every 12 hours |
| Full README refresh | `update-readme.yml` | Weekly, Monday 00:00 UTC |

All workflows can also be triggered manually via **Actions → Run workflow**.

---

## Local Testing

```bash
# Clone the repo
git clone https://github.com/mihir-dixit2k27/mihir-dixit2k27.git
cd mihir-dixit2k27

# Install dependencies
pip install -r requirements.txt

# Set required env vars
export GITHUB_TOKEN="ghp_..."
export GITHUB_USERNAME="mihir-dixit2k27"
export BLOG_RSS_URL="https://mihirdixit.dev/blog/rss.xml"

# Run individual scripts
python scripts/update_blog.py
python scripts/update_activity.py

# Or run all at once
python scripts/update_readme.py
```

The scripts are idempotent — running them multiple times with the same data
will not produce duplicate commits.

---

## Customization

See [`customization.md`](./customization.md) for instructions on editing
structured sections (projects, OSS dashboard, tech stack, etc.).

---

## Dependabot

`dependabot.yml` is configured to keep GitHub Actions versions up to date,
with weekly checks on Monday mornings.

---

## Troubleshooting

**Workflow fails with `403 Forbidden`**  
Ensure the workflow has `permissions: contents: write` and that Actions are
enabled in the repository settings.

**Blog posts not updating**  
Check that `BLOG_RSS_URL` is set correctly and the feed is publicly reachable.
Run `python scripts/update_blog.py` locally to debug.

**GitHub API rate limits**  
The `update_activity.py` script adds 500 ms sleeps between Search API calls
to stay within secondary rate limits. If you hit primary rate limits, add a
`GITHUB_TOKEN` with `public_repo` scope.
