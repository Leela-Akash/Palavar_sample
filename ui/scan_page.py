"""Scan execution page."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QTextCursor
import logging
import config
from components.section_header import SectionHeader
from components.glow_button import GlowButton
from core.scanner import run_cloud_scan

logger = logging.getLogger(__name__)


class ScanWorker(QThread):
    """Background worker for running scans."""
    
    log_signal = Signal(str)
    finished_signal = Signal(dict)
    
    def __init__(self, credentials):
        """Initialize worker with credentials."""
        super().__init__()
        self.credentials = credentials
    
    def run(self):
        """Execute scan in background thread."""
        self.log_signal.emit("[*] Initializing CloudStrike scanner...")
        self.log_signal.emit("[*] Loading cloud credentials...")
        
        if self.credentials.get('aws', {}).get('access_key'):
            self.log_signal.emit("[*] AWS: Authenticating and enumerating resources...")
        if self.credentials.get('azure', {}).get('tenant_id'):
            self.log_signal.emit("[*] Azure: Connecting to subscriptions...")
        if self.credentials.get('gcp', {}).get('project_id'):
            self.log_signal.emit("[*] GCP: Analyzing project resources...")
        
        self.log_signal.emit("[*] Running security checks...")
        
        result = run_cloud_scan(self.credentials)
        
        findings_count = len(result.get('findings', []))
        attacks_count = len(result.get('attacks', []))
        
        self.log_signal.emit(f"[+] Scan complete! Found {findings_count} issues.")
        self.log_signal.emit(f"[+] Generated {attacks_count} attack simulations.")
        self.finished_signal.emit(result)


class ScanPage(QWidget):
    """Cloud security scan execution page."""
    
    scan_completed = Signal(dict)
    
    def __init__(self, parent=None):
        """Initialize scan page."""
        super().__init__(parent)
        self.worker = None
        self.credentials_callback = None
        self.setup_ui()
    
    def set_credentials_callback(self, callback):
        """Set callback function to retrieve credentials."""
        self.credentials_callback = callback
        
    def setup_ui(self):
        """Setup scan UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG
        )
        layout.setSpacing(config.SPACING_LG)
        
        header = SectionHeader("Scan Center")
        layout.addWidget(header)
        
        self.scan_btn = GlowButton("▶ Start Cloud Scan")
        self.scan_btn.clicked.connect(self.start_scan)
        layout.addWidget(self.scan_btn, alignment=Qt.AlignCenter)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet(f"""
            QTextEdit {{
                background-color: {config.COLOR_BACKGROUND};
                color: {config.COLOR_PRIMARY};
                border: 1px solid {config.COLOR_BORDER};
                border-radius: 4px;
                padding: {config.SPACING_SM}px;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
            }}
        """)
        layout.addWidget(self.terminal)
        
    def start_scan(self):
        """Start security scan."""
        logger.info("Starting cloud security scan...")
        self.scan_btn.setEnabled(False)
        self.terminal.clear()
        
        credentials = {}
        if self.credentials_callback:
            credentials = self.credentials_callback()
        
        self.worker = ScanWorker(credentials)
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished_signal.connect(self.on_scan_complete)
        self.worker.start()
        
    def append_log(self, message: str):
        """Append message to terminal output."""
        self.terminal.append(message)
        self.terminal.moveCursor(QTextCursor.End)
        
    def on_scan_complete(self, result: dict):
        """Handle scan completion."""
        self.scan_btn.setEnabled(True)
        self.scan_completed.emit(result)
        findings_count = len(result.get('findings', []))
        logger.info(f"Scan completed with {findings_count} findings")
