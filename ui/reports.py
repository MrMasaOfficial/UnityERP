from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QLabel, QLineEdit,
                             QComboBox, QMessageBox, QHeaderView, QFormLayout,
                             QDateEdit, QTabWidget)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime, timedelta
from translations import t

class ReportsWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_sales_report_tab(), t('sales'))
        self.tabs.addTab(self.create_purchase_report_tab(), t('purchasing'))
        self.tabs.addTab(self.create_inventory_report_tab(), t('inventory'))
        self.tabs.addTab(self.create_accounting_report_tab(), t('accounting'))
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def update_ui_language(self):
        self.tabs.setTabText(0, t('sales'))
        self.tabs.setTabText(1, t('purchasing'))
        self.tabs.setTabText(2, t('inventory'))
        self.tabs.setTabText(3, t('accounting'))

    def create_sales_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        filter_layout = QFormLayout()
        
        self.sales_from_date = QDateEdit()
        self.sales_from_date.setDate(QDate.currentDate().addMonths(-1))
        self.sales_to_date = QDateEdit()
        self.sales_to_date.setDate(QDate.currentDate())
        
        self.sales_customer_combo = QComboBox()
        self.sales_customer_combo.addItem(t('all'), None)
        customers = self.db.fetchall('SELECT * FROM customers')
        for cust in customers:
            self.sales_customer_combo.addItem(cust['name'], cust['id'])
        
        filter_layout.addRow(t('from_date') + ':', self.sales_from_date)
        filter_layout.addRow(t('to_date') + ':', self.sales_to_date)
        filter_layout.addRow(t('customer') + ':', self.sales_customer_combo)
        
        layout.addLayout(filter_layout)
        
        button_layout = QHBoxLayout()
        
        generate_btn = QPushButton(t('view'))
        generate_btn.clicked.connect(self.load_sales_report)
        button_layout.addWidget(generate_btn)
        
        export_btn = QPushButton(t('export'))
        export_btn.clicked.connect(self.export_sales_pdf)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        self.sales_report_table = QTableWidget()
        self.sales_report_table.setColumnCount(7)
        self.sales_report_table.setHorizontalHeaderLabels([
            t('invoice_number'), t('customer'), t('date'), t('items'), t('quantity'), t('price'), t('total')
        ])
        self.sales_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.sales_report_table)
        
        widget.setLayout(layout)
        return widget

    def create_purchase_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        filter_layout = QFormLayout()
        
        self.purchase_from_date = QDateEdit()
        self.purchase_from_date.setDate(QDate.currentDate().addMonths(-1))
        self.purchase_to_date = QDateEdit()
        self.purchase_to_date.setDate(QDate.currentDate())
        
        self.purchase_supplier_combo = QComboBox()
        self.purchase_supplier_combo.addItem(t('all'), None)
        suppliers = self.db.fetchall('SELECT * FROM suppliers')
        for supp in suppliers:
            self.purchase_supplier_combo.addItem(supp['name'], supp['id'])
        
        filter_layout.addRow(t('from_date') + ':', self.purchase_from_date)
        filter_layout.addRow(t('to_date') + ':', self.purchase_to_date)
        filter_layout.addRow(t('supplier') + ':', self.purchase_supplier_combo)
        
        layout.addLayout(filter_layout)
        
        button_layout = QHBoxLayout()
        
        generate_btn = QPushButton(t('view'))
        generate_btn.clicked.connect(self.load_purchase_report)
        button_layout.addWidget(generate_btn)
        
        export_btn = QPushButton(t('export'))
        export_btn.clicked.connect(self.export_purchase_pdf)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        self.purchase_report_table = QTableWidget()
        self.purchase_report_table.setColumnCount(7)
        self.purchase_report_table.setHorizontalHeaderLabels([
            t('po_number'), t('supplier'), t('date'), t('items'), t('quantity'), t('price'), t('total')
        ])
        self.purchase_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.purchase_report_table)
        
        widget.setLayout(layout)
        return widget

    def create_inventory_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        filter_layout = QFormLayout()
        
        self.inventory_category_combo = QComboBox()
        self.inventory_category_combo.addItem(t('all'), None)
        categories = self.db.fetchall('SELECT * FROM categories')
        for cat in categories:
            self.inventory_category_combo.addItem(cat['name'], cat['id'])
        
        filter_layout.addRow(t('category') + ':', self.inventory_category_combo)
        
        layout.addLayout(filter_layout)
        
        button_layout = QHBoxLayout()
        
        generate_btn = QPushButton(t('view'))
        generate_btn.clicked.connect(self.load_inventory_report)
        button_layout.addWidget(generate_btn)
        
        export_btn = QPushButton(t('export'))
        export_btn.clicked.connect(self.export_inventory_pdf)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        self.inventory_report_table = QTableWidget()
        self.inventory_report_table.setColumnCount(7)
        self.inventory_report_table.setHorizontalHeaderLabels([
            t('code'), t('items'), t('category'), t('unit'), t('quantity'), t('price'), t('total')
        ])
        self.inventory_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.inventory_report_table)
        
        widget.setLayout(layout)
        return widget

    def create_accounting_report_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        pl_btn = QPushButton(t('income_statement'))
        pl_btn.clicked.connect(self.generate_pl_report)
        button_layout.addWidget(pl_btn)
        
        balance_btn = QPushButton(t('balance_sheet'))
        balance_btn.clicked.connect(self.generate_balance_report)
        button_layout.addWidget(balance_btn)
        
        trial_btn = QPushButton(t('trial_balance'))
        trial_btn.clicked.connect(self.generate_trial_balance)
        button_layout.addWidget(trial_btn)
        
        export_btn = QPushButton(t('export'))
        export_btn.clicked.connect(self.export_accounting_pdf)
        button_layout.addWidget(export_btn)
        
        layout.addLayout(button_layout)
        
        self.accounting_report_table = QTableWidget()
        self.accounting_report_table.setColumnCount(3)
        self.accounting_report_table.setHorizontalHeaderLabels([t('accounts'), t('account_type'), t('amount')])
        self.accounting_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.accounting_report_table)
        
        widget.setLayout(layout)
        return widget

    def load_sales_report(self):
        from_date = self.sales_from_date.date().toString('yyyy-MM-dd')
        to_date = self.sales_to_date.date().toString('yyyy-MM-dd')
        customer_id = self.sales_customer_combo.currentData()
        
        query = '''SELECT i.invoice_number, c.name, i.invoice_date, it.item_id, 
                   item.name as item_name, it.quantity, it.unit_price, it.total_price
                   FROM invoices i JOIN customers c ON i.customer_id = c.id
                   JOIN invoice_items it ON i.id = it.invoice_id
                   JOIN items item ON it.item_id = item.id
                   WHERE i.invoice_date BETWEEN ? AND ?'''
        
        params = [from_date, to_date]
        if customer_id:
            query += ' AND c.id = ?'
            params.append(customer_id)
        
        query += ' ORDER BY i.invoice_date DESC'
        results = self.db.fetchall(query, tuple(params))
        
        self.sales_report_table.setRowCount(len(results))
        for row, res in enumerate(results):
            self.sales_report_table.setItem(row, 0, QTableWidgetItem(res['invoice_number']))
            self.sales_report_table.setItem(row, 1, QTableWidgetItem(res['name']))
            self.sales_report_table.setItem(row, 2, QTableWidgetItem(res['invoice_date']))
            self.sales_report_table.setItem(row, 3, QTableWidgetItem(res['item_name']))
            self.sales_report_table.setItem(row, 4, QTableWidgetItem(str(res['quantity'])))
            self.sales_report_table.setItem(row, 5, QTableWidgetItem(str(res['unit_price'])))
            self.sales_report_table.setItem(row, 6, QTableWidgetItem(str(res['total_price'])))

    def load_purchase_report(self):
        from_date = self.purchase_from_date.date().toString('yyyy-MM-dd')
        to_date = self.purchase_to_date.date().toString('yyyy-MM-dd')
        supplier_id = self.purchase_supplier_combo.currentData()
        
        query = '''SELECT po.po_number, s.name, po.order_date, pi.item_id,
                   item.name as item_name, pi.quantity, pi.unit_price, pi.total_price
                   FROM purchase_orders po JOIN suppliers s ON po.supplier_id = s.id
                   JOIN purchase_items pi ON po.id = pi.purchase_order_id
                   JOIN items item ON pi.item_id = item.id
                   WHERE po.order_date BETWEEN ? AND ?'''
        
        params = [from_date, to_date]
        if supplier_id:
            query += ' AND s.id = ?'
            params.append(supplier_id)
        
        query += ' ORDER BY po.order_date DESC'
        results = self.db.fetchall(query, tuple(params))
        
        self.purchase_report_table.setRowCount(len(results))
        for row, res in enumerate(results):
            self.purchase_report_table.setItem(row, 0, QTableWidgetItem(res['po_number']))
            self.purchase_report_table.setItem(row, 1, QTableWidgetItem(res['name']))
            self.purchase_report_table.setItem(row, 2, QTableWidgetItem(res['order_date']))
            self.purchase_report_table.setItem(row, 3, QTableWidgetItem(res['item_name']))
            self.purchase_report_table.setItem(row, 4, QTableWidgetItem(str(res['quantity'])))
            self.purchase_report_table.setItem(row, 5, QTableWidgetItem(str(res['unit_price'])))
            self.purchase_report_table.setItem(row, 6, QTableWidgetItem(str(res['total_price'])))

    def load_inventory_report(self):
        category_id = self.inventory_category_combo.currentData()
        
        query = '''SELECT i.code, i.name, c.name as category, i.unit, i.quantity_on_hand,
                   i.price, (i.quantity_on_hand * i.price) as total_value
                   FROM items i JOIN categories c ON i.category_id = c.id'''
        
        if category_id:
            query += f' WHERE c.id = {category_id}'
        
        results = self.db.fetchall(query)
        
        self.inventory_report_table.setRowCount(len(results))
        for row, res in enumerate(results):
            self.inventory_report_table.setItem(row, 0, QTableWidgetItem(res['code']))
            self.inventory_report_table.setItem(row, 1, QTableWidgetItem(res['name']))
            self.inventory_report_table.setItem(row, 2, QTableWidgetItem(res['category']))
            self.inventory_report_table.setItem(row, 3, QTableWidgetItem(res['unit']))
            self.inventory_report_table.setItem(row, 4, QTableWidgetItem(str(res['quantity_on_hand'])))
            self.inventory_report_table.setItem(row, 5, QTableWidgetItem(str(res['price'])))
            self.inventory_report_table.setItem(row, 6, QTableWidgetItem(str(res['total_value'])))

    def generate_pl_report(self):
        query = '''SELECT account_type, SUM(current_balance) as total
                   FROM accounts GROUP BY account_type'''
        results = self.db.fetchall(query)
        
        self.accounting_report_table.setRowCount(len(results))
        for row, res in enumerate(results):
            self.accounting_report_table.setItem(row, 0, QTableWidgetItem(res['account_type']))
            self.accounting_report_table.setItem(row, 1, QTableWidgetItem(res['account_type']))
            self.accounting_report_table.setItem(row, 2, QTableWidgetItem(str(res['total'])))
        
        QMessageBox.information(self, t('success'), t('report_loaded'))

    def generate_balance_report(self):
        query = 'SELECT * FROM accounts'
        results = self.db.fetchall(query)
        
        self.accounting_report_table.setRowCount(len(results))
        for row, res in enumerate(results):
            self.accounting_report_table.setItem(row, 0, QTableWidgetItem(res['name']))
            self.accounting_report_table.setItem(row, 1, QTableWidgetItem(res['account_type']))
            self.accounting_report_table.setItem(row, 2, QTableWidgetItem(str(res['current_balance'])))
        
        QMessageBox.information(self, t('success'), t('report_loaded'))

    def generate_trial_balance(self):
        query = '''SELECT account_number, name, account_type, current_balance
                   FROM accounts ORDER BY account_type, account_number'''
        results = self.db.fetchall(query)
        
        self.accounting_report_table.setRowCount(len(results))
        for row, res in enumerate(results):
            self.accounting_report_table.setItem(row, 0, QTableWidgetItem(res['name']))
            self.accounting_report_table.setItem(row, 1, QTableWidgetItem(res['account_type']))
            self.accounting_report_table.setItem(row, 2, QTableWidgetItem(str(res['current_balance'])))
        
        QMessageBox.information(self, t('success'), t('report_loaded'))

    def export_sales_pdf(self):
        QMessageBox.information(self, t('success'), t('export_pending'))

    def export_purchase_pdf(self):
        QMessageBox.information(self, t('success'), t('export_pending'))

    def export_inventory_pdf(self):
        QMessageBox.information(self, t('success'), t('export_pending'))

    def export_accounting_pdf(self):
        QMessageBox.information(self, t('success'), t('export_pending'))
