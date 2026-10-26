---
name: skill-import
description: Import AI agent skills from external GitHub repositories into tall27/ai-skills
author: tall27
version: 1.0.0
tags: [utility, skills, github, import]
---

# Skill Import

Import skills from external GitHub repositories into the `tall27/ai-skills` repository.

## When to Use

Use this skill when the user asks to:
- Import a skill from another GitHub repository
- Add an external skill to the ai-skills collection
- Fetch a skill from a URL or GitHub path

## Workflow

### Step 1: Parse the Source

The user will provide one of these formats:
- GitHub URL: `https://github.com/owner/repo/tree/main/skills/skill-name`
- GitHub shorthand: `owner/repo/skills/skill-name`
- Raw URL to SKILL.md: `https://raw.githubusercontent.com/owner/repo/main/skills/skill-name/SKILL.md`

Extract:
- `owner`: Repository owner
- `repo`: Repository name
- `path`: Path to skill directory (must contain SKILL.md)
- `skill_name`: Name of the skill (last component of path, or derive from SKILL.md)

### Step 2: Validate the Skill

1. Fetch the SKILL.md file to verify it exists
2. Check YAML frontmatter for `name` field
3. If `name` exists, use it as `skill_name`; otherwise use directory name

### Step 3: Download the Skill

Use one of these methods:

**Method A: Single SKILL.md file**
```bash
curl -sL "https://raw.githubusercontent.com/{owner}/{repo}/main/{path}/SKILL.md" -o "skills/{skill_name}/SKILL.md"
```

**Method B: Entire directory (if skill has multiple files)**
```bash
# Clone repo sparsely
git clone --filter=blob:none --sparse https://github.com/{owner}/{repo}.git temp_repo
cd temp_repo
git sparse-checkout set {path}
# Copy to skills directory
cp -r {path} ../skills/{skill_name}
cd .. && rm -rf temp_repo
```

**Method C: Using GitHub API (for listing directory contents)**
```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/contents/{path}" | jq -r '.[].name'
```

### Step 4: Update Repository Files

After importing, update these files:

**README.md** - Add skill to the catalog table:
```markdown
| [{skill_name}](skills/{skill_name}/) | {category} | {description} |
```

**install.py** - No changes needed (auto-discovers skills from `skills/` directory)

### Step 5: Commit Changes

```bash
git add skills/{skill_name} README.md
git commit -m "feat: import {skill_name} skill from {owner}/{repo}"
```

## Examples

### Example 1: Import from TerminalSkills

User: "Import the pdf-analyzer skill from TerminalSkills/skills"

```bash
# Create directory
mkdir -p skills/pdf-analyzer

# Download SKILL.md
curl -sL "https://raw.githubusercontent.com/TerminalSkills/skills/main/skills/pdf-analyzer/SKILL.md" \
  -o "skills/pdf-analyzer/SKILL.md"

# Check for additional files
curl -s "https://api.github.com/repos/TerminalSkills/skills/contents/skills/pdf-analyzer" | \
  jq -r '.[] | select(.name != "SKILL.md") | .name'

# If additional files exist, download them too
```

### Example 2: Import from Anthropic's skills repo

User: "Add the code-review skill from anthropics/skills"

```bash
mkdir -p skills/code-review
curl -sL "https://raw.githubusercontent.com/anthropics/skills/main/code-review/SKILL.md" \
  -o "skills/code-review/SKILL.md"
```

## Error Handling

- **404 on SKILL.md**: The path is incorrect or skill doesn't exist
- **Rate limit**: Use authenticated requests with `gh api` instead of `curl`
- **Name conflict**: Ask user to choose a different name or overwrite

## Important Notes

1. Always verify the skill has a valid `SKILL.md` before importing
2. Preserve the original skill structure (don't rename internal files)
3. Add attribution in commit message: `from {owner}/{repo}`
4. Update README.md catalog after successful import
5. The skill becomes part of this repository (committed, not linked)
