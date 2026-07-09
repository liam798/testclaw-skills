#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
CHECK_FILES = [
    ROOT / "SKILL.md",
    ROOT / "references" / "tools.md",
    ROOT / "references" / "flows.md",
    ROOT / "references" / "evidence-workflow.md",
]


def extract_relative_refs(text: str) -> set[str]:
    refs = set()
    patterns = [
        r"`(references/[^`]+)`",
        r"`(scripts/[^`]+)`",
        r"`(agents/[^`]+)`",
        r"`(assets/[^`]+)`",
    ]
    for pattern in patterns:
        refs.update(re.findall(pattern, text))
    return refs


def main() -> int:
    missing: list[str] = []
    for file_path in CHECK_FILES:
        text = file_path.read_text(encoding="utf-8")
        for ref in sorted(extract_relative_refs(text)):
            target = ROOT / ref
            if not target.exists():
                missing.append(f"{file_path.relative_to(ROOT)} -> {ref}")

    if missing:
        print("以下引用不存在：", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("testclaw-cli 引用检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
