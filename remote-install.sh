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
  mkdir -p "$(dirname "$INSTALL_DIR")"
  git clone "https://github.com/${REPO}.git" "$INSTALL_DIR" 2>/dev/null
  echo "  ✓ Cloned to $INSTALL_DIR"
fi

echo ""

# --- Run the local installer ---
cd "$INSTALL_DIR"
bash install.sh
