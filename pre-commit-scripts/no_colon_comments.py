#!/usr/bin/env python3
import re
import sys
from pathlib import Path

# Only check .py files
PYTHON_FILE_EXTENSIONS = {".py"}


def check_file_for_colon_comment(file_path):
    with Path(file_path).open(encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if "test_file" in file_path:
                raise ValueError(f"{line=}")
            if re.search(r"^\s*#:", line):
                print(
                    f"{file_path}:{i}: Found Sphinx-style comment ('#:') - use a docstring instead."
                )
                return True
    return False


def main():
    failed = False
    for file in sys.argv[1:]:
        if Path(file).suffix in PYTHON_FILE_EXTENSIONS and check_file_for_colon_comment(
            file
        ):
            failed = True
    if failed:
        print(
            "\nERROR: Sphinx-style comments detected. Please use docstrings for documentation."
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
