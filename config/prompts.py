# System prompt for the File Analysis step (Step 2)
# We force JSON mode here so the Pydantic parser works correctly.
ANALYSIS_SYSTEM_PROMPT = """You are a Senior Software Architect and Code Analyst. 
Your goal is to extract technical details from source code with high accuracy.
You must output strictly valid JSON matching the requested schema."""

# The template for sending code to the LLM. 
# We use {filename} and {content} as placeholders.
ANALYSIS_USER_PROMPT = """Analyze the following source code file: '{filename}'.
Extract the architecture, dependencies, and logic flow.

Key Requirements:
1. Identify the TYPE of element (class, function, variable).
2. Summarize the purpose of the file in 1-2 sentences.
3. List external dependencies (imports).
4. Note any technical debt or complex algorithms in 'technical_notes'.

CODE CONTENT:
{content}
"""

# System prompt for the Final README generation (Step 3)
README_SYSTEM_PROMPT = """You are an expert Technical Writer. 
You are writing documentation for a GitHub repository.
Your writing style is professional, clear, and concise.
Do not mention that you are an AI. Write as if you are the lead developer."""

# The template for generating the README
README_USER_PROMPT = """Here is the technical summary of the entire project, broken down by file.
Based on this data, write a comprehensive `README.md` file.

The README must include:
1. **Project Title & Description**: Infer what the project does from the summaries.
2. **Key Features**: Bullet points of main capabilities.
3. **Architecture Overview**: How the files relate to each other.
4. **Installation/Usage**: Standard Python instructions (pip install, etc).

PROJECT DATA:
{project_summary}
"""