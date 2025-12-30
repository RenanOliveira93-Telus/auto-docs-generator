from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from config.settings import settings
from rich.console import Console

console = Console()

# --- Data Models (Structured Output) ---
# This forces the LLM to give us clean JSON data, not just chat text.

class CodeElement(BaseModel):
    name: str = Field(..., description="Name of the class or function")
    type: str = Field(..., description="Either 'class', 'function', or 'variable'")
    description: str = Field(..., description="A technical summary of what this element does")
    inputs: List[str] = Field(default_factory=list, description="List of arguments/inputs")
    outputs: str = Field(..., description="Return type or description of output")

class FileAnalysis(BaseModel):
    summary: str = Field(..., description="A high-level summary of the file's purpose (1-2 sentences)")
    dependencies: List[str] = Field(default_factory=list, description="External libraries or internal modules imported")
    elements: List[CodeElement] = Field(default_factory=list, description="Key classes and functions defined in this file")
    technical_notes: Optional[str] = Field(None, description="Any specific algorithms, patterns, or warnings found")

# --- The Client Wrapper ---

class LLMClient:
    def __init__(self):
        try:
            self.client = OpenAI(
                api_key=settings.get_api_key(),
                base_url=settings.get_api_base()
            )
            self.model = settings.get_model()
        except Exception as e:
            console.print(f"[bold red]❌ Failed to initialize AI Client:[/bold red] {e}")
            raise

    def analyze_code(self, filename: str, code_content: str) -> FileAnalysis:
        """
        Sends a single file to the LLM and asks for a structured analysis.
        """
        prompt = f"""
        You are a Senior Software Architect. Analyze the following source code file: '{filename}'.
        Extract the architecture, dependencies, and logic flow. 
        Focus on technical accuracy.
        
        CODE:
        {code_content[:15000]}  # Truncate to avoid token limits if file is huge
        """

        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful coding assistant that outputs strict JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format=FileAnalysis
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            console.print(f"[red]⚠️ Error analyzing {filename}: {e}[/red]")
            # Return an empty analysis object so the pipeline doesn't crash
            return FileAnalysis(summary="Analysis Failed", dependencies=[], elements=[], technical_notes=str(e))

    def generate_readme(self, project_summary: str) -> str:
        """
        Generates the final User Manual / README based on all file summaries.
        Returns a Markdown string.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a technical writer creating a professional README.md."},
                    {"role": "user", "content": f"Here is the technical summary of a project. Write a comprehensive README.md including: Introduction, Installation, Usage, and Architecture Overview.\n\nDATA:\n{project_summary}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"# Error Generating README\n\n{e}"