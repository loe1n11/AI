"""
Configuration management for AI Knowledge Assistant
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


class Config:
    """Load and manage application configuration"""
    
    def __init__(self, config_file: str = "config.json"):
        """Initialize configuration from file"""
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self._load_config()
        self._load_env_vars()
    
    def _load_config(self) -> None:
        """Load configuration from JSON file"""
        if Path(self.config_file).exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Default configuration
            self.config = {
                "app_name": "AI Knowledge Assistant",
                "version": "2.0",
                "debug": False,
                "embedding_model": "text-embedding-3-small",
                "chat_model": "gpt-3.5-turbo",
                "max_context_length": 2000,
                "chunk_size": 500,
                "chunk_overlap": 50,
                "database_path": "./data/chroma_db"
            }
    
    def _load_env_vars(self) -> None:
        """Load environment variables"""
        from dotenv import load_dotenv
        load_dotenv(".env")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_api_key(self) -> str:
        """Get OpenAI API key from environment"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        return api_key
    
    def __repr__(self) -> str:
        return f"<Config: {self.config}>"
