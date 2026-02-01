"""
Security utilities for input sanitization
"""

import html
import re
from typing import Any, Dict, List, Union

class SecurityUtils:
    """Security utilities for sanitizing user input"""
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """Sanitize text for HTML output to prevent XSS"""
        if not isinstance(text, str):
            text = str(text)
        return html.escape(text, quote=True)
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively sanitize dictionary values"""
        if not isinstance(data, dict):
            return {}
        
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = SecurityUtils.sanitize_html(value)
            elif isinstance(value, dict):
                sanitized[key] = SecurityUtils.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = SecurityUtils.sanitize_list(value)
            else:
                sanitized[key] = value
        return sanitized
    
    @staticmethod
    def sanitize_list(data: List[Any]) -> List[Any]:
        """Sanitize list items"""
        if not isinstance(data, list):
            return []
        
        sanitized = []
        for item in data:
            if isinstance(item, str):
                sanitized.append(SecurityUtils.sanitize_html(item))
            elif isinstance(item, dict):
                sanitized.append(SecurityUtils.sanitize_dict(item))
            elif isinstance(item, list):
                sanitized.append(SecurityUtils.sanitize_list(item))
            else:
                sanitized.append(item)
        return sanitized
    
    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """Validate API key format"""
        if not isinstance(api_key, str):
            return False
        
        # Basic validation for Gemini API keys
        api_key = api_key.strip()
        if len(api_key) < 20:
            return False
        
        # Check for suspicious patterns
        if any(char in api_key for char in ['<', '>', '"', "'", '&']):
            return False
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        if not isinstance(filename, str):
            filename = str(filename)
        
        # Remove path separators and dangerous characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'\.\.', '_', filename)  # Prevent directory traversal
        
        # Limit length
        if len(filename) > 100:
            filename = filename[:100]
        
        return filename.strip()