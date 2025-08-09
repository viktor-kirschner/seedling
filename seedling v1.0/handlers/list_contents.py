# MIT License - Copyright (c) 2025 Viktor Kirschner
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

def run(*args):
    """
    Lists the contents of a specified directory with details.
    Provides clear output for empty directories or errors.
    Usage: list_contents [optional_path]
    """
    try:
        # Use the first argument as the path, or default to the current directory '.'
        target_path_str = args[0] if args else '.'
        target_path = Path(target_path_str).resolve()

        # --- Error Handling ---
        if not target_path.exists():
            return f"[ERROR] The path '{target_path}' does not exist."
        if not target_path.is_dir():
            return f"[ERROR] The path '{target_path}' is a file, not a directory."

        # --- Listing Contents ---
        items = os.listdir(target_path)

        if not items:
            return f"[INFO] The directory '{target_path}' is empty."

        # --- Formatting the Output ---
        output_lines = [f"Contents of '{target_path}':"]
        for item_name in sorted(items):
            item_path = target_path / item_name
            item_type = "DIR " if item_path.is_dir() else "FILE"
            output_lines.append(f"  - {item_type.ljust(5)} {item_name}")
        
        return "\n".join(output_lines)

    except PermissionError:
        return f"[ERROR] Permission denied to access '{target_path_str}'."
    except Exception as e:
        return f"[ERROR] An unexpected error occurred: {e}"

if __name__ == "__main__":
    # This allows the script to be run directly for testing.
    # The first command-line argument after the script name is passed to run().
    args_to_pass = sys.argv[1:]
    print(run(*args_to_pass))
