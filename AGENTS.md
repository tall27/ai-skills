# AI Skills Repository

This repository contains reusable AI agent skills following the [Agent Skills](https://agentskills.io) open standard and [AGENTS.md](https://agents.md) conventions.

## Project Structure

```
ai-skills/
├── AGENTS.md          # This file - instructions for AI agents
├── README.md          # Human documentation
├── install.py         # Cross-platform installer script
└── skills/            # All skills live here
    └── <skill-name>/
        └── SKILL.md   # Skill definition (YAML frontmatter + instructions)
```

## Working with This Repository

### Adding a New Skill

1. Create a directory under `skills/` with the skill name (lowercase, hyphens allowed)
2. Add a `SKILL.md` file with required YAML frontmatter:
   ```yaml
   ---
   name: skill-name
   description: Brief description (1-1024 chars)
   ---
   ```
3. Add instructions in markdown below the frontmatter
4. Update `README.md` to include the new skill in the catalog

### Skill Naming Rules

- 1-64 characters
- Lowercase alphanumeric with single hyphen separators
- No leading/trailing hyphens
- No consecutive hyphens (`--`)
- Must match directory name

Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`

### Testing install.py

```bash
# List available skills
python install.py --list

# Dry run installation
python install.py --all --dry-run

# Install to specific target
python install.py --all --target agents
```

### Code Standards

- Python scripts should be Python 3.10+ compatible
- Use type hints where applicable
- Keep SKILL.md files focused and actionable
- No credentials or secrets in the repository

## Installation Targets

The installer copies skills to these standard locations:

| Target | Path | Used By |
|--------|------|---------|
| `claude` | `~/.claude/skills/` | Claude Code |
| `opencode` | `~/.config/opencode/skills/` | OpenCode |
| `agents` | `~/.agents/skills/` | AGENTS.md compatible tools (Codex, Jules, Cursor, etc.) |

## Importing External Skills

Use the `skill-import` skill to add skills from other GitHub repositories:

1. Provide the GitHub URL or path
2. The skill will be downloaded and committed to this repository
3. README.md should be updated with the new skill

## Commit Message Format

- `feat: add <skill-name> skill` - new skill
- `fix: <skill-name> - description` - bug fix in skill
- `docs: update README` - documentation changes
- `chore: update install.py` - tooling changes
