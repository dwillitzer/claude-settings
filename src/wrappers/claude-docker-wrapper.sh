#!/bin/bash

# Claude Code Docker Wrapper
# Runs Claude in a Docker container to use --dangerously-skip-permissions

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Create a temporary directory for the session
SESSION_DIR=$(mktemp -d)
echo "Session directory: $SESSION_DIR"

# Run Claude in Docker with permission bypass
docker run -it --rm \
    -v "$SESSION_DIR:/workspace" \
    -v "$HOME/.claude:/root/.claude:ro" \
    -v "/Library/Application Support/ClaudeCode:/Library/Application Support/ClaudeCode:ro" \
    -e ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY}" \
    --network none \
    node:20-slim \
    bash -c "
        npm install -g @anthropic-ai/claude-code && \
        cd /workspace && \
        claude --dangerously-skip-permissions $*
    "

# Cleanup
rm -rf "$SESSION_DIR"