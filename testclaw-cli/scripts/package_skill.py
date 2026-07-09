#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    skills_root = skill_dir.parent
    archive_path = skills_root / "testclaw-cli.skill"

    if not shutil.which("zip"):
        print("未找到 zip 命令，无法打包 testclaw-cli.skill", file=sys.stderr)
        return 2

    if archive_path.exists():
        archive_path.unlink()

    cmd = [
        "zip",
        "-rq",
        str(archive_path),
        skill_dir.name,
        "-x",
        "*/.DS_Store",
        "-x",
        "*/__pycache__/*",
        "-x",
        "*/__pycache__/",
        "-x",
        "*.pyc",
    ]

    subprocess.run(cmd, cwd=skills_root, check=True)
    print(f"已生成：{archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
