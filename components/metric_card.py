"""Metric card component for dashboard statistics."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
import config


class MetricCard(QWidget):
    """Dashboard metric card with icon, number, and label."""
    
    def __init__(self, icon: str, label: str, value: str = "--", border_color: str = None, parent=None):
        """
        Initialize metric card.
        
        Args:
            icon: Emoji icon
            label: Metric label
            value: Metric value
            border_color: Left border color
            parent: Parent widget
        """
        super().__init__(parent)
        self.border_color = border_color or config.COLOR_PRIMARY
        self.setup_ui(icon, label, value)
        
    def setup_ui(self, icon: str, label: str, value: str):
        """Setup metric card UI."""
        self.setStyleSheet(f"""
            MetricCard {{
                background-color: {config.COLOR_CARD};
                border: 1px solid {config.COLOR_BORDER};
                border-left: 4px solid {self.border_color};
                border-radius: 8px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(config.SPACING_MD, config.SPACING_MD, config.SPACING_MD, config.SPACING_MD)
        layout.setSpacing(config.SPACING_XS)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 32pt;
        """)
        layout.addWidget(icon_label)
        
        # Value
        self.value_label = QLabel(value)
        self.value_label.setObjectName("value_label")
        self.value_label.setStyleSheet(f"""
            color: {self.border_color};
            font-family: {config.FONT_FAMILY};
            font-size: 48pt;
            font-weight: bold;
        """)
        layout.addWidget(self.value_label)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        layout.addWidget(label_widget)
        
    def update_value(self, value: str, color: str = None):
        """Update metric value and color."""
        self.value_label.setText(value)
        if color:
            self.border_color = color
            self.value_label.setStyleSheet(f"""
                color: {color};
                font-family: {config.FONT_FAMILY};
                font-size: 48pt;
                font-weight: bold;
            """)
            self.setStyleSheet(f"""
                MetricCard {{
                    background-color: {config.COLOR_CARD};
                    border: 1px solid {config.COLOR_BORDER};
                    border-left: 4px solid {color};
                    border-radius: 8px;
                }}
            """)
