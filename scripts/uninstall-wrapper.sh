#!/bin/bash

# Uninstall Claude Code Permission Wrapper

echo "Claude Code Permission Wrapper Uninstaller"
echo "========================================="
echo ""

INSTALL_DIR="/usr/local/bin"
WRAPPER_PATH="$INSTALL_DIR/claude"

if [ -L "$WRAPPER_PATH" ]; then
    echo "Found wrapper at: $WRAPPER_PATH"
    
    # Check if we need sudo
    if [ -w "$INSTALL_DIR" ]; then
        rm "$WRAPPER_PATH"
    else
        echo "Need sudo permission to remove from $INSTALL_DIR"
        sudo rm "$WRAPPER_PATH"
    fi
    
    echo "✓ Wrapper removed"
    echo ""
    echo "Claude Code will now use the original command at:"
    which claude
else
    echo "No wrapper found at $WRAPPER_PATH"
fi