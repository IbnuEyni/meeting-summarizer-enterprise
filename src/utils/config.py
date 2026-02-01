"""
Environment configuration utility
"""

import os
from typing import Optional

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False

class Config:
    _env_loaded = False
    
    @classmethod
    def load_env(cls):
        """Load environment variables from .env file once"""
        if DOTENV_AVAILABLE and not cls._env_loaded:
            load_dotenv()
            cls._env_loaded = True
    
    @classmethod
    def get_gemini_api_key(cls) -> Optional[str]:
        """Get Gemini API key from environment"""
        cls.load_env()
        return os.getenv('GEMINI_API_KEY')
    
    @classmethod
    def has_valid_gemini_key(cls) -> bool:
        """Check if valid Gemini API key exists"""
        key = cls.get_gemini_api_key()
        return key is not None and key != 'your_gemini_api_key_here' and len(key.strip()) > 0