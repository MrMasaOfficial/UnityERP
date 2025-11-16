from enum import Enum

class ThemeMode(Enum):
    LIGHT = 'light'
    DARK = 'dark'
    AUTO = 'auto'

LIGHT_THEME_STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #ffffff;
        color: #000000;
    }
    
    QTabWidget::pane {
        border: 1px solid #d0d0d0;
    }
    
    QTabBar::tab {
        background-color: #e6e6e6;
        color: #000000;
        padding: 5px 15px;
        border: 1px solid #cccccc;
        border-bottom: none;
    }
    
    QTabBar::tab:selected {
        background-color: #ffffff;
        border: 1px solid #d0d0d0;
        border-bottom: none;
    }
    
    QPushButton {
        background-color: #1f4788;
        color: white;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #2a5fa0;
    }
    
    QPushButton:pressed {
        background-color: #1a3d6e;
    }
    
    QPushButton:disabled {
        background-color: #cccccc;
        color: #666666;
    }
    
    QTableWidget {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #d0d0d0;
        gridline-color: #e0e0e0;
    }
    
    QTableWidget::item {
        padding: 5px;
    }
    
    QTableWidget::item:selected {
        background-color: #1f4788;
        color: white;
    }
    
    QHeaderView::section {
        background-color: #2a5fa0;
        color: white;
        padding: 5px;
        border: none;
        font-weight: bold;
    }
    
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
        background-color: #f5f5f5;
        color: #000000;
        border: 1px solid #cccccc;
        padding: 5px;
        border-radius: 3px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border: 2px solid #1f4788;
    }
    
    QComboBox {
        background-color: #f5f5f5;
        color: #000000;
        border: 1px solid #cccccc;
        padding: 5px;
        border-radius: 3px;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #cccccc;
    }
    
    QComboBox::down-arrow {
        image: url(noimg);
    }
    
    QDateEdit {
        background-color: #f5f5f5;
        color: #000000;
        border: 1px solid #cccccc;
        padding: 5px;
        border-radius: 3px;
    }
    
    QMessageBox {
        background-color: #ffffff;
        color: #000000;
    }
    
    QDialog {
        background-color: #ffffff;
        color: #000000;
    }
    
    QLabel {
        color: #000000;
    }
    
    QMenuBar {
        background-color: #f0f0f0;
        color: #000000;
        border-bottom: 1px solid #d0d0d0;
    }
    
    QMenu {
        background-color: #ffffff;
        color: #000000;
        border: 1px solid #d0d0d0;
    }
    
    QMenu::item:selected {
        background-color: #1f4788;
        color: white;
    }
"""

DARK_THEME_STYLESHEET = """
    QMainWindow, QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    
    QTabWidget::pane {
        border: 1px solid #3a3a3a;
    }
    
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #e0e0e0;
        padding: 5px 15px;
        border: 1px solid #3a3a3a;
        border-bottom: none;
    }
    
    QTabBar::tab:selected {
        background-color: #1e1e1e;
        border: 1px solid #404040;
        border-bottom: none;
    }
    
    QPushButton {
        background-color: #2a5fa0;
        color: #e0e0e0;
        border: none;
        padding: 6px 12px;
        border-radius: 4px;
        font-weight: bold;
    }
    
    QPushButton:hover {
        background-color: #3a7fc0;
    }
    
    QPushButton:pressed {
        background-color: #1a3d6e;
    }
    
    QPushButton:disabled {
        background-color: #404040;
        color: #666666;
    }
    
    QTableWidget {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #3a3a3a;
        gridline-color: #3a3a3a;
    }
    
    QTableWidget::item {
        padding: 5px;
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QTableWidget::item:selected {
        background-color: #2a5fa0;
        color: #e0e0e0;
    }
    
    QHeaderView::section {
        background-color: #1a3d6e;
        color: #e0e0e0;
        padding: 5px;
        border: none;
        font-weight: bold;
    }
    
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: 1px solid #4a4a4a;
        padding: 5px;
        border-radius: 3px;
    }
    
    QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
        border: 2px solid #2a5fa0;
    }
    
    QComboBox {
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: 1px solid #4a4a4a;
        padding: 5px;
        border-radius: 3px;
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #4a4a4a;
    }
    
    QComboBox::down-arrow {
        image: url(noimg);
    }
    
    QDateEdit {
        background-color: #3a3a3a;
        color: #e0e0e0;
        border: 1px solid #4a4a4a;
        padding: 5px;
        border-radius: 3px;
    }
    
    QMessageBox {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QDialog {
        background-color: #2d2d2d;
        color: #e0e0e0;
    }
    
    QLabel {
        color: #e0e0e0;
    }
    
    QMenuBar {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border-bottom: 1px solid #3a3a3a;
    }
    
    QMenu {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #3a3a3a;
    }
    
    QMenu::item:selected {
        background-color: #2a5fa0;
        color: #e0e0e0;
    }
"""

class ThemeManager:
    def __init__(self, theme_mode=ThemeMode.LIGHT):
        self.theme_mode = theme_mode
    
    def get_stylesheet(self):
        if self.theme_mode == ThemeMode.DARK:
            return DARK_THEME_STYLESHEET
        else:
            return LIGHT_THEME_STYLESHEET
    
    def set_theme(self, theme_mode):
        if isinstance(theme_mode, str):
            theme_mode = ThemeMode(theme_mode)
        self.theme_mode = theme_mode
    
    def get_theme(self):
        return self.theme_mode
    
    def toggle_theme(self):
        if self.theme_mode == ThemeMode.DARK:
            self.theme_mode = ThemeMode.LIGHT
        else:
            self.theme_mode = ThemeMode.DARK

theme_manager = ThemeManager(ThemeMode.LIGHT)

def get_stylesheet():
    return theme_manager.get_stylesheet()

def set_theme(theme):
    theme_manager.set_theme(theme)

def get_current_theme():
    return theme_manager.get_theme()

def toggle_theme():
    theme_manager.toggle_theme()
