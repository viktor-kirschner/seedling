# MIT License - Copyright (c) 2025 Viktor Kirschner
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
# Constants assuming standard project structure relative to the main script
HANDLERS_DIR = "handlers"
PRIMING_PROMPT_FILE = "priming_prompt.txt"

def run(*args):
    """
    Deletes a command's .py file and its corresponding entry from the priming prompt.
    Usage: delete_command <command_name>
    """
    if len(args) != 1:
        return "[ERROR] Incorrect usage. Required: delete_command <command_name>"

    command_name = args[0]

    if not command_name or not command_name.strip():
        return "[ERROR] Command name cannot be empty."

    file_path = os.path.join(HANDLERS_DIR, f"{command_name}.py")
    file_deleted = False
    prompt_updated = False

    # --- Step 1: Delete the command's .py file ---
    if not os.path.exists(file_path):
        # If the file doesn't exist, we can still try to clean the prompt
        print(f"[INFO] Command file '{command_name}.py' not found. Checking priming prompt anyway.")
    else:
        try:
            os.remove(file_path)
            file_deleted = True
        except Exception as e:
            return f"[ERROR] Failed to delete file '{file_path}': {e}"

    # --- Step 2: Remove the command's entry from the priming prompt ---
    if not os.path.exists(PRIMING_PROMPT_FILE):
        return f"[ERROR] '{PRIMING_PROMPT_FILE}' not found. Cannot update it."

    try:
        with open(PRIMING_PROMPT_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        in_command_block = False
        # The command signature we are looking for, e.g., "* `delete_command <command_name>`"
        command_signature = f"* `{command_name}"

        for line in lines:
            # Check if the current line is the start of the command block to delete
            if line.strip().startswith(command_signature):
                in_command_block = True
                prompt_updated = True  # Mark that we found and are removing something
                continue  # Skip this line
            
            # If we are in a block, check for the next command or end of section
            if in_command_block:
                # If the line starts a new command block or is empty, we're done with the old one
                if line.strip().startswith('* `') or not line.strip():
                    in_command_block = False
            
            # If we are not in the block-to-be-deleted, keep the line
            if not in_command_block:
                new_lines.append(line)

        # If we made changes, write them back to the file
        if prompt_updated:
            with open(PRIMING_PROMPT_FILE, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)

    except Exception as e:
        return f"[ERROR] Failed to read or update '{PRIMING_PROMPT_FILE}': {e}"
    
    # --- Final Report ---
    report = []
    if file_deleted:
        report.append(f"Successfully deleted command file '{command_name}.py'.")
    if prompt_updated:
        report.append(f"Successfully removed '{command_name}' entry from the priming prompt.")
    
    if not report:
        return f"[INFO] Command '{command_name}' was not found in the handlers directory or the priming prompt."

    return "[SUCCESS] " + " ".join(report)


if __name__ == "__main__":
    # This allows the script to be run directly for testing.
    if len(sys.argv) > 1:
        print(run(sys.argv[1]))
    else:
        print("Usage: python delete_command.py <command_name>")
