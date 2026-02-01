"""
LLM-Powered Meeting Analyzer using Google Gemini API with LangChain
"""

import json
import os
from typing import List, Dict
from ..models.meeting_models import ActionItem, Decision, MeetingAnalysis
from dotenv import load_dotenv
import logging

try:
    import google.generativeai as genai
    from langchain_google_genai import ChatGoogleGenerativeAI
    GEMINI_AVAILABLE = True
except ImportError as e:
    print(f"Import warning: {e}")
    GEMINI_AVAILABLE = False

class LLMAnalyzer:
    def __init__(self, api_key: str):
        if not GEMINI_AVAILABLE:
            raise ImportError("Google Generative AI not installed. Run: pip install google-generativeai langchain-google-genai")
        
        load_dotenv(override=True)
        os.environ['GOOGLE_API_KEY'] = api_key
        genai.configure(api_key=api_key)
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0,
            google_api_key=api_key
        )
    
    def analyze_meeting(self, transcript: str) -> MeetingAnalysis:
        """Analyze meeting using Gemini LLM with comprehensive error handling"""
        
        # Input validation
        if not isinstance(transcript, str) or not transcript.strip():
            return self._create_fallback_analysis("Empty or invalid transcript provided")
        
        if len(transcript) > 50000:  # 50KB limit
            transcript = transcript[:50000] + "... [truncated]"
        
        prompt = f"""
        Analyze this meeting transcript and extract the following information in JSON format:

        {{
            "decisions": [
                {{
                    "content": "decision text",
                    "impact_level": "High/Medium/Low",
                    "stakeholders": ["name1", "name2"],
                    "confidence": 0.95
                }}
            ],
            "action_items": [
                {{
                    "assignee": "person name",
                    "task": "task description",
                    "deadline": "deadline or 'Not specified'",
                    "priority": "critical/high/medium/low",
                    "confidence": 0.9
                }}
            ],
            "metadata": {{
                "next_meeting": "next meeting info or 'Not specified'",
                "attendees": ["name1", "name2"],
                "meeting_length": 50
            }},
            "sentiment": {{
                "positive": 30.0,
                "negative": 20.0,
                "neutral": 50.0
            }},
            "risks": ["risk1", "risk2"],
            "summary_stats": {{
                "total_decisions": 3,
                "high_impact_decisions": 1,
                "total_actions": 5,
                "critical_actions": 2,
                "avg_confidence": 0.85
            }}
        }}

        Return ONLY valid JSON, no other text.

        Transcript:
        {transcript}
        """
        
        try:
            print("🚀 Step 1: Invoking LLM...")
            response = self.llm.invoke(prompt)
            print("✅ Step 1: LLM response received")
        except Exception as e:
            print(f"❌ Step 1 Error - LLM invoke: {e}")
            return self._create_fallback_analysis(f"LLM invocation failed: {str(e)}")
            
        try:
            print("🚀 Step 2: Extracting response content...")
            response_text = response.content.strip()
            print(f"✅ Step 2: Response text extracted (length: {len(response_text)})")
        except Exception as e:
            print(f"❌ Step 2 Error - Content extraction: {e}")
            return self._create_fallback_analysis(f"Content extraction failed: {str(e)}")
            
        try:
            print("🚀 Step 3: Cleaning markdown formatting...")
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json', '').replace('```', '').strip()
            print("✅ Step 3: Markdown cleaned")
        except Exception as e:
            print(f"❌ Step 3 Error - Markdown cleaning: {e}")
            return self._create_fallback_analysis(f"Markdown cleaning failed: {str(e)}")
            
        try:
            print("🚀 Step 4: Parsing JSON...")
            result = json.loads(response_text)
            print("✅ Step 4: JSON parsed successfully")
        except json.JSONDecodeError as e:
            print(f"❌ Step 4 Error - JSON parsing: {e}")
            print(f"Raw response: {response_text[:500]}...")
            return self._create_fallback_analysis(f"JSON parsing failed: {str(e)}")
        except Exception as e:
            print(f"❌ Step 4 Error - Unexpected JSON error: {e}")
            return self._create_fallback_analysis(f"Unexpected JSON error: {str(e)}")
            
        try:
            print("🚀 Step 5: Converting to data models...")
            # Validate result structure
            if not isinstance(result, dict):
                return self._create_fallback_analysis("Invalid result format - not a dictionary")
            
            # Convert to data models with validation
            decisions = []
            if 'decisions' in result and isinstance(result['decisions'], list):
                for d in result['decisions']:
                    if isinstance(d, dict) and all(key in d for key in ['content', 'impact_level', 'stakeholders', 'confidence']):
                        decisions.append(Decision(
                            content=str(d['content'])[:500],  # Limit length
                            impact_level=str(d['impact_level']),
                            stakeholders=[str(s) for s in d['stakeholders']][:5],  # Limit count
                            confidence=float(d['confidence']) if isinstance(d['confidence'], (int, float)) else 0.5
                        ))
            print(f"✅ Step 5a: {len(decisions)} decisions converted")
            
            action_items = []
            if 'action_items' in result and isinstance(result['action_items'], list):
                for a in result['action_items']:
                    if isinstance(a, dict) and all(key in a for key in ['assignee', 'task', 'deadline', 'priority', 'confidence']):
                        action_items.append(ActionItem(
                            assignee=str(a['assignee'])[:100],  # Limit length
                            task=str(a['task'])[:500],
                            deadline=str(a['deadline'])[:100],
                            priority=str(a['priority']).lower(),
                            confidence=float(a['confidence']) if isinstance(a['confidence'], (int, float)) else 0.5
                        ))
            print(f"✅ Step 5b: {len(action_items)} action items converted")
        except Exception as e:
            print(f"❌ Step 5 Error - Data model conversion: {e}")
            print(f"Result keys: {list(result.keys()) if 'result' in locals() else 'No result'}")
            return self._create_fallback_analysis(f"Data model conversion failed: {str(e)}")
            
        try:
            print("🚀 Step 6: Creating MeetingAnalysis object...")
            
            # Safe extraction with defaults
            metadata = result.get('metadata', {})
            if not isinstance(metadata, dict):
                metadata = {}
            
            sentiment = result.get('sentiment', {})
            if not isinstance(sentiment, dict):
                sentiment = {'positive': 33.3, 'negative': 33.3, 'neutral': 33.3}
            
            risks = result.get('risks', [])
            if not isinstance(risks, list):
                risks = []
            risks = [str(r)[:200] for r in risks[:5]]  # Limit count and length
            
            summary_stats = result.get('summary_stats', {})
            if not isinstance(summary_stats, dict):
                summary_stats = {}
            
            analysis = MeetingAnalysis(
                decisions=decisions,
                action_items=action_items,
                metadata=metadata,
                sentiment=sentiment,
                risks=risks,
                summary_stats=summary_stats
            )
            print("✅ Step 6: MeetingAnalysis created successfully")
            return analysis
        except Exception as e:
            print(f"❌ Step 6 Error - MeetingAnalysis creation: {e}")
            return self._create_fallback_analysis(f"MeetingAnalysis creation failed: {str(e)}")
    
    def _create_fallback_analysis(self, error_message: str) -> MeetingAnalysis:
        """Create fallback analysis when LLM fails"""
        try:
            return MeetingAnalysis(
                decisions=[],
                action_items=[],
                metadata={"next_meeting": "Not specified", "attendees": [], "meeting_length": 0},
                sentiment={"positive": 0, "negative": 0, "neutral": 100},
                risks=[f"Analysis Error: {error_message[:200]}"],  # Limit error message length
                summary_stats={"total_decisions": 0, "high_impact_decisions": 0, "total_actions": 0, "critical_actions": 0, "avg_confidence": 0}
            )
        except Exception:
            # Ultimate fallback if even the fallback fails
            return MeetingAnalysis(
                decisions=[],
                action_items=[],
                metadata={},
                sentiment={"positive": 0, "negative": 0, "neutral": 100},
                risks=["Critical error in analysis"],
                summary_stats={}
            )