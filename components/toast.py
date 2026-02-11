"""Toast notification component for user feedback."""
from PySide6.QtWidgets import QWidget, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter
import config


class ToastNotification(QWidget):
    """Floating toast notification popup."""
    
    def __init__(self, message: str, parent=None):
        """
        Initialize toast notification.
        
        Args:
            message: Notification message
            parent: Parent widget
        """
        super().__init__(parent)
        self.message = message
        self.setup_ui()
        self.setup_animation()
        
    def setup_ui(self):
        """Setup toast UI."""
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: #111827;
                border: 2px solid {config.COLOR_PRIMARY};
                border-radius: 8px;
                padding: {config.SPACING_MD}px;
            }}
        """)
        
        self.label = QLabel(self.message)
        self.label.setStyleSheet(f"""
            color: {config.COLOR_TEXT};
            font-family: {config.FONT_FAMILY};
            font-size: {config.FONT_SIZE_NORMAL}pt;
            background: transparent;
            border: none;
        """)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.setFixedSize(300, 60)
        
    def setup_animation(self):
        """Setup fade in/out animation."""
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_in.setDuration(300)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_out.finished.connect(self.close)
        
    def show_toast(self):
        """Show toast with auto-hide."""
        if self.parent():
            parent_rect = self.parent().rect()
            x = parent_rect.width() - self.width() - 20
            y = parent_rect.height() - self.height() - 20
            self.move(x, y)
        
        self.show()
        self.fade_in.start()
        
        QTimer.singleShot(3000, self.hide_toast)
        
    def hide_toast(self):
        """Hide toast with fade out."""
        self.fade_out.start()
    
    def paintEvent(self, event):
        """Custom paint for rounded corners."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        super().paintEvent(event)


def show_toast(parent, message: str):
    """
    Show toast notification.
    
    Args:
        parent: Parent widget
        message: Toast message
    """
    toast = ToastNotification(message, parent)
    toast.show_toast()
