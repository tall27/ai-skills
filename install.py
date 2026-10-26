#!/usr/bin/env python3
"""
AI Skills Installer - Cross-platform skill installation for AI coding agents.

Supports:
- Claude Code (~/.claude/skills/)
- OpenCode (~/.config/opencode/skills/)
- Universal agents (~/.agents/skills/)

Usage:
    python install.py --list                    # List available skills
    python install.py --install mailtm          # Install specific skill(s)
    python install.py --install mailtm n8n-*    # Install with wildcards
    python install.py --all                     # Install all skills
    python install.py --all --target claude     # Install to specific target only
    python install.py --uninstall mailtm        # Remove a skill
"""

import argparse
import fnmatch
import os
import platform
import shutil
import sys
from pathlib import Path
from typing import Optional


# ANSI colors (disabled on Windows without colorama)
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"

    @classmethod
    def disable(cls):
        cls.RESET = cls.GREEN = cls.YELLOW = cls.RED = cls.CYAN = cls.BOLD = ""


# Disable colors on Windows if not in modern terminal
if platform.system() == "Windows":
    try:
        os.system("")  # Enable ANSI on Windows 10+
    except Exception:
        Colors.disable()


def get_home() -> Path:
    """Get user home directory cross-platform."""
    return Path.home()


def get_target_paths() -> dict[str, Path]:
    """
    Get installation paths for each supported AI tool.
    Returns dict of target_name -> path.
    """
    home = get_home()

    targets = {
        "claude": home / ".claude" / "skills",
        "opencode": home / ".config" / "opencode" / "skills",
        "agents": home / ".agents" / "skills",
    }

    return targets


def get_skills_dir() -> Path:
    """Get the skills source directory (relative to this script)."""
    return Path(__file__).parent / "skills"


def list_available_skills() -> list[str]:
    """List all available skills in the repository."""
    skills_dir = get_skills_dir()
    if not skills_dir.exists():
        return []

    skills = []
    for item in skills_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append(item.name)

    return sorted(skills)


def detect_installed_targets() -> dict[str, Path]:
    """Detect which AI tools have their skills directories already set up."""
    targets = get_target_paths()
    installed = {}

    for name, path in targets.items():
        # Check if parent directory exists (indicates tool is likely installed)
        parent = path.parent
        if parent.exists():
            installed[name] = path

    return installed


def match_skills(patterns: list[str], available: list[str]) -> list[str]:
    """Match skill patterns (supports wildcards) against available skills."""
    matched = set()
    for pattern in patterns:
        for skill in available:
            if fnmatch.fnmatch(skill, pattern):
                matched.add(skill)
    return sorted(matched)


def copy_skill(skill_name: str, target_path: Path, force: bool = False) -> bool:
    """
    Copy a skill to the target directory.
    Returns True if successful.
    """
    source = get_skills_dir() / skill_name
    dest = target_path / skill_name

    if not source.exists():
        print(f"{Colors.RED}Error: Skill '{skill_name}' not found{Colors.RESET}")
        return False

    if dest.exists():
        if not force:
            print(
                f"{Colors.YELLOW}  Skipping {skill_name} (already exists, use --force to overwrite){Colors.RESET}"
            )
            return False
        shutil.rmtree(dest)

    try:
        shutil.copytree(source, dest)
        # Skills that read ../_shared/ (the NGTS family) need the shared folder next to them.
        shared = get_skills_dir() / "_shared"
        if shared.exists() and "../_shared/" in (source / "SKILL.md").read_text(encoding="utf-8"):
            shutil.copytree(shared, target_path / "_shared", dirs_exist_ok=True)
        return True
    except Exception as e:
        print(f"{Colors.RED}Error copying {skill_name}: {e}{Colors.RESET}")
        return False


def remove_skill(skill_name: str, target_path: Path) -> bool:
    """Remove a skill from the target directory."""
    dest = target_path / skill_name

    if not dest.exists():
        return False

    try:
        shutil.rmtree(dest)
        return True
    except Exception as e:
        print(f"{Colors.RED}Error removing {skill_name}: {e}{Colors.RESET}")
        return False


def print_skill_list(skills: list[str]):
    """Print formatted list of available skills."""
    print(f"\n{Colors.BOLD}Available Skills:{Colors.RESET}\n")

    # Group skills by prefix
    groups: dict[str, list[str]] = {}
    for skill in skills:
        prefix = skill.split("-")[0] if "-" in skill else "other"
        groups.setdefault(prefix, []).append(skill)

    for prefix, group_skills in sorted(groups.items()):
        if len(group_skills) > 1 and prefix != "other":
            print(
                f"  {Colors.CYAN}{prefix}-*{Colors.RESET} ({len(group_skills)} skills)"
            )
            for skill in group_skills:
                print(f"    - {skill}")
        else:
            for skill in group_skills:
                print(f"  {Colors.CYAN}{skill}{Colors.RESET}")
    print()


def print_targets(targets: dict[str, Path], detected: dict[str, Path]):
    """Print available installation targets."""
    print(f"\n{Colors.BOLD}Installation Targets:{Colors.RESET}\n")
    for name, path in targets.items():
        status = (
            f"{Colors.GREEN}(detected){Colors.RESET}"
            if name in detected
            else f"{Colors.YELLOW}(not found){Colors.RESET}"
        )
        print(f"  {name:10} {path} {status}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Install AI agent skills to supported tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py --list
  python install.py --install mailtm
  python install.py --install "n8n-*"
  python install.py --all
  python install.py --all --target claude opencode
  python install.py --uninstall mailtm
        """,
    )

    parser.add_argument(
        "--list", "-l", action="store_true", help="List available skills"
    )
    parser.add_argument(
        "--install",
        "-i",
        nargs="+",
        metavar="SKILL",
        help="Install specific skills (supports wildcards like 'n8n-*')",
    )
    parser.add_argument(
        "--all", "-a", action="store_true", help="Install all available skills"
    )
    parser.add_argument(
        "--uninstall",
        "-u",
        nargs="+",
        metavar="SKILL",
        help="Uninstall specific skills",
    )
    parser.add_argument(
        "--target",
        "-t",
        nargs="+",
        choices=["claude", "opencode", "agents", "all"],
        default=["all"],
        help="Installation target(s) (default: all detected)",
    )
    parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing skills"
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be done without doing it",
    )

    args = parser.parse_args()

    # Get available skills and targets
    available_skills = list_available_skills()
    all_targets = get_target_paths()
    detected_targets = detect_installed_targets()

    # Handle --list
    if args.list:
        print_skill_list(available_skills)
        print_targets(all_targets, detected_targets)
        return 0

    # No action specified
    if not args.install and not args.all and not args.uninstall:
        parser.print_help()
        return 1

    # Determine target paths
    if "all" in args.target:
        # Use all detected targets, or all targets if none detected
        targets = detected_targets if detected_targets else all_targets
    else:
        targets = {name: all_targets[name] for name in args.target}

    # Handle --uninstall
    if args.uninstall:
        skills_to_remove = match_skills(args.uninstall, available_skills)
        if not skills_to_remove:
            print(f"{Colors.RED}No matching skills found{Colors.RESET}")
            return 1

        print(f"\n{Colors.BOLD}Uninstalling skills:{Colors.RESET}")
        for target_name, target_path in targets.items():
            print(f"\n  {Colors.CYAN}{target_name}{Colors.RESET} ({target_path})")
            for skill in skills_to_remove:
                if args.dry_run:
                    print(f"    Would remove: {skill}")
                else:
                    if remove_skill(skill, target_path):
                        print(f"    {Colors.GREEN}Removed:{Colors.RESET} {skill}")
                    else:
                        print(f"    {Colors.YELLOW}Not found:{Colors.RESET} {skill}")
        return 0

    # Handle --install or --all
    if args.all:
        skills_to_install = available_skills
    else:
        skills_to_install = match_skills(args.install, available_skills)

    if not skills_to_install:
        print(f"{Colors.RED}No matching skills found{Colors.RESET}")
        print(f"Available skills: {', '.join(available_skills)}")
        return 1

    # Create target directories if needed
    for target_name, target_path in targets.items():
        if not target_path.exists() and not args.dry_run:
            target_path.mkdir(parents=True, exist_ok=True)

    # Install skills
    print(f"\n{Colors.BOLD}Installing {len(skills_to_install)} skill(s):{Colors.RESET}")
    total_installed = 0

    for target_name, target_path in targets.items():
        print(f"\n  {Colors.CYAN}{target_name}{Colors.RESET} ({target_path})")
        installed_count = 0

        for skill in skills_to_install:
            if args.dry_run:
                print(f"    Would install: {skill}")
                installed_count += 1
            else:
                if copy_skill(skill, target_path, args.force):
                    print(f"    {Colors.GREEN}Installed:{Colors.RESET} {skill}")
                    installed_count += 1

        total_installed += installed_count

    print(f"\n{Colors.GREEN}Done!{Colors.RESET} Installed to {len(targets)} target(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
