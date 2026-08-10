#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess
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

REQUIRED_CONTENT = {
    "testclaw-cli/SKILL.md": (
        "使用真实设备打开浏览器、访问网页、读取页面内容、截图确认",
        "证据采集硬闸门",
        "evidence preflight 任一项失败时",
        "最终回复必须列出 `video`、`log`、`network`、`screenshots`、`performance`、`structured report`",
    ),
    "testclaw-cli/references/evidence-workflow.md": (
        "启动前硬闸门",
        "浏览器打开网页、截图取证和 UI 校对",
        "不得执行安装、打开应用、打开浏览器、访问网页、截图、点击、输入、读取页面内容或总结页面",
        "如果执行者已经操作真实设备后才发现未提前启动录屏、日志或网络记录",
    ),
    "testclaw-cli/references/examples.md": (
        "应命中：真机浏览器网页巡检",
        "不得先打开网页、截图或读取页面内容后再补录证据",
    ),
    "testclaw-cli/references/regression-matrix.md": (
        "真实设备浏览器访问网页、截图确认、页面内容总结必须按手工冒烟处理",
        "R13 必须在打开浏览器或访问网页前完成 evidence preflight",
    ),
    "testclaw-cli/references/templates.md": (
        "模板 6：真机浏览器网页巡检",
        "最终回复必须列出 video、log、network、screenshots、performance、structured report",
    ),
    "testclaw-cli/agents/openai.yaml": (
        "打开浏览器/网页",
        "任何会操作或观察真实设备 UI 的任务都必须先完成 evidence preflight",
    ),
}

FORBIDDEN_SOURCE_PATTERNS = (
    ".DS_Store",
    "__pycache__/",
    ".pyc",
    ".skill",
)


def git_list(repo_dir: Path, *args: str) -> set[str]:
    result = subprocess.run(
        ["git", "-C", str(repo_dir), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return set()
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    repo_dir = skill_dir.parent

    missing = sorted(
        item for item in REQUIRED_SOURCE_ENTRIES if not (repo_dir / item).exists()
    )
    committed_or_candidate_files = git_list(repo_dir, "ls-files") | git_list(
        repo_dir, "ls-files", "--others", "--exclude-standard"
    )
    forbidden = sorted(
        item
        for item in committed_or_candidate_files
        if any(pattern in item for pattern in FORBIDDEN_SOURCE_PATTERNS)
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

    content_failures: list[str] = []
    for item, expected_phrases in REQUIRED_CONTENT.items():
        content = (repo_dir / item).read_text(encoding="utf-8")
        for phrase in expected_phrases:
            if phrase not in content:
                content_failures.append(f"{item}: 缺少 `{phrase}`")

    if content_failures:
        print("关键 evidence contract 内容缺失：", file=sys.stderr)
        for item in content_failures:
            print(f"- {item}", file=sys.stderr)
        return 1

    print("testclaw-cli 源码完整性检查通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
