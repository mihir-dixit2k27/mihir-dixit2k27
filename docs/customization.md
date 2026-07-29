# docs/customization.md
# Customization Guide

This document explains how to update each section of `README.md` manually
and how to modify the automation scripts.

---

## Editing Static Sections

Most sections are plain markdown. Edit `README.md` directly.

### Adding a New Project

Copy the template below into the **Featured Projects** section:

```markdown
### [Project Name](https://github.com/mihir-dixit2k27/project-name) — Short Description

> One sentence describing what the project is and what problem it solves.

**Stack:** `Go` `PostgreSQL` `Docker`

**Key Design Decisions**

- Decision one
- Decision two

[Repository](https://github.com/mihir-dixit2k27/project-name)
```

### Updating Current Focus

Edit the `<!-- CURRENT_FOCUS_START --> ... <!-- CURRENT_FOCUS_END -->` block:

```markdown
<!-- CURRENT_FOCUS_START -->
| Area | What |
|------|------|
| **Building** | Your current project |
| **Contributing** | OSS project you are working on |
| **Writing** | Blog post in progress |
| **Studying** | Topic you are learning |
<!-- CURRENT_FOCUS_END -->
```

---

## Editing Automation Scripts

### Changing Which OSS Repos Are Tracked

In `scripts/update_activity.py`, edit the `TRACKED_REPOS` list:

```python
TRACKED_REPOS: list[tuple[str, str, str, str]] = [
    # (owner, repo, area, display_name)
    ("prometheus", "prometheus", "Core · Query · API", "Prometheus"),
    # Add or remove entries here
]
```

### Changing the Blog Feed URL

Set the `BLOG_RSS_URL` repository variable in GitHub Actions settings.
For local testing, set the env var:

```bash
export BLOG_RSS_URL="https://your-blog.com/feed.xml"
python scripts/update_blog.py
```

### Adding a New Auto-Updated Block

1. Add HTML comment markers to `README.md`:
   ```markdown
   <!-- MY_BLOCK_START -->
   content here
   <!-- MY_BLOCK_END -->
   ```

2. Use the `replace_block` helper in `scripts/update_activity.py` or write
   a new script that calls the same pattern.

3. Add the new script to the `MODULES_IN_ORDER` list in `scripts/update_readme.py`.

---

## Adding Architecture Diagrams

Place SVG or PNG diagrams in `assets/architecture/`. Reference them from
the project sections using:

```markdown
![OpenFlow Architecture](./assets/architecture/openflow.svg)
```

---

## Updating the Banner

Edit `assets/banner.svg` directly. The banner uses system fonts (SF Mono,
JetBrains Mono, Fira Code) and standard GitHub Dark palette colors:

| Token | Hex |
|-------|-----|
| Background | `#0d1117` |
| Surface | `#161b22` |
| Border | `#21262d` |
| Muted text | `#8b949e` |
| Primary text | `#e6edf3` |
| Blue accent | `#58a6ff` |
| Green accent | `#3fb950` |

---

## Sync with Codeforces

The Codeforces rating in the banner SVG (`assets/banner.svg`) and README
metrics table must be updated manually when your rating changes. Search for
`1422` and replace with the new rating.
