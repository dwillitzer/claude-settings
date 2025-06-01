#!/bin/bash

# Install Claude Code Permission Wrapper

echo "Claude Code Permission Wrapper Installer"
echo "======================================="
echo ""
echo "This will install a wrapper that fixes the broken permission system"
echo "by auto-approving commands that match your configured patterns."
echo ""

# Check if claude is installed
if ! command -v claude &> /dev/null; then
    echo "Error: Claude Code is not installed or not in PATH"
    echo "Please install it first with: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check which wrapper to use
if command -v python3 &> /dev/null; then
    WRAPPER="$SCRIPT_DIR/claude-wrapper.py"
    echo "Using Python wrapper (more accurate pattern matching)"
else
    WRAPPER="$SCRIPT_DIR/claude-wrapper.sh"
    echo "Using Bash wrapper (basic pattern matching)"
fi

# Create a symlink in a directory that's earlier in PATH than npm's bin
INSTALL_DIR="/usr/local/bin"

# Check if we can write to /usr/local/bin
if [ -w "$INSTALL_DIR" ]; then
    ln -sf "$WRAPPER" "$INSTALL_DIR/claude"
    echo "✓ Wrapper installed to $INSTALL_DIR/claude"
else
    echo "Need sudo permission to install to $INSTALL_DIR"
    sudo ln -sf "$WRAPPER" "$INSTALL_DIR/claude"
    echo "✓ Wrapper installed to $INSTALL_DIR/claude"
fi

# Verify installation
echo ""
echo "Verifying installation..."

# Check which claude will be used
WHICH_CLAUDE=$(which claude)
if [[ "$WHICH_CLAUDE" == "$INSTALL_DIR/claude" ]]; then
    echo "✓ Wrapper is now the default 'claude' command"
    echo ""
    echo "Installation complete!"
    echo ""
    echo "The wrapper will:"
    echo "- Load your permission patterns from settings files"
    echo "- Auto-approve commands matching your allow patterns"
    echo "- Respect deny patterns"
    echo "- Fall back to normal prompting for other commands"
    echo ""
    echo "To uninstall, run: rm $INSTALL_DIR/claude"
else
    echo "⚠ Warning: claude is still pointing to: $WHICH_CLAUDE"
    echo "You may need to update your PATH or restart your terminal"
fi