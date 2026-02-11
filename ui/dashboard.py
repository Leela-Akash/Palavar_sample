"""Dashboard page with overview statistics."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
import config
from components.section_header import SectionHeader
from components.metric_card import MetricCard
from components.cyber_card import CyberCard


class DashboardPage(QWidget):
    """Main dashboard with security overview."""
    
    def __init__(self, parent=None):
        """Initialize dashboard page."""
        super().__init__(parent)
        self.metric_cards = {}
        self.activities = []
        self.setup_ui()
        
    def setup_ui(self):
        """Setup dashboard UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG
        )
        layout.setSpacing(config.SPACING_LG)
        
        # Section title
        header = SectionHeader("Security Overview")
        layout.addWidget(header)
        
        # Load scan history
        from core.scan_history import ScanHistory
        history_stats = ScanHistory.get_stats()
        
        # Row of 4 metric cards
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(config.SPACING_MD)
        
        metrics = [
            ("security_score", "🛡️", "Security Score", "--", config.COLOR_PRIMARY),
            ("total_findings", "🔍", "Findings", "--", config.COLOR_WARNING),
            ("attack_paths", "⚔️", "Attack Paths", "--", config.COLOR_CRITICAL),
            ("risk_level", "⚠️", "Risk Level", "--", config.COLOR_ACCENT)
        ]
        
        self.metric_cards = {}
        for key, icon, label, value, color in metrics:
            card = MetricCard(icon, label, value, color)
            self.metric_cards[key] = card
            metrics_layout.addWidget(card)
        
        layout.addLayout(metrics_layout)
        
        # Two-column grid
        grid_layout = QHBoxLayout()
        grid_layout.setSpacing(config.SPACING_MD)
        
        # Left column: Security Insights
        insights_card = CyberCard("Security Insights")
        
        insights_layout = QVBoxLayout()
        insights_layout.setSpacing(config.SPACING_SM)
        
        # Placeholder for charts
        chart_label = QLabel("📊 Security Score Distribution")
        chart_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            padding: {config.SPACING_XL}px;
            background-color: {config.COLOR_BACKGROUND};
            border: 1px dashed {config.COLOR_BORDER};
            border-radius: 4px;
        """)
        chart_label.setAlignment(Qt.AlignCenter)
        insights_layout.addWidget(chart_label)
        
        findings_label = QLabel("📈 Findings by Cloud Provider")
        findings_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            padding: {config.SPACING_XL}px;
            background-color: {config.COLOR_BACKGROUND};
            border: 1px dashed {config.COLOR_BORDER};
            border-radius: 4px;
        """)
        findings_label.setAlignment(Qt.AlignCenter)
        insights_layout.addWidget(findings_label)
        
        insights_card.add_layout(insights_layout)
        grid_layout.addWidget(insights_card, 2)
        
        # Right column: Recent Activity
        activity_card = CyberCard("Recent Activity")
        
        self.activity_list = QListWidget()
        self.activity_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {config.COLOR_BACKGROUND};
                border: 1px solid {config.COLOR_BORDER};
                border-radius: 4px;
                padding: {config.SPACING_SM}px;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
            }}
            QListWidget::item {{
                color: {config.COLOR_TEXT};
                padding: {config.SPACING_SM}px;
                border-bottom: 1px solid {config.COLOR_BORDER};
            }}
            QListWidget::item:hover {{
                background-color: {config.COLOR_CARD};
            }}
        """)
        
        # Add initial welcome message
        self.add_activity("✨ CloudStrike initialized")
        self.add_activity("🛡️ Ready to scan cloud infrastructure")
        
        activity_card.add_widget(self.activity_list)
        grid_layout.addWidget(activity_card, 1)
        
        layout.addLayout(grid_layout)
        
        # Scan history info
        history_layout = QHBoxLayout()
        history_layout.setSpacing(config.SPACING_MD)
        
        self.last_scan_label = QLabel(f"Last Scan: {history_stats['last_scan']}")
        self.last_scan_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        history_layout.addWidget(self.last_scan_label)
        
        self.total_scans_label = QLabel(f"Total Scans: {history_stats['total_scans']}")
        self.total_scans_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        history_layout.addWidget(self.total_scans_label)
        
        history_layout.addStretch()
        layout.addLayout(history_layout)
    
    def update_stats(self, result: dict):
        """
        Update dashboard statistics from scan result.
        
        Args:
            result: Scan result with findings, attacks, and risk
        """
        from core.scan_history import ScanHistory
        from datetime import datetime
        
        risk = result.get('risk', {})
        findings = result.get('findings', [])
        attacks = result.get('attacks', [])
        
        security_score = risk.get('security_score', 0)
        risk_level = risk.get('risk_level', 'Unknown')
        
        # Determine score color
        if security_score >= 80:
            score_color = config.COLOR_PRIMARY
        elif security_score >= 60:
            score_color = config.COLOR_WARNING
        else:
            score_color = config.COLOR_CRITICAL
        
        # Determine risk level color
        risk_colors = {
            "Low": config.COLOR_PRIMARY,
            "Medium": config.COLOR_WARNING,
            "High": config.COLOR_CRITICAL,
            "Critical": config.COLOR_CRITICAL
        }
        risk_color = risk_colors.get(risk_level, config.COLOR_TEXT)
        
        # Update metric cards
        self.metric_cards["security_score"].update_value(str(security_score), score_color)
        self.metric_cards["total_findings"].update_value(str(len(findings)), config.COLOR_WARNING)
        self.metric_cards["attack_paths"].update_value(str(len(attacks)), config.COLOR_CRITICAL)
        self.metric_cards["risk_level"].update_value(risk_level, risk_color)
        
        # Update history labels
        history_stats = ScanHistory.get_stats()
        self.last_scan_label.setText(f"Last Scan: {history_stats['last_scan']}")
        self.total_scans_label.setText(f"Total Scans: {history_stats['total_scans']}")
        
        # Add activity to feed
        self.add_activity(f"🔍 Scan completed - {len(findings)} findings")
        self.add_activity(f"📊 Risk score: {security_score}")
        self.add_activity(f"⚔️ {len(attacks)} attack paths identified")

    def add_activity(self, message: str):
        """
        Add activity to feed.
        
        Args:
            message: Activity message
        """
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        activity = f"{message} | {timestamp}"
        
        item = QListWidgetItem(activity)
        self.activity_list.insertItem(0, item)
        self.activities.insert(0, activity)
        
        # Keep only last 15 activities
        while self.activity_list.count() > 15:
            self.activity_list.takeItem(self.activity_list.count() - 1)
        while len(self.activities) > 15:
            self.activities.pop()
