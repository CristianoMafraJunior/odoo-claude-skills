#!/usr/bin/env python3
"""Validate skills/*/SKILL.md frontmatter and cross-references.

Checks:
- Every skill has a SKILL.md with a valid YAML frontmatter block.
- frontmatter `name` matches the directory name.
- frontmatter `description` is present and not absurdly long.
- Any `reference/*.md` mentioned in a SKILL.md body resolves to a real file
  somewhere under skills/*/reference/ (own or another skill's, since some
  skills point at a shared reference folder instead of duplicating it).
- README.md links to every skill directory that exists, and to no others.
"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?\n)---\n", re.DOTALL)
REFERENCE_RE = re.compile(r"reference/[\w.-]+\.md")
DESCRIPTION_MAX_LEN = 1024

errors = []


def fail(message):
    errors.append(message)


skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
reference_basenames = {p.name for p in SKILLS_DIR.glob("*/reference/*.md")}

for skill_dir in skill_dirs:
    name = skill_dir.name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        fail(f"{name}: missing SKILL.md")
        continue

    text = skill_md.read_text()
    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(f"{name}: SKILL.md has no valid leading --- frontmatter block")
        continue

    try:
        meta = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(f"{name}: frontmatter is not valid YAML ({exc})")
        continue

    if not isinstance(meta, dict):
        fail(f"{name}: frontmatter did not parse to a mapping")
        continue

    if meta.get("name") != name:
        fail(f"{name}: frontmatter name '{meta.get('name')}' does not match directory name")

    description = meta.get("description")
    if not description or not description.strip():
        fail(f"{name}: frontmatter description is empty or missing")
    elif len(description) > DESCRIPTION_MAX_LEN:
        fail(
            f"{name}: description is {len(description)} chars, "
            f"longer than the {DESCRIPTION_MAX_LEN}-char recommended limit"
        )

    for ref in REFERENCE_RE.findall(text):
        basename = Path(ref).name
        if basename not in reference_basenames:
            fail(
                f"{name}: SKILL.md references '{ref}' but no file named "
                f"'{basename}' exists under any skills/*/reference/"
            )

readme_text = README.read_text()
linked_skills = set(re.findall(r"skills/([a-z0-9-]+)/SKILL\.md", readme_text))
actual_skills = {p.name for p in skill_dirs}

missing_from_readme = actual_skills - linked_skills
extra_in_readme = linked_skills - actual_skills

if missing_from_readme:
    fail(f"README.md does not link to: {', '.join(sorted(missing_from_readme))}")
if extra_in_readme:
    fail(f"README.md links to nonexistent skill(s): {', '.join(sorted(extra_in_readme))}")

if errors:
    print("Skill validation failed:\n")
    for error in errors:
        print(f"  - {error}")
    sys.exit(1)

print(f"OK: {len(skill_dirs)} skills validated, README cross-references consistent.")
