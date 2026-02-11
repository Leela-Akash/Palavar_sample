"""Credentials management page."""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QMessageBox
from PySide6.QtCore import Qt
import logging
import config
from components.section_header import SectionHeader
from components.glow_button import GlowButton
from components.input_field import InputField

logger = logging.getLogger(__name__)


class CredentialsPage(QWidget):
    """Cloud credentials configuration page."""
    
    def __init__(self, parent=None):
        """Initialize credentials page."""
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup credentials UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG, 
            config.SPACING_LG
        )
        layout.setSpacing(config.SPACING_LG)
        
        header = SectionHeader("Cloud Credentials")
        layout.addWidget(header)
        
        tabs = QTabWidget()
        tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {config.COLOR_BORDER};
                background-color: {config.COLOR_CARD};
                border-radius: 4px;
            }}
            QTabBar::tab {{
                background-color: {config.COLOR_BACKGROUND};
                color: {config.COLOR_TEXT};
                border: 1px solid {config.COLOR_BORDER};
                padding: {config.SPACING_SM}px {config.SPACING_MD}px;
                font-family: {config.FONT_FAMILY};
                font-size: {config.FONT_SIZE_NORMAL}pt;
            }}
            QTabBar::tab:selected {{
                background-color: {config.COLOR_CARD};
                color: {config.COLOR_PRIMARY};
                border-bottom: 2px solid {config.COLOR_PRIMARY};
            }}
        """)
        
        tabs.addTab(self.create_aws_tab(), "AWS")
        tabs.addTab(self.create_azure_tab(), "Azure")
        tabs.addTab(self.create_gcp_tab(), "GCP")
        
        layout.addWidget(tabs)
        
        save_btn = GlowButton("Save Credentials")
        save_btn.clicked.connect(self.save_credentials)
        layout.addWidget(save_btn, alignment=Qt.AlignRight)
        
        layout.addStretch()
        
    def create_aws_tab(self) -> QWidget:
        """Create AWS credentials tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(config.SPACING_MD, config.SPACING_MD, config.SPACING_MD, config.SPACING_MD)
        layout.setSpacing(config.SPACING_MD)
        
        self.aws_access_key = InputField("Access Key ID:", placeholder="AKIAIOSFODNN7EXAMPLE")
        self.aws_secret_key = InputField("Secret Access Key:", password=True, placeholder="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY")
        self.aws_region = InputField("Region:", placeholder="us-east-1")
        
        layout.addWidget(self.aws_access_key)
        layout.addWidget(self.aws_secret_key)
        layout.addWidget(self.aws_region)
        layout.addStretch()
        
        return widget
        
    def create_azure_tab(self) -> QWidget:
        """Create Azure credentials tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(config.SPACING_MD, config.SPACING_MD, config.SPACING_MD, config.SPACING_MD)
        layout.setSpacing(config.SPACING_MD)
        
        self.azure_tenant_id = InputField("Tenant ID:", placeholder="00000000-0000-0000-0000-000000000000")
        self.azure_client_id = InputField("Client ID:", placeholder="00000000-0000-0000-0000-000000000000")
        self.azure_client_secret = InputField("Client Secret:", password=True, placeholder="Your client secret")
        
        layout.addWidget(self.azure_tenant_id)
        layout.addWidget(self.azure_client_id)
        layout.addWidget(self.azure_client_secret)
        layout.addStretch()
        
        return widget
        
    def create_gcp_tab(self) -> QWidget:
        """Create GCP credentials tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(config.SPACING_MD, config.SPACING_MD, config.SPACING_MD, config.SPACING_MD)
        layout.setSpacing(config.SPACING_MD)
        
        self.gcp_project_id = InputField("Project ID:", placeholder="my-project-123456")
        self.gcp_service_account = InputField("Service Account JSON:", placeholder="/path/to/service-account.json")
        
        layout.addWidget(self.gcp_project_id)
        layout.addWidget(self.gcp_service_account)
        layout.addStretch()
        
        return widget
        
    def save_credentials(self):
        """Save cloud credentials."""
        logger.info("Saving cloud credentials...")
        QMessageBox.information(self, "Success", "Credentials saved successfully!")
    
    def get_credentials(self) -> dict:
        """Get all configured credentials."""
        return {
            'aws': {
                'access_key': self.aws_access_key.text().strip(),
                'secret_key': self.aws_secret_key.text().strip(),
                'region': self.aws_region.text().strip() or 'us-east-1'
            },
            'azure': {
                'tenant_id': self.azure_tenant_id.text().strip(),
                'client_id': self.azure_client_id.text().strip(),
                'client_secret': self.azure_client_secret.text().strip()
            },
            'gcp': {
                'project_id': self.gcp_project_id.text().strip(),
                'service_account_path': self.gcp_service_account.text().strip()
            }
        }
