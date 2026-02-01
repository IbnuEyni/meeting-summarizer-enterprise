"""
Enterprise Meeting Analyzer - Core Analysis Engine
"""

import re
from typing import List, Dict
from ..models.meeting_models import ActionItem, Decision, MeetingAnalysis
from ..utils.text_processor import TextProcessor
from ..utils.patterns import PatternConfig

class EnterpriseAnalyzer:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.patterns = PatternConfig()
    
    def analyze_meeting(self, transcript: str) -> MeetingAnalysis:
        """Main analysis method"""
        sentences = self.text_processor.preprocess_text(transcript)
        
        decisions = self._extract_decisions(sentences)
        action_items = self._extract_actions(sentences)
        metadata = self._extract_metadata(sentences)
        sentiment = self._analyze_sentiment(sentences)
        risks = self._assess_risks(sentences)
        stats = self._generate_stats(decisions, action_items)
        
        return MeetingAnalysis(
            decisions=decisions,
            action_items=action_items,
            metadata=metadata,
            sentiment=sentiment,
            risks=risks,
            summary_stats=stats
        )
    
    def _extract_decisions(self, sentences: List[str]) -> List[Decision]:
        """Extract decisions with confidence scoring"""
        decisions = []
        
        for sentence in sentences:
            for pattern, confidence in self.patterns.DECISION_PATTERNS:
                match = re.search(pattern, sentence.lower())
                if match:
                    content = match.groups()[-1].strip()
                    if len(content) > 15:
                        decisions.append(Decision(
                            content=content.capitalize(),
                            impact_level=self._assess_impact(sentence),
                            stakeholders=self.text_processor.extract_names(sentence),
                            confidence=confidence
                        ))
        
        return sorted(decisions, key=lambda x: x.confidence, reverse=True)[:5]
    
    def _extract_actions(self, sentences: List[str]) -> List[ActionItem]:
        """Extract action items with priority detection"""
        actions = []
        
        for sentence in sentences:
            for pattern, confidence in self.patterns.ACTION_PATTERNS:
                match = re.search(pattern, sentence.lower())
                if match:
                    actions.append(ActionItem(
                        assignee=match.group(1).capitalize(),
                        task=match.group(2).strip(),
                        deadline=self.text_processor.extract_deadline(sentence),
                        priority=self._assess_priority(sentence),
                        confidence=confidence
                    ))
        
        return sorted(actions, key=lambda x: (x.priority == 'critical', x.confidence), reverse=True)[:8]
    
    def _assess_impact(self, sentence: str) -> str:
        """Assess decision impact level"""
        sentence_lower = sentence.lower()
        if any(word in sentence_lower for word in self.patterns.IMPACT_KEYWORDS['high']):
            return 'High'
        elif any(word in sentence_lower for word in self.patterns.IMPACT_KEYWORDS['medium']):
            return 'Medium'
        return 'Low'
    
    def _assess_priority(self, sentence: str) -> str:
        """Assess action item priority"""
        sentence_lower = sentence.lower()
        for priority, keywords in self.patterns.PRIORITY_KEYWORDS.items():
            if any(keyword in sentence_lower for keyword in keywords):
                return priority
        return 'medium'
    
    def _extract_metadata(self, sentences: List[str]) -> Dict:
        """Extract meeting metadata"""
        next_meeting = "Not specified"
        attendees = set()
        
        for sentence in sentences:
            meeting_match = re.search(r'next meeting (.+)', sentence.lower())
            if meeting_match:
                next_meeting = meeting_match.group(1).strip().title()
            
            names = self.text_processor.extract_names(sentence)
            attendees.update(names)
        
        return {
            'next_meeting': next_meeting,
            'attendees': list(attendees)[:10],
            'meeting_length': len(sentences)
        }
    
    def _analyze_sentiment(self, sentences: List[str]) -> Dict:
        """Analyze meeting sentiment"""
        sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for sentiment, keywords in self.patterns.SENTIMENT_INDICATORS.items():
                if any(keyword in sentence_lower for keyword in keywords):
                    sentiment_scores[sentiment] += 1
        
        total = sum(sentiment_scores.values()) or 1
        return {k: round(v/total * 100, 1) for k, v in sentiment_scores.items()}
    
    def _assess_risks(self, sentences: List[str]) -> List[str]:
        """Identify potential risks"""
        risks = []
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in self.patterns.RISK_KEYWORDS):
                risks.append(sentence.strip())
        return risks[:3]
    
    def _generate_stats(self, decisions: List[Decision], actions: List[ActionItem]) -> Dict:
        """Generate summary statistics"""
        return {
            'total_decisions': len(decisions),
            'high_impact_decisions': len([d for d in decisions if d.impact_level == 'High']),
            'total_actions': len(actions),
            'critical_actions': len([a for a in actions if a.priority == 'critical']),
            'avg_confidence': round(sum(d.confidence for d in decisions) / len(decisions) if decisions else 0, 2)
        }