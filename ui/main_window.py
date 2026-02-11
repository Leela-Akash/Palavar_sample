"""Main application window."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import config
from ui.dashboard import DashboardPage
from ui.credentials_page import CredentialsPage
from ui.scan_page import ScanPage
from ui.report_page import ReportPage


class MainWindow(QMainWindow):
    """CloudStrike main application window."""
    
    def __init__(self):
        """Initialize main window."""
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup main window UI."""
        self.setWindowTitle("CloudStrike - Cloud Security Auditor")
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {config.COLOR_BACKGROUND};
            }}
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        self.pages = QStackedWidget()
        
        self.dashboard_page = DashboardPage()
        self.credentials_page = CredentialsPage()
        self.scan_page = ScanPage()
        self.report_page = ReportPage()
        
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.credentials_page)
        self.pages.addWidget(self.scan_page)
        self.pages.addWidget(self.report_page)
        
        self.scan_page.set_credentials_callback(self.credentials_page.get_credentials)
        self.scan_page.scan_completed.connect(self.on_scan_complete)
        
        main_layout.addWidget(self.pages)
        
    def create_sidebar(self) -> QWidget:
        """
        Create navigation sidebar.
        
        Returns:
            Sidebar widget
        """
        sidebar = QWidget()
        sidebar.setFixedWidth(config.SIDEBAR_WIDTH)
        sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {config.COLOR_CARD};
                border-right: 1px solid {config.COLOR_BORDER};
            }}
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        logo = QLabel("⚡ CloudStrike")
        logo.setStyleSheet(f"""
            color: {config.COLOR_PRIMARY};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_TITLE}pt;
            font-weight: bold;
            padding: {config.SPACING_LG}px;
            background-color: {config.COLOR_BACKGROUND};
        """)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)
        
        nav_items = [
            ("📊 Dashboard", 0),
            ("🔑 Credentials", 1),
            ("🔍 Scan Center", 2),
            ("📋 Reports", 3)
        ]
        
        self.nav_buttons = []
        for text, page_idx in nav_items:
            btn = self.create_nav_button(text, page_idx)
            self.nav_buttons.append(btn)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        version_label = QLabel("v1.0.0-alpha")
        version_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}66;
            font-family: {config.FONT_FAMILY};
            font-size: 8pt;
            padding: {config.SPACING_SM}px;
        """)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        self.nav_buttons[0].setProperty("active", True)
        self.update_nav_styles()
        
        return sidebar
        
    def create_nav_button(self, text: str, page_idx: int) -> QPushButton:
        """
        Create navigation button.
        
        Args:
            text: Button text
            page_idx: Page index to navigate to
            
        Returns:
            Configured navigation button
        """
        btn = QPushButton(text)
        btn.setProperty("active", False)
        btn.clicked.connect(lambda: self.navigate_to(page_idx))
        return btn
        
    def navigate_to(self, page_idx: int):
        """
        Navigate to specified page.
        
        Args:
            page_idx: Page index
        """
        self.pages.setCurrentIndex(page_idx)
        
        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == page_idx)
        
        self.update_nav_styles()
        
    def update_nav_styles(self):
        """Update navigation button styles."""
        for btn in self.nav_buttons:
            is_active = btn.property("active")
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {config.COLOR_PRIMARY + '22' if is_active else 'transparent'};
                    color: {config.COLOR_PRIMARY if is_active else config.COLOR_TEXT};
                    border: none;
                    border-left: 3px solid {config.COLOR_PRIMARY if is_active else 'transparent'};
                    text-align: left;
                    padding: {config.SPACING_MD}px {config.SPACING_LG}px;
                    font-family: {config.FONT_FAMILY};
                    font-size: {config.FONT_SIZE_NORMAL}pt;
                    font-weight: {'bold' if is_active else 'normal'};
                }}
                QPushButton:hover {{
                    background-color: {config.COLOR_PRIMARY}11;
                }}
            """)
            
    def on_scan_complete(self, result: dict):
        """
        Handle scan completion.
        
        Args:
            result: Dictionary with findings, attacks, and risk from scan
        """
        from core.scan_history import ScanHistory
        
        ScanHistory.save_scan(result)
        self.dashboard_page.update_stats(result)
        self.report_page.update_findings(result)
        self.navigate_to(3)
