import sys
import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from core.file_walker import FileWalker
from core.generator import DocumentationGenerator

console = Console()

def get_project_name(target_path):
    """
    Extracts the folder name from the full path to use as the project name.
    Example: 'C:/Users/Dev/My-API-Service' -> 'My-API-Service'
    """
    return Path(target_path).name

def save_output(project_name, filename, content):
    """
    Saves files to 'output/{project_name}/{filename}'.
    Creates the folder if it doesn't exist.
    """
    # 1. Define the specific folder for this project
    project_output_dir = Path("output") / project_name
    
    # 2. Create it if it missing
    project_output_dir.mkdir(parents=True, exist_ok=True)
    
    # 3. Save the file
    file_path = project_output_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    console.print(f"[bold green]✔ Saved:[/bold green] {file_path}")

def get_target_directory():
    """
    Opens a native folder selection dialog window.
    Returns the path string or None if cancelled/failed.
    """
    try:
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        console.print("[cyan]📂 Opening folder picker...[/cyan]")
        path = filedialog.askdirectory(title="Select the Project Folder to Document")
        
        root.destroy()
        return path if path else None
    except Exception as e:
        console.print(f"[yellow]⚠️ GUI Picker unavailable ({e}). Switching to manual input.[/yellow]")
        return None

def main():
    console.print(Panel.fit("[bold magenta]Auto-Docs Generator[/bold magenta]", subtitle="Powered by FuelIX & Python"))

    # 1. Input Phase
    target_path = get_target_directory()

    if not target_path:
        console.print("[bold yellow]No folder selected via window.[/bold yellow]")
        target_path = console.input("[bold green]Please type the path manually (e.g., ../my-project): [/bold green]")

    if not target_path or not os.path.exists(target_path):
        console.print(f"[bold red]❌ Invalid path:[/bold red] {target_path}")
        return

    # Extract the project name for folder creation
    project_name = get_project_name(target_path)
    console.print(f"[bold cyan]🎯 Target Project:[/bold cyan] {project_name}")

    try:
        # 2. Ingestion Phase
        walker = FileWalker(target_path)
        file_map = walker.walk()
        
        if not file_map:
            console.print("[red]❌ No valid files found to analyze in that folder.[/red]")
            return

        # 3. Analysis & Generation Phase
        generator = DocumentationGenerator()
        
        console.print("\n[bold yellow]🤖 Starting AI Analysis...[/bold yellow]")
        project_context, technical_docs = generator.process_project(file_map)

        console.print("\n[bold yellow]📝 Generating Final Documentation...[/bold yellow]")
        readme_md, reference_md = generator.create_final_docs(project_context, technical_docs)

        # 4. Output Phase (Now using project_name)
        save_output(project_name, "README.md", readme_md)
        save_output(project_name, "TECHNICAL_REFERENCE.md", reference_md)

        console.print(f"\n[bold blue]✨ Success! Docs saved in: output/{project_name}/[/bold blue]")

    except Exception as e:
        console.print(f"[bold red]Critical Error:[/bold red] {e}")

if __name__ == "__main__":
    main()