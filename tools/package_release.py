"""Create a sanitized full source ZIP for human review; never modifies Git."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

SOURCE = Path(__file__).resolve().parents[1]
DIST = SOURCE / "dist"
OUTPUT = DIST / "Verdant-Capital-Studio-UI-v2.zip"
EXCLUDE_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache",
                "data_cache", "rag_db", "dist", ".verdant_patch_backup"}


def package():
    DIST.mkdir(exist_ok=True)
    count = 0
    with ZipFile(OUTPUT, "w", ZIP_DEFLATED, compresslevel=7) as archive:
        for file in SOURCE.rglob("*"):
            if not file.is_file():
                continue
            rel = file.relative_to(SOURCE)
            if any(part in EXCLUDE_DIRS for part in rel.parts):
                continue
            if file.name == ".env" or file.suffix in {".db", ".sqlite", ".pyc"}:
                continue
            if file.name.endswith(".log"):
                continue
            archive.write(file, Path(SOURCE.name) / rel)
            count += 1
    print(f"Created {OUTPUT} with {count} source files")
    return OUTPUT


if __name__ == "__main__":
    package()
