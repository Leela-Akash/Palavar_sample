"""Reusable aligned input field component."""
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout
from PySide6.QtCore import Qt
import config


class InputField(QWidget):
    """Perfectly aligned label + input field component."""
    
    def __init__(
        self, 
        label_text: str, 
        placeholder: str = "", 
        password: bool = False,
        help_text: str = "",
        parent=None
    ):
        """
        Initialize input field.
        
        Args:
            label_text: Label text
            placeholder: Placeholder text for input
            password: Enable password mode if True
            help_text: Optional help text below input
            parent: Parent widget
        """
        super().__init__(parent)
        self.input = QLineEdit()
        self.setup_ui(label_text, placeholder, password, help_text)
        
    def setup_ui(self, label_text: str, placeholder: str, password: bool, help_text: str):
        """Setup input field UI."""
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(config.SPACING_SM)
        
        label = QLabel(label_text)
        label.setFixedWidth(config.INPUT_LABEL_WIDTH)
        label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
        """)
        label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.input.setPlaceholderText(placeholder)
        if password:
            self.input.setEchoMode(QLineEdit.Password)
        
        self.input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {config.COLOR_BACKGROUND};
                color: {config.COLOR_TEXT};
                border: 1px solid {config.COLOR_BORDER};
                border-radius: 4px;
                padding: {config.SPACING_SM}px;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
            }}
            QLineEdit:focus {{
                border: 1px solid {config.COLOR_PRIMARY};
            }}
        """)
        
        layout.addWidget(label, 0, 0)
        layout.addWidget(self.input, 0, 1)
        
        if help_text:
            help_label = QLabel(help_text)
            help_label.setStyleSheet(f"""
                color: {config.COLOR_TEXT}88;
                font-family: {config.FONT_FAMILY};
                font-size: 8pt;
                font-style: italic;
            """)
            layout.addWidget(help_label, 1, 1)
            
    def text(self) -> str:
        """Get input text value."""
        return self.input.text()
    
    def set_text(self, text: str):
        """Set input text value."""
        self.input.setText(text)
