"""Reusable status badge component."""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
import config


class StatusBadge(QLabel):
    """Small colored status badge."""
    
    def __init__(self, text: str, status_type: str = "info", parent=None):
        """
        Initialize status badge.
        
        Args:
            text: Badge text
            status_type: One of 'critical', 'warning', 'info', 'secure'
            parent: Parent widget
        """
        super().__init__(text, parent)
        self.setup_style(status_type)
        
    def setup_style(self, status_type: str):
        """Apply badge styling based on status type."""
        color_map = {
            "critical": config.COLOR_CRITICAL,
            "warning": config.COLOR_WARNING,
            "info": config.COLOR_PRIMARY,
            "secure": config.COLOR_PRIMARY
        }
        
        color = color_map.get(status_type.lower(), config.COLOR_TEXT)
        
        self.setStyleSheet(f"""
            background-color: {color}22;
            color: {color};
            border: 1px solid {color};
            border-radius: 4px;
            padding: {config.SPACING_XS}px {config.SPACING_SM}px;
            font-family: {config.FONT_FAMILY};
            font-size: 9pt;
            font-weight: bold;
        """)
        self.setAlignment(Qt.AlignCenter)
