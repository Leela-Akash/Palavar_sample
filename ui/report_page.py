"""Security findings report page."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QTextEdit, QPushButton, QHBoxLayout, QApplication
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
        self.attacks = []
        self.current_result = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup report UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG
        )
        layout.setSpacing(config.SPACING_LG)
        
        # Header with export buttons
        header_layout = QHBoxLayout()
        header = SectionHeader("Security Report")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        from components.glow_button import GlowButton
        self.export_json_btn = GlowButton("Export JSON")
        self.export_json_btn.clicked.connect(self.export_json)
        header_layout.addWidget(self.export_json_btn)
        
        self.export_pdf_btn = GlowButton("Export PDF", primary=False)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        header_layout.addWidget(self.export_pdf_btn)
        
        layout.addLayout(header_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: transparent;
            }}
        """)
        
        self.findings_container = QWidget()
        self.findings_layout = QVBoxLayout(self.findings_container)
        self.findings_layout.setSpacing(config.SPACING_LG)
        self.findings_layout.setContentsMargins(0, 0, 0, 0)
        
        self.empty_label = QLabel("No findings yet. Run a scan to see results.")
        self.empty_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-style: italic;
        """)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.findings_layout.addWidget(self.empty_label)
        
        self.findings_layout.addStretch()
        
        scroll.setWidget(self.findings_container)
        layout.addWidget(scroll)
        
    def update_findings(self, result: dict):
        """
        Update report with new findings and attack simulations.
        
        Args:
            result: Dictionary with 'findings', 'attacks', 'risk', and 'remediation'
        """
        self.current_result = result
        self.findings = result.get('findings', [])
        self.attacks = result.get('attacks', [])
        risk = result.get('risk', {})
        remediation = result.get('remediation', [])
        
        while self.findings_layout.count() > 0:
            item = self.findings_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.findings and not self.attacks:
            self.empty_label = QLabel("No findings yet. Run a scan to see results.")
            self.empty_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT}88;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                font-style: italic;
            """)
            self.empty_label.setAlignment(Qt.AlignCenter)
            self.findings_layout.addWidget(self.empty_label)
        else:
            if risk:
                summary_header = SectionHeader("📊 Security Summary")
                self.findings_layout.addWidget(summary_header)
                
                summary_card = self.create_summary_card(risk)
                self.findings_layout.addWidget(summary_card)
            
            if remediation:
                remediation_header = SectionHeader("🛠️ Auto-Remediation Scripts")
                self.findings_layout.addWidget(remediation_header)
                
                for script in remediation:
                    card = self.create_remediation_card(script)
                    self.findings_layout.addWidget(card)
            
            if self.attacks:
                attack_header = SectionHeader("⚔️ Attack Simulations")
                self.findings_layout.addWidget(attack_header)
                
                for attack in self.attacks:
                    card = self.create_attack_card(attack)
                    self.findings_layout.addWidget(card)
            
            if self.findings:
                findings_header = SectionHeader("🔍 Security Findings")
                self.findings_layout.addWidget(findings_header)
                
                for finding in self.findings:
                    card = self.create_finding_card(finding)
                    self.findings_layout.addWidget(card)
        
        self.findings_layout.addStretch()
        
    def create_finding_card(self, finding: dict) -> CyberCard:
        """
        Create a finding card.
        
        Args:
            finding: Finding dictionary
            
        Returns:
            Configured CyberCard widget
        """
        card = CyberCard()
        
        header_layout = QVBoxLayout()
        header_layout.setSpacing(config.SPACING_SM)
        
        title_label = QLabel(finding["title"])
        title_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_HEADER}pt;
            font-weight: bold;
        """)
        header_layout.addWidget(title_label)
        
        badges_layout = QVBoxLayout()
        badges_layout.setSpacing(config.SPACING_XS)
        
        severity_badge = StatusBadge(finding["severity"], finding["severity"].lower())
        cloud_badge = StatusBadge(finding["cloud"], "info")
        
        badges_layout.addWidget(severity_badge)
        badges_layout.addWidget(cloud_badge)
        
        header_layout.addLayout(badges_layout)
        
        desc_label = QLabel(finding["description"])
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}cc;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        header_layout.addWidget(desc_label)
        
        if finding.get("remediation"):
            remediation_label = QLabel(f"💡 Remediation: {finding['remediation']}")
            remediation_label.setWordWrap(True)
            remediation_label.setStyleSheet(f"""
                color: {config.COLOR_PRIMARY};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                margin-top: {config.SPACING_SM}px;
            """)
            header_layout.addWidget(remediation_label)
        
        card.add_layout(header_layout)
        
        return card
    
    def create_attack_card(self, attack: dict) -> CyberCard:
        """
        Create an attack simulation card.
        
        Args:
            attack: Attack dictionary
            
        Returns:
            Configured CyberCard widget
        """
        card = CyberCard()
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(config.SPACING_SM)
        
        title_label = QLabel(attack["title"])
        title_label.setStyleSheet(f"""
            color: {config.COLOR_ACCENT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_HEADER}pt;
            font-weight: bold;
        """)
        content_layout.addWidget(title_label)
        
        badges_layout = QVBoxLayout()
        badges_layout.setSpacing(config.SPACING_XS)
        
        severity_badge = StatusBadge(attack["severity"], attack["severity"].lower())
        cloud_badge = StatusBadge(attack["cloud"], "info")
        
        badges_layout.addWidget(severity_badge)
        badges_layout.addWidget(cloud_badge)
        
        content_layout.addLayout(badges_layout)
        
        steps_label = QLabel("Attack Chain:")
        steps_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
            margin-top: {config.SPACING_SM}px;
        """)
        content_layout.addWidget(steps_label)
        
        for idx, step in enumerate(attack.get("steps", []), 1):
            step_label = QLabel(f"{idx}. {step}")
            step_label.setWordWrap(True)
            step_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT}cc;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                padding-left: {config.SPACING_MD}px;
            """)
            content_layout.addWidget(step_label)
        
        impact_label = QLabel(f"⚠️ Impact: {attack.get('impact', 'Unknown')}")
        impact_label.setWordWrap(True)
        impact_label.setStyleSheet(f"""
            color: {config.COLOR_CRITICAL};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            margin-top: {config.SPACING_SM}px;
            font-weight: bold;
        """)
        content_layout.addWidget(impact_label)
        
        card.add_layout(content_layout)
        
        return card
    
    def create_summary_card(self, risk: dict) -> CyberCard:
        """
        Create security summary card.
        
        Args:
            risk: Risk analysis dictionary
            
        Returns:
            Configured CyberCard widget
        """
        card = CyberCard()
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(config.SPACING_MD)
        
        security_score = risk.get('security_score', 0)
        risk_level = risk.get('risk_level', 'Unknown')
        summary = risk.get('summary', '')
        top_risks = risk.get('top_risks', [])
        
        # Score display
        score_label = QLabel(f"Security Score: {security_score}/100")
        if security_score >= 80:
            score_color = config.COLOR_PRIMARY
        elif security_score >= 60:
            score_color = config.COLOR_WARNING
        else:
            score_color = config.COLOR_CRITICAL
        
        score_label.setStyleSheet(f"""
            color: {score_color};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_TITLE}pt;
            font-weight: bold;
        """)
        content_layout.addWidget(score_label)
        
        # Risk level badge
        risk_badge = StatusBadge(f"Risk Level: {risk_level}", risk_level.lower())
        content_layout.addWidget(risk_badge)
        
        # Summary text
        summary_label = QLabel(summary)
        summary_label.setWordWrap(True)
        summary_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            margin-top: {config.SPACING_SM}px;
        """)
        content_layout.addWidget(summary_label)
        
        # Top risks
        if top_risks:
            top_risks_label = QLabel("🎯 Top Priority Risks:")
            top_risks_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                font-weight: bold;
                margin-top: {config.SPACING_SM}px;
            """)
            content_layout.addWidget(top_risks_label)
            
            for idx, risk_title in enumerate(top_risks, 1):
                risk_item = QLabel(f"{idx}. {risk_title}")
                risk_item.setWordWrap(True)
                risk_item.setStyleSheet(f"""
                    color: {config.COLOR_ACCENT};
                    font-family: {config.FONT_FAMILY};
                    font-size: {config.FONT_SIZE_NORMAL}pt;
                    padding-left: {config.SPACING_MD}px;
                """)
                content_layout.addWidget(risk_item)
        
        card.add_layout(content_layout)
        
        return card

    def create_remediation_card(self, script: dict) -> CyberCard:
        """
        Create a remediation script card.
        
        Args:
            script: Remediation script dictionary
            
        Returns:
            Configured CyberCard widget
        """
        card = CyberCard()
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(config.SPACING_SM)
        
        title_label = QLabel(script["title"])
        title_label.setStyleSheet(f"""
            color: {config.COLOR_PRIMARY};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_HEADER}pt;
            font-weight: bold;
        """)
        content_layout.addWidget(title_label)
        
        cloud_badge = StatusBadge(script["cloud"], "info")
        content_layout.addWidget(cloud_badge)
        
        # CLI Script section
        cli_header = QLabel("CLI Commands:")
        cli_header.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
            margin-top: {config.SPACING_SM}px;
        """)
        content_layout.addWidget(cli_header)
        
        cli_text = QTextEdit()
        cli_text.setPlainText(script.get("cli_script", ""))
        cli_text.setReadOnly(True)
        cli_text.setMaximumHeight(150)
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
        content_layout.addWidget(cli_text)
        
        cli_copy_btn = QPushButton("📋 Copy CLI")
        cli_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(script.get("cli_script", "")))
        cli_copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.COLOR_CARD};
                color: {config.COLOR_PRIMARY};
                border: 1px solid {config.COLOR_PRIMARY};
                border-radius: 4px;
                padding: {config.SPACING_XS}px {config.SPACING_SM}px;
                font-family: {config.FONT_FAMILY};
                font-size: 9pt;
            }}
            QPushButton:hover {{
                background-color: {config.COLOR_PRIMARY}22;
            }}
        """)
        content_layout.addWidget(cli_copy_btn)
        
        # Terraform section
        tf_header = QLabel("Terraform:")
        tf_header.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
            margin-top: {config.SPACING_SM}px;
        """)
        content_layout.addWidget(tf_header)
        
        tf_text = QTextEdit()
        tf_text.setPlainText(script.get("terraform", ""))
        tf_text.setReadOnly(True)
        tf_text.setMaximumHeight(150)
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
        content_layout.addWidget(tf_text)
        
        tf_copy_btn = QPushButton("📋 Copy Terraform")
        tf_copy_btn.clicked.connect(lambda: self.copy_to_clipboard(script.get("terraform", "")))
        tf_copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.COLOR_CARD};
                color: {config.COLOR_ACCENT};
                border: 1px solid {config.COLOR_ACCENT};
                border-radius: 4px;
                padding: {config.SPACING_XS}px {config.SPACING_SM}px;
                font-family: {config.FONT_FAMILY};
                font-size: 9pt;
            }}
            QPushButton:hover {{
                background-color: {config.COLOR_ACCENT}22;
            }}
        """)
        content_layout.addWidget(tf_copy_btn)
        
        card.add_layout(content_layout)
        
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
