#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys
import zipfile


REQUIRED_ARCHIVE_ENTRIES = {
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

FORBIDDEN_ARCHIVE_PATTERNS = (
    ".DS_Store",
    "__pycache__/",
    ".pyc",
)


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    archive_path = skill_dir.parent / "testclaw-cli.skill"

    if not archive_path.exists():
        print(f"未找到打包产物：{archive_path}", file=sys.stderr)
        return 2

    with zipfile.ZipFile(archive_path) as zf:
        names = set(zf.namelist())

    missing = sorted(REQUIRED_ARCHIVE_ENTRIES - names)
    forbidden = sorted(
        name for name in names if any(pattern in name for pattern in FORBIDDEN_ARCHIVE_PATTERNS)
    )

    if missing:
        print("缺少以下打包文件：", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        return 1

    if forbidden:
        print("打包产物包含不应出现的文件：", file=sys.stderr)
        for item in forbidden:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("testclaw-cli.skill 完整性检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
