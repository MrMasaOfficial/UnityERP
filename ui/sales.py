from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLabel, 
                             QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox,
                             QMessageBox, QHeaderView, QFormLayout, QTabWidget,
                             QDateEdit, QTextEdit)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime, timedelta
from translations import t

class SalesWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_invoices()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_invoices_tab(), t('invoices'))
        self.tabs.addTab(self.create_customers_tab(), t('customers'))
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def update_ui_language(self):
        self.tabs.setTabText(0, t('invoices'))
        self.tabs.setTabText(1, t('customers'))

    def create_invoices_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(t('new_invoice'))
        add_btn.clicked.connect(self.new_invoice_dialog)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton(t('edit'))
        edit_btn.clicked.connect(self.edit_invoice_dialog)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton(t('delete'))
        delete_btn.clicked.connect(self.delete_invoice)
        button_layout.addWidget(delete_btn)
        
        print_btn = QPushButton(t('print'))
        print_btn.clicked.connect(self.print_invoice_pdf)
        button_layout.addWidget(print_btn)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_invoices)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.invoices_table = QTableWidget()
        self.invoices_table.setColumnCount(8)
        self.invoices_table.setHorizontalHeaderLabels([
            t('invoice_number'), t('customer'), t('date'), t('subtotal'), t('discount'), t('tax'), t('total'), t('status')
        ])
        self.invoices_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.invoices_table)
        
        widget.setLayout(layout)
        return widget

    def create_customers_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(t('new_customer'))
        add_btn.clicked.connect(self.add_customer_dialog)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton(t('edit'))
        edit_btn.clicked.connect(self.edit_customer_dialog)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton(t('delete'))
        delete_btn.clicked.connect(self.delete_customer)
        button_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_customers)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(7)
        self.customers_table.setHorizontalHeaderLabels([
            t('name'), t('contact'), t('phone'), t('email'), t('address'), t('city'), t('balance')
        ])
        self.customers_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.customers_table)
        
        widget.setLayout(layout)
        return widget

    def load_invoices(self):
        query = '''SELECT inv.id, inv.invoice_number, c.name, inv.invoice_date,
                   inv.subtotal, inv.discount, inv.tax, inv.total_amount, inv.status
                   FROM invoices inv JOIN customers c ON inv.customer_id = c.id
                   ORDER BY inv.invoice_date DESC'''
        invoices = self.db.fetchall(query)
        
        self.invoices_table.setRowCount(len(invoices))
        for row, inv in enumerate(invoices):
            self.invoices_table.setItem(row, 0, QTableWidgetItem(inv['invoice_number']))
            self.invoices_table.setItem(row, 1, QTableWidgetItem(inv['name']))
            self.invoices_table.setItem(row, 2, QTableWidgetItem(inv['invoice_date']))
            self.invoices_table.setItem(row, 3, QTableWidgetItem(str(inv['subtotal'])))
            self.invoices_table.setItem(row, 4, QTableWidgetItem(str(inv['discount'])))
            self.invoices_table.setItem(row, 5, QTableWidgetItem(str(inv['tax'])))
            self.invoices_table.setItem(row, 6, QTableWidgetItem(str(inv['total_amount'])))
            self.invoices_table.setItem(row, 7, QTableWidgetItem(inv['status']))

    def load_customers(self):
        query = 'SELECT * FROM customers'
        customers = self.db.fetchall(query)
        
        self.customers_table.setRowCount(len(customers))
        for row, cust in enumerate(customers):
            self.customers_table.setItem(row, 0, QTableWidgetItem(cust['name']))
            self.customers_table.setItem(row, 1, QTableWidgetItem(cust['contact_person'] or ''))
            self.customers_table.setItem(row, 2, QTableWidgetItem(cust['phone'] or ''))
            self.customers_table.setItem(row, 3, QTableWidgetItem(cust['email'] or ''))
            self.customers_table.setItem(row, 4, QTableWidgetItem(cust['address'] or ''))
            self.customers_table.setItem(row, 5, QTableWidgetItem(cust['city'] or ''))
            self.customers_table.setItem(row, 6, QTableWidgetItem(str(cust['balance'])))

    def new_invoice_dialog(self):
        dialog = InvoiceDialog(self.db)
        if dialog.exec_():
            self.load_invoices()

    def edit_invoice_dialog(self):
        row = self.invoices_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_invoice'))
            return
        
        inv_number = self.invoices_table.item(row, 0).text()
        invoice = self.db.fetchone('SELECT * FROM invoices WHERE invoice_number = ?', (inv_number,))
        
        if invoice['status'] == 'Completed':
            QMessageBox.warning(self, t('warning'), t('complete_invoice'))
            return
        
        dialog = InvoiceDialog(self.db, invoice)
        if dialog.exec_():
            self.load_invoices()

    def delete_invoice(self):
        row = self.invoices_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_invoice'))
            return
        
        if QMessageBox.question(self, t('confirm'), t('confirm_delete')) == QMessageBox.Yes:
            inv_number = self.invoices_table.item(row, 0).text()
            invoice = self.db.fetchone('SELECT id FROM invoices WHERE invoice_number = ?', (inv_number,))
            self.db.delete('invoice_items', {'invoice_id': invoice['id']})
            self.db.delete('invoices', {'id': invoice['id']})
            self.load_invoices()
            QMessageBox.information(self, t('success'), t('operation_successful'))

    def print_invoice_pdf(self):
        row = self.invoices_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_invoice'))
            return
        
        inv_number = self.invoices_table.item(row, 0).text()
        from utils.pdf_generator import generate_invoice_pdf
        try:
            generate_invoice_pdf(self.db, inv_number)
            QMessageBox.information(self, t('success'), t('pdf_saved'))
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')

    def add_customer_dialog(self):
        dialog = CustomerDialog(self.db)
        if dialog.exec_():
            self.load_customers()

    def edit_customer_dialog(self):
        row = self.customers_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_customer'))
            return
        
        name = self.customers_table.item(row, 0).text()
        customer = self.db.fetchone('SELECT * FROM customers WHERE name = ?', (name,))
        dialog = CustomerDialog(self.db, customer)
        if dialog.exec_():
            self.load_customers()

    def delete_customer(self):
        row = self.customers_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_customer'))
            return
        
        if QMessageBox.question(self, t('confirm'), t('confirm_delete')) == QMessageBox.Yes:
            name = self.customers_table.item(row, 0).text()
            customer = self.db.fetchone('SELECT id FROM customers WHERE name = ?', (name,))
            self.db.delete('customers', {'id': customer['id']})
            self.load_customers()
            QMessageBox.information(self, t('success'), t('operation_successful'))

class InvoiceDialog(QDialog):
    def __init__(self, db, invoice=None):
        super().__init__()
        self.db = db
        self.invoice = invoice
        self.invoice_items = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(t('new_invoice') if not self.invoice else t('edit') + ' ' + t('invoices').lower())
        self.setGeometry(100, 100, 900, 600)
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.inv_number_input = QLineEdit()
        self.inv_number_input.setReadOnly(True)
        if not self.invoice:
            self.inv_number_input.setText(self.generate_invoice_number())
        else:
            self.inv_number_input.setText(self.invoice['invoice_number'])
        
        self.customer_combo = QComboBox()
        customers = self.db.fetchall('SELECT * FROM customers')
        for cust in customers:
            self.customer_combo.addItem(cust['name'], cust['id'])
        
        self.invoice_date_input = QDateEdit()
        self.invoice_date_input.setDate(QDate.currentDate())
        
        self.due_date_input = QDateEdit()
        self.due_date_input.setDate(QDate.currentDate().addDays(30))
        
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setMaximum(999999)
        self.discount_input.valueChanged.connect(self.calculate_total)
        
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setMaximum(100)
        self.tax_input.setSuffix('%')
        self.tax_input.setValue(15)
        self.tax_input.valueChanged.connect(self.calculate_total)
        
        if self.invoice:
            self.customer_combo.setCurrentText(
                self.db.fetchone('SELECT name FROM customers WHERE id = ?', 
                (self.invoice['customer_id'],))['name']
            )
            self.discount_input.setValue(self.invoice['discount'])
            self.tax_input.setValue((self.invoice['tax'] / self.invoice['subtotal'] * 100) if self.invoice['subtotal'] > 0 else 15)
        
        form_layout.addRow(t('invoice_number') + ':', self.inv_number_input)
        form_layout.addRow(t('customer') + ':', self.customer_combo)
        form_layout.addRow(t('date') + ':', self.invoice_date_input)
        form_layout.addRow(t('due_date') + ':', self.due_date_input)
        form_layout.addRow(t('discount') + ':', self.discount_input)
        form_layout.addRow(t('tax') + ':', self.tax_input)
        
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
        
        add_item_btn = QPushButton(t('add_product'))
        add_item_btn.clicked.connect(self.add_item_to_invoice)
        
        item_layout.addWidget(self.item_combo)
        item_layout.addWidget(QLabel(t('quantity') + ':'))
        item_layout.addWidget(self.item_qty)
        item_layout.addWidget(add_item_btn)
        
        layout.addLayout(item_layout)
        
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        total_layout.addWidget(QLabel(t('subtotal') + ':'))
        self.subtotal_label = QLineEdit()
        self.subtotal_label.setReadOnly(True)
        total_layout.addWidget(self.subtotal_label)
        
        total_layout.addWidget(QLabel(t('final_total') + ':'))
        self.total_label = QLineEdit()
        self.total_label.setReadOnly(True)
        total_layout.addWidget(self.total_label)
        
        layout.addLayout(total_layout)
        
        save_btn = QPushButton(t('save'))
        save_btn.clicked.connect(self.save_invoice)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
        
        if self.invoice:
            self.load_invoice_items()

    def generate_invoice_number(self):
        last_inv = self.db.fetchone('SELECT invoice_number FROM invoices ORDER BY id DESC LIMIT 1')
        if last_inv:
            num = int(last_inv['invoice_number'].split('-')[1]) + 1
        else:
            num = 1001
        return f"INV-{num}"

    def add_item_to_invoice(self):
        item_id = self.item_combo.currentData()
        qty = self.item_qty.value()
        
        item = self.db.fetchone('SELECT * FROM items WHERE id = ?', (item_id,))
        
        if qty > item['quantity_on_hand']:
            QMessageBox.warning(self, t('warning'), t('invalid_quantity'))
            return
        
        total = item['price'] * qty
        self.invoice_items.append({
            'item_id': item_id,
            'quantity': qty,
            'unit_price': item['price'],
            'total_price': total
        })
        
        self.refresh_invoice_items_table()
        self.calculate_total()

    def refresh_invoice_items_table(self):
        self.items_table.setRowCount(len(self.invoice_items))
        for row, item_data in enumerate(self.invoice_items):
            item = self.db.fetchone('SELECT name FROM items WHERE id = ?', (item_data['item_id'],))
            self.items_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.items_table.setItem(row, 1, QTableWidgetItem(str(item_data['quantity'])))
            self.items_table.setItem(row, 2, QTableWidgetItem(str(item_data['unit_price'])))
            self.items_table.setItem(row, 3, QTableWidgetItem(str(item_data['total_price'])))
            
            remove_btn = QPushButton(t('delete'))
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_item(r))
            self.items_table.setCellWidget(row, 4, remove_btn)

    def remove_item(self, row):
        self.invoice_items.pop(row)
        self.refresh_invoice_items_table()
        self.calculate_total()

    def calculate_total(self):
        subtotal = sum(item['total_price'] for item in self.invoice_items)
        discount = self.discount_input.value()
        tax_percent = self.tax_input.value()
        
        after_discount = subtotal - discount
        tax_amount = after_discount * (tax_percent / 100)
        total = after_discount + tax_amount
        
        self.subtotal_label.setText(str(subtotal))
        self.total_label.setText(str(total))

    def load_invoice_items(self):
        items = self.db.fetchall('SELECT * FROM invoice_items WHERE invoice_id = ?', (self.invoice['id'],))
        for item in items:
            self.invoice_items.append({
                'item_id': item['item_id'],
                'quantity': item['quantity'],
                'unit_price': item['unit_price'],
                'total_price': item['total_price']
            })
        self.refresh_invoice_items_table()

    def save_invoice(self):
        try:
            if not self.invoice_items:
                QMessageBox.warning(self, t('warning'), t('add_items_invoice'))
                return
            
            subtotal = sum(item['total_price'] for item in self.invoice_items)
            discount = self.discount_input.value()
            tax_percent = self.tax_input.value()
            after_discount = subtotal - discount
            tax_amount = after_discount * (tax_percent / 100)
            total = after_discount + tax_amount
            
            customer_id = self.customer_combo.currentData()
            
            if self.invoice:
                self.db.update('invoices', {
                    'customer_id': customer_id,
                    'invoice_date': self.invoice_date_input.date().toString('yyyy-MM-dd'),
                    'due_date': self.due_date_input.date().toString('yyyy-MM-dd'),
                    'subtotal': subtotal,
                    'discount': discount,
                    'tax': tax_amount,
                    'total_amount': total
                }, {'id': self.invoice['id']})
                
                self.db.delete('invoice_items', {'invoice_id': self.invoice['id']})
            else:
                inv_id = self.db.insert('invoices', {
                    'invoice_number': self.inv_number_input.text(),
                    'customer_id': customer_id,
                    'invoice_date': self.invoice_date_input.date().toString('yyyy-MM-dd'),
                    'due_date': self.due_date_input.date().toString('yyyy-MM-dd'),
                    'subtotal': subtotal,
                    'discount': discount,
                    'tax': tax_amount,
                    'total_amount': total,
                    'status': 'Pending'
                })
            
            inv_id = inv_id if not self.invoice else self.invoice['id']
            for item_data in self.invoice_items:
                self.db.insert('invoice_items', {
                    'invoice_id': inv_id,
                    'item_id': item_data['item_id'],
                    'quantity': item_data['quantity'],
                    'unit_price': item_data['unit_price'],
                    'total_price': item_data['total_price']
                })
                
                item = self.db.fetchone('SELECT quantity_on_hand FROM items WHERE id = ?', (item_data['item_id'],))
                new_qty = item['quantity_on_hand'] - item_data['quantity']
                self.db.update('items', {'quantity_on_hand': new_qty}, {'id': item_data['item_id']})
                
                self.db.insert('stock_movements', {
                    'item_id': item_data['item_id'],
                    'movement_type': 'Sale',
                    'quantity': item_data['quantity'],
                    'reference_doc': self.inv_number_input.text()
                })
            
            QMessageBox.information(self, t('success'), t('invoice_saved'))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')

class CustomerDialog(QDialog):
    def __init__(self, db, customer=None):
        super().__init__()
        self.db = db
        self.customer = customer
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(t('new_customer') if not self.customer else t('edit') + ' ' + t('customer'))
        layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        self.city_input = QLineEdit()
        
        if self.customer:
            self.name_input.setText(self.customer['name'])
            self.name_input.setReadOnly(True)
            self.contact_input.setText(self.customer['contact_person'] or '')
            self.phone_input.setText(self.customer['phone'] or '')
            self.email_input.setText(self.customer['email'] or '')
            self.address_input.setText(self.customer['address'] or '')
            self.city_input.setText(self.customer['city'] or '')
        
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
            
            if self.customer:
                self.db.update('customers', {
                    'contact_person': self.contact_input.text(),
                    'phone': self.phone_input.text(),
                    'email': self.email_input.text(),
                    'address': self.address_input.text(),
                    'city': self.city_input.text()
                }, {'id': self.customer['id']})
            else:
                self.db.insert('customers', {
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
