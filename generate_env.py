#!/usr/bin/env python3
"""Create a local .env file from a safe template.

Usage:
    python generate_env.py
    python generate_env.py --template .temp.env --output .env

The template may contain placeholders like:
    export GITLAB_PASSWORD = REPLACE_WITH_GITLAB_PASSWORD

If a placeholder is present, the script will:
1. look for the same variable in the process environment
2. otherwise prompt the user in the terminal
3. write the generated .env file in the project root
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


DEFAULT_TEMPLATE = ".temp.env"
DEFAULT_OUTPUT = ".env"
PLACEHOLDER_PATTERN = re.compile(r"REPLACE_WITH_[A-Z0-9_]+|your_[a-z0-9_@.-]+@example\.com")


def resolve_user_value(key: str, default_value: str | None = None) -> str:
    env_value = os.getenv(key)
    if env_value is not None and env_value.strip():
        return env_value.strip()

    if default_value is not None and default_value.strip():
        return default_value.strip()

    prompt = f"Nhập giá trị cho {key}: "
    return input(prompt).strip()


def process_line(line: str) -> str:
    if "=" not in line:
        return line

    left, right = line.split("=", 1)
    value = right.strip()

    if not PLACEHOLDER_PATTERN.search(value):
        return line

    key = left.strip().replace("export ", "", 1).strip()
    if not key:
        return line

    key = key.replace(" ", "")
    value_to_use = resolve_user_value(key)
    return f"{left}= {value_to_use}"


def generate_env(template_path: Path, output_path: Path) -> None:
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    lines = []
    for raw_line in template_path.read_text(encoding="utf-8").splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            lines.append(raw_line)
            continue

        lines.append(process_line(raw_line))

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Đã tạo file .env tại: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a local .env file from a safe template.")
    parser.add_argument("--template", default=DEFAULT_TEMPLATE, help="Template file path, default .temp.env")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output file path, default .env")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent
    template_path = (project_root / args.template).resolve()
    output_path = (project_root / args.output).resolve()

    generate_env(template_path, output_path)


if __name__ == "__main__":
    main()
