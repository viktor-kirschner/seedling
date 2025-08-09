# MIT License - Copyright (c) 2025 Viktor Kirschner
import os
import shutil
from pathlib import Path
import sys

# Get where the script itself is located — the "clean" source
SOURCE_DIR = Path(sys.argv[0]).parent.resolve()

# Get where the command was *called* from — the target
TARGET_DIR = Path(os.getcwd()).resolve()

# Files/folders to copy
ITEMS_TO_COPY = [
    "cli_tool.py",
    "ai_connector.py",
    "agentk.bat",
    "priming_prompt.txt",
    "license.txt",
    "handlers",  # folder
]

def main():
    if SOURCE_DIR == TARGET_DIR:
        print("❌ Refusing to overwrite the source folder.")
        return

    print(f"📦 Deploying clean Nemo into:\n  {TARGET_DIR}")

    for item in ITEMS_TO_COPY:
        src = SOURCE_DIR / item
        dst = TARGET_DIR / item

        if not src.exists():
            print(f"⚠️  Missing from source: {item}")
            continue

        if dst.exists():
            if dst.is_dir():
                shutil.rmtree(dst)
            else:
                dst.unlink()

        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    print("✅ Done.")

if __name__ == "__main__":
    main()
