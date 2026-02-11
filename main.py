"""CloudStrike - Automated Cloud Pentesting & Security Auditor."""
import sys
import logging
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def setup_logging():
    """Configure application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting CloudStrike application...")
    
    app = QApplication(sys.argv)
    app.setApplicationName("CloudStrike")
    app.setOrganizationName("CloudStrike Security")
    
    # Load global stylesheet
    try:
        with open('assets/theme.qss', 'r') as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        logger.warning(f"Could not load theme.qss: {e}")
    
    window = MainWindow()
    window.show()
    
    logger.info("Application started successfully")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
