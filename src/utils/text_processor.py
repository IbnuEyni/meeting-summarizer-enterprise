"""
Text processing utilities
"""

import re
from typing import List

class TextProcessor:
    MIN_SENTENCE_LENGTH = 10
    MAX_NAMES = 3
    
    # Compiled regex patterns for better performance
    _DEADLINE_PATTERNS = [
        re.compile(r'by (\w+day|\w+\s+\d+)'),
        re.compile(r'due (\w+day|\w+\s+\d+)'),
        re.compile(r'deadline (\w+day|\w+\s+\d+)'),
        re.compile(r'before (\w+day|\w+\s+\d+)')
    ]
    
    @staticmethod
    def preprocess_text(text: str) -> List[str]:
        """Clean and split text into sentences"""
        text = re.sub(r'\s+', ' ', text)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if len(s.strip()) > TextProcessor.MIN_SENTENCE_LENGTH]
    
    @staticmethod
    def extract_names(text: str) -> List[str]:
        """Extract capitalized names from text"""
        names = re.findall(r'\b[A-Z][a-z]+\b', text)
        return list(set(names))[:TextProcessor.MAX_NAMES]
    
    @staticmethod
    def extract_deadline(sentence: str) -> str:
        """Extract deadline from sentence"""
        sentence_lower = sentence.lower()
        
        for pattern in TextProcessor._DEADLINE_PATTERNS:
            match = pattern.search(sentence_lower)
            if match:
                return match.group(1).title()
        return 'Not specified'