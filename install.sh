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
install_skill_symlink() {
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

# --- Helper: install ui-ux-pro-max for a given agent ---
install_uiux_dependency() {
  local agent="$1"

  case "$agent" in
    claude)
      if claude plugin list 2>/dev/null | grep -qi "ui-ux-pro-max"; then
        echo "  ✓ ui-ux-pro-max already installed (Claude Code)"
      else
        echo "  ⚙ Installing ui-ux-pro-max for Claude Code..."
        if claude plugin add ui-ux-pro-max 2>/dev/null; then
          echo "  ✓ ui-ux-pro-max installed (Claude Code)"
        else
          echo "  ⚠ Could not auto-install ui-ux-pro-max for Claude Code."
          echo "    Run manually: claude plugin add ui-ux-pro-max"
        fi
      fi
      ;;
    gemini|copilot|codex)
      # Map agent name to uipro CLI name
      local uipro_name="$agent"

      # Check if already installed by looking for the skill directory
      local skill_dir=""
      case "$agent" in
        gemini)  skill_dir="$HOME/.gemini/skills/ui-ux-pro-max" ;;
        copilot) skill_dir=".github/skills/ui-ux-pro-max" ;;
        codex)   skill_dir="$HOME/.codex/skills/ui-ux-pro-max" ;;
      esac

      if [ -n "$skill_dir" ] && [ -d "$skill_dir" ]; then
        echo "  ✓ ui-ux-pro-max already installed ($agent)"
      else
        echo "  ⚙ Installing ui-ux-pro-max for $agent..."
        if command -v npx &>/dev/null; then
          if npx uipro-cli init --ai "$uipro_name" 2>/dev/null; then
            echo "  ✓ ui-ux-pro-max installed ($agent)"
          else
            echo "  ⚠ Could not install ui-ux-pro-max for $agent."
            echo "    Run manually: npx uipro-cli init --ai $uipro_name"
          fi
        else
          echo "  ⚠ npx not found — cannot install ui-ux-pro-max for $agent."
          echo "    Install Node.js, then run: npx uipro-cli init --ai $uipro_name"
        fi
      fi
      ;;
  esac
}

# --- Helper: install html-magazine as Claude Code plugin ---
install_claude_plugin() {
  if claude plugin add "$REPO_DIR" 2>/dev/null; then
    echo "  ✓ html-magazine installed (Claude Code plugin)"
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
    echo "  ── $agent ──"

    # Install dependency first
    install_uiux_dependency "$agent"

    # Install html-magazine
    case "$agent" in
      claude)
        install_claude_plugin
        ;;
      gemini)
        install_skill_symlink "$HOME/.gemini/skills" "~/.gemini/skills (Gemini CLI)"
        ;;
      copilot)
        echo "  ℹ Copilot — user-level not supported, use project-level"
        ;;
      codex)
        install_skill_symlink "$HOME/.codex/skills" "~/.codex/skills (OpenAI Codex)"
        ;;
    esac
    echo ""
  done
fi

# --- Project-level installs ---
if [ "$choice" = "2" ] || [ "$choice" = "3" ]; then
  echo "  Installing project-level..."
  echo ""

  for agent in "${agents[@]}"; do
    echo "  ── $agent ──"

    # Install dependency first
    install_uiux_dependency "$agent"

    # Install html-magazine
    case "$agent" in
      claude)
        install_claude_plugin
        ;;
      gemini)
        install_skill_symlink ".gemini/skills" ".gemini/skills (Gemini CLI)"
        ;;
      copilot)
        install_skill_symlink ".github/skills" ".github/skills (GitHub Copilot)"
        ;;
      codex)
        install_skill_symlink ".codex/skills" ".codex/skills (OpenAI Codex)"
        ;;
    esac
    echo ""
  done
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
