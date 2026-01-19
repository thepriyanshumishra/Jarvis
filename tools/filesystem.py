import os
from typing import List, Optional
from tools.registry import ToolRegistry

@ToolRegistry.register(name="read_file", description="Reads the content of a file. Args: path")
def read_file(path: str) -> str:
    try:
        if not os.path.exists(path):
            return f"Error: File '{path}' does not exist."
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@ToolRegistry.register(name="write_file", description="Writes content to a file. Args: path, content")
def write_file(path: str, content: str) -> str:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@ToolRegistry.register(name="list_files", description="Lists files in a directory. Args: path")
def list_files(path: str = ".") -> str:
    try:
        if not os.path.exists(path):
            return f"Error: Directory '{path}' does not exist."
        files = os.listdir(path)
        return "\n".join(files)
    except Exception as e:
        return f"Error listing directory: {str(e)}"
