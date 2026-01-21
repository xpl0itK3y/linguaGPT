"""
Application configuration management module
"""
import json
from pathlib import Path


class Config:
    """Class for managing application configuration"""
    
    def __init__(self):
        self.config_file = Path.home() / ".gpt_translator_config.json"
        self.api_key = ""
        self.model = "gpt-4o-mini"
        self.ui_language = "en"
        self.load()
    
    def load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.api_key = data.get("api_key", "")
                self.model = data.get("model", "gpt-4o-mini")
                self.ui_language = data.get("ui_language", "en")
        else:
            self.api_key = ""
            self.model = "gpt-4o-mini"
            self.ui_language = "en"
    
    def save(self, api_key=None, model=None, ui_language=None):
        """Save configuration to file"""
        if api_key is not None:
            self.api_key = api_key
        if model is not None:
            self.model = model
        if ui_language is not None:
            self.ui_language = ui_language
        
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "api_key": self.api_key,
                    "model": self.model,
                    "ui_language": self.ui_language,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )
    
    def delete(self):
        """Delete configuration file"""
        if self.config_file.exists():
            self.config_file.unlink()
        self.api_key = ""
        self.model = "gpt-4o-mini"
        self.ui_language = "en"
