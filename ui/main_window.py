"""Main application window."""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel
)
from PySide6.QtCore import Qt
import config

from ui.dashboard import DashboardPage
from ui.credentials_page import CredentialsPage
from ui.scan_page import ScanPage
from ui.report_page import ReportPage


class MainWindow(QMainWindow):
    """CloudStrike main application window."""

    def __init__(self):
        super().__init__()
        self.last_scan_time = "Never"
        self.scan_status = "Ready"
        self.setup_ui()

    # ---------------- MAIN UI ---------------- #

    def setup_ui(self):
        self.setWindowTitle("CloudStrike - Cloud Security Auditor")
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)

        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {config.COLOR_BACKGROUND};
            }}
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header_bar = self.create_header_bar()
        main_layout.addWidget(header_bar)

        # Content area
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        sidebar = self.create_sidebar()
        content_layout.addWidget(sidebar)

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
        self.scan_page.scan_started.connect(self.on_scan_started)

        content_layout.addWidget(self.pages)
        main_layout.addLayout(content_layout)

    # ---------------- SIDEBAR ---------------- #

    def create_sidebar(self) -> QWidget:
        sidebar = QWidget()
        sidebar.setFixedWidth(240)   # ⭐ FIXED WIDTH (was too small)

        sidebar.setStyleSheet(f"""
            QWidget {{
                background-color: {config.COLOR_CARD};
                border-right: 1px solid {config.COLOR_BORDER};
            }}
        """)

        layout = QVBoxLayout(sidebar)

        # ⭐ FIX: Proper sidebar padding
        layout.setContentsMargins(16, 20, 16, 20)
        layout.setSpacing(8)

        # ⭐ FIX: Logo alignment + clipping issue solved
        logo = QLabel("⚡ CloudStrike")
        logo.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        logo.setContentsMargins(4, 0, 0, 12)

        logo.setStyleSheet(f"""
            color: {config.COLOR_PRIMARY};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_TITLE}pt;
            font-weight: bold;
        """)

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
        btn = QPushButton(text)
        btn.setProperty("active", False)
        btn.clicked.connect(lambda: self.navigate_to(page_idx))
        return btn

    def navigate_to(self, page_idx: int):
        self.pages.setCurrentIndex(page_idx)

        for i, btn in enumerate(self.nav_buttons):
            btn.setProperty("active", i == page_idx)

        self.update_nav_styles()

        titles = [
            "Security Overview",
            "Cloud Credentials",
            "Scan Center",
            "Security Reports"
        ]
        self.set_page_title(titles[page_idx])

    def update_nav_styles(self):
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

    # ---------------- HEADER ---------------- #

    def create_header_bar(self) -> QWidget:
        header = QWidget()
        header.setFixedHeight(60)

        header.setStyleSheet("""
            QWidget {
                background-color: #111827;
                border-bottom: 1px solid #1f2937;
            }
        """)

        layout = QHBoxLayout(header)

        # ⭐ FIX: Add vertical padding
        layout.setContentsMargins(config.SPACING_LG, 12, config.SPACING_LG, 12)

        # ⭐ FIX: Bigger title
        self.page_title_label = QLabel("Security Overview")
        self.page_title_label.setStyleSheet(f"""
            color: {config.COLOR_PRIMARY};
            font-family: {config.FONT_FAMILY};
            font-size: 18pt;
            font-weight: bold;
        """)
        layout.addWidget(self.page_title_label)

        layout.addStretch()

        self.last_scan_label = QLabel(f"Last Scan: {self.last_scan_time}")
        self.last_scan_label.setStyleSheet(f"""
            color: {config.COLOR_TEXT}88;
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            margin-right: {config.SPACING_MD}px;
        """)
        layout.addWidget(self.last_scan_label)

        from components.status_badge import StatusBadge
        self.status_badge = StatusBadge(self.scan_status, "info")
        layout.addWidget(self.status_badge)

        return header

    def set_page_title(self, title: str):
        self.page_title_label.setText(title)

    # ---------------- SCAN EVENTS ---------------- #

    def on_scan_started(self):
        from components.toast import show_toast
        self.scan_status = "Scanning"
        self.status_badge.setText(self.scan_status)
        self.status_badge.setup_style("warning")
        show_toast(self, "Scan started")
        self.dashboard_page.add_activity("🔍 Cloud scan initiated")

    def on_scan_complete(self, result: dict):
        from core.scan_history import ScanHistory
        from datetime import datetime
        from components.toast import show_toast

        ScanHistory.save_scan(result)
        self.dashboard_page.update_stats(result)
        self.report_page.update_findings(result)

        self.last_scan_time = datetime.now().strftime("%H:%M:%S")
        self.last_scan_label.setText(f"Last Scan: {self.last_scan_time}")

        self.scan_status = "Completed"
        self.status_badge.setText(self.scan_status)
        self.status_badge.setup_style("info")

        findings_count = len(result.get('findings', []))
        show_toast(self, f"Scan complete! Found {findings_count} issues")

        self.navigate_to(3)
