# MIT License - Copyright (c) 2025 Viktor Kirschner
# Seedling has improved this tool for itself
import os
import sys
import mimetypes
from pathlib import Path

# Reconfigure stdout for proper UTF-8 handling
sys.stdout.reconfigure(encoding='utf-8')

# Set a limit for file size to avoid overwhelming the AI's context window
MAX_CHARS = 50000
MAX_LINES = 1000

def is_binary(path: Path) -> bool:
    """Checks if a file is likely binary using multiple methods."""
    try:
        # Method 1: Check for null bytes
        with open(path, 'rb') as f:
            chunk = f.read(8192)
            if b'\x00' in chunk:
                return True
        
        # Method 2: Check MIME type
        mime_type, _ = mimetypes.guess_type(str(path))
        if mime_type and not mime_type.startswith('text/'):
            # Common text MIME types that don't start with text/
            text_mimes = {
                'application/json',
                'application/javascript',
                'application/xml',
                'application/x-yaml',
                'application/x-httpd-php'
            }
            if mime_type not in text_mimes:
                return True
        
        # Method 3: Try to decode as UTF-8
        try:
            with open(path, 'r', encoding='utf-8') as f:
                f.read(8192)
            return False
        except UnicodeDecodeError:
            return True
            
    except Exception:
        return True

def format_content(content: str, show_line_numbers: bool = False, max_lines: int = None) -> str:
    """Format content with optional line numbers and line limits."""
    lines = content.splitlines()
    
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        truncated = True
    else:
        truncated = False
    
    if show_line_numbers:
        numbered_lines = []
        for i, line in enumerate(lines, 1):
            numbered_lines.append(f"{i:4d}: {line}")
        formatted_content = "\n".join(numbered_lines)
    else:
        formatted_content = "\n".join(lines)
    
    return formatted_content, truncated

def run(*args):
    """
    Reads and returns the content of a specified text file.
    Handles errors, binary files, and truncates large files.
    
    Usage: read_file <filename> [options]
    
    Options:
        --line-numbers    Show line numbers
        --max-lines=N     Limit output to N lines (default: 1000)
        --raw             Show raw content without formatting
    """
    if not args:
        return "[ERROR] No filename provided. Usage: read_file <filename> [options]"
    
    # Parse arguments
    filename = args[0]
    options = args[1:] if len(args) > 1 else []
    
    show_line_numbers = "--line-numbers" in options
    raw_output = "--raw" in options
    max_lines = None
    
    for opt in options:
        if opt.startswith("--max-lines="):
            try:
                max_lines = int(opt.split("=", 1)[1])
            except ValueError:
                return "[ERROR] Invalid --max-lines value. Use a number."
    
    # Use pathlib for better path handling
    target_path = Path(filename).resolve()
    
    # Check if file exists and is accessible
    if not target_path.exists():
        return f"[ERROR] File not found: '{filename}'"
    if not target_path.is_file():
        return f"[ERROR] Path is a directory, not a file: '{filename}'"
    
    # Check file permissions
    if not os.access(target_path, os.R_OK):
        return f"[ERROR] Permission denied to read file: '{filename}'"
    
    # Check if binary file
    if is_binary(target_path):
        # Get file size for binary files
        file_size = target_path.stat().st_size
        mime_type, _ = mimetypes.guess_type(str(target_path))
        mime_info = f" ({mime_type})" if mime_type else ""
        return f"[ERROR] Cannot read file: '{filename}' appears to be a binary file{mime_info}. Size: {file_size:,} bytes"

    try:
        # Read the file with proper encoding detection
        with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        output = [f"--- Content of {filename} ---"]
        
        # Check if content is too large
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS]
            truncated_chars = True
        else:
            truncated_chars = False
        
        # Format content based on options
        if not raw_output:
            formatted_content, truncated_lines = format_content(
                content, 
                show_line_numbers, 
                max_lines if max_lines else MAX_LINES
            )
            output.append(formatted_content)
            
            info_parts = []
            if truncated_chars:
                info_parts.append(f"truncated to {MAX_CHARS} characters")
            if truncated_lines and max_lines:
                info_parts.append(f"limited to {max_lines} lines")
            elif truncated_lines:
                info_parts.append(f"limited to {MAX_LINES} lines")
            
            if info_parts:
                output.append(f"--- [INFO] File {', '.join(info_parts)}. ---")
            else:
                output.append("--- [INFO] End of file. ---")
        else:
            output.append(content)
            if truncated_chars:
                output.append(f"--- [INFO] File truncated to {MAX_CHARS} characters ---")
        
        return "\n".join(output)
            
    except Exception as e:
        return f"[ERROR] An unexpected error occurred while reading '{filename}': {e}"

if __name__ == "__main__":
    # This allows the script to be run directly for testing.
    if len(sys.argv) > 1:
        print(run(*sys.argv[1:]))
    else:
        print("Usage: python read_file.py <filename> [--line-numbers] [--max-lines=N] [--raw]")