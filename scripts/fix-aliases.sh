#!/bin/bash

# Remove incorrect aliases
sed -i.bak '/# Claude Code Aliases/,/^$/d' ~/.zshrc

echo "Removed incorrect aliases from ~/.zshrc"
echo ""
echo "Unfortunately, Claude Code has no auto-approve functionality."
echo "The permission system is broken as documented in:"
echo "https://github.com/anthropics/claude-code/issues/1410"
echo ""
echo "Current workarounds:"
echo "1. Click 'Yes' on every prompt (annoying but secure)"
echo "2. Use Claude in a Docker container with --dangerously-skip-permissions"
echo "3. Wait for Anthropic to fix the permission system"
echo ""
echo "The settings files ARE properly configured, but Claude ignores them."