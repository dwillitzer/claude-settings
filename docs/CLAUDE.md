# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository contains comprehensive permission settings for Claude Code. The main file is `settings.json` which defines allowed and denied operations for Claude Code sessions.

## Key Architecture

### Settings Structure
The `settings.json` file contains a single root object with a `permissions` key that has two arrays:
- `allow`: Patterns for permitted operations (1000+ patterns)
- `deny`: Patterns for blocked operations (security-focused)

Pattern format: `"Tool(specifier)"` where Tool is the Claude tool name (Bash, Read, WebFetch, etc.) and specifier is the pattern to match.

### Settings Hierarchy
Claude Code applies settings in order of precedence:
1. Enterprise policies: `/Library/Application Support/ClaudeCode/policies.json` (macOS)
2. Command line arguments
3. Local project settings: `.claude/settings.local.json`
4. Shared project settings: `.claude/settings.json`
5. User/Global settings: `~/.claude/settings.json`

## Common Development Tasks

### Validating JSON Syntax
```bash
# Check if settings.json is valid JSON
python -m json.tool settings.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Pretty-print and validate
python -m json.tool settings.json > settings.formatted.json
```

### Testing Permission Patterns
When adding new patterns, ensure they follow the correct format:
- Bash commands: `"Bash(command pattern)"`
- File operations: `"Read(**)"`, `"Edit(**)"`, `"Write(**)"` 
- Web operations: `"WebFetch(domain:example.com)"`

### Deploying Settings
```bash
# Deploy as system-wide policy (macOS, requires sudo)
sudo ln -sf /path/to/settings.json "/Library/Application Support/ClaudeCode/policies.json"

# Deploy as user global settings
mkdir -p ~/.claude
cp settings.json ~/.claude/settings.json

# Deploy as project settings
mkdir -p .claude
cp settings.json .claude/settings.json
```

## Important Considerations

1. **Personal Settings**: Keep personal server names and domains in separate files (`.claude/settings.local.json` or `~/.claude/settings.json`), not in the main `settings.json` which is for community use.

2. **Security**: The deny list is critical for preventing malicious operations. Always test new patterns carefully and consider security implications.

3. **Pattern Specificity**: More specific patterns take precedence. For example, `"Bash(rm -rf /)"` in deny will override `"Bash(rm *)"` in allow.

4. **Merging Behavior**: Settings files merge additively - patterns from multiple files combine rather than replace each other.