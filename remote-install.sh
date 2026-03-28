#!/usr/bin/env bash
set -euo pipefail

# HTML Magazine — Remote Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/bluedusk/html-magazine/main/remote-install.sh | bash

REPO="bluedusk/html-magazine"
INSTALL_DIR="${HOME}/.claude/plugins/marketplaces/html-magazine"

echo ""
echo "  HTML Magazine — Remote Installer"
echo "  ================================="
echo ""

# --- Check for claude CLI ---
if ! command -v claude &>/dev/null; then
  echo "  Error: 'claude' CLI not found."
  echo "  Install Claude Code first: https://claude.ai/code"
  exit 1
fi

# --- Check for git ---
if ! command -v git &>/dev/null; then
  echo "  Error: 'git' not found. Please install git first."
  exit 1
fi

# --- Clone or update ---
if [ -d "$INSTALL_DIR" ]; then
  echo "  Updating existing installation..."
  cd "$INSTALL_DIR"
  git pull --ff-only origin main 2>/dev/null || {
    echo "  ⚠ Could not update — resetting to latest..."
    git fetch origin main
    git reset --hard origin/main
  }
  echo "  ✓ Updated to latest version"
else
  echo "  Cloning html-magazine..."
  git clone "https://github.com/${REPO}.git" "$INSTALL_DIR" 2>/dev/null
  echo "  ✓ Cloned to $INSTALL_DIR"
fi

echo ""

# --- Install dependency: ui-ux-pro-max ---
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

echo ""

# --- Install html-magazine plugin ---
echo "  Installing html-magazine plugin..."

if claude plugin add "$INSTALL_DIR" 2>/dev/null; then
  echo "  ✓ html-magazine installed"
else
  echo "  ⚠ Could not auto-install. Please run:"
  echo "    claude plugin add $INSTALL_DIR"
fi

echo ""
echo "  ✅ Done! Restart Claude Code to pick up the new skills."
echo ""
echo "  Usage:"
echo "    /html-magazine              — invoke via slash command"
echo "    'Turn this into a magazine' — or just ask naturally"
echo ""
