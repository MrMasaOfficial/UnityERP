from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLabel, 
                             QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
                             QMessageBox, QHeaderView, QFormLayout, QTabWidget)
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
from translations import t

class InventoryWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_items()
        self.setup_alerts()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.items_tab = self.create_items_tab()
        self.stock_movement_tab = self.create_stock_movement_tab()
        self.alerts_tab = self.create_alerts_tab()
        
        self.tabs.addTab(self.items_tab, t('items'))
        self.tabs.addTab(self.stock_movement_tab, t('stock_movements'))
        self.tabs.addTab(self.alerts_tab, t('alerts'))
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_items_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(t('add'))
        add_btn.clicked.connect(self.add_item_dialog)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton(t('edit'))
        edit_btn.clicked.connect(self.edit_item_dialog)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton(t('delete'))
        delete_btn.clicked.connect(self.delete_item)
        button_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_items)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(8)
        self.items_table.setHorizontalHeaderLabels([
            t('code'), t('name'), t('category'), t('unit'), t('price'), t('quantity'), t('min_quantity'), t('status')
        ])
        self.items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.items_table)
        
        widget.setLayout(layout)
        return widget

    def create_stock_movement_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        self.movement_table = QTableWidget()
        self.movement_table.setColumnCount(6)
        self.movement_table.setHorizontalHeaderLabels([
            t('name'), t('movement_type'), t('quantity'), t('reference_doc'), t('notes'), t('date')
        ])
        self.movement_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_stock_movements)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        layout.addWidget(self.movement_table)
        
        widget.setLayout(layout)
        return widget

    def create_alerts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(4)
        self.alerts_table.setHorizontalHeaderLabels([
            t('code'), t('name'), t('quantity'), t('min_quantity')
        ])
        self.alerts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.alerts_table)
        
        widget.setLayout(layout)
        return widget

    def setup_alerts(self):
        self.alert_timer = QTimer()
        self.alert_timer.timeout.connect(self.check_alerts)
        self.alert_timer.start(60000)

    def check_alerts(self):
        query = '''SELECT i.id, i.code, i.name, i.quantity_on_hand, i.min_quantity
                   FROM items i WHERE i.quantity_on_hand <= i.min_quantity'''
        items = self.db.fetchall(query)
        
        self.alerts_table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.alerts_table.setItem(row, 0, QTableWidgetItem(item['code']))
            self.alerts_table.setItem(row, 1, QTableWidgetItem(item['name']))
            self.alerts_table.setItem(row, 2, QTableWidgetItem(str(item['quantity_on_hand'])))
            self.alerts_table.setItem(row, 3, QTableWidgetItem(str(item['min_quantity'])))

    def load_items(self):
        query = '''SELECT i.id, i.code, i.name, c.name as category, i.unit, 
                   i.price, i.quantity_on_hand, i.min_quantity
                   FROM items i JOIN categories c ON i.category_id = c.id'''
        items = self.db.fetchall(query)
        
        self.items_table.setRowCount(len(items))
        for row, item in enumerate(items):
            self.items_table.setItem(row, 0, QTableWidgetItem(item['code']))
            self.items_table.setItem(row, 1, QTableWidgetItem(item['name']))
            self.items_table.setItem(row, 2, QTableWidgetItem(item['category']))
            self.items_table.setItem(row, 3, QTableWidgetItem(item['unit']))
            self.items_table.setItem(row, 4, QTableWidgetItem(str(item['price'])))
            self.items_table.setItem(row, 5, QTableWidgetItem(str(item['quantity_on_hand'])))
            self.items_table.setItem(row, 6, QTableWidgetItem(str(item['min_quantity'])))
            
            status = t('warning') if item['quantity_on_hand'] <= item['min_quantity'] else t('good')
            self.items_table.setItem(row, 7, QTableWidgetItem(status))

    def load_stock_movements(self):
        query = '''SELECT i.code, sm.movement_type, sm.quantity, sm.reference_doc, 
                   sm.notes, sm.created_at FROM stock_movements sm 
                   JOIN items i ON sm.item_id = i.id
                   ORDER BY sm.created_at DESC LIMIT 100'''
        movements = self.db.fetchall(query)
        
        self.movement_table.setRowCount(len(movements))
        for row, movement in enumerate(movements):
            self.movement_table.setItem(row, 0, QTableWidgetItem(movement['code']))
            self.movement_table.setItem(row, 1, QTableWidgetItem(movement['movement_type']))
            self.movement_table.setItem(row, 2, QTableWidgetItem(str(movement['quantity'])))
            self.movement_table.setItem(row, 3, QTableWidgetItem(movement['reference_doc'] or ''))
            self.movement_table.setItem(row, 4, QTableWidgetItem(movement['notes'] or ''))
            self.movement_table.setItem(row, 5, QTableWidgetItem(movement['created_at']))

    def add_item_dialog(self):
        dialog = AddItemDialog(self.db)
        if dialog.exec_():
            self.load_items()

    def edit_item_dialog(self):
        row = self.items_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_item'))
            return
        
        code = self.items_table.item(row, 0).text()
        item = self.db.fetchone('SELECT * FROM items WHERE code = ?', (code,))
        dialog = AddItemDialog(self.db, item)
        if dialog.exec_():
            self.load_items()

    def delete_item(self):
        row = self.items_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_item'))
            return
        
        if QMessageBox.question(self, t('confirm'), t('confirm_delete')) == QMessageBox.Yes:
            code = self.items_table.item(row, 0).text()
            item = self.db.fetchone('SELECT id FROM items WHERE code = ?', (code,))
            self.db.delete('items', {'id': item['id']})
            self.load_items()
            QMessageBox.information(self, t('success'), t('operation_successful'))

    def update_ui_language(self):
        self.tabs.setTabText(0, t('items'))
        self.tabs.setTabText(1, t('stock_movements'))
        self.tabs.setTabText(2, t('alerts'))
        
        self.items_table.setHorizontalHeaderLabels([
            t('code'), t('name'), t('category'), t('unit'), t('price'), t('quantity'), t('min_quantity'), t('status')
        ])
        self.movement_table.setHorizontalHeaderLabels([
            t('name'), t('movement_type'), t('quantity'), t('reference_doc'), t('notes'), t('date')
        ])
        self.alerts_table.setHorizontalHeaderLabels([
            t('code'), t('name'), t('quantity'), t('min_quantity')
        ])
        
        self.load_items()
        self.load_stock_movements()
        self.check_alerts()

class AddItemDialog(QDialog):
    def __init__(self, db, item=None):
        super().__init__()
        self.db = db
        self.item = item
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(t('new_item') if not self.item else t('edit'))
        layout = QFormLayout()
        
        self.code_input = QLineEdit()
        self.name_input = QLineEdit()
        
        self.category_combo = QComboBox()
        categories = self.db.fetchall('SELECT * FROM categories')
        for cat in categories:
            self.category_combo.addItem(cat['name'], cat['id'])
        
        self.unit_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(999999)
        
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(999999)
        
        self.min_quantity_input = QSpinBox()
        self.min_quantity_input.setMaximum(999999)
        
        if self.item:
            self.code_input.setText(self.item['code'])
            self.code_input.setReadOnly(True)
            self.name_input.setText(self.item['name'])
            cat_idx = self.category_combo.findData(self.item['category_id'])
            self.category_combo.setCurrentIndex(cat_idx)
            self.unit_input.setText(self.item['unit'])
            self.price_input.setValue(self.item['price'])
            self.quantity_input.setValue(self.item['quantity_on_hand'])
            self.min_quantity_input.setValue(self.item['min_quantity'])
        
        layout.addRow(t('code') + ':', self.code_input)
        layout.addRow(t('name') + ':', self.name_input)
        layout.addRow(t('category') + ':', self.category_combo)
        layout.addRow(t('unit') + ':', self.unit_input)
        layout.addRow(t('price') + ':', self.price_input)
        layout.addRow(t('quantity') + ':', self.quantity_input)
        layout.addRow(t('min_quantity') + ':', self.min_quantity_input)
        
        save_btn = QPushButton(t('save'))
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)
        
        self.setLayout(layout)

    def save(self):
        try:
            if not self.code_input.text() or not self.name_input.text():
                QMessageBox.warning(self, t('warning'), t('required_field'))
                return
            
            category_id = self.category_combo.currentData()
            
            if self.item:
                self.db.update('items', {
                    'name': self.name_input.text(),
                    'category_id': category_id,
                    'unit': self.unit_input.text(),
                    'price': self.price_input.value(),
                    'quantity_on_hand': self.quantity_input.value(),
                    'min_quantity': self.min_quantity_input.value()
                }, {'id': self.item['id']})
            else:
                self.db.insert('items', {
                    'code': self.code_input.text(),
                    'name': self.name_input.text(),
                    'category_id': category_id,
                    'unit': self.unit_input.text(),
                    'price': self.price_input.value(),
                    'quantity_on_hand': self.quantity_input.value(),
                    'min_quantity': self.min_quantity_input.value()
                })
            
            QMessageBox.information(self, t('success'), t('operation_successful'))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')
