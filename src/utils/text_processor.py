"""
Text processing utilities
"""

import re
from typing import List

class TextProcessor:
    @staticmethod
    def preprocess_text(text: str) -> List[str]:
        """Clean and split text into sentences"""
        text = re.sub(r'\s+', ' ', text)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > 10]
    
    @staticmethod
    def extract_names(text: str) -> List[str]:
        """Extract capitalized names from text"""
        names = re.findall(r'\b[A-Z][a-z]+\b', text)
        return list(set(names))[:3]
    
    @staticmethod
    def extract_deadline(sentence: str) -> str:
        """Extract deadline from sentence"""
        patterns = [
            r'by (\w+day|\w+\s+\d+)',
            r'due (\w+day|\w+\s+\d+)',
            r'deadline (\w+day|\w+\s+\d+)',
            r'before (\w+day|\w+\s+\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, sentence.lower())
            if match:
                return match.group(1).title()
        return 'Not specified'