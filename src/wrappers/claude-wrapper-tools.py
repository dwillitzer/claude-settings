#!/usr/bin/env python3
"""
Claude Code Permission Wrapper using --allowedTools flag

This wrapper loads your permission patterns and passes them to Claude
using the --allowedTools and --disallowedTools flags.
"""

import json
import os
import sys
from pathlib import Path

# Original claude binary
CLAUDE_ORIGINAL = "/Users/devops/.npm-global/bin/claude"

def load_settings():
    """Load settings from all locations in precedence order"""
    settings_locations = [
        # Enterprise policies (highest precedence)
        "/Library/Application Support/ClaudeCode/policies.json",
        # User settings (lowest precedence)
        Path.home() / ".claude" / "settings.json",
    ]
    
    allow_patterns = []
    deny_patterns = []
    
    # Load in reverse order so higher precedence overwrites
    for location in reversed(settings_locations):
        if os.path.exists(location):
            try:
                with open(location, 'r') as f:
                    data = json.load(f)
                    permissions = data.get('permissions', {})
                    
                    if 'allow' in permissions:
                        allow_patterns.extend(permissions['allow'])
                    if 'deny' in permissions:
                        deny_patterns.extend(permissions['deny'])
                        
            except Exception:
                pass
    
    # Remove duplicates while preserving order
    allow_patterns = list(dict.fromkeys(allow_patterns))
    deny_patterns = list(dict.fromkeys(deny_patterns))
    
    return allow_patterns, deny_patterns

def main():
    args = sys.argv[1:]
    
    # Check if tool flags are already present
    has_allowed_tools = any(arg.startswith('--allowedTools') for arg in args)
    has_disallowed_tools = any(arg.startswith('--disallowedTools') for arg in args)
    
    cmd = [CLAUDE_ORIGINAL]
    
    # Add permission flags if not already present
    if not has_allowed_tools or not has_disallowed_tools:
        allow_patterns, deny_patterns = load_settings()
        
        if allow_patterns and not has_allowed_tools:
            # Pass all allow patterns as a single argument
            cmd.extend(['--allowedTools', ' '.join(allow_patterns)])
        
        if deny_patterns and not has_disallowed_tools:
            # Pass all deny patterns as a single argument
            cmd.extend(['--disallowedTools', ' '.join(deny_patterns)])
    
    # Add original arguments
    cmd.extend(args)
    
    # Execute claude with the same environment
    os.execvp(cmd[0], cmd)

if __name__ == '__main__':
    main()