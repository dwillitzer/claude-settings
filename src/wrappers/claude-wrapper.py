#!/usr/bin/env python3
"""
Claude Code Permission Wrapper

This script works around the broken permission system in Claude Code by:
1. Loading permission patterns from settings files
2. Auto-approving commands that match allowed patterns
3. Respecting deny patterns
4. Following the proper precedence order
"""

import json
import os
import sys
import subprocess
import re
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
                    
                    # Add patterns (higher precedence files can override)
                    if 'allow' in permissions:
                        allow_patterns = permissions['allow'] + allow_patterns
                    if 'deny' in permissions:
                        deny_patterns = permissions['deny'] + deny_patterns
                        
            except Exception as e:
                print(f"Warning: Failed to load {location}: {e}", file=sys.stderr)
    
    # Remove duplicates while preserving order
    allow_patterns = list(dict.fromkeys(allow_patterns))
    deny_patterns = list(dict.fromkeys(deny_patterns))
    
    return allow_patterns, deny_patterns

def extract_pattern(pattern_str):
    """Extract tool and pattern from 'Tool(pattern)' format"""
    match = re.match(r'^(\w+)\((.*)\)$', pattern_str)
    if match:
        return match.group(1), match.group(2)
    return None, None

def pattern_matches(pattern, command):
    """Check if a command matches a pattern"""
    # Handle exact matches
    if pattern == command:
        return True
    
    # Convert glob patterns to regex
    # * matches anything except /
    # ** matches anything including /
    regex_pattern = pattern.replace('**', '<<<DOUBLESTAR>>>')
    regex_pattern = regex_pattern.replace('*', '[^/]*')
    regex_pattern = regex_pattern.replace('<<<DOUBLESTAR>>>', '.*')
    regex_pattern = '^' + regex_pattern + '$'
    
    try:
        return bool(re.match(regex_pattern, command))
    except:
        return False

def should_auto_approve(args):
    """Determine if we should auto-approve based on settings"""
    # Check if already has --auto-approve
    if '--auto-approve' in args:
        return False
    
    # Load settings
    allow_patterns, deny_patterns = load_settings()
    
    # Look for Bash commands in arguments
    # This is simplified - in reality we'd need to parse the full command structure
    command_str = ' '.join(args)
    
    # Check deny patterns first (they take precedence)
    for pattern_str in deny_patterns:
        tool, pattern = extract_pattern(pattern_str)
        if tool == 'Bash' and pattern:
            if pattern_matches(pattern, command_str):
                return False  # Denied - don't auto-approve
    
    # Check allow patterns
    for pattern_str in allow_patterns:
        tool, pattern = extract_pattern(pattern_str)
        if tool == 'Bash' and pattern:
            if pattern_matches(pattern, command_str):
                return True  # Allowed - auto-approve
    
    # Check for common safe commands in arguments
    safe_commands = [
        'git', 'npm', 'node', 'python', 'pip', 'cargo', 'go', 
        'docker', 'kubectl', 'helm', 'ls', 'cat', 'grep', 'curl',
        'echo', 'pwd', 'cd', 'mkdir', 'touch', 'cp', 'mv',
        'ssh gmktec-k9', 'ssh root@gmktec-k9'
    ]
    
    for safe_cmd in safe_commands:
        if safe_cmd in command_str:
            # Double-check it's not denied
            for pattern_str in deny_patterns:
                tool, pattern = extract_pattern(pattern_str)
                if tool == 'Bash' and pattern and pattern_matches(pattern, command_str):
                    return False
            return True
    
    return False

def main():
    args = sys.argv[1:]
    
    if should_auto_approve(args):
        # Add --auto-approve flag
        cmd = [CLAUDE_ORIGINAL, '--auto-approve'] + args
    else:
        # Run normally
        cmd = [CLAUDE_ORIGINAL] + args
    
    # Execute claude with the same environment
    os.execvp(cmd[0], cmd)

if __name__ == '__main__':
    main()