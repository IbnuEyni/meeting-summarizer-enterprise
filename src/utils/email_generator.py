"""
Executive email template generator
"""

from datetime import datetime
from ..models.meeting_models import MeetingAnalysis

class EmailGenerator:
    @staticmethod
    def generate_executive_email(analysis: MeetingAnalysis, meeting_title: str = "Executive Meeting") -> str:
        """Generate professional HTML email"""
        
        decisions = analysis.decisions
        actions = analysis.action_items
        metadata = analysis.metadata
        sentiment = analysis.sentiment
        stats = analysis.summary_stats
        
        sentiment_chart = f"Positive: {sentiment['positive']}% | Negative: {sentiment['negative']}% | Neutral: {sentiment['neutral']}%"
        
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
                        <div class="stat-number">{stats['total_decisions']}</div>
                        <div class="stat-label">Key Decisions</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['total_actions']}</div>
                        <div class="stat-label">Action Items</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['high_impact_decisions']}</div>
                        <div class="stat-label">High Impact</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number">{stats['avg_confidence']}</div>
                        <div class="stat-label">Avg Confidence</div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🎯 Strategic Decisions</h2>
                    {''.join([f'''
                    <div class="decision-item {'high-impact' if d.impact_level == 'High' else ''}">
                        <strong>{d.content}</strong>
                        <div class="confidence">Impact: {d.impact_level} | Confidence: {d.confidence}</div>
                        {f"<div style='margin-top:8px;'><small>Stakeholders: {', '.join(d.stakeholders)}</small></div>" if d.stakeholders else ""}
                    </div>
                    ''' for d in decisions]) if decisions else '<p>No strategic decisions recorded</p>'}
                </div>
                
                <div class="section">
                    <h2>✅ Action Items & Assignments</h2>
                    {''.join([f'''
                    <div class="action-item {'critical' if a.priority == 'critical' else ''}">
                        <strong>{a.assignee}</strong>: {a.task}
                        <span class="priority-badge {a.priority}-badge">{a.priority}</span>
                        <div style="margin-top:8px;"><small>Deadline: {a.deadline} | Confidence: {a.confidence}</small></div>
                    </div>
                    ''' for a in actions]) if actions else '<p>No action items assigned</p>'}
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
                            <p><strong>Next Meeting:</strong> {metadata['next_meeting']}</p>
                            <p><strong>Attendees:</strong> {len(metadata['attendees'])} participants</p>
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