"""
Streamlit UI components
"""

import streamlit as st
import plotly.express as px
from datetime import datetime
from ..models.meeting_models import MeetingAnalysis

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
    def render_sidebar():
        """Render sidebar configuration"""
        with st.sidebar:
            st.header("⚙️ Configuration")
            meeting_title = st.text_input("Meeting Title", "10 Academy Executive Meeting")
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
            
            return meeting_title, analysis_depth
    
    @staticmethod
    def render_file_upload():
        """Render file upload component"""
        return st.file_uploader("📁 Upload Meeting Transcript", type=['txt'], 
                               help="Upload a .txt file containing your meeting transcript")
    
    @staticmethod
    def render_metrics(analysis: MeetingAnalysis):
        """Render metrics dashboard"""
        col1, col2, col3, col4 = st.columns(4)
        stats = analysis.summary_stats
        
        with col1:
            st.metric("Decisions", stats['total_decisions'])
        with col2:
            st.metric("Action Items", stats['total_actions'])
        with col3:
            st.metric("High Impact", stats['high_impact_decisions'])
        with col4:
            st.metric("Confidence", f"{stats['avg_confidence']}")
    
    @staticmethod
    def render_results(analysis: MeetingAnalysis):
        """Render analysis results"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🎯 Strategic Decisions")
            for i, decision in enumerate(analysis.decisions, 1):
                st.markdown(f"""
                **{i}. {decision.content}**  
                *Impact: {decision.impact_level} | Confidence: {decision.confidence}*
                """)
            
            st.subheader("✅ Action Items")
            for i, action in enumerate(analysis.action_items, 1):
                priority_color = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                st.markdown(f"""
                {priority_color.get(action.priority, '⚪')} **{action.assignee}**: {action.task}  
                *Deadline: {action.deadline} | Priority: {action.priority.title()}*
                """)
        
        with col2:
            st.subheader("📊 Meeting Analytics")
            
            # Sentiment chart
            sentiment_data = analysis.sentiment
            fig = px.pie(
                values=list(sentiment_data.values()),
                names=list(sentiment_data.keys()),
                title="Sentiment Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Metadata
            st.subheader("📋 Meeting Details")
            st.write(f"**Next Meeting:** {analysis.metadata['next_meeting']}")
            st.write(f"**Attendees:** {len(analysis.metadata['attendees'])} participants")
            
            if analysis.risks:
                st.subheader("⚠️ Risk Indicators")
                for risk in analysis.risks:
                    st.warning(risk)
    
    @staticmethod
    def render_demo_transcript():
        """Return demo transcript"""
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