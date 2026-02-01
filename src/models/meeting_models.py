"""
Data models for meeting analysis
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ActionItem:
    assignee: str
    task: str
    deadline: str
    priority: str
    confidence: float

@dataclass
class Decision:
    content: str
    impact_level: str
    stakeholders: List[str]
    confidence: float

@dataclass
class MeetingAnalysis:
    decisions: List[Decision]
    action_items: List[ActionItem]
    metadata: Dict[str, str]
    sentiment: Dict[str, float]
    risks: List[str]
    summary_stats: Dict[str, float]