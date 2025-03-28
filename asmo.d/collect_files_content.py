# asmo.d/collect_files_content.py
import argparse
import os
from pathlib import Path

DEFAULT_IGNORE = {
    ".idea",
    ".vscode",
    ".DS_Store",
    ".git",
    ".venv",
    ".docker_volumes",
    "asmo.d",
    "__pycache__",
    "migrations",
    "node_modules",
    "dist",
    "build",
}

DEFAULT_EXTENSIONS = {
    "Dockerfile",
    "package.json",
    "tsconfig.json",
    ".yml",
    ".yaml",
    ".toml",
    ".py",
    ".js",
    ".ts",
    ".vue",
    ".html",
}


def should_include(file: Path, include_exts, exclude_exts):
    name = file.name
    suffix = file.suffix

    if name in include_exts or suffix in include_exts:
        if name not in exclude_exts and suffix not in exclude_exts:
            return True
    return False


def is_ignored(path: Path, ignore_patterns):
    return any(part in ignore_patterns for part in path.parts)


def collect_file_contents(
    root_path: Path,
    output_file: Path,
    include_exts,
    exclude_exts,
    ignore_patterns,
):
    with open(output_file, "w", encoding="utf-8") as out:
        for file_path in root_path.rglob("*"):
            if not file_path.is_file():
                continue

            if is_ignored(file_path, ignore_patterns):
                continue

            if should_include(file_path, include_exts, exclude_exts):
                try:
                    rel_path = file_path.relative_to(root_path)
                    out.write(f"{rel_path}:\n")
                    out.write(file_path.read_text(encoding="utf-8"))
                    out.write("\n\n")
                    print(f"Included: {rel_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a text file containing contents of project files."
    )
    parser.add_argument("-d", "--directory", required=True, help="Directory to scan")
    parser.add_argument("-o", "--output", default="prompt.txt", help="Output file")
    parser.add_argument("-i", "--ignore", nargs="*", help="Additional ignore patterns")
    parser.add_argument("-e", "--include", help="Comma-separated extensions to include")
    parser.add_argument("-x", "--exclude", help="Comma-separated extensions to exclude")

    args = parser.parse_args()

    path = Path(args.directory).resolve()
    output_file = Path(args.output).resolve()

    ignore_patterns = DEFAULT_IGNORE.union(set(args.ignore or []))

    include_exts = (
        set(
            f".{ext.strip()}" if not ext.startswith(".") else ext.strip()
            for ext in args.include.split(",")
        )
        if args.include
        else DEFAULT_EXTENSIONS
    )

    exclude_exts = (
        set(
            f".{ext.strip()}" if not ext.startswith(".") else ext.strip()
            for ext in args.exclude.split(",")
        )
        if args.exclude
        else set()
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    collect_file_contents(
        path, output_file, include_exts, exclude_exts, ignore_patterns
    )

    print(f"\n✅ Written to: {output_file}")
    print(f"Ignored: {sorted(ignore_patterns)}")
    print(f"Included: {sorted(include_exts)}")
    print(f"Excluded: {sorted(exclude_exts)}")


if __name__ == "__main__":
    main()
