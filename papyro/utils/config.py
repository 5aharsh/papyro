import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file globally
load_dotenv()

# Configuration Keys
KEY_TITLE = "title"
KEY_THEME = "theme"
KEY_NAV_ORDER = "nav_order"

# Env Var Names
ENV_CONTENT_DIR = "PAPYRO_CONTENT_DIR"

class ContentDirectoryError(Exception):
    """Raised when the content directory is missing or inaccessible."""
    def __init__(self, path: Path):
        self.path = path
        self.message = f"Content directory not found at: {path.absolute()}"
        super().__init__(self.message)

def get_content_dir() -> Path:
    """
    Returns the Path to the content directory.
    Priority:
    1. Environment variable PAPYRO_CONTENT_DIR
    2. Default: <project_root>/papyro/content
    """
    env_content_dir = os.getenv(ENV_CONTENT_DIR)
    if env_content_dir:
        return Path(env_content_dir)
    return Path(__file__).parent.parent / "content"

def validate_content_dir():
    """Checks if the content directory exists and is a directory."""
    path = get_content_dir()
    if not path.exists() or not path.is_dir():
        raise ContentDirectoryError(path)

def load_config():
    """
    Load site configuration from JSON.
    """
    config = {
        KEY_THEME: "papyro-default",
        KEY_TITLE: "Papyro",
        KEY_NAV_ORDER: []
    } # Defaults
    
    config_path = get_content_dir() / "site-config.json"
    
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config.update(json.load(f))
        
    return config

def get_theme_path():
    config = load_config()
    return Path(__file__).parent.parent / "templates" / config[KEY_THEME]
