# AI Skills

A personal collection of AI agent skills following the [Agent Skills](https://agentskills.io) open standard and [AGENTS.md](https://agents.md) conventions.

Works across **60k+ projects** and tools including:
- **Claude Code** / **OpenCode** / **Cursor** / **Windsurf**
- **OpenAI Codex** / **Google Jules** / **GitHub Copilot**
- **Aider** / **Zed** / **VS Code** / **RooCode**
- And [many more...](https://agents.md)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/tall27/ai-skills.git
cd ai-skills

# List available skills
python install.py --list

# Install all skills to detected AI tools
python install.py --all

# Install specific skills
python install.py --install mailtm "n8n-*"

# Install to specific target only
python install.py --all --target claude
```

## Installation Targets

The installer automatically detects and copies skills to:

| Target | Path | Tool |
|--------|------|------|
| `claude` | `~/.claude/skills/` | Claude Code |
| `opencode` | `~/.config/opencode/skills/` | OpenCode |
| `agents` | `~/.agents/skills/` | AGENTS.md compatible (Codex, Jules, Cursor, Copilot, etc.) |

## Skills Catalog

### Utility Skills

| Skill | Description |
|-------|-------------|
| [mailtm](skills/mailtm/) | Temporary email via mail.tm for testing sign-up flows, OTPs, and email verification |
| [skill-import](skills/skill-import/) | Import skills from external GitHub repositories |

### n8n Workflow Automation

| Skill | Description |
|-------|-------------|
| [n8n-workflow-patterns](skills/n8n-workflow-patterns/) | Proven workflow architectural patterns from real n8n workflows |
| [n8n-code-javascript](skills/n8n-code-javascript/) | Write JavaScript code in n8n Code nodes |
| [n8n-code-python](skills/n8n-code-python/) | Write Python code in n8n Code nodes |
| [n8n-expression-syntax](skills/n8n-expression-syntax/) | Validate n8n expression syntax and fix common errors |
| [n8n-mcp-tools-expert](skills/n8n-mcp-tools-expert/) | Expert guide for using n8n-mcp MCP tools effectively |
| [n8n-node-configuration](skills/n8n-node-configuration/) | Operation-aware node configuration guidance |
| [n8n-validation-expert](skills/n8n-validation-expert/) | Interpret validation errors and guide fixing them |

## Usage

### Install specific skills

```bash
# Single skill
python install.py --install mailtm

# Multiple skills
python install.py --install mailtm n8n-workflow-patterns

# Wildcard pattern
python install.py --install "n8n-*"
```

### Install to specific targets

```bash
# Only Claude Code
python install.py --all --target claude

# Multiple targets
python install.py --all --target claude opencode
```

### Overwrite existing skills

```bash
python install.py --install mailtm --force
```

### Uninstall skills

```bash
python install.py --uninstall mailtm
```

### Dry run (see what would happen)

```bash
python install.py --all --dry-run
```

## Importing External Skills

Use the `skill-import` skill to add skills from other GitHub repositories:

1. Load the skill in your AI tool
2. Ask: "Import the pdf-analyzer skill from TerminalSkills/skills"
3. The AI will download and commit the skill to this repository

See [skill-import/SKILL.md](skills/skill-import/SKILL.md) for details.

## Skill Structure

Each skill follows the Agent Skills standard:

```
skills/
└── skill-name/
    ├── SKILL.md          # Required: YAML frontmatter + instructions
    ├── helper.py         # Optional: helper scripts
    └── resources/        # Optional: additional files
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Brief description
author: your-name
version: 1.0.0
tags: [tag1, tag2]
---

# Skill Name

Instructions for the AI agent...
```

## Syncing Across Machines

1. Make changes to skills in this repository
2. Push to GitHub: `git push`
3. On another machine: `git pull && python install.py --all --force`

## Standards

This repository follows two complementary standards:

- **[AGENTS.md](https://agents.md)** - Instructions for AI agents working with this repository (see `AGENTS.md` in root)
- **[Agent Skills](https://agentskills.io)** - Reusable skill definitions via `SKILL.md` files

## License

MIT
