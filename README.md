# Claude Code Settings

This repository contains comprehensive permission settings for Claude Code, Anthropic's AI-powered coding assistant.

## Settings Hierarchy and Precedence

According to the [official Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/settings), settings are applied in the following order of precedence (from highest to lowest):

1. **Enterprise policies**
   - macOS: `/Library/Application Support/ClaudeCode/policies.json`
   - Linux/Windows WSL: `/etc/claude-code/policies.json`
   - These are system-wide policies that cannot be overridden

2. **Command line arguments**
   - Flags passed when running Claude Code
   - Example: `claude --allow "Bash(npm test)"`

3. **Local project settings** 
   - Location: `.claude/settings.local.json`
   - Project-specific overrides for individual developers
   - Should be added to `.gitignore`

4. **Shared project settings**
   - Location: `.claude/settings.json` 
   - Team/project settings checked into version control
   - This is what this repository provides

5. **User/Global settings**
   - Location: `~/.claude/settings.json`
   - Personal preferences across all projects
   - Lowest precedence

## How Settings Merge

Settings files are merged together, with higher precedence files overriding values from lower precedence files. This allows:

- Users to set personal defaults globally
- Teams to share common project settings
- Individual developers to override both for their local environment
- Enterprises to enforce security policies

## Using These Settings

### Option 1: As Team/Project Settings
Copy `settings.json` to your project's `.claude/settings.json`:

```bash
mkdir -p .claude
curl -o .claude/settings.json https://raw.githubusercontent.com/dwillitzer/claude-settings/main/settings.json
```

### Option 2: As Global User Settings
Copy to your home directory:

```bash
mkdir -p ~/.claude
curl -o ~/.claude/settings.json https://raw.githubusercontent.com/dwillitzer/claude-settings/main/settings.json
```

### Option 3: As Local Overrides
For project-specific overrides, create `.claude/settings.local.json` and add to `.gitignore`:

```bash
echo ".claude/settings.local.json" >> .gitignore
```

## Permissions Overview

This configuration includes:

### Allow List (600+ patterns)
- **Docker operations**: Container management, logs, exec, compose, volumes, networks, images
- **Git operations**: All common git commands and workflows (status, add, commit, push, pull, branch, merge, etc.)
- **SSH/Remote access**: SSH connections, SCP, rsync to specified servers
- **File operations**: Read, write, edit, search, manipulate files (cat, grep, sed, awk, etc.)
- **Development tools**: npm, node, python, make, yarn, pnpm, testing frameworks (jest, pytest)
- **System utilities**: Process management, network tools, system info (ps, lsof, netstat, df, du)
- **Web tools**: curl, wget, API interactions, http-server
- **Database tools**: psql, pg_dump, redis-cli operations
- **Claude-specific tools**: Read, Edit, MultiEdit, Glob, Grep, WebFetch, WebSearch, TodoRead, TodoWrite, Task

### Deny List (Security-focused)
- **Destructive operations**: Prevents rm -rf /, format commands, mass deletion
- **Security risks**: Blocks reverse shells, credential theft attempts, malicious downloads
- **System damage**: Prevents shutdown, reboot, firewall disabling, kernel modifications
- **Data exposure**: Blocks credential searches, cloud metadata access, password history
- **Malicious activities**: Prevents crypto mining, network backdoors, process injection
- **Dangerous Docker**: Blocks privileged containers, host PID/network access, socket mounting
- **User management**: Prevents password changes, user account modifications
- **Log deletion**: Blocks removal of system logs and audit trails

## Customization

To customize for your needs:

1. Fork this repository
2. Edit `settings.json` to add/remove permissions
3. Use the Tool(specifier) format:
   - `"Bash(git *)"` - Allow all git commands
   - `"Bash(rm -rf /)"` - Deny specific dangerous commands
   - `"Read(**)"` - Allow reading any file
   - `"WebFetch(domain:*.example.com)"` - Allow fetching from specific domains

Common customizations:
- **Add new servers**: Update SSH patterns to include your servers
- **Add new tools**: Include patterns for additional development tools
- **Restrict further**: Add more patterns to the deny list
- **Domain access**: Add domains to WebFetch permissions as needed

## Security Considerations

- These settings are permissive for development productivity
- Review and adjust based on your security requirements
- Use enterprise policies for enforcing stricter controls
- Always use `settings.local.json` for sensitive project-specific settings
- Regularly audit the allow list to ensure it matches your needs
- Consider using more restrictive settings for production environments

## References

- [Claude Code Settings Documentation](https://docs.anthropic.com/en/docs/claude-code/settings) - Official settings hierarchy and configuration guide
- [Claude Code Security Documentation](https://docs.anthropic.com/en/docs/claude-code/security) - Security best practices and permission model
- [Claude Code CLI Usage](https://docs.anthropic.com/en/docs/claude-code/cli-usage) - Command line options and flags

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

Please ensure any new patterns follow the existing format and include both allow and deny considerations.

## License

MIT License - This configuration is provided as-is for the Claude Code community. Use at your own discretion.