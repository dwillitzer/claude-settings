# Claude Code Settings

This repository contains comprehensive permission settings for Claude Code to enable productive development workflows while maintaining security.

## What is this?

These settings configure which commands and operations Claude Code can perform without requiring manual approval. The configuration follows the principle of least privilege while enabling common development tasks.

## How to use

1. Copy `settings.json` to your Claude Code configuration directory:
   - On macOS/Linux: `~/.config/claude/`
   - On Windows: `%APPDATA%\claude\`

2. Restart Claude Code for the settings to take effect.

## What's included?

### Allowed operations:
- **Docker**: Full container management, compose operations, volume management
- **Git**: All version control operations except force pushes to main/master
- **SSH**: Access to specific servers (currently configured for gmktec-k9)
- **File operations**: Reading, editing, searching, and basic file management
- **Package management**: npm, apt, and other package managers
- **Network tools**: curl, wget, and API testing utilities
- **Development tools**: Node.js, build tools, testing frameworks
- **System monitoring**: Process management, logs, system status

### Denied operations:
- Destructive system operations (rm -rf /, format drives, etc.)
- User account modifications
- Credential theft attempts
- Network backdoors and reverse shells
- Cryptocurrency mining
- Force pushes to main/master branches

## Customization

You can customize these settings for your needs:

1. **Add new servers**: Update SSH patterns to include your servers
2. **Add new tools**: Include patterns for additional development tools
3. **Restrict further**: Add more patterns to the deny list
4. **Domain access**: Add domains to WebFetch permissions as needed

## Security considerations

- These settings allow broad development capabilities
- Review and adjust based on your security requirements
- Regularly audit the allow list to ensure it matches your needs
- Consider using more restrictive settings for production environments

## Contributing

Feel free to submit PRs with improvements or additional safety measures.

## License

MIT License - Use at your own risk