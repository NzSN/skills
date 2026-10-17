#!/usr/bin/env python3
"""Install every skill in this repository into the DSH user skill directory.

DSH scans each skill root one level deep: ``<root>/<name>/SKILL.md``. This
repository keeps skills under bucket folders (``skills/engineering/tdd/SKILL.md``),
so pointing DSH at the repo's ``skills/`` tree finds nothing. This script
links each skill directory into ``$DSH_HOME/skills`` (``~/.dsh/skills`` by
default) instead.

Entries are symlinks back into this repository, so a ``git pull`` keeps
installed skills current. Pass ``--copy`` to copy the skill directories
instead, which is useful on Windows or when the checkout may move.
"""

from __future__ import annotations

import argparse
import errno
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_ROOT = REPO_ROOT / "skills"

KEBAB_CASE = re.compile(r"\A[a-z0-9]+(?:-[a-z0-9]+)*\Z")
FRONTMATTER = re.compile(r"\A---\r?\n(.*?)\r?\n---\s*(?:\r?\n|\Z)", re.DOTALL)
NAME_LINE = re.compile(r"^name:\s*(\S.*?)\s*$", re.MULTILINE)

COPY_IGNORES = shutil.ignore_patterns("node_modules", ".git")


class InstallError(Exception):
    """A problem that should stop the install without a traceback."""


@dataclass(frozen=True)
class Skill:
    name: str
    source: Path


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="install-dsh-skills.py",
        description="Install every skill in this repository into the DSH user skill directory.",
        epilog=(
            "Examples:\n"
            "  python3 scripts/install-dsh-skills.py --dry-run\n"
            "  python3 scripts/install-dsh-skills.py --copy --dest ./skill-copies"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dest",
        metavar="DIR",
        help="skill root to install into (default: $DSH_HOME/skills, else ~/.dsh/skills)",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="copy skill directories instead of symlinking them",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace real files or directories already present in the destination",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print what would change without touching the destination",
    )
    return parser.parse_args(argv)


def discover_skills() -> List[Skill]:
    if not SKILLS_ROOT.is_dir():
        raise InstallError(f"skill tree not found: {SKILLS_ROOT}")

    skills = [
        Skill(name=skill_md.parent.name, source=skill_md.parent)
        for skill_md in sorted(SKILLS_ROOT.glob("*/*/SKILL.md"))
    ]
    if not skills:
        raise InstallError(f"no skills found under {SKILLS_ROOT}")

    by_name: dict[str, Skill] = {}
    for skill in skills:
        clash = by_name.get(skill.name)
        if clash is not None:
            raise InstallError(
                f"two skills share the name {skill.name!r}:\n"
                f"  {clash.source}\n  {skill.source}"
            )
        by_name[skill.name] = skill
    return skills


def resolve_dest(explicit: Optional[str]) -> Path:
    if explicit is not None:
        dest = Path(explicit).expanduser()
    else:
        dsh_home = os.environ.get("DSH_HOME")
        dest = (Path(dsh_home).expanduser() if dsh_home else Path.home() / ".dsh") / "skills"
    dest = dest.absolute()

    if dest == SKILLS_ROOT or SKILLS_ROOT in dest.parents:
        raise InstallError(
            f"refusing to install into this repo's own skill tree: {dest}\n"
            f"Pass --dest for a directory outside {SKILLS_ROOT}."
        )

    if dest.is_symlink():
        resolved = Path(os.path.realpath(dest))
        if resolved == REPO_ROOT or REPO_ROOT in resolved.parents:
            raise InstallError(
                f"{dest} is a symlink into this repo ({resolved}).\n"
                f"Remove it (rm {dest}) and re-run; the script will recreate it as a real directory."
            )
        if not dest.exists():
            raise InstallError(f"destination is a dangling symlink: {dest}")
    elif dest.exists() and not dest.is_dir():
        raise InstallError(f"destination exists but is not a directory: {dest}")

    return dest


def read_declared_name(source: Path) -> Optional[str]:
    try:
        text = (source / "SKILL.md").read_text(encoding="utf-8")
    except OSError:
        return None

    frontmatter = FRONTMATTER.match(text)
    if frontmatter is None:
        return None
    match = NAME_LINE.search(frontmatter.group(1))
    if match is None:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def warn_about_declared_names(skills: List[Skill]) -> None:
    for skill in skills:
        declared = read_declared_name(skill.source)
        if declared is not None and declared == skill.name:
            continue
        if declared is None:
            print(
                f"warning: {relative(skill.source / 'SKILL.md')} has no frontmatter name; DSH will skip it",
                file=sys.stderr,
            )
        elif not KEBAB_CASE.match(declared):
            print(
                f"warning: {relative(skill.source / 'SKILL.md')} declares the invalid name {declared!r}; DSH will skip it",
                file=sys.stderr,
            )
        else:
            print(
                f"warning: {relative(skill.source)} declares the name {declared!r}; "
                f"DSH will list it as {declared!r}",
                file=sys.stderr,
            )


def build_plan(
    skills: List[Skill], dest: Path, copy: bool, force: bool
) -> Tuple[List[Tuple[Skill, str]], List[Path]]:
    """Return the intended action per skill, plus destination conflicts.

    Actions:
      install  - no entry yet
      update   - an existing symlink that points somewhere else
      replace  - an existing symlink (in copy mode) or a real entry with --force
      current  - already installed and up to date
    """
    plan: List[Tuple[Skill, str]] = []
    conflicts: List[Path] = []

    for skill in skills:
        target = dest / skill.name
        if target.is_symlink():
            if copy:
                action = "replace"
            elif os.path.realpath(target) == os.path.realpath(skill.source):
                action = "current"
            else:
                action = "update"
        elif target.exists():
            if force:
                action = "replace"
            else:
                conflicts.append(target)
                continue
        else:
            action = "install"
        plan.append((skill, action))

    return plan, conflicts


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def install(skill: Skill, dest: Path, action: str, copy: bool) -> None:
    target = dest / skill.name
    if action in ("update", "replace"):
        remove_path(target)
    if copy:
        shutil.copytree(skill.source, target, symlinks=True, ignore=COPY_IGNORES)
    else:
        target.symlink_to(skill.source, target_is_directory=True)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def display(path: Path) -> str:
    try:
        return f"~/{path.relative_to(Path.home())}"
    except ValueError:
        return str(path)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    dest: Optional[Path] = None

    try:
        dest = resolve_dest(args.dest)
        skills = discover_skills()
        warn_about_declared_names(skills)
        plan, conflicts = build_plan(skills, dest, args.copy, args.force)

        if conflicts:
            shown = conflicts[:8]
            lines = "\n".join(f"  {display(target)}" for target in shown)
            if len(conflicts) > len(shown):
                lines += f"\n  ... and {len(conflicts) - len(shown)} more"
            raise InstallError(
                f"destination already contains real files or directories:\n{lines}\n"
                f"Re-run with --force to replace them."
            )

        if not args.dry_run and plan:
            dest.mkdir(parents=True, exist_ok=True)

        counts = {"install": 0, "update": 0, "replace": 0, "current": 0}
        for skill, action in plan:
            counts[action] += 1
            if action == "current":
                continue
            if not args.dry_run:
                install(skill, dest, action, args.copy)
            print(f"{describe(action, args.copy, args.dry_run)} {display(dest / skill.name)}")

        changed = counts["install"] + counts["update"] + counts["replace"]
        if changed == 0:
            summary = f"All {len(plan)} skills are already installed in {display(dest)}"
        elif args.dry_run:
            summary = f"Would {copy_verb(args.copy)} {changed} {plural(changed)} into {display(dest)}"
        else:
            verb = "Copied" if args.copy else "Linked"
            summary = f"{verb} {changed} {plural(changed)} into {display(dest)}"
        if changed and counts["current"]:
            summary += f" ({counts['current']} already up to date)"
        print(summary)
    except InstallError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"error: {error}", file=sys.stderr)
        read_only = error.errno in (errno.EACCES, errno.EPERM, errno.EROFS)
        if read_only and dest is not None:
            print(
                f"hint: {display(dest)} is not writable; check its permissions or pass --dest",
                file=sys.stderr,
            )
        if not args.copy:
            print("hint: symlinks may need extra privileges on Windows; try --copy", file=sys.stderr)
        return 1

    return 0


def describe(action: str, copy: bool, dry_run: bool) -> str:
    base_verb = {
        "install": "copy" if copy else "link",
        "update": "relink",
        "replace": "copy" if copy else "link",
    }[action]
    if dry_run:
        return f"would {base_verb}"
    return {"link": "linked", "relink": "relinked", "copy": "copied"}[base_verb]


def copy_verb(copy: bool) -> str:
    return "copy" if copy else "link"


def plural(count: int) -> str:
    return "skill" if count == 1 else "skills"


if __name__ == "__main__":
    sys.exit(main())
