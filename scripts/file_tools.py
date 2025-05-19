import os
import sys
from typing import Dict, List, Optional, Union

def resolve_path(path: Optional[str], default_path: Optional[str] = None) -> str:
    """Resolves a file path to an absolute path."""
    file_path = path or default_path
    if not file_path:
        raise ValueError("No path provided and no default path specified")
    return os.path.abspath(file_path) if not os.path.isabs(file_path) else file_path

def get_input_path(args: Optional[List[str]] = None, default_dir: Optional[str] = None, 
                  default_filename: str = "sample.md") -> str:
    """Gets input file path from command line args or uses default."""
    args = args or sys.argv
    if default_dir is None:
        base_dir = os.path.dirname(os.path.abspath(args[0]))
        default_dir = os.path.join(base_dir, "..", "docs")
    
    doc_path = args[1] if len(args) > 1 else os.path.join(default_dir, default_filename)
    return resolve_path(doc_path)

def get_derived_paths(input_path: str, results_dir: str = "results", 
                     docs_dir: Optional[str] = None) -> Dict[str, str]:
    """Generates output paths based on an input path."""
    filename = os.path.basename(input_path).split(".")[0]
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(base_dir, "..", results_dir, f"{filename}_scores.json")
    
    if docs_dir is None:
        improved_path = os.path.join(os.path.dirname(input_path), f"{filename}_improved.md")
    else:
        improved_path = os.path.join(base_dir, "..", docs_dir, f"{filename}_improved.md")
    
    return {
        "results_path": results_path,
        "improved_path": improved_path,
        "filename": filename
    }

def read_file(file_path: str) -> str:
    """Reads a file and returns its contents."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path: str, content: str) -> None:
    """Writes content to a file, creating directories if needed."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)