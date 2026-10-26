# AI Skills

Централизованное хранилище AI-скиллов для синхронизации между несколькими машинами (Windows, macOS, Linux).

Следует стандартам [Agent Skills](https://agentskills.io) и [AGENTS.md](https://agents.md).

Работает с **60k+ проектами** и инструментами:
- **Claude Code** / **OpenCode** / **Cursor** / **Windsurf**
- **OpenAI Codex** / **Google Jules** / **GitHub Copilot**
- **Aider** / **Zed** / **VS Code** / **RooCode**
- И [многими другими...](https://agents.md)

## Quick Start

```bash
# Клонировать репозиторий
git clone https://github.com/tall27/ai-skills.git
cd ai-skills

# Показать доступные скиллы
python install.py --list

# Установить все скиллы
python install.py --all

# Установить конкретный скилл
python install.py --install mailtm

# Установить только для Claude
python install.py --all --target claude
```

## Куда устанавливаются скиллы

| Директория | Инструменты |
|------------|-------------|
| `~/.claude/skills/` | Claude Code |
| `~/.config/opencode/skills/` | OpenCode |
| `~/.agents/skills/` | Codex, Jules, Cursor, Copilot и др. |

## Skills Catalog (17 скиллов)

### Utility Skills

| Skill | Description |
|-------|-------------|
| [mailtm](skills/mailtm/) | Временная почта для тестирования регистраций, OTP, верификации email |
| [skill-import](skills/skill-import/) | Импорт скиллов из других GitHub репозиториев |

### Web Scraping & Automation

| Skill | Description |
|-------|-------------|
| [puppeteer-stealth](skills/puppeteer-stealth/) | Обход bot detection на защищённых сайтах с puppeteer-extra stealth plugin |

### n8n Workflow Automation

| Skill | Description |
|-------|-------------|
| [n8n-workflow-patterns](skills/n8n-workflow-patterns/) | Архитектурные паттерны для n8n воркфлоу |
| [n8n-code-javascript](skills/n8n-code-javascript/) | JavaScript в n8n Code nodes |
| [n8n-code-python](skills/n8n-code-python/) | Python в n8n Code nodes |
| [n8n-expression-syntax](skills/n8n-expression-syntax/) | Валидация синтаксиса n8n выражений |
| [n8n-mcp-tools-expert](skills/n8n-mcp-tools-expert/) | Гайд по n8n-mcp MCP tools |
| [n8n-node-configuration](skills/n8n-node-configuration/) | Конфигурация n8n нод |
| [n8n-validation-expert](skills/n8n-validation-expert/) | Интерпретация ошибок валидации |

### NGTS (Palo Alto Strata Cloud Manager) — обзор в [NGTS/](NGTS/)

Общие правила API лежат в [skills/_shared](skills/_shared/); `install.py` копирует их вместе с любым `ngts-*` скиллом.

| Skill | Description |
|-------|-------------|
| [ngts-auth-access](skills/ngts-auth-access/) | OAuth‑токены, поиск TSG, NGTS Built-in Accounts |
| [ngts-certificate-governance](skills/ngts-certificate-governance/) | Issuing templates (request policies), issuance policies Built-in PKI, правила согласования |
| [ngts-certificate-inventory](skills/ngts-certificate-inventory/) | Инвентарь сертификатов, TLS endpoints, discovery, теги, мониторинг продления |
| [ngts-certificate-provisioning](skills/ngts-certificate-provisioning/) | Импорт и запросы сертификатов, SCEP‑серверы, диагностика SCEP enrollment |
| [ngts-issuers](skills/ngts-issuers/) | Distributed issuers, sub-CA providers, создание и вывод из эксплуатации root/sub‑CA Built-in PKI |
| [ngts-machines-connectors](skills/ngts-machines-connectors/) | Машины, коннекторы, учётные данные, VSatellites |
| [ngts-platform-ops](skills/ngts-platform-ops/) | Activity и audit логи |

## Использование install.py

```bash
# Показать все скиллы
python install.py --list

# Установить все
python install.py --all

# Установить конкретные скиллы
python install.py --install mailtm n8n-workflow-patterns

# Установить по паттерну
python install.py --install "n8n-*"

# Установить только для определённых инструментов
python install.py --all --target claude opencode

# Перезаписать существующие
python install.py --all --force

# Удалить скилл
python install.py --uninstall mailtm

# Dry run (посмотреть что будет сделано)
python install.py --all --dry-run
```

## Синхронизация между машинами

**На машине где изменил скиллы:**
```bash
git add . && git commit -m "update skills" && git push
```

**На другой машине:**
```bash
git pull && python install.py --all --force
```

## Структура скилла

```
skills/
└── skill-name/
    ├── SKILL.md          # Обязательно: YAML frontmatter + инструкции
    ├── helper.py         # Опционально: вспомогательные скрипты
    └── resources/        # Опционально: дополнительные файлы
```

### Формат SKILL.md

```markdown
---
name: skill-name
description: Краткое описание
author: your-name
version: 1.0.0
tags: [tag1, tag2]
---

# Skill Name

Инструкции для AI агента...
```

## Импорт внешних скиллов

Используй скилл `skill-import` для добавления скиллов из других GitHub репозиториев:

1. Загрузи скилл в AI инструменте
2. Попроси: "Import the pdf-analyzer skill from TerminalSkills/skills"
3. AI скачает и закоммитит скилл в этот репозиторий

## Standards

- **[AGENTS.md](https://agents.md)** — инструкции для AI агентов (см. `AGENTS.md` в корне)
- **[Agent Skills](https://agentskills.io)** — стандарт для `SKILL.md` файлов

## License

MIT
