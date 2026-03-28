#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo "  HTML Magazine Installer"
echo "  ======================="
echo ""

# --- Check for claude CLI ---
if ! command -v claude &>/dev/null; then
  echo "  Error: 'claude' CLI not found."
  echo "  Install Claude Code first: https://claude.ai/code"
  exit 1
fi

# --- Check and install dependency: ui-ux-pro-max ---
echo "  Checking dependency: ui-ux-pro-max..."

if claude plugin list 2>/dev/null | grep -qi "ui-ux-pro-max"; then
  echo "  ✓ ui-ux-pro-max is already installed"
else
  echo "  ⚙ ui-ux-pro-max not found — installing..."
  if claude plugin add ui-ux-pro-max 2>/dev/null; then
    echo "  ✓ ui-ux-pro-max installed successfully"
  else
    echo ""
    echo "  ⚠ Could not auto-install ui-ux-pro-max."
    echo "  Please install it manually:"
    echo ""
    echo "    claude plugin add ui-ux-pro-max"
    echo ""
    echo "  html-magazine requires ui-ux-pro-max for HTML rendering."
    echo "  Continuing with html-magazine installation..."
    echo ""
  fi
fi

echo ""

# --- Install html-magazine ---
echo "  Installing html-magazine..."

if claude plugin add "$SCRIPT_DIR" 2>/dev/null; then
  echo "  ✓ html-magazine installed"
else
  echo "  ⚠ Could not auto-install. Please run:"
  echo "    claude plugin add $SCRIPT_DIR"
fi

# --- Check Python dependencies for PDF export ---
echo ""
echo "  Checking optional dependencies..."

if command -v python3 &>/dev/null; then
  if python3 -c "import playwright" 2>/dev/null; then
    echo "  ✓ playwright (PDF export) available"
  else
    echo "  ℹ playwright not installed — PDF export will prompt to install when needed"
    echo "    To install now: pip install playwright && playwright install chromium"
  fi
else
  echo "  ℹ python3 not found — PDF export will not be available"
fi

echo ""
echo "  ✅ Done! Restart Claude Code to pick up the new skills."
echo ""
echo "  Usage:"
echo "    /html-magazine              — invoke via slash command"
echo "    'Turn this into a magazine' — or just ask naturally"
echo ""
