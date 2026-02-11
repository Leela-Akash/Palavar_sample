"""Reusable section header component."""
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
import config


class SectionHeader(QLabel):
    """Large neon section title."""
    
    def __init__(self, text: str, parent=None):
        """
        Initialize section header.
        
        Args:
            text: Header text
            parent: Parent widget
        """
        super().__init__(text, parent)
        self.setStyleSheet(f"""
            color: {config.COLOR_PRIMARY};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_TITLE}pt;
            font-weight: bold;
            padding: {config.SPACING_SM}px 0px;
        """)
        self.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
