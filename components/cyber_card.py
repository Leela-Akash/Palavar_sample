"""Reusable cyber-themed card container."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
import config


class CyberCard(QWidget):
    """Dark container card with title and content area."""
    
    def __init__(self, title: str = "", parent=None):
        """
        Initialize cyber card.
        
        Args:
            title: Card title text
            parent: Parent widget
        """
        super().__init__(parent)
        self.content_layout = QVBoxLayout()
        self.setup_ui(title)
        
    def setup_ui(self, title: str):
        """Setup card UI structure."""
        self.setStyleSheet(f"""
            CyberCard {{
                background-color: {config.COLOR_CARD};
                border: 1px solid {config.COLOR_BORDER};
                border-radius: 8px;
            }}
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            config.SPACING_MD, 
            config.SPACING_MD, 
            config.SPACING_MD, 
            config.SPACING_MD
        )
        main_layout.setSpacing(config.SPACING_SM)
        
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet(f"""
                color: {config.COLOR_PRIMARY};
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_HEADER}pt;
                font-weight: bold;
            """)
            main_layout.addWidget(title_label)
        
        self.content_layout.setSpacing(config.SPACING_SM)
        main_layout.addLayout(self.content_layout)
        
    def add_widget(self, widget: QWidget):
        """Add widget to card content area."""
        self.content_layout.addWidget(widget)
        
    def add_layout(self, layout):
        """Add layout to card content area."""
        self.content_layout.addLayout(layout)
