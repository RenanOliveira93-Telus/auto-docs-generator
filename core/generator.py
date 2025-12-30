import os
from rich.progress import Progress
from core.llm_client import LLMClient
from typing import Dict, List
from pathlib import Path

class DocumentationGenerator:
    def __init__(self):
        self.llm = LLMClient()
        self.analyzed_files = []

    def process_project(self, file_map: Dict[str, str]):
        """
        Main logic: 
        1. Analyze each file.
        2. Compile results.
        3. Generate Final Docs.
        """
        total_files = len(file_map)
        
        # We collect strings here to build the final context for the README
        project_context = []
        technical_docs = []

        with Progress() as progress:
            task = progress.add_task("[green]🤖 Analyzing Codebase...", total=total_files)
            
            for file_path, content in file_map.items():
                # 1. Analyze the file (Step 2 - The Analyst)
                analysis = self.llm.analyze_code(file_path, content)
                
                # 2. Store structured data for the Project Overview
                context_entry = f"File: {file_path}\nSummary: {analysis.summary}\nDependencies: {', '.join(analysis.dependencies)}"
                project_context.append(context_entry)

                # 3. Create the Technical Reference Page for this file
                doc_page = self._format_technical_page(file_path, analysis)
                technical_docs.append(doc_page)
                
                progress.advance(task)

        return project_context, technical_docs

    def _format_technical_page(self, file_path, analysis) -> str:
        """Converts the structured JSON analysis into readable Markdown."""
        md = f"## Module: `{file_path}`\n\n"
        md += f"**Summary:** {analysis.summary}\n\n"
        
        if analysis.dependencies:
            md += f"**Dependencies:** `{', '.join(analysis.dependencies)}`\n\n"
            
        if analysis.elements:
            md += "### Classes & Functions\n"
            for item in analysis.elements:
                md += f"- **{item.type.title()} `{item.name}`**\n"
                md += f"  - *Description:* {item.description}\n"
                if item.inputs:
                    md += f"  - *Inputs:* {item.inputs}\n"
                md += f"  - *Returns:* `{item.outputs}`\n"
        
        md += "\n---\n"
        return md

    def create_final_docs(self, project_context: List[str], technical_docs: List[str]):
        """
        Assembles the README and the Technical Reference file.
        """
        # Join all summaries to send to the LLM for the README
        full_project_summary = "\n\n".join(project_context)
        
        # Call LLM for the high-level README
        readme_content = self.llm.generate_readme(full_project_summary)
        
        # Combine all technical pages into one big Reference Manual
        reference_content = "# Technical Reference Manual\n\n" + "\n".join(technical_docs)

        return readme_content, reference_content