"""Reusable neon glow button component."""
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QColor
import config


class GlowButton(QPushButton):
    """Cyberpunk-style button with neon glow effect."""
    
    def __init__(self, text: str, primary: bool = True, parent=None):
        """
        Initialize glow button.
        
        Args:
            text: Button text
            primary: Use primary color if True, accent color if False
            parent: Parent widget
        """
        super().__init__(text, parent)
        self.primary = primary
        self._glow_intensity = 0
        self.setup_style()
        
    def setup_style(self):
        """Apply button styling."""
        color = config.COLOR_PRIMARY if self.primary else config.COLOR_ACCENT
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {config.COLOR_CARD};
                color: {color};
                border: 2px solid {color};
                border-radius: 4px;
                padding: {config.SPACING_SM}px {config.SPACING_MD}px;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {color}22;
                box-shadow: 0 0 20px {color};
            }}
            QPushButton:pressed {{
                background-color: {color}44;
            }}
            QPushButton:disabled {{
                color: #555;
                border-color: #555;
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
        
    def _get_glow_intensity(self) -> int:
        return self._glow_intensity
    
    def _set_glow_intensity(self, value: int):
        self._glow_intensity = value
        
    glow_intensity = Property(int, _get_glow_intensity, _set_glow_intensity)


from PySide6.QtCore import Qt
