# Auto-Docs Generator

An automated documentation generator for Python projects using AI analysis. This tool scans your project files, analyzes the code structure, and generates comprehensive README and technical reference documentation.

## Features

- **GUI Folder Selection**: Easy-to-use graphical interface for selecting project directories
- **AI-Powered Analysis**: Leverages advanced language models to understand and document your code
- **Comprehensive Documentation**: Generates both user-friendly README and detailed technical references
- **Python Project Focus**: Optimized for Python codebase analysis
- **Rich Console Output**: Beautiful terminal interface with progress indicators

## Requirements

- Python 3.11.9
- Tkinter (included with Python, but ensure it's properly configured)
- Internet connection for AI API calls

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/auto-docs-generator.git
   cd auto-docs-generator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env_example .env
   ```
   Edit `.env` with your actual API credentials.

## Configuration

Create a `.env` file based on `.env_example` with the following variables:

- `FUELIX_API_BASE_URL`: API endpoint URL
- `FUELIX_API_KEY`: Your API key for the AI service
- `SECRET_KEY`: Secret key for secure operations
- `MODEL_NAME`: AI model to use (default: gpt-4o-mini)

## Usage

Run the application:

```bash
python main.py
```

1. A folder selection dialog will appear
2. Choose the Python project directory you want to document
3. The tool will analyze all Python files in the directory
4. Generated documentation will be saved in the `output/` folder:
   - `README_AI.md`: User-friendly project overview
   - `TECHNICAL_REFERENCE.md`: Detailed technical documentation

## Project Structure

```
auto-docs-generator/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env_example           # Environment variables template
├── config/                # Configuration files
│   ├── prompts.py         # AI prompts and templates
│   └── settings.py        # Application settings
├── core/                  # Core functionality
│   ├── file_walker.py     # File system traversal
│   ├── generator.py       # Documentation generation
│   └── llm_client.py      # AI service client
└── output/                # Generated documentation (created automatically)
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

All changes must be submitted via Pull Request. Direct commits to main are not allowed.

## License

[Add your license here]

## Support

If you encounter any issues, please open an issue on GitHub.
