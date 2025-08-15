import os
from pathlib import Path
import argparse

def combine_python_files(folder_path: str, output_file: str = "context_file.txt", exclude_dirs: list[str] = None) -> None:
    folder = Path(folder_path)
    if not folder.is_dir():
        raise ValueError(f"{folder_path} is not a valid directory")

    exclude_dirs = exclude_dirs or []
    exclude_dirs = set(exclude_dirs) | {".venv", "__pycache__"}

    with open(output_file, "w", encoding="utf-8") as outfile:
        for file_path in folder.glob("**/*.py"):
            if file_path.is_file() and not any(excluded in file_path.parts for excluded in exclude_dirs):
                outfile.write(f"\n\n# File: {file_path.relative_to(folder)}\n")
                with open(file_path, "r", encoding="utf-8") as infile:
                    outfile.write(infile.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine Python files into a single context file")
    parser.add_argument("folder_path", help="Path to the folder containing Python files")
    parser.add_argument("--output", default="context_file.txt", help="Output file name")
    parser.add_argument("--exclude", nargs="*", default=[], help="Directories to exclude (e.g., .venv)")
    args = parser.parse_args()

    combine_python_files(args.folder_path, args.output, args.exclude)
    print(f"Combined Python files into {args.output}")