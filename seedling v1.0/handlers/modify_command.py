# MIT License - Copyright (c) 2025 Viktor Kirschner
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

# The directory where commands are stored by default.
HANDLERS_DIR = "handlers"

def run(*args):
    """
    Overwrites an existing command file with new code, using the same flexible
    pathing logic as the main CLI tool.
    """
    if len(args) != 2:
        return "[ERROR] Incorrect usage. Required: modify_command <name> \"<new_code>\""

    command_name = args[0]
    new_code = args[1]

    if not command_name or not command_name.strip():
        return "[ERROR] Command name cannot be empty."

    # --- Start of New Logic ---

    # 1. Handle the filename extension intelligently
    if not command_name.endswith('.py'):
        name_with_ext = f"{command_name}.py"
    else:
        name_with_ext = command_name

    ai_path = Path(name_with_ext)
    final_path = None

    # 2. Use the same path-finding logic as the main tool
    # Check if the AI specified a subdirectory (e.g., "plugins/command.py").
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
        return f"[ERROR] Command '{command_name}' not found at expected path '{final_path}'. Cannot modify."

    # --- End of New Logic ---

    try:
        # Write the new code to the file, overwriting existing content
        with open(final_path, 'w', encoding='utf-8') as f:
            # The AI sometimes sends newlines as '\\n' strings, so we process them.
            processed_code = new_code.replace('\\n', '\n')
            f.write(processed_code)
        return f"[SUCCESS] Command '{command_name}' at '{final_path}' has been modified successfully."
    except Exception as e:
        return f"[ERROR] An unexpected error occurred while modifying command '{command_name}': {e}"

if __name__ == "__main__":
    # This allows the script to be run directly for testing.
    if len(sys.argv) > 2:
        print(run(*sys.argv[1:]))
    else:
        print("Usage: python modify_command.py <command_name> \"<new_code>\"")