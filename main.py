#!/usr/bin/env python3
"""
🚀 ENTERPRISE MEETING SUMMARIZER - Modular Architecture
Main Streamlit application with clean separation of concerns
"""

import streamlit as st
from datetime import datetime

from src.analyzers.meeting_analyzer import EnterpriseAnalyzer
from src.utils.email_generator import EmailGenerator
from src.ui.streamlit_ui import StreamlitUI

def main():
    # Setup page
    StreamlitUI.setup_page()
    
    # Render header
    StreamlitUI.render_header()
    
    # Render sidebar
    meeting_title, analysis_depth = StreamlitUI.render_sidebar()
    
    # File upload
    uploaded_file = StreamlitUI.render_file_upload()
    
    if uploaded_file:
        # Read transcript
        transcript_text = uploaded_file.read().decode('utf-8')
        
        # Preview
        with st.expander("📄 Transcript Preview"):
            st.text_area("Content", transcript_text[:1000] + "..." if len(transcript_text) > 1000 else transcript_text, height=200)
        
        # Process transcript
        if st.button("🚀 Generate Executive Summary", type="primary"):
            with st.spinner("🧠 Analyzing with Advanced AI..."):
                # Initialize analyzer
                analyzer = EnterpriseAnalyzer()
                
                # Analyze meeting
                analysis = analyzer.analyze_meeting(transcript_text)
                
                # Generate email
                email_generator = EmailGenerator()
                html_email = email_generator.generate_executive_email(analysis, meeting_title)
            
            st.success("✅ Analysis Complete!")
            
            # Render metrics
            StreamlitUI.render_metrics(analysis)
            
            # Render results
            StreamlitUI.render_results(analysis)
            
            # Email preview
            st.subheader("📧 Executive Email Summary")
            st.components.v1.html(html_email, height=800, scrolling=True)
            
            # Download button
            st.download_button(
                label="📥 Download Executive Summary",
                data=html_email,
                file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                type="primary"
            )
    
    else:
        # Demo section
        st.info("👆 Upload a transcript to get started, or try the demo below")
        
        if st.button("🎯 Try Executive Demo"):
            demo_transcript = StreamlitUI.render_demo_transcript()
            
            # Process demo
            analyzer = EnterpriseAnalyzer()
            analysis = analyzer.analyze_meeting(demo_transcript)
            
            email_generator = EmailGenerator()
            html_email = email_generator.generate_executive_email(analysis, "Executive Strategy Meeting")
            
            st.subheader("🎯 Demo Results")
            st.json(analysis.summary_stats)
            
            st.subheader("📧 Executive Summary Preview")
            st.components.v1.html(html_email, height=600, scrolling=True)

if __name__ == "__main__":
    main()