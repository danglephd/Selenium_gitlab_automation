#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python_bin="${project_root}/.venv/bin/python"

if [[ ! -x "${python_bin}" ]]; then
    echo "Không tìm thấy virtualenv tại ${project_root}/.venv." >&2
    echo "Chạy: python3 -m venv .venv && .venv/bin/python -m pip install -r requirements.txt" >&2
    exit 1
fi

cd "${project_root}"
"${python_bin}" -m pytest test/testrpa_create_testcaseFB.py