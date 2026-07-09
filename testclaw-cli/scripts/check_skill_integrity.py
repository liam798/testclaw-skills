#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys


REQUIRED_SOURCE_ENTRIES = {
    "testclaw-cli/SKILL.md",
    "testclaw-cli/agents/openai.yaml",
    "testclaw-cli/references/flows.md",
    "testclaw-cli/references/tools.md",
    "testclaw-cli/references/evidence-workflow.md",
    "testclaw-cli/references/templates.md",
    "testclaw-cli/references/examples.md",
    "testclaw-cli/references/regression-matrix.md",
    "testclaw-cli/scripts/package_skill.py",
    "testclaw-cli/scripts/lint_skill_refs.py",
    "testclaw-cli/scripts/check_skill_integrity.py",
}

FORBIDDEN_SOURCE_PATTERNS = (
    ".DS_Store",
    "__pycache__/",
    ".pyc",
    ".skill",
)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    repo_dir = skill_dir.parent

    missing = sorted(
        item for item in REQUIRED_SOURCE_ENTRIES if not (repo_dir / item).exists()
    )
    forbidden = sorted(
        str(path.relative_to(repo_dir))
        for path in repo_dir.rglob("*")
        if any(pattern in str(path.relative_to(repo_dir)) for pattern in FORBIDDEN_SOURCE_PATTERNS)
    )

    if missing:
        print("缺少以下必需文件：", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        return 1

    if forbidden:
        print("源码仓库包含不应提交的产物：", file=sys.stderr)
        for item in forbidden:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("testclaw-cli 源码完整性检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
