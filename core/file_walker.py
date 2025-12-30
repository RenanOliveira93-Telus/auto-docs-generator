import os
from pathlib import Path
from typing import Dict, List
from config.settings import settings
from rich.console import Console

console = Console()

class FileWalker:
    def __init__(self, target_dir: str):
        self.target_dir = Path(target_dir).resolve()
        
        if not self.target_dir.exists():
            raise ValueError(f"The target directory '{self.target_dir}' does not exist.")

    def should_ignore(self, path: Path) -> bool:
        """Checks if a file or directory should be ignored based on settings."""
        # Check if any part of the path is in the ignore list
        for part in path.parts:
            if part in settings.IGNORE_DIRS:
                return True
        return False

    def walk(self) -> Dict[str, str]:
        """
        Scans the target directory and reads content of allowed files.
        Returns a dictionary: { "relative/path/to/file.py": "file_content" }
        """
        file_map = {}
        console.print(f"[bold blue]🔍 Scanning directory:[/bold blue] {self.target_dir}")

        # Walk through the directory top-down
        for root, dirs, files in os.walk(self.target_dir):
            root_path = Path(root)

            # Modify 'dirs' in-place to prevent os.walk from visiting ignored directories
            # This is more efficient than checking after the fact [cite: 282]
            dirs[:] = [d for d in dirs if d not in settings.IGNORE_DIRS]

            for file in files:
                file_path = root_path / file

                # check extension
                if file_path.suffix not in settings.ALLOWED_EXTENSIONS:
                    continue

                # check ignore rules again just in case
                if self.should_ignore(file_path):
                    continue

                try:
                    # calculating relative path for cleaner documentation titles
                    relative_path = file_path.relative_to(self.target_dir)
                    
                    # Read file content
                    # Using 'errors="ignore"' to skip binary files acting like text
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        file_map[str(relative_path)] = content
                        
                except Exception as e:
                    console.print(f"[red]⚠️ Error reading {file_path}: {e}[/red]")

        console.print(f"[green]✅ Found {len(file_map)} valid files.[/green]")
        return file_map