"""Dashboard page with overview statistics."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
import config
from components.cyber_card import CyberCard
from components.section_header import SectionHeader


class DashboardPage(QWidget):
    """Main dashboard with security overview."""
    
    def __init__(self, parent=None):
        """Initialize dashboard page."""
        super().__init__(parent)
        self.stat_cards = {}
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
        
        header = SectionHeader("Security Dashboard")
        layout.addWidget(header)
        
        self.stats_layout = QGridLayout()
        self.stats_layout.setSpacing(config.SPACING_MD)
        
        # Load scan history
        from core.scan_history import ScanHistory
        history_stats = ScanHistory.get_stats()
        
        stats = [
            ("security_score", "Security Score", "--", config.COLOR_PRIMARY),
            ("total_findings", "Total Findings", "--", config.COLOR_WARNING),
            ("attack_paths", "Attack Paths", "--", config.COLOR_CRITICAL),
            ("risk_level", "Risk Level", "--", config.COLOR_TEXT)
        ]
        
        for idx, (key, title, value, color) in enumerate(stats):
            card = self.create_stat_card(title, value, color)
            self.stat_cards[key] = card
            row = idx // 2
            col = idx % 2
            self.stats_layout.addWidget(card, row, col)
        
        layout.addLayout(self.stats_layout)
        
        # Scan history info
        history_layout = QVBoxLayout()
        history_layout.setSpacing(config.SPACING_SM)
        
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
        
        layout.addLayout(history_layout)
        layout.addStretch()
        
    def create_stat_card(self, title: str, value: str, color: str) -> CyberCard:
        """
        Create a statistics card.
        
        Args:
            title: Stat title
            value: Stat value
            color: Value color
            
        Returns:
            Configured CyberCard widget
        """
        card = CyberCard()
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        
        value_label = QLabel(value)
        value_label.setObjectName("value_label")
        value_label.setStyleSheet(f"""
            color: {color};
            font-family: {config.FONT_FAMILY};
            font-size: 32pt;
            font-weight: bold;
        """)
        
        card.add_widget(title_label)
        card.add_widget(value_label)
        
        return card
    
    def update_stats(self, result: dict):
        """
        Update dashboard statistics from scan result.
        
        Args:
            result: Scan result with findings, attacks, and risk
        """
        from core.scan_history import ScanHistory
        
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
        
        # Update cards
        self._update_card_value("security_score", str(security_score), score_color)
        self._update_card_value("total_findings", str(len(findings)), config.COLOR_WARNING)
        self._update_card_value("attack_paths", str(len(attacks)), config.COLOR_CRITICAL)
        self._update_card_value("risk_level", risk_level, risk_color)
        
        # Update history labels
        history_stats = ScanHistory.get_stats()
        self.last_scan_label.setText(f"Last Scan: {history_stats['last_scan']}")
        self.total_scans_label.setText(f"Total Scans: {history_stats['total_scans']}")
    
    def _update_card_value(self, key: str, value: str, color: str):
        """Update a stat card's value and color."""
        card = self.stat_cards.get(key)
        if card:
            value_label = card.findChild(QLabel, "value_label")
            if value_label:
                value_label.setText(value)
                value_label.setStyleSheet(f"""
                    color: {color};
                    font-family: {config.FONT_FAMILY};
                    font-size: 32pt;
                    font-weight: bold;
                """)
