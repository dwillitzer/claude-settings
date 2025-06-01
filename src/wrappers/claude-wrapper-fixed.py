#!/usr/bin/env python3
"""
Claude Code Permission Wrapper - Fixed Version

This wrapper automatically adds --auto-approve flag when starting Claude
if no explicit approval flags are present.
"""

import os
import sys

# Original claude binary
CLAUDE_ORIGINAL = "/Users/devops/.npm-global/bin/claude"

def main():
    args = sys.argv[1:]
    
    # Check if any approval-related flags are already present
    approval_flags = ['--auto-approve', '--no-auto-approve', '--ask']
    has_approval_flag = any(flag in args for flag in approval_flags)
    
    # If no approval flags, add --auto-approve
    if not has_approval_flag:
        cmd = [CLAUDE_ORIGINAL, '--auto-approve'] + args
    else:
        cmd = [CLAUDE_ORIGINAL] + args
    
    # Execute claude with the same environment
    os.execvp(cmd[0], cmd)

if __name__ == '__main__':
    main()