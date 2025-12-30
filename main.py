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

def save_output(filename, content):
    """Helper to save files to the output directory."""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    file_path = output_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    console.print(f"[bold green]✔ Saved:[/bold green] {file_path}")

def get_target_directory():
    """
    Opens a native folder selection dialog window.
    Returns the path string or None if cancelled/failed.
    """
    try:
        # Create a hidden root window so a blank box doesn't appear
        root = tk.Tk()
        root.withdraw()
        
        # Bring the dialog to the front
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

    # 1. Input Phase (The "Easy" Way)
    target_path = get_target_directory()

    # If the user closed the window or GUI failed, ask manually
    if not target_path:
        console.print("[bold yellow]No folder selected via window.[/bold yellow]")
        target_path = console.input("[bold green]Please type the path manually (e.g., ../my-project): [/bold green]")

    # Validate input
    if not target_path or not os.path.exists(target_path):
        console.print(f"[bold red]❌ Invalid path:[/bold red] {target_path}")
        return

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

        # 4. Output Phase
        save_output("README_AI.md", readme_md)
        save_output("TECHNICAL_REFERENCE.md", reference_md)

        console.print("\n[bold blue]✨ Documentation Complete! check the /output folder.[/bold blue]")

    except Exception as e:
        console.print(f"[bold red]Critical Error:[/bold red] {e}")

if __name__ == "__main__":
    main()