#!/usr/bin/env python3
"""
🚀 ENTERPRISE MEETING SUMMARIZER - Modular Architecture
Main Streamlit application with Pattern-Based and LLM-Powered analysis
"""

import streamlit as st
from datetime import datetime

from src.analyzers.meeting_analyzer import EnterpriseAnalyzer
from src.analyzers.llm_analyzer import LLMAnalyzer
from src.utils.email_generator import EmailGenerator
from src.ui.streamlit_ui import StreamlitUI

def main():
    # Setup page
    StreamlitUI.setup_page()
    
    # Render header
    StreamlitUI.render_header()
    
    # Render sidebar
    config = StreamlitUI.render_sidebar()
    
    # File upload
    uploaded_file = StreamlitUI.render_file_upload()
    
    if uploaded_file:
        # Read transcript with error handling
        try:
            transcript_text = uploaded_file.read().decode('utf-8')
        except UnicodeDecodeError:
            st.error("❌ File encoding error. Please ensure the file is UTF-8 encoded.")
            return
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            return
        
        # Validate transcript content
        if not transcript_text.strip():
            st.error("❌ The uploaded file appears to be empty.")
            return
        
        if len(transcript_text) > 100000:  # 100KB limit
            st.warning("⚠️ Large file detected. Processing may take longer.")
        
        # Preview
        with st.expander("📄 Transcript Preview"):
            st.text_area("Content", transcript_text[:1000] + "..." if len(transcript_text) > 1000 else transcript_text, height=200)
        
        # Process transcript
        if st.button("🚀 Generate Executive Summary", type="primary"):
            # Validate API key for Gemini method
            if "Gemini-Powered" in config.analysis_method and not config.api_key:
                st.error("❌ Please enter your Google Gemini API key to use Gemini analysis")
                return
            
            # Validate API key format
            if "Gemini-Powered" in config.analysis_method and config.api_key:
                if len(config.api_key.strip()) < 20 or not config.api_key.startswith('AI'):
                    st.error("❌ Invalid API key format. Please check your Gemini API key.")
                    return
            
            try:
                # Choose analyzer based on method
                if "Gemini-Powered" in config.analysis_method:
                    spinner_text = "🧠 Analyzing with Gemini AI..."
                    try:
                        analyzer = LLMAnalyzer(config.api_key)
                    except Exception as e:
                        st.error(f"❌ Gemini Analyzer Error: {str(e)}")
                        return
                else:
                    spinner_text = "🔍 Analyzing with Pattern Recognition..."
                    analyzer = EnterpriseAnalyzer()
                
                with st.spinner(spinner_text):
                    # Analyze meeting with timeout protection
                    try:
                        analysis = analyzer.analyze_meeting(transcript_text)
                    except Exception as e:
                        st.error(f"❌ Analysis failed: {str(e)}")
                        return
                    
                    # Generate email with error handling
                    try:
                        email_generator = EmailGenerator()
                        html_email = email_generator.generate_executive_email(analysis, config.meeting_title)
                    except Exception as e:
                        st.error(f"❌ Email generation failed: {str(e)}")
                        return
                
                # Show analysis method used
                method_badge = "🧠 Gemini-Powered" if "Gemini-Powered" in config.analysis_method else "🔍 Pattern-Based"
                st.success(f"✅ Analysis Complete! (Method: {method_badge})")
                
                # Render metrics with error handling
                try:
                    StreamlitUI.render_metrics(analysis)
                except Exception as e:
                    st.warning(f"⚠️ Metrics display error: {str(e)}")
                
                # Render results with error handling
                try:
                    StreamlitUI.render_results(analysis)
                except Exception as e:
                    st.warning(f"⚠️ Results display error: {str(e)}")
                
                # Email preview with error handling
                try:
                    st.subheader("📧 Executive Email Summary")
                    st.components.v1.html(html_email, height=800, scrolling=True)
                except Exception as e:
                    st.warning(f"⚠️ Email preview error: {str(e)}")
                
                # Download button
                try:
                    st.download_button(
                        label="📥 Download Executive Summary",
                        data=html_email,
                        file_name=f"executive_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                        type="primary"
                    )
                except Exception as e:
                    st.warning(f"⚠️ Download button error: {str(e)}")
                    
            except Exception as e:
                st.error(f"❌ Unexpected error during processing: {str(e)}")
                st.info("📝 Please try again or contact support if the issue persists.")
    
    else:
        # Demo section
        st.info("👆 Upload a transcript to get started, or try the demo below")
        
        if st.button("🎯 Try Executive Demo"):
            demo_transcript = StreamlitUI.get_demo_transcript()
            
            # Process demo with selected method
            if "Gemini-Powered" in config.analysis_method and config.api_key:
                analyzer = LLMAnalyzer(config.api_key)
                method_badge = "🧠 Gemini-Powered"
            else:
                analyzer = EnterpriseAnalyzer()
                method_badge = "🔍 Pattern-Based"
            
            with st.spinner(f"Processing demo with {method_badge} analysis..."):
                analysis = analyzer.analyze_meeting(demo_transcript)
            
            email_generator = EmailGenerator()
            html_email = email_generator.generate_executive_email(analysis, "Executive Strategy Meeting")
            
            st.subheader(f"🎯 Demo Results ({method_badge})")
            st.json(analysis.summary_stats)
            
            st.subheader("📧 Executive Summary Preview")
            st.components.v1.html(html_email, height=600, scrolling=True)

if __name__ == "__main__":
    main()