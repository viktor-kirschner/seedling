# MIT License - Copyright (c) 2025 Viktor Kirschner
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

# The directory where command scripts are stored by default.
HANDLERS_DIR = "handlers"

def run(*args):
    """
    Finds a specific line in a file and replaces it, using flexible pathing.
    """
    if len(args) != 3:
        return "[ERROR] Incorrect usage. Required: edit_line <name> \"<exact_line_to_find>\" \"<replacement_line>\""

    command_name, line_to_find, replacement_line = args

    # --- Start of Fix: Standardized Path-Finding Logic ---

    # 1. Handle the filename extension intelligently
    if not command_name.endswith('.py'):
        name_with_ext = f"{command_name}.py"
    else:
        name_with_ext = command_name

    ai_path = Path(name_with_ext)
    final_path = None

    # 2. Use the same path-finding logic as the main tool
    if str(ai_path.parent) != '.':
        # AI specified a directory. Check if this directory exists at the root level.
        potential_root_dir = ai_path.parent
        if potential_root_dir.is_dir():
            # The directory exists at the root, so that's where we'll look.
            final_path = potential_root_dir / ai_path.name
        else:
            # Otherwise, we default to looking inside the 'handlers' directory.
            final_path = Path(HANDLERS_DIR) / ai_path
    else:
        # No subdirectory was specified, so the file must be in 'handlers'.
        final_path = Path(HANDLERS_DIR) / ai_path

    # 3. Check if the command file exists at the determined path
    if not final_path.is_file():
        return f"[ERROR] Command '{command_name}' not found at expected path '{final_path}'."

    # --- End of Fix ---

    try:
        # Read all lines from the file into a list
        with open(final_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Find the line to replace
        line_found = False
        target_line_stripped = line_to_find.strip()
        
        # Ensure the replacement line ends with a newline character
        if not replacement_line.endswith('\n'):
            replacement_line += '\n'

        for i, line in enumerate(lines):
            # Compare lines by stripping whitespace to avoid minor formatting issues
            if line.strip() == target_line_stripped:
                lines[i] = replacement_line
                line_found = True
                break # Stop after finding and replacing the first match

        if not line_found:
            return f"[ERROR] The target line \"{line_to_find}\" was not found in the file. No changes were made."

        # Write the modified list of lines back to the file
        with open(final_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        
        return f"[SUCCESS] The line in file '{final_path}' was edited successfully."

    except Exception as e:
        return f"[ERROR] An unexpected error occurred while editing '{command_name}': {e}"

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(run(sys.argv[1], sys.argv[2], sys.argv[3]))
    else:
        print("Usage: python edit_line.py <command_name> \"<line_to_find>\" \"<replacement_line>\"")