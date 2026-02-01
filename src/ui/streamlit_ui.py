"""
Streamlit UI components
"""

import streamlit as st
import plotly.express as px
from datetime import datetime
from ..models.meeting_models import MeetingAnalysis
from .config_models import SidebarConfig

class StreamlitUI:
    @staticmethod
    def setup_page():
        """Configure Streamlit page"""
        st.set_page_config(
            page_title="Enterprise Meeting Summarizer", 
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🚀 Enterprise Meeting Summarizer</h1>
            <p>Advanced AI-powered meeting analysis with sentiment, priority scoring, and executive insights</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar() -> SidebarConfig:
        """Render sidebar configuration"""
        with st.sidebar:
            st.header("⚙️ Configuration")
            meeting_title = st.text_input("Meeting Title", "10 Academy Executive Meeting")
            
            # Analysis method toggle
            st.subheader("🤖 Analysis Method")
            analysis_method = st.radio(
                "Choose Analysis Engine:",
                ["🔍 Pattern-Based (Fast)", "🧠 Gemini-Powered (Advanced)"],
                help="Pattern-based uses regex patterns. Gemini-powered uses Google AI."
            )
            
            # Check for .env API key
            from ..utils.config import Config
            env_api_key = Config.get_gemini_api_key()
            has_env_key = Config.has_valid_gemini_key()
            
            # API key handling
            api_key = None
            if "Gemini-Powered" in analysis_method:
                if has_env_key:
                    api_key = env_api_key
                else:
                    st.info("📝 No .env file found. Enter API key below:")
                    api_key = st.text_input(
                        "Google Gemini API Key:",
                        type="password",
                        help="Enter your Google Gemini API key for LLM analysis"
                    )
                    if not api_key:
                        st.warning("⚠️ API key required for Gemini analysis")
            
            analysis_depth = st.selectbox("Analysis Depth", ["Standard", "Deep", "Executive"])
            
            st.header("📊 Features")
            st.markdown("""
            ✅ **Advanced Pattern Recognition**  
            ✅ **Confidence Scoring**  
            ✅ **Priority Assessment**  
            ✅ **Sentiment Analysis**  
            ✅ **Risk Detection**  
            ✅ **Executive Reporting**
            """)
            
            return SidebarConfig(
                meeting_title=meeting_title,
                analysis_depth=analysis_depth,
                analysis_method=analysis_method,
                api_key=api_key
            )
    
    @staticmethod
    def render_file_upload():
        """Render file upload component"""
        return st.file_uploader("📁 Upload Meeting Transcript", type=['txt'], 
                               help="Upload a .txt file containing your meeting transcript")
    
    @staticmethod
    def render_metrics(analysis: MeetingAnalysis):
        """Render metrics dashboard with error handling"""
        try:
            col1, col2, col3, col4 = st.columns(4)
            stats = analysis.summary_stats or {}
            
            with col1:
                st.metric("Decisions", stats.get('total_decisions', 0))
            with col2:
                st.metric("Action Items", stats.get('total_actions', 0))
            with col3:
                st.metric("High Impact", stats.get('high_impact_decisions', 0))
            with col4:
                st.metric("Confidence", f"{stats.get('avg_confidence', 0)}")
        except Exception as e:
            st.error(f"Error displaying metrics: {str(e)}")
    
    @staticmethod
    def render_results(analysis: MeetingAnalysis):
        """Render analysis results"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎯 Strategic Decisions")
            try:
                for i, decision in enumerate(analysis.decisions, 1):
                    content = getattr(decision, 'content', 'No content available')
                    impact = getattr(decision, 'impact_level', 'Unknown')
                    confidence = getattr(decision, 'confidence', 0)
                    
                    st.markdown(f"""
                    **{i}. {content}**  
                    *Impact: {impact} | Confidence: {confidence}*
                    """)
            except Exception as e:
                st.warning(f"Could not display decisions: {str(e)}")
            
            st.subheader("✅ Action Items")
            try:
                for i, action in enumerate(analysis.action_items, 1):
                    priority_color = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                    priority = getattr(action, 'priority', 'unknown')
                    assignee = getattr(action, 'assignee', 'Unassigned')
                    task = getattr(action, 'task', 'No task specified')
                    deadline = getattr(action, 'deadline', 'Not specified')
                    confidence = getattr(action, 'confidence', 0)
                    
                    st.markdown(f"""
                    {priority_color.get(priority, '⚪')} **{assignee}**: {task}  
                    *Deadline: {deadline} | Priority: {priority.title() if priority else 'Unknown'}*
                    """)
            except Exception as e:
                st.warning(f"Could not display action items: {str(e)}")
        
        with col2:
            st.subheader("📊 Meeting Analytics")
            
            # Sentiment chart
            try:
                sentiment_data = analysis.sentiment or {'positive': 33.3, 'negative': 33.3, 'neutral': 33.3}
                if sentiment_data and any(sentiment_data.values()):
                    fig = px.pie(
                        values=list(sentiment_data.values()),
                        names=list(sentiment_data.keys()),
                        title="Sentiment Distribution"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No sentiment data available")
            except Exception as e:
                st.warning(f"Could not display sentiment chart: {str(e)}")
            
            # Meeting metadata with safe access
            st.subheader("📋 Meeting Details")
            metadata = analysis.metadata or {}
            st.write(f"**Next Meeting:** {metadata.get('next_meeting', 'Not specified')}")
            participant_count = len(metadata.get('attendees', []))
            st.write(f"**Attendees:** {participant_count} participants")
            
            if analysis.risks:
                st.subheader("⚠️ Risk Indicators")
                for risk in analysis.risks:
                    st.warning(risk)
    
    @staticmethod
    def get_demo_transcript() -> str:
        """Get demo transcript data"""
        return """
        Executive team meeting started at 9 AM. We decided to implement the new AI-driven customer analytics platform by Q2.
        Sarah will lead the technical implementation and must have the MVP ready by March 15th.
        It was agreed that the budget allocation is $2.5M for this critical initiative.
        John is responsible for stakeholder communication and needs to present to the board next Friday.
        We concluded that this is a high-priority strategic decision that will impact our competitive position.
        Action item: Mike - conduct security audit by end of week, this is urgent.
        The team agreed we need additional data scientists to support this initiative.
        Risk identified: potential delay if we don't secure cloud infrastructure soon.
        Next meeting scheduled for next Tuesday at 10 AM to review progress and address any blockers.
        Final decision: proceed with full implementation despite the aggressive timeline.
        """