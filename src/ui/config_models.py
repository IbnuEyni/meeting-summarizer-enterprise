"""
Configuration models for UI components
"""

from dataclasses import dataclass
from typing import Optional

@dataclass
class SidebarConfig:
    """Configuration data from sidebar"""
    meeting_title: str
    analysis_depth: str
    analysis_method: str
    api_key: Optional[str] = None