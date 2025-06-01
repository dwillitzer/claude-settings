#!/usr/bin/env python3
"""
Claude Code Permission Wrapper with Debug Logging
"""

import json
import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

# Original claude binary
CLAUDE_ORIGINAL = "/Users/devops/.npm-global/bin/claude"
DEBUG_LOG = "/tmp/claude-wrapper-debug.log"

def log_debug(message):
    """Log debug information"""
    with open(DEBUG_LOG, 'a') as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

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
    
    log_debug("Loading settings from:")
    
    # Load in reverse order so higher precedence overwrites
    for location in reversed(settings_locations):
        if os.path.exists(location):
            try:
                with open(location, 'r') as f:
                    data = json.load(f)
                    permissions = data.get('permissions', {})
                    
                    # Add patterns (higher precedence files can override)
                    if 'allow' in permissions:
                        allow_count = len(permissions['allow'])
                        allow_patterns = permissions['allow'] + allow_patterns
                        log_debug(f"  {location}: {allow_count} allow patterns")
                    if 'deny' in permissions:
                        deny_count = len(permissions['deny'])
                        deny_patterns = permissions['deny'] + deny_patterns
                        log_debug(f"  {location}: {deny_count} deny patterns")
                        
            except Exception as e:
                log_debug(f"  Failed to load {location}: {e}")
    
    # Remove duplicates while preserving order
    allow_patterns = list(dict.fromkeys(allow_patterns))
    deny_patterns = list(dict.fromkeys(deny_patterns))
    
    log_debug(f"Total loaded: {len(allow_patterns)} allow, {len(deny_patterns)} deny patterns")
    
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
    log_debug(f"Checking args: {args}")
    
    # Check if already has --auto-approve
    if '--auto-approve' in args:
        log_debug("Already has --auto-approve, skipping")
        return False
    
    # Load settings
    allow_patterns, deny_patterns = load_settings()
    
    # Look for Bash commands in arguments
    # This is simplified - in reality we'd need to parse the full command structure
    command_str = ' '.join(args)
    log_debug(f"Command string: '{command_str}'")
    
    # Check deny patterns first (they take precedence)
    for pattern_str in deny_patterns:
        tool, pattern = extract_pattern(pattern_str)
        if tool == 'Bash' and pattern:
            if pattern_matches(pattern, command_str):
                log_debug(f"DENIED by pattern: {pattern_str}")
                return False  # Denied - don't auto-approve
    
    # Check allow patterns
    for pattern_str in allow_patterns:
        tool, pattern = extract_pattern(pattern_str)
        if tool == 'Bash' and pattern:
            if pattern_matches(pattern, command_str):
                log_debug(f"ALLOWED by pattern: {pattern_str}")
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
                    log_debug(f"Safe command '{safe_cmd}' found but DENIED by: {pattern_str}")
                    return False
            log_debug(f"ALLOWED by safe command: {safe_cmd}")
            return True
    
    log_debug("No matching patterns found")
    return False

def main():
    args = sys.argv[1:]
    
    log_debug("="*60)
    log_debug(f"Claude wrapper called with args: {sys.argv}")
    
    if should_auto_approve(args):
        # Add --auto-approve flag
        cmd = [CLAUDE_ORIGINAL, '--auto-approve'] + args
        log_debug(f"AUTO-APPROVING with command: {cmd}")
    else:
        # Run normally
        cmd = [CLAUDE_ORIGINAL] + args
        log_debug(f"Running normally with command: {cmd}")
    
    # Execute claude with the same environment
    os.execvp(cmd[0], cmd)

if __name__ == '__main__':
    main()