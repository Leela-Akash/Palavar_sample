"""Report export utilities for CloudStrike."""
import json
import logging
from datetime import datetime
from typing import Dict

logger = logging.getLogger(__name__)


class ReportExporter:
    """Handles report export to JSON and PDF formats."""
    
    @staticmethod
    def export_json(result: Dict, filename: str = None) -> str:
        """
        Export scan result to JSON file.
        
        Args:
            result: Scan result dictionary
            filename: Output filename (optional)
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cloudstrike_report_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(result, f, indent=2)
            
            logger.info(f"Exported JSON report to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export JSON: {e}")
            raise
    
    @staticmethod
    def export_pdf(result: Dict, filename: str = None) -> str:
        """
        Export scan result to PDF file.
        
        Args:
            result: Scan result dictionary
            filename: Output filename (optional)
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cloudstrike_report_{timestamp}.pdf"
        
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
            from reportlab.lib.units import inch
            
            doc = SimpleDocTemplate(filename, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title = Paragraph("<b>CloudStrike Security Report</b>", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 0.3*inch))
            
            # Risk Summary
            risk = result.get('risk', {})
            summary_data = [
                ['Security Score', str(risk.get('security_score', 0))],
                ['Risk Level', risk.get('risk_level', 'Unknown')],
                ['Total Findings', str(len(result.get('findings', [])))],
                ['Attack Paths', str(len(result.get('attacks', [])))]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Findings
            story.append(Paragraph("<b>Security Findings</b>", styles['Heading2']))
            story.append(Spacer(1, 0.1*inch))
            
            for finding in result.get('findings', [])[:10]:
                finding_text = f"<b>{finding['title']}</b> [{finding['severity']}]<br/>{finding['description']}"
                story.append(Paragraph(finding_text, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
            
            doc.build(story)
            logger.info(f"Exported PDF report to {filename}")
            return filename
            
        except ImportError:
            logger.error("reportlab not installed. Install with: pip install reportlab")
            raise ImportError("reportlab required for PDF export")
        except Exception as e:
            logger.error(f"Failed to export PDF: {e}")
            raise
