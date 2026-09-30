#!/usr/bin/env python3
"""Build a clean, upload-ready OpenAI plugin ZIP from this repository."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
OUTPUT = DIST / "fiverr-gig-optimizer-openai-plugin.zip"
PREFIX = Path("fiverr-gig-optimizer")

INCLUDE_FILES = (
    Path(".codex-plugin/plugin.json"),
    Path("README.md"),
    Path("LICENSE"),
    Path("LICENSE-DATA"),
    Path("chatgpt/INSTRUCTIONS.md"),
    Path("docs/guides/OPENAI_SETUP.md"),
    Path("assets/plugin-logo.png"),
    Path("assets/plugin-icon.png"),
)


def included_paths():
    paths = [ROOT / item for item in INCLUDE_FILES]
    skill_root = ROOT / "skills" / "fiverr-gig-optimizer"
    paths.extend(
        path for path in skill_root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )
    return sorted(set(paths))


def build(output=OUTPUT):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    files = included_paths()
    missing = [str(path.relative_to(ROOT)) for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing plugin files: " + ", ".join(missing))
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, (PREFIX / path.relative_to(ROOT)).as_posix())
    return output, len(files)


if __name__ == "__main__":
    result, count = build()
    print(f"Wrote {result} ({count} files).")
