from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLabel, 
                             QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
                             QMessageBox, QHeaderView, QFormLayout, QTabWidget,
                             QDateEdit)
from PyQt5.QtCore import Qt, QDate
from translations import t

class PurchasingWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_purchase_orders()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_po_tab(), t('po'))
        self.tabs.addTab(self.create_suppliers_tab(), t('suppliers'))
        self.tabs.addTab(self.create_invoices_tab(), t('supplier_invoices'))
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def update_ui_language(self):
        self.tabs.setTabText(0, t('po'))
        self.tabs.setTabText(1, t('suppliers'))
        self.tabs.setTabText(2, t('supplier_invoices'))

    def create_po_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(t('new_po'))
        add_btn.clicked.connect(self.new_po_dialog)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton(t('edit'))
        edit_btn.clicked.connect(self.edit_po_dialog)
        button_layout.addWidget(edit_btn)
        
        approve_btn = QPushButton(t('approve'))
        approve_btn.clicked.connect(self.approve_po)
        button_layout.addWidget(approve_btn)
        
        receive_btn = QPushButton(t('receive'))
        receive_btn.clicked.connect(self.receive_po)
        button_layout.addWidget(receive_btn)
        
        delete_btn = QPushButton(t('delete'))
        delete_btn.clicked.connect(self.delete_po)
        button_layout.addWidget(delete_btn)
        
        print_btn = QPushButton(t('print'))
        print_btn.clicked.connect(self.print_po_pdf)
        button_layout.addWidget(print_btn)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_purchase_orders)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.po_table = QTableWidget()
        self.po_table.setColumnCount(7)
        self.po_table.setHorizontalHeaderLabels([
            t('po_number'), t('supplier'), t('date'), t('total'), t('status'), t('reference_doc'), t('notes')
        ])
        self.po_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.po_table)
        
        widget.setLayout(layout)
        return widget

    def create_suppliers_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(t('new_supplier'))
        add_btn.clicked.connect(self.add_supplier_dialog)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton(t('edit'))
        edit_btn.clicked.connect(self.edit_supplier_dialog)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton(t('delete'))
        delete_btn.clicked.connect(self.delete_supplier)
        button_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_suppliers)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.suppliers_table = QTableWidget()
        self.suppliers_table.setColumnCount(7)
        self.suppliers_table.setHorizontalHeaderLabels([
            t('name'), t('contact'), t('phone'), t('email'), t('address'), t('city'), t('balance')
        ])
        self.suppliers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.suppliers_table)
        
        widget.setLayout(layout)
        return widget

    def create_invoices_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(5)
        self.invoices_table.setHorizontalHeaderLabels([
            t('supplier'), t('amount'), t('date'), t('reference_doc'), t('notes')
        ])
        self.invoices_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.invoices_table)
        
        widget.setLayout(layout)
        return widget

    def load_purchase_orders(self):
        query = '''SELECT po.id, po.po_number, s.name, po.order_date, po.total_amount, 
                   po.status, po.notes FROM purchase_orders po 
                   JOIN suppliers s ON po.supplier_id = s.id
                   ORDER BY po.order_date DESC'''
        pos = self.db.fetchall(query)
        
        self.po_table.setRowCount(len(pos))
        for row, po in enumerate(pos):
            self.po_table.setItem(row, 0, QTableWidgetItem(po['po_number']))
            self.po_table.setItem(row, 1, QTableWidgetItem(po['name']))
            self.po_table.setItem(row, 2, QTableWidgetItem(po['order_date']))
            self.po_table.setItem(row, 3, QTableWidgetItem(str(po['total_amount'])))
            self.po_table.setItem(row, 4, QTableWidgetItem(po['status']))
            self.po_table.setItem(row, 5, QTableWidgetItem(t('view') if po['id'] else ''))
            self.po_table.setItem(row, 6, QTableWidgetItem(po['notes'] or ''))

    def load_suppliers(self):
        query = 'SELECT * FROM suppliers'
        suppliers = self.db.fetchall(query)
        
        self.suppliers_table.setRowCount(len(suppliers))
        for row, supp in enumerate(suppliers):
            self.suppliers_table.setItem(row, 0, QTableWidgetItem(supp['name']))
            self.suppliers_table.setItem(row, 1, QTableWidgetItem(supp['contact_person'] or ''))
            self.suppliers_table.setItem(row, 2, QTableWidgetItem(supp['phone'] or ''))
            self.suppliers_table.setItem(row, 3, QTableWidgetItem(supp['email'] or ''))
            self.suppliers_table.setItem(row, 4, QTableWidgetItem(supp['address'] or ''))
            self.suppliers_table.setItem(row, 5, QTableWidgetItem(supp['city'] or ''))
            self.suppliers_table.setItem(row, 6, QTableWidgetItem(str(supp['balance'])))

    def new_po_dialog(self):
        dialog = PODialog(self.db)
        if dialog.exec_():
            self.load_purchase_orders()

    def edit_po_dialog(self):
        row = self.po_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_po'))
            return
        
        po_number = self.po_table.item(row, 0).text()
        po = self.db.fetchone('SELECT * FROM purchase_orders WHERE po_number = ?', (po_number,))
        
        if po['status'] == 'Received':
            QMessageBox.warning(self, t('warning'), t('received_po'))
            return
        
        dialog = PODialog(self.db, po)
        if dialog.exec_():
            self.load_purchase_orders()

    def approve_po(self):
        row = self.po_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_po'))
            return
        
        po_number = self.po_table.item(row, 0).text()
        po = self.db.fetchone('SELECT * FROM purchase_orders WHERE po_number = ?', (po_number,))
        
        self.db.update('purchase_orders', {'status': 'Approved'}, {'id': po['id']})
        self.load_purchase_orders()
        QMessageBox.information(self, t('success'), t('po_approved'))

    def receive_po(self):
        row = self.po_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_po'))
            return
        
        po_number = self.po_table.item(row, 0).text()
        po = self.db.fetchone('SELECT * FROM purchase_orders WHERE po_number = ?', (po_number,))
        po_items = self.db.fetchall('SELECT * FROM purchase_items WHERE purchase_order_id = ?', (po['id'],))
        
        for item in po_items:
            current_item = self.db.fetchone('SELECT quantity_on_hand FROM items WHERE id = ?', (item['item_id'],))
            new_qty = current_item['quantity_on_hand'] + item['quantity']
            self.db.update('items', {'quantity_on_hand': new_qty}, {'id': item['item_id']})
            
            self.db.insert('stock_movements', {
                'item_id': item['item_id'],
                'movement_type': 'Purchase',
                'quantity': item['quantity'],
                'reference_doc': po_number
            })
        
        self.db.update('purchase_orders', {'status': 'Received'}, {'id': po['id']})
        self.load_purchase_orders()
        QMessageBox.information(self, t('success'), t('po_received'))

    def delete_po(self):
        row = self.po_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_po'))
            return
        
        if QMessageBox.question(self, t('confirm'), t('confirm_delete')) == QMessageBox.Yes:
            po_number = self.po_table.item(row, 0).text()
            po = self.db.fetchone('SELECT id FROM purchase_orders WHERE po_number = ?', (po_number,))
            self.db.delete('purchase_items', {'purchase_order_id': po['id']})
            self.db.delete('purchase_orders', {'id': po['id']})
            self.load_purchase_orders()
            QMessageBox.information(self, t('success'), t('operation_successful'))

    def print_po_pdf(self):
        row = self.po_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_po'))
            return
        
        po_number = self.po_table.item(row, 0).text()
        from utils.pdf_generator import generate_po_pdf
        try:
            generate_po_pdf(self.db, po_number)
            QMessageBox.information(self, t('success'), t('pdf_saved'))
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')

    def add_supplier_dialog(self):
        dialog = SupplierDialog(self.db)
        if dialog.exec_():
            self.load_suppliers()

    def edit_supplier_dialog(self):
        row = self.suppliers_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_supplier'))
            return
        
        name = self.suppliers_table.item(row, 0).text()
        supplier = self.db.fetchone('SELECT * FROM suppliers WHERE name = ?', (name,))
        dialog = SupplierDialog(self.db, supplier)
        if dialog.exec_():
            self.load_suppliers()

    def delete_supplier(self):
        row = self.suppliers_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_supplier'))
            return
        
        if QMessageBox.question(self, t('confirm'), t('confirm_delete')) == QMessageBox.Yes:
            name = self.suppliers_table.item(row, 0).text()
            supplier = self.db.fetchone('SELECT id FROM suppliers WHERE name = ?', (name,))
            self.db.delete('suppliers', {'id': supplier['id']})
            self.load_suppliers()
            QMessageBox.information(self, t('success'), t('operation_successful'))

class PODialog(QDialog):
    def __init__(self, db, po=None):
        super().__init__()
        self.db = db
        self.po = po
        self.po_items = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(t('new_po') if not self.po else t('edit') + ' ' + t('po').lower())
        self.setGeometry(100, 100, 900, 600)
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.po_number_input = QLineEdit()
        self.po_number_input.setReadOnly(True)
        if not self.po:
            self.po_number_input.setText(self.generate_po_number())
        else:
            self.po_number_input.setText(self.po['po_number'])
        
        self.supplier_combo = QComboBox()
        suppliers = self.db.fetchall('SELECT * FROM suppliers')
        for supp in suppliers:
            self.supplier_combo.addItem(supp['name'], supp['id'])
        
        self.order_date_input = QDateEdit()
        self.order_date_input.setDate(QDate.currentDate())
        
        self.notes_input = QLineEdit()
        
        if self.po:
            self.supplier_combo.setCurrentText(
                self.db.fetchone('SELECT name FROM suppliers WHERE id = ?', 
                (self.po['supplier_id'],))['name']
            )
            self.notes_input.setText(self.po['notes'] or '')
        
        form_layout.addRow(t('po_number') + ':', self.po_number_input)
        form_layout.addRow(t('supplier') + ':', self.supplier_combo)
        form_layout.addRow(t('date') + ':', self.order_date_input)
        form_layout.addRow(t('notes') + ':', self.notes_input)
        
        layout.addLayout(form_layout)
        
        self.items_table = QTableWidget()
        self.items_table.setColumnCount(5)
        self.items_table.setHorizontalHeaderLabels([t('items'), t('quantity'), t('price'), t('total'), ''])
        layout.addWidget(self.items_table)
        
        item_layout = QHBoxLayout()
        self.item_combo = QComboBox()
        items = self.db.fetchall('SELECT * FROM items')
        for item in items:
            self.item_combo.addItem(f"{item['name']} ({item['code']})", item['id'])
        
        self.item_qty = QSpinBox()
        self.item_qty.setMinimum(1)
        
        self.item_price = QDoubleSpinBox()
        self.item_price.setMaximum(999999)
        
        add_item_btn = QPushButton(t('add_product'))
        add_item_btn.clicked.connect(self.add_item_to_po)
        
        item_layout.addWidget(self.item_combo)
        item_layout.addWidget(QLabel(t('quantity') + ':'))
        item_layout.addWidget(self.item_qty)
        item_layout.addWidget(QLabel(t('price') + ':'))
        item_layout.addWidget(self.item_price)
        item_layout.addWidget(add_item_btn)
        
        layout.addLayout(item_layout)
        
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(QLabel(t('total') + ':'))
        self.total_label = QLineEdit()
        self.total_label.setReadOnly(True)
        total_layout.addWidget(self.total_label)
        layout.addLayout(total_layout)
        
        save_btn = QPushButton(t('save'))
        save_btn.clicked.connect(self.save_po)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
        
        if self.po:
            self.load_po_items()

    def generate_po_number(self):
        last_po = self.db.fetchone('SELECT po_number FROM purchase_orders ORDER BY id DESC LIMIT 1')
        if last_po:
            num = int(last_po['po_number'].split('-')[1]) + 1
        else:
            num = 5001
        return f"PO-{num}"

    def add_item_to_po(self):
        item_id = self.item_combo.currentData()
        qty = self.item_qty.value()
        price = self.item_price.value()
        
        if price <= 0:
            QMessageBox.warning(self, t('warning'), t('invalid_price'))
            return
        
        total = price * qty
        self.po_items.append({
            'item_id': item_id,
            'quantity': qty,
            'unit_price': price,
            'total_price': total
        })
        
        self.refresh_po_items_table()
        self.calculate_total()

    def refresh_po_items_table(self):
        self.items_table.setRowCount(len(self.po_items))
        for row, item_data in enumerate(self.po_items):
            item = self.db.fetchone('SELECT name FROM items WHERE id = ?', (item_data['item_id'],))
            self.items_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.items_table.setItem(row, 1, QTableWidgetItem(str(item_data['quantity'])))
            self.items_table.setItem(row, 2, QTableWidgetItem(str(item_data['unit_price'])))
            self.items_table.setItem(row, 3, QTableWidgetItem(str(item_data['total_price'])))
            
            remove_btn = QPushButton(t('delete'))
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_item(r))
            self.items_table.setCellWidget(row, 4, remove_btn)

    def remove_item(self, row):
        self.po_items.pop(row)
        self.refresh_po_items_table()
        self.calculate_total()

    def calculate_total(self):
        total = sum(item['total_price'] for item in self.po_items)
        self.total_label.setText(str(total))

    def load_po_items(self):
        items = self.db.fetchall('SELECT * FROM purchase_items WHERE purchase_order_id = ?', (self.po['id'],))
        for item in items:
            self.po_items.append({
                'item_id': item['item_id'],
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total_price': item['total_price']
            })
        self.refresh_po_items_table()

    def save_po(self):
        try:
            if not self.po_items:
                QMessageBox.warning(self, t('warning'), t('add_items_invoice'))
                return
            
            total = sum(item['total_price'] for item in self.po_items)
            supplier_id = self.supplier_combo.currentData()
            
            if self.po:
                self.db.update('purchase_orders', {
                    'supplier_id': supplier_id,
                    'order_date': self.order_date_input.date().toString('yyyy-MM-dd'),
                    'total_amount': total,
                    'notes': self.notes_input.text()
                }, {'id': self.po['id']})
                
                self.db.delete('purchase_items', {'purchase_order_id': self.po['id']})
            else:
                po_id = self.db.insert('purchase_orders', {
                    'po_number': self.po_number_input.text(),
                    'supplier_id': supplier_id,
                    'order_date': self.order_date_input.date().toString('yyyy-MM-dd'),
                    'total_amount': total,
                    'status': 'Pending',
                    'notes': self.notes_input.text()
                })
            
            po_id = po_id if not self.po else self.po['id']
            for item_data in self.po_items:
                self.db.insert('purchase_items', {
                    'purchase_order_id': po_id,
                    'item_id': item_data['item_id'],
                    'quantity': item_data['quantity'],
                    'unit_price': item_data['unit_price'],
                    'total_price': item_data['total_price']
                })
            
            QMessageBox.information(self, t('success'), t('po_saved'))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')

class SupplierDialog(QDialog):
    def __init__(self, db, supplier=None):
        super().__init__()
        self.db = db
        self.supplier = supplier
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(t('new_supplier') if not self.supplier else t('edit') + ' ' + t('supplier'))
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        self.city_input = QLineEdit()
        
        if self.supplier:
            self.name_input.setText(self.supplier['name'])
            self.name_input.setReadOnly(True)
            self.contact_input.setText(self.supplier['contact_person'] or '')
            self.phone_input.setText(self.supplier['phone'] or '')
            self.email_input.setText(self.supplier['email'] or '')
            self.address_input.setText(self.supplier['address'] or '')
            self.city_input.setText(self.supplier['city'] or '')
        
        layout.addRow(t('name') + ':', self.name_input)
        layout.addRow(t('contact') + ':', self.contact_input)
        layout.addRow(t('phone') + ':', self.phone_input)
        layout.addRow(t('email') + ':', self.email_input)
        layout.addRow(t('address') + ':', self.address_input)
        layout.addRow(t('city') + ':', self.city_input)
        
        save_btn = QPushButton(t('save'))
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)
        
        self.setLayout(layout)

    def save(self):
        try:
            if not self.name_input.text():
                QMessageBox.warning(self, t('warning'), t('required_field'))
                return
            
            if self.supplier:
                self.db.update('suppliers', {
                    'contact_person': self.contact_input.text(),
                    'phone': self.phone_input.text(),
                    'email': self.email_input.text(),
                    'address': self.address_input.text(),
                    'city': self.city_input.text()
                }, {'id': self.supplier['id']})
            else:
                self.db.insert('suppliers', {
                    'name': self.name_input.text(),
                    'contact_person': self.contact_input.text(),
                    'phone': self.phone_input.text(),
                    'email': self.email_input.text(),
                    'address': self.address_input.text(),
                    'city': self.city_input.text(),
                    'balance': 0
                })
            
            QMessageBox.information(self, t('success'), t('operation_successful'))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')
