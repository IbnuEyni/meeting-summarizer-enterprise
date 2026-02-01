"""
Pattern configurations for analysis
"""

import re
import logging

class PatternConfig:
    try:
        DECISION_PATTERNS = [
            (r'we (decided|agreed|concluded|determined) (to|that) (.+)', 0.9),
            (r'(decision|conclusion): (.+)', 0.8),
            (r'it was (decided|agreed) (.+)', 0.85),
            (r'we will (go with|choose|select|implement) (.+)', 0.8),
            (r'final decision (.+)', 0.95),
            (r'approved (.+)', 0.7)
        ]
        
        # Compile regex patterns to catch errors early
        for pattern, _ in DECISION_PATTERNS:
            re.compile(pattern)

        ACTION_PATTERNS = [
            (r'(\w+) (will|should|needs to|must) (.+)', 0.8),
            (r'action item: (\w+) - (.+)', 0.9),
            (r'(\w+) is responsible for (.+)', 0.85),
            (r'(\w+) to (.+) by (.+)', 0.9),
            (r'assign (\w+) to (.+)', 0.7)
        ]

        for pattern, _ in ACTION_PATTERNS:
            re.compile(pattern)

        PRIORITY_KEYWORDS = {
            'critical': ['urgent', 'asap', 'critical', 'emergency', 'immediately'],
            'high': ['important', 'priority', 'must', 'required', 'essential'],
            'medium': ['should', 'recommended', 'preferred', 'consider'],
            'low': ['could', 'maybe', 'optional', 'nice to have']
        }
        
        SENTIMENT_INDICATORS = {
            'positive': ['great', 'excellent', 'perfect', 'amazing', 'successful'],
            'negative': ['problem', 'issue', 'concern', 'delay', 'blocker'],
            'neutral': ['update', 'status', 'review', 'discuss', 'consider']
        }
        
        IMPACT_KEYWORDS = {
            'high': ['budget', 'hire', 'fire', 'strategy', 'launch', 'cancel'],
            'medium': ['feature', 'timeline', 'resource', 'process']
        }
        
        RISK_KEYWORDS = ['delay', 'blocker', 'issue', 'problem', 'concern', 'risk']
    except re.error as e:
        logging.error(f"Regex compilation error in PatternConfig: {e}")
        raise