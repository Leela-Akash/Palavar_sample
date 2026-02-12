"""Security findings report page."""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, QTextEdit, 
    QPushButton, QHBoxLayout, QApplication, QGridLayout, QProgressBar
)
from PySide6.QtCore import Qt
import config
from components.section_header import SectionHeader
from components.cyber_card import CyberCard
from components.status_badge import StatusBadge


class ReportPage(QWidget):
    """Security findings report page."""
    
    def __init__(self, parent=None):
        """Initialize report page."""
        super().__init__(parent)
        self.findings = []
        self.current_result = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup report UI."""
        # Main vertical layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(config.SPACING_LG, config.SPACING_LG, config.SPACING_LG, config.SPACING_LG)
        layout.setSpacing(0)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        # Container for centered content
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left stretch
        scroll_layout.addStretch()
        
        # Centered content (max 1100px)
        self.findings_container = QWidget()
        self.findings_container.setMaximumWidth(1100)
        self.findings_layout = QVBoxLayout(self.findings_container)
        self.findings_layout.setSpacing(32)
        self.findings_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header with export buttons
        header_layout = QHBoxLayout()
        header_layout.setSpacing(config.SPACING_MD)
        header_layout.addStretch()
        
        from components.glow_button import GlowButton
        self.export_json_btn = GlowButton("Export JSON")
        self.export_json_btn.clicked.connect(self.export_json)
        header_layout.addWidget(self.export_json_btn)
        
        self.export_pdf_btn = GlowButton("Export PDF", primary=False)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        header_layout.addWidget(self.export_pdf_btn)
        
        self.findings_layout.addLayout(header_layout)
        
        # Empty state
        self.empty_card = None
        
        self.findings_layout.addStretch()
        
        scroll_layout.addWidget(self.findings_container)
        
        # Right stretch
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
    def update_findings(self, result: dict):
        """
        Update report with new findings and remediation.
        
        Args:
            result: Dictionary with 'findings', 'risk', and 'remediation'
        """
        self.current_result = result
        self.findings = result.get('findings', [])
        risk = result.get('risk', {})
        remediation = result.get('remediation', [])
        attacks = result.get('attacks', [])
        
        # Clear existing widgets (skip first item which is header with export buttons)
        while self.findings_layout.count() > 1:
            item = self.findings_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
        
        if not self.findings:
            empty_card = CyberCard()
            empty_layout = QVBoxLayout()
            empty_layout.setAlignment(Qt.AlignCenter)
            empty_layout.setSpacing(config.SPACING_SM)
            
            icon_label = QLabel("🟢")
            icon_label.setStyleSheet(f"""
                font-size: 48pt;
            """)
            icon_label.setAlignment(Qt.AlignCenter)
            empty_layout.addWidget(icon_label)
            
            title_label = QLabel("No vulnerabilities detected")
            title_label.setStyleSheet(f"""
                color: {config.COLOR_PRIMARY};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_TITLE}pt;
                font-weight: bold;
            """)
            title_label.setAlignment(Qt.AlignCenter)
            empty_layout.addWidget(title_label)
            
            subtitle_label = QLabel("Your cloud environment follows security best practices.")
            subtitle_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT}88;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
            """)
            subtitle_label.setAlignment(Qt.AlignCenter)
            empty_layout.addWidget(subtitle_label)
            
            empty_card.add_layout(empty_layout)
            self.findings_layout.insertWidget(1, empty_card)
        else:
            # Executive Summary Header
            summary_header = SectionHeader("📊 Executive Summary")
            self.findings_layout.insertWidget(1, summary_header)
            
            # 4-card grid (2x2)
            summary_grid = QGridLayout()
            summary_grid.setSpacing(20)
            
            # Row 0: Score | Risk
            score_card = self.create_score_card(risk)
            summary_grid.addWidget(score_card, 0, 0)
            
            risk_card = self.create_risk_level_card(risk)
            summary_grid.addWidget(risk_card, 0, 1)
            
            # Row 1: Findings | Attack Paths
            findings_card = self.create_findings_count_card(len(self.findings))
            summary_grid.addWidget(findings_card, 1, 0)
            
            attacks_card = self.create_attacks_count_card(len(attacks))
            summary_grid.addWidget(attacks_card, 1, 1)
            
            self.findings_layout.insertLayout(2, summary_grid)
            
            # Risks & Findings section
            if self.findings:
                findings_header = SectionHeader("🔍 Risks & Findings")
                self.findings_layout.insertWidget(3, findings_header)
                
                # Create collapsible vulnerability cards
                insert_index = 4
                for finding in self.findings:
                    # Find matching remediation
                    matching_remediation = None
                    for rem in remediation:
                        if finding['cloud'] == rem['cloud'] and finding['title'].lower() in rem['title'].lower():
                            matching_remediation = rem
                            break
                    
                    # Find matching attack
                    matching_attack = None
                    for attack in attacks:
                        if finding['cloud'] == attack['cloud']:
                            matching_attack = attack
                            break
                    
                    card = self.create_collapsible_vulnerability_card(finding, matching_remediation, matching_attack)
                    self.findings_layout.insertWidget(insert_index, card)
                    insert_index += 1
        
        self.findings_layout.addStretch()
        
    def create_score_card(self, risk: dict) -> CyberCard:
        """Create security score card."""
        card = CyberCard()
        layout = QVBoxLayout()
        layout.setSpacing(config.SPACING_SM)
        
        title = QLabel("Security Score")
        title.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        security_score = risk.get('security_score', 0)
        score_label = QLabel(f"{security_score}/100")
        
        if security_score >= 80:
            score_color = config.COLOR_PRIMARY
        elif security_score >= 60:
            score_color = config.COLOR_WARNING
        else:
            score_color = config.COLOR_CRITICAL
        
        score_label.setStyleSheet(f"""
            color: {score_color};
            font-family: {config.FONT_FAMILY};
            font-size: 32pt;
            font-weight: bold;
        """)
        layout.addWidget(score_label)
        
        # Progress bar
        progress = QProgressBar()
        progress.setMaximumWidth(220)
        progress.setMaximumHeight(8)
        progress.setValue(security_score)
        progress.setTextVisible(False)
        progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                border-radius: 4px;
                background-color: {config.COLOR_BACKGROUND};
            }}
            QProgressBar::chunk {{
                background-color: {score_color};
                border-radius: 4px;
            }}
        """)
        layout.addWidget(progress)
        
        risk_level = risk.get('risk_level', 'Unknown')
        risk_label = QLabel(f"Risk: {risk_level}")
        risk_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        layout.addWidget(risk_label)
        
        card.add_layout(layout)
        return card
    
    def create_risk_level_card(self, risk: dict) -> CyberCard:
        """Create risk level card."""
        card = CyberCard()
        layout = QVBoxLayout()
        layout.setSpacing(config.SPACING_SM)
        
        title = QLabel("Risk Level")
        title.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        risk_level = risk.get('risk_level', 'Unknown').upper()
        
        if risk_level == 'CRITICAL':
            level_color = config.COLOR_CRITICAL
        elif risk_level == 'HIGH':
            level_color = config.COLOR_CRITICAL
        elif risk_level == 'MEDIUM':
            level_color = config.COLOR_WARNING
        else:
            level_color = config.COLOR_PRIMARY
        
        level_label = QLabel(risk_level)
        level_label.setStyleSheet(f"""
            color: {level_color};
            font-family: {config.FONT_FAMILY};
            font-size: 24pt;
            font-weight: bold;
        """)
        layout.addWidget(level_label)
        
        desc = QLabel("Current security posture")
        desc.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        layout.addWidget(desc)
        
        card.add_layout(layout)
        return card
    
    def create_findings_count_card(self, count: int) -> CyberCard:
        """Create total findings count card."""
        card = CyberCard()
        layout = QVBoxLayout()
        layout.setSpacing(config.SPACING_SM)
        
        title = QLabel("Total Findings")
        title.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        count_label = QLabel(str(count))
        count_label.setStyleSheet(f"""
            color: {config.COLOR_ACCENT};
            font-family: {config.FONT_FAMILY};
            font-size: 32pt;
            font-weight: bold;
        """)
        layout.addWidget(count_label)
        
        desc = QLabel("Security issues detected")
        desc.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        layout.addWidget(desc)
        
        card.add_layout(layout)
        return card
    
    def create_attacks_count_card(self, count: int) -> CyberCard:
        """Create attack paths count card."""
        card = CyberCard()
        layout = QVBoxLayout()
        layout.setSpacing(config.SPACING_SM)
        
        title = QLabel("Attack Paths Found")
        title.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        count_label = QLabel(str(count))
        count_label.setStyleSheet(f"""
            color: {config.COLOR_CRITICAL};
            font-family: {config.FONT_FAMILY};
            font-size: 32pt;
            font-weight: bold;
        """)
        layout.addWidget(count_label)
        
        desc = QLabel("Potential attack vectors")
        desc.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        layout.addWidget(desc)
        
        card.add_layout(layout)
        return card
    
    def create_collapsible_vulnerability_card(self, finding: dict, remediation: dict = None, attack: dict = None) -> CyberCard:
        """Create collapsible vulnerability card."""
        card = CyberCard()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        
        # Collapsed header (always visible)
        header_layout = QHBoxLayout()
        
        title_label = QLabel(finding["title"])
        title_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_HEADER}pt;
            font-weight: bold;
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        severity_badge = StatusBadge(finding["severity"], finding["severity"].lower())
        header_layout.addWidget(severity_badge)
        
        cloud_badge = StatusBadge(finding["cloud"], "info")
        header_layout.addWidget(cloud_badge)
        
        main_layout.addLayout(header_layout)
        
        # Short description (always visible)
        short_desc = finding["description"][:100] + "..." if len(finding["description"]) > 100 else finding["description"]
        desc_label = QLabel(short_desc)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}cc;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        main_layout.addWidget(desc_label)
        
        # Expandable details container
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 12, 0, 0)
        details_layout.setSpacing(12)
        details_widget.setVisible(False)
        
        # Full description
        if len(finding["description"]) > 100:
            full_desc = QLabel(finding["description"])
            full_desc.setWordWrap(True)
            full_desc.setStyleSheet(f"""
                color: {config.COLOR_TEXT};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
            """)
            details_layout.addWidget(full_desc)
        
        # Attack Path subsection
        if attack:
            attack_header = QLabel("Attack Path")
            attack_header.setStyleSheet(f"""
                color: {config.COLOR_TEXT};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                font-weight: bold;
                margin-top: 8px;
            """)
            details_layout.addWidget(attack_header)
            
            attack_label = QLabel(attack['title'])
            attack_label.setWordWrap(True)
            attack_label.setStyleSheet(f"""
                color: {config.COLOR_ACCENT};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                padding-left: {config.SPACING_MD}px;
            """)
            details_layout.addWidget(attack_label)
        
        # Remediation subsections
        if remediation:
            # CLI Fix
            cli_header = QLabel("CLI Fix")
            cli_header.setStyleSheet(f"""
                color: {config.COLOR_TEXT};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                font-weight: bold;
                margin-top: 8px;
            """)
            details_layout.addWidget(cli_header)
            
            cli_text = QTextEdit()
            cli_text.setPlainText(remediation.get("cli_script", ""))
            cli_text.setReadOnly(True)
            cli_text.setMaximumHeight(80)
            cli_text.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {config.COLOR_BACKGROUND};
                    color: {config.COLOR_PRIMARY};
                    border: 1px solid {config.COLOR_BORDER};
                    border-radius: 4px;
                    padding: {config.SPACING_SM}px;
                    font-family: {config.FONT_FAMILY};
                    font-size: 9pt;
                }}
            """)
            details_layout.addWidget(cli_text)
            
            cli_copy_btn = QPushButton("📋 Copy CLI")
            cli_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(remediation.get("cli_script", "")))
            cli_copy_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config.COLOR_CARD};
                    color: {config.COLOR_PRIMARY};
                    border: 1px solid {config.COLOR_PRIMARY};
                    border-radius: 4px;
                    padding: {config.SPACING_XS}px {config.SPACING_MD}px;
                    font-family: {config.FONT_FAMILY};
                    font-size: 9pt;
                }}
                QPushButton:hover {{
                    background-color: {config.COLOR_PRIMARY}22;
                }}
            """)
            details_layout.addWidget(cli_copy_btn, alignment=Qt.AlignLeft)
            
            # Terraform Fix
            tf_header = QLabel("Terraform Fix")
            tf_header.setStyleSheet(f"""
                color: {config.COLOR_TEXT};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                font-weight: bold;
                margin-top: 8px;
            """)
            details_layout.addWidget(tf_header)
            
            tf_text = QTextEdit()
            tf_text.setPlainText(remediation.get("terraform", ""))
            tf_text.setReadOnly(True)
            tf_text.setMaximumHeight(80)
            tf_text.setStyleSheet(f"""
                QTextEdit {{
                    background-color: {config.COLOR_BACKGROUND};
                    color: {config.COLOR_ACCENT};
                    border: 1px solid {config.COLOR_BORDER};
                    border-radius: 4px;
                    padding: {config.SPACING_SM}px;
                    font-family: {config.FONT_FAMILY};
                    font-size: 9pt;
                }}
            """)
            details_layout.addWidget(tf_text)
            
            tf_copy_btn = QPushButton("📋 Copy Terraform")
            tf_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(remediation.get("terraform", "")))
            tf_copy_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config.COLOR_CARD};
                    color: {config.COLOR_ACCENT};
                    border: 1px solid {config.COLOR_ACCENT};
                    border-radius: 4px;
                    padding: {config.SPACING_XS}px {config.SPACING_MD}px;
                    font-family: {config.FONT_FAMILY};
                    font-size: 9pt;
                }}
                QPushButton:hover {{
                    background-color: {config.COLOR_ACCENT}22;
                }}
            """)
            details_layout.addWidget(tf_copy_btn, alignment=Qt.AlignLeft)
        
        main_layout.addWidget(details_widget)
        
        # Toggle button
        toggle_btn = QPushButton("View Details ▼")
        toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {config.COLOR_PRIMARY};
                border: none;
                text-align: left;
                padding: {config.SPACING_XS}px 0px;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
            }}
            QPushButton:hover {{
                color: {config.COLOR_PRIMARY}cc;
            }}
        """)
        
        def toggle_details():
            is_visible = details_widget.isVisible()
            details_widget.setVisible(not is_visible)
            toggle_btn.setText("Hide Details ▲" if not is_visible else "View Details ▼")
        
        toggle_btn.clicked.connect(toggle_details)
        main_layout.addWidget(toggle_btn)
        
        card.add_layout(main_layout)
        return card
    
    def copy_to_clipboard(self, text: str):
        """Copy text to system clipboard."""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def export_json(self):
        """Export report as JSON."""
        if not self.current_result:
            from components.toast import show_toast
            show_toast(self, "No scan results to export. Run a scan first.")
            return
        
        from PySide6.QtWidgets import QFileDialog
        from datetime import datetime
        import json
        
        default_name = f"cloudstrike_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save JSON Report",
            default_name,
            "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_result, f, indent=4)
                
                from components.toast import show_toast
                show_toast(self, f"Report saved: {file_path}")
            except Exception as e:
                from components.toast import show_toast
                show_toast(self, f"Export failed: {str(e)}")
    
    def export_pdf(self):
        """Export report as PDF."""
        if not self.current_result:
            from components.toast import show_toast
            show_toast(self, "No scan results to export. Run a scan first.")
            return
        
        from PySide6.QtWidgets import QFileDialog
        from datetime import datetime
        
        default_name = f"cloudstrike_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            default_name,
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            try:
                from reportlab.lib.pagesizes import letter
                from reportlab.lib import colors
                from reportlab.lib.styles import getSampleStyleSheet
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
                from reportlab.lib.units import inch
                
                doc = SimpleDocTemplate(file_path, pagesize=letter)
                story = []
                styles = getSampleStyleSheet()
                
                # Title
                title = Paragraph("<b>CloudStrike Security Report</b>", styles['Title'])
                story.append(title)
                story.append(Spacer(1, 0.2*inch))
                
                # Timestamp
                timestamp = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
                story.append(timestamp)
                story.append(Spacer(1, 0.3*inch))
                
                # Risk Summary
                risk = self.current_result.get('risk', {})
                summary_data = [
                    ['Security Score', str(risk.get('security_score', 0))],
                    ['Risk Level', risk.get('risk_level', 'Unknown')],
                    ['Total Findings', str(len(self.current_result.get('findings', [])))],
                    ['Attack Paths', str(len(self.current_result.get('attacks', [])))]  
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
                
                for finding in self.current_result.get('findings', [])[:10]:
                    finding_text = f"<b>{finding['title']}</b> [{finding['severity']}]<br/>{finding['description']}"
                    story.append(Paragraph(finding_text, styles['Normal']))
                    story.append(Spacer(1, 0.1*inch))
                
                doc.build(story)
                
                from components.toast import show_toast
                show_toast(self, f"PDF saved: {file_path}")
                
            except ImportError:
                from components.toast import show_toast
                show_toast(self, "PDF export requires reportlab. Install: pip install reportlab")
            except Exception as e:
                from components.toast import show_toast
                show_toast(self, f"Export failed: {str(e)}")
