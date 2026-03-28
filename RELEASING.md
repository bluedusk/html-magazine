# Releasing html-magazine

## Quick release

Run `/release` in Claude Code. It will:

1. Ask for the new version (patch / minor / major or explicit)
2. Help draft release notes from git log
3. Bump `.claude-plugin/plugin.json`
4. Commit, tag, and push
5. Create the GitHub release

## Version files

Only one file needs to be updated on each release:

| File | Field |
|------|-------|
| `.claude-plugin/plugin.json` | `"version"` |

## Versioning rules

This project follows [Semantic Versioning](https://semver.org/):

- **patch** (x.x.**1**) — bug fixes, content tweaks, style reference updates
- **minor** (x.**1**.0) — new features, new styles, new workflow steps (backwards compatible)
- **major** (**1**.0.0) — breaking changes to the skill interface or rendering spec

## Git tags

Every release gets a `v<VERSION>` tag (e.g. `v1.1.0`). Tags are pushed to `origin`.

## Manual steps (if not using `/release`)

```bash
# 1. Update version
# Edit .claude-plugin/plugin.json — bump "version"

# 2. Commit and tag
git add .claude-plugin/plugin.json
git commit -m "Release v1.1.0"
git tag v1.1.0

# 3. Push
git push origin main
git push origin v1.1.0

# 4. GitHub release
gh release create v1.1.0 \
  --repo bluedusk/html-magazine \
  --title "v1.1.0" \
  --notes "Your release notes here"
```
