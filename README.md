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

## Available Settings Files

This repository provides two versions of the settings file:

1. **settings.json** - Clean configuration without comments, ideal for direct use
2. **settings.jsonc** - Same configuration with detailed comments explaining each section

The JSONC version is helpful when you want to understand and customize the settings, while the regular JSON version is cleaner for production use.

## Using These Settings

### Option 1: As Team/Project Settings
Copy `settings.json` (or `settings.jsonc` if you prefer the commented version) to your project's `.claude/settings.json`:

```bash
mkdir -p .claude
# For clean version without comments
curl -o .claude/settings.json https://raw.githubusercontent.com/dwillitzer/claude-settings/main/settings.json

# OR for commented version
curl -o .claude/settings.json https://raw.githubusercontent.com/dwillitzer/claude-settings/main/settings.jsonc
```

### Option 2: As Global User Settings
Copy to your home directory:

```bash
mkdir -p ~/.claude
# For clean version without comments
curl -o ~/.claude/settings.json https://raw.githubusercontent.com/dwillitzer/claude-settings/main/settings.json

# OR for commented version
curl -o ~/.claude/settings.json https://raw.githubusercontent.com/dwillitzer/claude-settings/main/settings.jsonc
```

### Option 3: As Local Overrides
For project-specific overrides, create `.claude/settings.local.json` and add to `.gitignore`:

```bash
echo ".claude/settings.local.json" >> .gitignore
```

## Permissions Overview

This configuration includes:

### Allow List (900+ patterns)
- **Docker & Container Orchestration**: Docker (containers, compose, volumes, networks), Kubernetes (kubectl, helm), Podman
- **Git & GitHub**: All git operations, GitHub CLI (gh) for PRs, issues, repos, workflows
- **Programming Languages & Package Managers**: 
  - JavaScript/TypeScript: npm, yarn, pnpm, bun, deno
  - Python: pip, pipenv, poetry, pyenv
  - Rust: cargo, rustc, rustup
  - Go: go mod, go build, go test
  - Ruby: gem, bundle, rbenv
  - Java: maven, gradle, javac
  - PHP: composer, php
- **Cloud Provider CLIs**: AWS CLI, Google Cloud SDK, Azure CLI, Vercel, Netlify, Heroku
- **Database Tools**: PostgreSQL, MySQL, MongoDB, SQLite, Redis with full client support
- **Development Environment**: Version managers (nvm, pyenv, rbenv), tmux, screen, direnv
- **File & Text Processing**: Read/write/edit files, grep, sed, awk, jq, yq, pipe operations
- **System Package Management**: apt, yum, dnf, brew, snap (with controlled sudo access)
- **Web & API Tools**: curl (all methods), wget, API testing, http-server
- **SSH/Remote Access**: SSH connections, SCP, rsync to specified servers
- **System Utilities**: Process management, network tools, system monitoring
- **Data Processing**: tar, zip, gzip, 7z, JSON/YAML processing
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
   - `"Bash(* | grep *)"` - Allow pipe operations
   - `"Bash(kubectl get pods)"` - Allow specific Kubernetes commands
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

### Sudo Permissions Warning

This configuration includes limited sudo access for package management only:
- `sudo apt install`, `sudo yum install`, etc. are allowed
- These are restricted to package installation commands
- **WARNING**: Review these permissions carefully for your environment
- Consider removing sudo permissions if not needed
- Never allow broad sudo access like `"Bash(sudo *)"` 

For maximum security, use a separate settings.local.json without sudo permissions for sensitive projects.

## Common Workflows

These permissions enable typical development workflows:

### Full-Stack Development
```bash
# Clone and setup a project
git clone https://github.com/user/project.git
cd project
npm install

# Run development servers
npm run dev
# or
docker-compose up -d

# Check logs
docker logs app-container | grep error
tail -f logs/app.log
```

### Working with GitHub
```bash
# Create a PR from Claude Code
gh pr create --title "Fix bug" --body "Description"

# Review PR status
gh pr status
gh pr checks

# Work with issues
gh issue list --label bug
gh issue create --title "New feature"
```

### Cloud Deployments
```bash
# Deploy to AWS
aws s3 sync ./build s3://my-bucket
aws cloudformation deploy --template-file template.yml

# Deploy to Vercel
vercel --prod

# Google Cloud operations
gcloud app deploy
gcloud compute instances list
```

### Database Operations
```bash
# PostgreSQL backup
pg_dump -h localhost -U user dbname > backup.sql

# MongoDB operations
mongosh --eval "db.collection.find()"
mongodump --db mydb --out ./backup

# Redis operations
redis-cli SET key value
redis-cli GET key
```

### Container Orchestration
```bash
# Kubernetes deployment
kubectl apply -f deployment.yaml
kubectl get pods
kubectl logs pod-name

# Helm charts
helm install myapp ./chart
helm upgrade myapp ./chart
```

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