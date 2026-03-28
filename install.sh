#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_NAME="html-magazine"

echo ""
echo "  HTML Magazine Installer"
echo "  ======================="
echo "  Repo: $REPO_DIR"
echo ""

# --- Detect available agents ---
agents=()
command -v claude &>/dev/null && agents+=("claude")
command -v gemini &>/dev/null && agents+=("gemini")
command -v gh &>/dev/null     && agents+=("copilot")
command -v codex &>/dev/null  && agents+=("codex")

if [ ${#agents[@]} -eq 0 ]; then
  echo "  No supported agents detected (claude, gemini, gh, codex)."
  echo "  You can install manually — see README.md"
  exit 0
fi

echo "  Detected: ${agents[*]}"
echo ""
echo "  Choose install scope:"
echo ""
echo "    1) User-level  — available in all projects (recommended)"
echo "    2) Project-level — available only in current project"
echo "    3) Both"
echo ""
read -rp "  Enter choice [1]: " choice
choice="${choice:-1}"

installed=0

# --- Helper: symlink skill into a directory ---
install_skill() {
  local target_dir="$1"
  local label="$2"
  local link="$target_dir/$SKILL_NAME"

  mkdir -p "$target_dir"
  if [ -L "$link" ]; then
    current="$(readlink "$link" 2>/dev/null || true)"
    if [ "$current" = "$REPO_DIR" ]; then
      echo "  ✓ $label — already installed"
    else
      rm -f "$link"
      ln -s "$REPO_DIR" "$link"
      echo "  ✓ $label — updated symlink"
    fi
  elif [ -e "$link" ]; then
    echo "  ✗ $label — path exists but is not a symlink, skipping"
  else
    ln -s "$REPO_DIR" "$link"
    echo "  ✓ $label — installed"
  fi
  installed=$((installed + 1))
}

# --- Helper: install as Claude Code plugin ---
install_claude_plugin() {
  # Install dependency: ui-ux-pro-max
  echo "  Checking dependency: ui-ux-pro-max..."
  if claude plugin list 2>/dev/null | grep -qi "ui-ux-pro-max"; then
    echo "  ✓ ui-ux-pro-max already installed"
  else
    echo "  ⚙ Installing ui-ux-pro-max..."
    if claude plugin add ui-ux-pro-max 2>/dev/null; then
      echo "  ✓ ui-ux-pro-max installed"
    else
      echo "  ⚠ Could not auto-install ui-ux-pro-max."
      echo "    Please install manually: claude plugin add ui-ux-pro-max"
    fi
  fi

  # Install html-magazine
  if claude plugin add "$REPO_DIR" 2>/dev/null; then
    echo "  ✓ Claude Code plugin installed"
  else
    echo "  ⚠ Could not auto-install. Run: claude plugin add $REPO_DIR"
  fi
  installed=$((installed + 1))
}

echo ""

# --- User-level installs ---
if [ "$choice" = "1" ] || [ "$choice" = "3" ]; then
  echo "  Installing user-level..."
  echo ""

  for agent in "${agents[@]}"; do
    case "$agent" in
      claude)
        install_claude_plugin
        ;;
      gemini)
        install_skill "$HOME/.gemini/skills" "~/.gemini/skills (Gemini CLI)"
        ;;
      copilot)
        # Copilot has no user-level skills path
        echo "  ℹ Copilot — user-level not supported, use project-level"
        ;;
      codex)
        install_skill "$HOME/.codex/skills" "~/.codex/skills (OpenAI Codex)"
        ;;
    esac
  done
  echo ""
fi

# --- Project-level installs ---
if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
  echo "  Installing project-level..."
  echo ""

  for agent in "${agents[@]}"; do
    case "$agent" in
      claude)
        install_claude_plugin
        ;;
      gemini)
        install_skill ".gemini/skills" ".gemini/skills (Gemini CLI)"
        ;;
      copilot)
        install_skill ".github/skills" ".github/skills (GitHub Copilot)"
        ;;
      codex)
        install_skill ".codex/skills" ".codex/skills (OpenAI Codex)"
        ;;
    esac
  done
  echo ""
fi

# --- Check optional dependencies ---
echo "  Checking optional dependencies..."

if command -v python3 &>/dev/null; then
  if python3 -c "import playwright" 2>/dev/null; then
    echo "  ✓ playwright (PDF export) available"
  else
    echo "  ℹ playwright not installed — PDF export will prompt when needed"
    echo "    To install: pip install playwright && playwright install chromium"
  fi
else
  echo "  ℹ python3 not found — PDF export will not be available"
fi

echo ""
echo "  ✅ Done. $installed path(s) configured."
echo "  Restart your agent to pick up the new skill."
echo ""
echo "  Usage:"
echo "    /html-magazine              — slash command (Claude Code)"
echo "    'Turn this into a magazine' — or just ask naturally"
echo ""
