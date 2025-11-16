import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QTabWidget, QMessageBox, QMenuBar, QMenu, QDialog,
                             QFormLayout, QComboBox, QPushButton, QLabel)
from PyQt5.QtCore import Qt
from database import Database
from ui.inventory import InventoryWidget
from ui.sales import SalesWidget
from ui.purchasing import PurchasingWidget
from ui.accounting import AccountingWidget
from ui.reports import ReportsWidget
from translations import t, set_language, get_language
from themes import set_theme, get_stylesheet, ThemeMode
from settings import settings_manager

class SettingsDialog(QDialog):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle(t('settings'))
        self.setGeometry(200, 200, 400, 250)
        
        layout = QFormLayout()
        
        language_label = QLabel(t('language') + ':')
        self.language_combo = QComboBox()
        self.language_combo.addItem(t('arabic'), 'ar')
        self.language_combo.addItem(t('english'), 'en')
        current_lang = settings_manager.get_language()
        self.language_combo.setCurrentIndex(0 if current_lang == 'ar' else 1)
        layout.addRow(language_label, self.language_combo)
        
        theme_label = QLabel(t('theme') + ':')
        self.theme_combo = QComboBox()
        self.theme_combo.addItem(t('light_mode'), 'light')
        self.theme_combo.addItem(t('dark_mode'), 'dark')
        current_theme = settings_manager.get_theme()
        self.theme_combo.setCurrentIndex(0 if current_theme == 'light' else 1)
        layout.addRow(theme_label, self.theme_combo)
        
        save_btn = QPushButton(t('save'))
        save_btn.clicked.connect(self.save_settings)
        layout.addRow(save_btn)
        
        self.setLayout(layout)
    
    def save_settings(self):
        lang = self.language_combo.currentData()
        theme = self.theme_combo.currentData()
        
        settings_manager.set_language(lang)
        settings_manager.set_theme(theme)
        set_language(lang)
        set_theme(theme)
        
        self.app.setStyleSheet(get_stylesheet())
        self.parent_window.update_ui_language()
        
        QMessageBox.information(self, t('success'), t('operation_successful'))
        self.accept()

class ERPMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.app = None
        self.tabs = None
        self.init_ui()

    def init_ui(self):
        current_lang = settings_manager.get_language()
        set_language(current_lang)
        
        current_theme = settings_manager.get_theme()
        set_theme(current_theme)
        
        self.setWindowTitle(t('title'))
        self.setGeometry(100, 100, 1200, 700)
        
        self.create_menu_bar()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.tabs = QTabWidget()
        
        self.inventory_widget = InventoryWidget(self.db)
        self.sales_widget = SalesWidget(self.db)
        self.purchasing_widget = PurchasingWidget(self.db)
        self.accounting_widget = AccountingWidget(self.db)
        self.reports_widget = ReportsWidget(self.db)
        
        self.tabs.addTab(self.inventory_widget, t('inventory'))
        self.tabs.addTab(self.sales_widget, t('sales'))
        self.tabs.addTab(self.purchasing_widget, t('purchasing'))
        self.tabs.addTab(self.accounting_widget, t('accounting'))
        self.tabs.addTab(self.reports_widget, t('reports'))
        
        layout.addWidget(self.tabs)
        self.show()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        settings_menu = menubar.addMenu(t('settings'))
        settings_action = settings_menu.addAction(t('settings'))
        settings_action.triggered.connect(self.open_settings)
    
    def open_settings(self):
        dialog = SettingsDialog(self, QApplication.instance())
        dialog.exec_()
    
    def update_ui_language(self):
        self.setWindowTitle(t('title'))
        self.tabs.setTabText(0, t('inventory'))
        self.tabs.setTabText(1, t('sales'))
        self.tabs.setTabText(2, t('purchasing'))
        self.tabs.setTabText(3, t('accounting'))
        self.tabs.setTabText(4, t('reports'))
        
        self.inventory_widget.update_ui_language()
        self.sales_widget.update_ui_language()
        self.purchasing_widget.update_ui_language()
        self.accounting_widget.update_ui_language()
        self.reports_widget.update_ui_language()

    def closeEvent(self, event):
        self.db.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    current_theme = settings_manager.get_theme()
    set_theme(current_theme)
    app.setStyleSheet(get_stylesheet())
    
    window = ERPMainWindow()
    window.app = app
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
