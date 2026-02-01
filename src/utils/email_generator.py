"""
Executive email template generator with security enhancements
"""

from datetime import datetime
from ..models.meeting_models import MeetingAnalysis
from .security import SecurityUtils

class EmailGenerator:
    @staticmethod
    def generate_executive_email(analysis: MeetingAnalysis, meeting_title: str = "Executive Meeting") -> str:
        """Generate professional HTML email with XSS protection"""
        
        try:
            # Sanitize inputs to prevent XSS
            meeting_title = SecurityUtils.sanitize_html(meeting_title)
            
            decisions = analysis.decisions or []
            actions = analysis.action_items or []
            metadata = analysis.metadata or {}
            sentiment = analysis.sentiment or {'positive': 0, 'negative': 0, 'neutral': 100}
            stats = analysis.summary_stats or {
                'total_decisions': 0, 'total_actions': 0, 
                'high_impact_decisions': 0, 'avg_confidence': 0
            }
            
            # Safe access with defaults - sanitize sentiment values
            positive = SecurityUtils.sanitize_html(str(sentiment.get('positive', 0)))
            negative = SecurityUtils.sanitize_html(str(sentiment.get('negative', 0)))
            neutral = SecurityUtils.sanitize_html(str(sentiment.get('neutral', 100)))
            sentiment_chart = f"Positive: {positive}% | Negative: {negative}% | Neutral: {neutral}%"
            
            # Generate sanitized decision items
            decision_items = []
            for d in decisions:
                content = SecurityUtils.sanitize_html(getattr(d, 'content', 'No content'))
                impact_level = SecurityUtils.sanitize_html(getattr(d, 'impact_level', 'Unknown'))
                confidence = getattr(d, 'confidence', 0)
                stakeholders = getattr(d, 'stakeholders', [])
                
                stakeholder_list = ', '.join([SecurityUtils.sanitize_html(str(s)) for s in stakeholders]) if stakeholders else ''
                
                decision_items.append(f'''
                <div class="decision-item {'high-impact' if impact_level == 'High' else ''}">
                    <strong>{content}</strong>
                    <div class="confidence">Impact: {impact_level} | Confidence: {confidence}</div>
                    {f"<div style='margin-top:8px;'><small>Stakeholders: {stakeholder_list}</small></div>" if stakeholder_list else ""}
                </div>
                ''')
            
            # Generate sanitized action items
            action_items = []
            for a in actions:
                assignee = SecurityUtils.sanitize_html(getattr(a, 'assignee', 'Unassigned'))
                task = SecurityUtils.sanitize_html(getattr(a, 'task', 'No task'))
                priority = getattr(a, 'priority', 'medium')
                deadline = SecurityUtils.sanitize_html(getattr(a, 'deadline', 'Not specified'))
                confidence = getattr(a, 'confidence', 0)
                
                action_items.append(f'''
                <div class="action-item {'critical' if priority == 'critical' else ''}">
                    <strong>{assignee}</strong>: {task}
                    <span class="priority-badge {priority}-badge">{priority}</span>
                    <div style="margin-top:8px;"><small>Deadline: {deadline} | Confidence: {confidence}</small></div>
                </div>
                ''')
        
            # Safe metadata access
            next_meeting = SecurityUtils.sanitize_html(metadata.get('next_meeting', 'Not specified'))
            attendees_count = SecurityUtils.sanitize_html(str(len(metadata.get('attendees', []))))
            
            # Sanitize stats before embedding in HTML
            total_decisions = SecurityUtils.sanitize_html(str(stats.get('total_decisions', 0)))
            total_actions = SecurityUtils.sanitize_html(str(stats.get('total_actions', 0)))
            high_impact = SecurityUtils.sanitize_html(str(stats.get('high_impact_decisions', 0)))
            avg_confidence = SecurityUtils.sanitize_html(str(stats.get('avg_confidence', 0)))
            
            return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background: #f8f9fa; }}
                    .container {{ max-width: 800px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
                    .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 12px 12px 0 0; }}
                    .header h1 {{ margin: 0; font-size: 28px; font-weight: 300; }}
                    .header .subtitle {{ opacity: 0.9; margin-top: 8px; }}
                    .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; padding: 20px; background: #f8f9fa; }}
                    .stat-card {{ background: white; padding: 15px; border-radius: 8px; text-align: center; border-left: 4px solid #667eea; }}
                    .stat-number {{ font-size: 24px; font-weight: bold; color: #667eea; }}
                    .stat-label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
                    .section {{ padding: 25px; }}
                    .section h2 {{ color: #333; border-bottom: 2px solid #667eea; padding-bottom: 8px; margin-bottom: 20px; }}
                    .decision-item, .action-item {{ background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #28a745; }}
                    .high-impact {{ border-left-color: #dc3545; }}
                    .critical {{ border-left-color: #fd7e14; }}
                    .priority-badge {{ display: inline-block; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold; text-transform: uppercase; }}
                    .critical-badge {{ background: #dc3545; color: white; }}
                    .high-badge {{ background: #fd7e14; color: white; }}
                    .medium-badge {{ background: #ffc107; color: black; }}
                    .confidence {{ float: right; color: #666; font-size: 12px; }}
                    .footer {{ background: #f8f9fa; padding: 20px; border-radius: 0 0 12px 12px; text-align: center; color: #666; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📊 {meeting_title}</h1>
                        <div class="subtitle">Executive Summary • Generated {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</div>
                    </div>
                    
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-number">{total_decisions}</div>
                            <div class="stat-label">Key Decisions</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{total_actions}</div>
                            <div class="stat-label">Action Items</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{high_impact}</div>
                            <div class="stat-label">High Impact</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{avg_confidence}</div>
                            <div class="stat-label">Avg Confidence</div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h2>🎯 Strategic Decisions</h2>
                        {''.join(decision_items) if decision_items else '<p>No strategic decisions recorded</p>'}
                    </div>
                    
                    <div class="section">
                        <h2>✅ Action Items & Assignments</h2>
                        {''.join(action_items) if action_items else '<p>No action items assigned</p>'}
                    </div>
                    
                    <div class="section">
                        <h2>📈 Meeting Analytics</h2>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                            <div>
                                <h4>Sentiment Analysis</h4>
                                <div>{sentiment_chart}</div>
                            </div>
                            <div>
                                <h4>Meeting Metadata</h4>
                                <p><strong>Next Meeting:</strong> {next_meeting}</p>
                                <p><strong>Attendees:</strong> {attendees_count} participants</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="footer">
                        <p>🤖 Generated by Enterprise Meeting Summarizer v2.0 | Powered by Advanced AI Analytics</p>
                        <p><small>This summary uses pattern recognition and confidence scoring for maximum accuracy</small></p>
                    </div>
                </div>
            </body>
            </html>
            """
            
        except Exception as e:
            # Return safe fallback HTML on error
            return f"""
            <!DOCTYPE html>
            <html><body>
            <h1>Meeting Summary Error</h1>
            <p>Unable to generate meeting summary: {SecurityUtils.sanitize_html(str(e))}</p>
            </body></html>
            """