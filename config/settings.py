import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # --- File System Settings ---
    IGNORE_DIRS = {
        '.git', '.idea', '.vscode', '__pycache__', 'venv', 'env', 
        'node_modules', 'dist', 'build', 'site-packages', '.DS_Store'
    }
    ALLOWED_EXTENSIONS = {'.py', '.md', '.txt', '.yml', '.yaml', '.json', '.js', '.ts', '.java'}

    # --- AI Provider Settings (FuelIX) ---
    @staticmethod
    def get_api_key():
        # Returns the FuelIX key
        return os.getenv("FUELIX_API_KEY")

    @staticmethod
    def get_api_base():
        # Returns the FuelIX URL
        return os.getenv("FUELIX_API_BASE_URL")
    
    @staticmethod
    def get_model():
        return os.getenv("MODEL_NAME", "gpt-4o-mini")

settings = Settings()