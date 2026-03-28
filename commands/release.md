---
name: release
description: Cut a new release — bumps version in plugin.json, commits, tags, pushes, and creates a GitHub release
user_invocable: true
---

You are cutting a new release for the html-magazine plugin. Follow these steps exactly.

## Step 1 — Determine the new version

Read the current version from `.claude-plugin/plugin.json`.

Ask the user what the new version should be, showing the current version and the three standard bump options:
- **patch** — bug fixes (e.g. 1.0.0 → 1.0.1)
- **minor** — new features, backwards compatible (e.g. 1.0.0 → 1.1.0)
- **major** — breaking changes (e.g. 1.0.0 → 2.0.0)

Accept either a bump type or an explicit version string (e.g. "1.2.0").

## Step 2 — Write release notes

Ask the user for release notes. Suggest drafting them from `git log` since the last tag:

```bash
git log $(git describe --tags --abbrev=0 2>/dev/null || git rev-list --max-parents=0 HEAD)..HEAD --oneline
```

Present the commits and ask: "What should the release notes highlight? Or should I draft them from these commits?"

If the user says to draft them, write concise bullet points grouped by type (Features, Fixes, Improvements). Skip internal/housekeeping commits.

## Step 3 — Bump the version

Update `.claude-plugin/plugin.json` — set `"version"` to the new version string. No other changes.

## Step 4 — Commit and tag

```bash
git add .claude-plugin/plugin.json
git commit -m "Release v<VERSION>"
git tag v<VERSION>
```

## Step 5 — Push

```bash
git push origin main
git push origin v<VERSION>
```

## Step 6 — Create GitHub release

```bash
gh release create v<VERSION> \
  --repo bluedusk/html-magazine \
  --title "v<VERSION>" \
  --notes "<RELEASE_NOTES>"
```

## Step 7 — Confirm

Print the GitHub release URL and confirm success.
