"""Attack simulation page."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
import config
from components.section_header import SectionHeader
from components.cyber_card import CyberCard
from components.status_badge import StatusBadge
from components.glow_button import GlowButton


class AttackPage(QWidget):
    """Attack simulation visualization page."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.attacks = []
        self.setup_ui()
    
    def setup_ui(self):
        """Setup attack page UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(config.SPACING_LG, config.SPACING_LG, config.SPACING_LG, config.SPACING_LG)
        layout.setSpacing(config.SPACING_LG)
        
        # Header with navigation button
        header_layout = QHBoxLayout()
        header = SectionHeader("⚔️ Attack Simulations")
        header_layout.addWidget(header)
        header_layout.addStretch()
        
        self.view_report_btn = GlowButton("View Full Report →")
        self.view_report_btn.clicked.connect(self.navigate_to_reports)
        header_layout.addWidget(self.view_report_btn)
        
        layout.addLayout(header_layout)
        
        # Scroll area for attacks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.attacks_container = QWidget()
        self.attacks_layout = QVBoxLayout(self.attacks_container)
        self.attacks_layout.setSpacing(config.SPACING_LG)
        self.attacks_layout.setContentsMargins(0, 0, 0, 0)
        
        self.empty_label = QLabel("No attack simulations yet. Run a scan to generate attack paths.")
        self.empty_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-style: italic;
        """)
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.attacks_layout.addWidget(self.empty_label)
        
        self.attacks_layout.addStretch()
        
        scroll.setWidget(self.attacks_container)
        layout.addWidget(scroll)
    
    def update_attacks(self, attacks: list):
        """Update attack simulations display."""
        self.attacks = attacks
        
        # Clear existing widgets
        while self.attacks_layout.count() > 0:
            item = self.attacks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.attacks:
            self.empty_label = QLabel("No attack simulations yet. Run a scan to generate attack paths.")
            self.empty_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT}88;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                font-style: italic;
            """)
            self.empty_label.setAlignment(Qt.AlignCenter)
            self.attacks_layout.addWidget(self.empty_label)
        else:
            # Add summary
            summary_label = QLabel(f"Generated {len(self.attacks)} potential attack paths based on discovered vulnerabilities.")
            summary_label.setWordWrap(True)
            summary_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                padding: {config.SPACING_MD}px;
                background-color: {config.COLOR_CARD};
                border-left: 3px solid {config.COLOR_ACCENT};
                border-radius: 4px;
            """)
            self.attacks_layout.addWidget(summary_label)
            
            # Add attack cards
            for attack in self.attacks:
                card = self.create_attack_card(attack)
                self.attacks_layout.addWidget(card)
        
        self.attacks_layout.addStretch()
    
    def create_attack_card(self, attack: dict) -> CyberCard:
        """Create an attack simulation card."""
        card = CyberCard()
        
        content_layout = QVBoxLayout()
        content_layout.setSpacing(config.SPACING_SM)
        
        # Title
        title_label = QLabel(attack["title"])
        title_label.setStyleSheet(f"""
            color: {config.COLOR_ACCENT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_HEADER}pt;
            font-weight: bold;
        """)
        content_layout.addWidget(title_label)
        
        # Badges
        badges_layout = QHBoxLayout()
        badges_layout.setSpacing(config.SPACING_SM)
        
        severity_badge = StatusBadge(attack["severity"], attack["severity"].lower())
        cloud_badge = StatusBadge(attack["cloud"], "info")
        
        badges_layout.addWidget(severity_badge)
        badges_layout.addWidget(cloud_badge)
        badges_layout.addStretch()
        
        content_layout.addLayout(badges_layout)
        
        # Attack chain steps
        steps_label = QLabel("🎯 Attack Chain:")
        steps_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            font-weight: bold;
            margin-top: {config.SPACING_MD}px;
        """)
        content_layout.addWidget(steps_label)
        
        for idx, step in enumerate(attack.get("steps", []), 1):
            step_label = QLabel(f"{idx}. {step}")
            step_label.setWordWrap(True)
            step_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT}cc;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                padding-left: {config.SPACING_LG}px;
                padding-top: {config.SPACING_XS}px;
            """)
            content_layout.addWidget(step_label)
        
        # Impact
        impact_label = QLabel(f"⚠️ Impact: {attack.get('impact', 'Unknown')}")
        impact_label.setWordWrap(True)
        impact_label.setStyleSheet(f"""
            color: {config.COLOR_CRITICAL};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            margin-top: {config.SPACING_MD}px;
            font-weight: bold;
            padding: {config.SPACING_SM}px;
            background-color: {config.COLOR_CRITICAL}22;
            border-radius: 4px;
        """)
        content_layout.addWidget(impact_label)
        
        card.add_layout(content_layout)
        
        return card
    
    def navigate_to_reports(self):
        """Navigate to reports page."""
        # Get main window and navigate
        main_window = self.window()
        if hasattr(main_window, 'navigate_to'):
            main_window.navigate_to(3)
