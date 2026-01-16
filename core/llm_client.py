from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from config.settings import settings
# Import the prompts
from config.prompts import (
    ANALYSIS_SYSTEM_PROMPT, 
    ANALYSIS_USER_PROMPT, 
    README_SYSTEM_PROMPT, 
    README_USER_PROMPT
)
from rich.console import Console

console = Console()

# --- Data Models (Unchanged) ---
class CodeElement(BaseModel):
    name: str = Field(..., description="Name of the class or function")
    type: str = Field(..., description="Either 'class', 'function', or 'variable'")
    description: str = Field(..., description="A technical summary of what this element does")
    inputs: List[str] = Field(default_factory=list, description="List of arguments/inputs")
    outputs: str = Field(..., description="Return type or description of output")

class FileAnalysis(BaseModel):
    summary: str = Field(..., description="A high-level summary of the file's purpose")
    dependencies: List[str] = Field(default_factory=list, description="External libraries imported")
    elements: List[CodeElement] = Field(default_factory=list, description="Key classes/functions")
    technical_notes: Optional[str] = Field(None, description="Specific algorithms or warnings")

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
        # Truncate content to avoid token limits (approx 15k chars is safe for most models)
        safe_content = code_content[:15000]
        
        # Inject values into the prompt template
        user_message = ANALYSIS_USER_PROMPT.format(filename=filename, content=safe_content)

        try:
            completion = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                response_format=FileAnalysis
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            console.print(f"[red]⚠️ Error analyzing {filename}: {e}[/red]")
            return FileAnalysis(
                summary="Analysis Failed", 
                dependencies=[], 
                elements=[], 
                technical_notes=f"Error: {str(e)}"
            )

    def generate_readme(self, project_summary: str) -> str:
        """
        Generates the final User Manual / README based on all file summaries.
        """
        # Inject values into the prompt template
        user_message = README_USER_PROMPT.format(project_summary=project_summary)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": README_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"# Error Generating README\n\n{e}"