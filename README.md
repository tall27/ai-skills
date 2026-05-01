# AI Skills

A centralized repository of reusable **AI agent skills** — install once, use across all your AI coding tools.

Follows the [Agent Skills](https://agentskills.io) and [AGENTS.md](https://agents.md) standards.

Works with **Claude Code**, **Cursor**, **Copilot**, **Aider**, **OpenCode**, **Codex**, **Jules**, **Zed**, **VS Code**, **RooCode**, and [many more](https://agents.md).

---

## What Is a Skill?

A skill is a folder with a `SKILL.md` file containing instructions that teach an AI agent how to use a specific tool or API. Instead of re-explaining things every session, you install the skill once and it's always available.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/tall27/ai-skills.git
cd ai-skills

# See available skills
python install.py --list

# Install everything
python install.py --all

# Install one skill
python install.py --install mailtm

# Install only for Claude Code
python install.py --all --target claude
```

---

## Skills (10 total)

### Utility
| Skill | What it does |
|-------|-------------|
| [mailtm](skills/mailtm/) | Temporary email for testing registrations, OTP, and email verification |
| [skill-import](skills/skill-import/) | Import skills from other GitHub repositories |

### Web Automation
| Skill | What it does |
|-------|-------------|
| [puppeteer-stealth](skills/puppeteer-stealth/) | Web scraping with bot-detection bypass via puppeteer-extra stealth plugin |

### n8n Workflow Automation
| Skill | What it does |
|-------|-------------|
| [n8n-workflow-patterns](skills/n8n-workflow-patterns/) | Architectural patterns for n8n workflows |
| [n8n-code-javascript](skills/n8n-code-javascript/) | JavaScript inside n8n Code nodes |
| [n8n-code-python](skills/n8n-code-python/) | Python inside n8n Code nodes |
| [n8n-expression-syntax](skills/n8n-expression-syntax/) | Validate n8n expression syntax |
| [n8n-mcp-tools-expert](skills/n8n-mcp-tools-expert/) | Guide for using n8n MCP tools |
| [n8n-node-configuration](skills/n8n-node-configuration/) | Help configuring n8n nodes |
| [n8n-validation-expert](skills/n8n-validation-expert/) | Interpret n8n validation errors |

---

## Where Skills Get Installed

| Directory | Tools |
|-----------|-------|
| `~/.claude/skills/` | Claude Code |
| `~/.config/opencode/skills/` | OpenCode |
| `~/.agents/skills/` | Codex, Jules, Cursor, Copilot, and others |

---

## Installer Options

```bash
python install.py --list                          # List all skills
python install.py --all                           # Install all skills
python install.py --install mailtm puppeteer-stealth  # Install specific skills
python install.py --install "n8n-*"               # Install by pattern
python install.py --all --target claude opencode  # Install for specific tools only
python install.py --all --force                   # Overwrite existing installs
python install.py --uninstall mailtm              # Remove a skill
python install.py --all --dry-run                 # Preview what would happen
```

---

## Sync Between Machines

**After making changes:**
```bash
git add . && git commit -m "update skills" && git push
```

**On another machine:**
```bash
git pull && python install.py --all --force
```

---

## Skill Structure

```
skills/
└── skill-name/
    ├── SKILL.md       # Required: YAML frontmatter + AI instructions
    ├── helper.py      # Optional: helper scripts
    └── resources/     # Optional: extra files
```

**SKILL.md format:**
```markdown
---
name: skill-name
description: Short description
author: your-name
version: 1.0.0
tags: [tag1, tag2]
---

# Skill Name

Instructions for the AI agent...
```

---

## Importing External Skills

Use the `skill-import` skill to pull in skills from other GitHub repos:

1. Load the skill in your AI tool
2. Ask: *"Import the pdf-analyzer skill from TerminalSkills/skills"*
3. The AI downloads and commits it to this repo

---

## License

MIT
