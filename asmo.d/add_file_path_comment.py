# asmo.d/add_file_path_comment.py
import argparse
import os
from typing import List, Union

SUPPORTED_EXTS = [".py", ".yaml", ".yml", ".js", ".ts", ".html", ".vue"]
SUPPORTED_FILENAMES = ["Dockerfile", "Makefile"]
DEFAULT_IGNORE_DIRS = [
    "migrations",
    "node_modules",
    "dist",
    "build",
    ".docker_volumes",
    ".git",
    ".venv",
]


def get_comment_syntax(file_name, ext) -> Union[str, tuple, None]:
    if file_name in SUPPORTED_FILENAMES or ext in [".py", ".yaml", ".yml", ".mk"]:
        return "#"
    elif ext in [".js", ".ts"]:
        return "//"
    elif ext in [".html", ".vue"]:
        return ("<!--", "-->")
    return None


def should_process(file_name, ext):
    return (
        file_name in SUPPORTED_FILENAMES
        or ext in SUPPORTED_EXTS
        or file_name.endswith(".mk")
    )


def process_file(file_path: str, root_dir: str = "."):
    file_name = os.path.basename(file_path)
    file_ext = os.path.splitext(file_name)[1].lower()

    if not should_process(file_name, file_ext):
        return

    comment_syntax = get_comment_syntax(file_name, file_ext)
    if not comment_syntax:
        print(f"Skipping unsupported type: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        print(f"Skipping {file_path}: {e}")
        return

    if not lines or all(line.strip() == "" for line in lines):
        return

    rel_path = os.path.relpath(file_path, root_dir)

    # Remove existing comment if it's the first line and matches pattern
    if isinstance(comment_syntax, tuple):
        if (
            lines
            and lines[0].strip().startswith(comment_syntax[0])
            and lines[0].strip().endswith(comment_syntax[1])
        ):
            lines.pop(0)
        new_comment = f"{comment_syntax[0]} {rel_path} {comment_syntax[1]}\n"
    else:
        if lines and lines[0].strip().startswith(comment_syntax):
            lines.pop(0)
        new_comment = f"{comment_syntax} {rel_path}\n"

    while lines and lines[0].strip() == "":
        lines.pop(0)

    lines.insert(0, new_comment)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Updated: {rel_path}")


def run_on_directory(root_dir: str, ignore_dirs: List[str]):
    for root, _, files in os.walk(root_dir):
        if any(ignored in root.split(os.sep) for ignored in ignore_dirs):
            continue

        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, root_dir=root_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Add file path comment to files.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-d", "--directory", help="Directory to scan recursively")
    group.add_argument("-f", "--files", nargs="+", help="Specific files to process")

    parser.add_argument(
        "--ignore-dirs",
        nargs="*",
        default=DEFAULT_IGNORE_DIRS,
        help="List of directory names to ignore when using --directory",
    )

    args = parser.parse_args()

    if args.directory:
        run_on_directory(args.directory, args.ignore_dirs)
    elif args.files:
        for file in args.files:
            process_file(file)
