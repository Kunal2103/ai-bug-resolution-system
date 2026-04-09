import os
import re
import sys
from langchain_core.tools import tool
from logger import logger
from exception import CustomException

@tool
def read_file(file_path: str) -> str:
    """Reads and returns the entire content of a file."""
    try:
        logger.info(f"Tool 'read_file' called for path: {file_path}")
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except Exception as e:
        raise CustomException(e, sys)

@tool
def search_logs(file_path: str, pattern: str, context_lines: int = 2) -> str:
    """
    Searches a log file for a regex pattern or keyword (like ripgrep).
    Returns the matching lines along with surrounding context lines.
    """
    try:
        logger.info(f"Tool 'search_logs' called for pattern '{pattern}' in {file_path}")
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' does not exist."

        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        matches = []
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            return f"Error: Invalid regex pattern '{pattern}'"

        for i, line in enumerate(lines):
            if regex.search(line):
                start = max(0, i - context_lines)
                end = min(len(lines), i + context_lines + 1)
                context = "".join(lines[start:end])
                matches.append(f"--- Match found around line {i+1} ---\n{context}")

        if not matches:
            return f"No matches found for pattern '{pattern}'."
        
        return "\n".join(matches)
    except Exception as e:
        raise CustomException(e, sys)
    
@tool
def write_file(file_path: str, content: str) -> str:
    """Writes content to a file, overwriting it if it exists. Used to save code or scripts."""
    try:
        logger.info(f"Tool 'write_file' called for path: {file_path}")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        raise CustomException(e, sys)


@tool
def list_directories(directory_path: str = ".") -> str:
    """Lists all files and directories in the given path. Useful for finding code files. Do not use this for logs."""
    try:

        logger.info(f"Tool 'list_directories' called to scan repository path: '{directory_path}'")
        tree = []
        for root, dirs, files in os.walk(directory_path):
            # Ignore hidden folders and pycache to save tokens
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            level = root.replace(directory_path, '').count(os.sep)
            indent = ' ' * 4 * level
            tree.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                if not f.startswith('.'):
                    tree.append(f"{subindent}{f}")
        result_string = "\n".join(tree)

        return result_string
        
    except Exception as e:
        raise CustomException(e, sys)