from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDialog, QLabel, 
                             QLineEdit, QDoubleSpinBox, QComboBox,
                             QMessageBox, QHeaderView, QFormLayout, QTabWidget,
                             QDateEdit)
from PyQt5.QtCore import Qt, QDate
from translations import t

class AccountingWidget(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_accounts()

    def init_ui(self):
        layout = QVBoxLayout()
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_accounts_tab(), t('accounts'))
        self.tabs.addTab(self.create_transactions_tab(), t('transactions'))
        self.tabs.addTab(self.create_receivables_tab(), t('receivables'))
        self.tabs.addTab(self.create_payables_tab(), t('payables'))
        
        layout.addWidget(self.tabs)
        self.setLayout(layout)
    
    def update_ui_language(self):
        self.tabs.setTabText(0, t('accounts'))
        self.tabs.setTabText(1, t('transactions'))
        self.tabs.setTabText(2, t('receivables'))
        self.tabs.setTabText(3, t('payables'))

    def create_accounts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(t('new_account'))
        add_btn.clicked.connect(self.add_account_dialog)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton(t('edit'))
        edit_btn.clicked.connect(self.edit_account_dialog)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton(t('delete'))
        delete_btn.clicked.connect(self.delete_account)
        button_layout.addWidget(delete_btn)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_accounts)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.accounts_table = QTableWidget()
        self.accounts_table.setColumnCount(6)
        self.accounts_table.setHorizontalHeaderLabels([
            t('account_number'), t('name'), t('account_type'), t('opening_balance'), t('current_balance'), t('date')
        ])
        self.accounts_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.accounts_table)
        
        widget.setLayout(layout)
        return widget

    def create_transactions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(t('new_transaction'))
        add_btn.clicked.connect(self.add_transaction_dialog)
        button_layout.addWidget(add_btn)
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_transactions)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(6)
        self.transactions_table.setHorizontalHeaderLabels([
            t('accounts'), t('debit_credit'), t('amount'), t('reference_doc'), t('description'), t('date')
        ])
        self.transactions_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.transactions_table)
        
        widget.setLayout(layout)
        return widget

    def create_receivables_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_receivables)
        layout.addWidget(refresh_btn)
        
        self.receivables_table = QTableWidget()
        self.receivables_table.setColumnCount(5)
        self.receivables_table.setHorizontalHeaderLabels([
            t('customer'), t('receivables_amount'), t('paid'), t('remaining'), t('status')
        ])
        self.receivables_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.receivables_table)
        
        widget.setLayout(layout)
        return widget

    def create_payables_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        refresh_btn = QPushButton(t('refresh'))
        refresh_btn.clicked.connect(self.load_payables)
        layout.addWidget(refresh_btn)
        
        self.payables_table = QTableWidget()
        self.payables_table.setColumnCount(5)
        self.payables_table.setHorizontalHeaderLabels([
            t('supplier'), t('payables_amount'), t('paid'), t('remaining'), t('status')
        ])
        self.payables_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.payables_table)
        
        widget.setLayout(layout)
        return widget

    def load_accounts(self):
        query = 'SELECT * FROM accounts'
        accounts = self.db.fetchall(query)
        
        self.accounts_table.setRowCount(len(accounts))
        for row, acc in enumerate(accounts):
            self.accounts_table.setItem(row, 0, QTableWidgetItem(acc['account_number']))
            self.accounts_table.setItem(row, 1, QTableWidgetItem(acc['name']))
            self.accounts_table.setItem(row, 2, QTableWidgetItem(acc['account_type']))
            self.accounts_table.setItem(row, 3, QTableWidgetItem(str(acc['opening_balance'])))
            self.accounts_table.setItem(row, 4, QTableWidgetItem(str(acc['current_balance'])))
            self.accounts_table.setItem(row, 5, QTableWidgetItem(acc['created_at']))

    def load_transactions(self):
        query = '''SELECT a.name, t.transaction_type, t.amount, t.reference_doc, 
                   t.description, t.created_at FROM transactions t 
                   JOIN accounts a ON t.account_id = a.id
                   ORDER BY t.created_at DESC LIMIT 100'''
        transactions = self.db.fetchall(query)
        
        self.transactions_table.setRowCount(len(transactions))
        for row, trans in enumerate(transactions):
            self.transactions_table.setItem(row, 0, QTableWidgetItem(trans['name']))
            self.transactions_table.setItem(row, 1, QTableWidgetItem(trans['transaction_type']))
            self.transactions_table.setItem(row, 2, QTableWidgetItem(str(trans['amount'])))
            self.transactions_table.setItem(row, 3, QTableWidgetItem(trans['reference_doc'] or ''))
            self.transactions_table.setItem(row, 4, QTableWidgetItem(trans['description'] or ''))
            self.transactions_table.setItem(row, 5, QTableWidgetItem(trans['created_at']))

    def load_receivables(self):
        query = '''SELECT c.id, c.name, 
                   COALESCE(SUM(i.total_amount), 0) as total,
                   COALESCE(SUM(i.paid_amount), 0) as paid,
                   COALESCE(SUM(i.total_amount - i.paid_amount), 0) as remaining
                   FROM customers c LEFT JOIN invoices i ON c.id = i.customer_id
                   GROUP BY c.id, c.name'''
        receivables = self.db.fetchall(query)
        
        self.receivables_table.setRowCount(len(receivables))
        for row, rec in enumerate(receivables):
            self.receivables_table.setItem(row, 0, QTableWidgetItem(rec['name']))
            self.receivables_table.setItem(row, 1, QTableWidgetItem(str(rec['total'])))
            self.receivables_table.setItem(row, 2, QTableWidgetItem(str(rec['paid'])))
            self.receivables_table.setItem(row, 3, QTableWidgetItem(str(rec['remaining'])))
            status = t('paid') if rec['remaining'] <= 0 else t('warning')
            self.receivables_table.setItem(row, 4, QTableWidgetItem(status))

    def load_payables(self):
        query = '''SELECT s.id, s.name,
                   COALESCE(SUM(po.total_amount), 0) as total,
                   COALESCE(SUM(COALESCE(p.amount, 0)), 0) as paid,
                   COALESCE(SUM(po.total_amount) - SUM(COALESCE(p.amount, 0)), 0) as remaining
                   FROM suppliers s LEFT JOIN purchase_orders po ON s.id = po.supplier_id
                   LEFT JOIN payments p ON po.id = p.purchase_order_id
                   GROUP BY s.id, s.name'''
        payables = self.db.fetchall(query)
        
        self.payables_table.setRowCount(len(payables))
        for row, pay in enumerate(payables):
            self.payables_table.setItem(row, 0, QTableWidgetItem(pay['name']))
            self.payables_table.setItem(row, 1, QTableWidgetItem(str(pay['total'])))
            self.payables_table.setItem(row, 2, QTableWidgetItem(str(pay['paid'])))
            self.payables_table.setItem(row, 3, QTableWidgetItem(str(pay['remaining'])))
            status = t('paid') if pay['remaining'] <= 0 else t('warning')
            self.payables_table.setItem(row, 4, QTableWidgetItem(status))

    def add_account_dialog(self):
        dialog = AccountDialog(self.db)
        if dialog.exec_():
            self.load_accounts()

    def edit_account_dialog(self):
        row = self.accounts_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_account'))
            return
        
        acc_number = self.accounts_table.item(row, 0).text()
        account = self.db.fetchone('SELECT * FROM accounts WHERE account_number = ?', (acc_number,))
        dialog = AccountDialog(self.db, account)
        if dialog.exec_():
            self.load_accounts()

    def delete_account(self):
        row = self.accounts_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, t('warning'), t('select_account'))
            return
        
        if QMessageBox.question(self, t('confirm'), t('confirm_delete')) == QMessageBox.Yes:
            acc_number = self.accounts_table.item(row, 0).text()
            account = self.db.fetchone('SELECT id FROM accounts WHERE account_number = ?', (acc_number,))
            self.db.delete('accounts', {'id': account['id']})
            self.load_accounts()
            QMessageBox.information(self, t('success'), t('operation_successful'))

    def add_transaction_dialog(self):
        dialog = TransactionDialog(self.db)
        if dialog.exec_():
            self.load_transactions()
            self.load_accounts()

class AccountDialog(QDialog):
    def __init__(self, db, account=None):
        super().__init__()
        self.db = db
        self.account = account
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(t('new_account') if not self.account else t('edit') + ' ' + t('accounts').lower())
        layout = QFormLayout()
        
        self.number_input = QLineEdit()
        self.name_input = QLineEdit()
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(['Assets', 'Liabilities', 'Equity', 'Revenue', 'Expenses'])
        
        self.opening_balance_input = QDoubleSpinBox()
        self.opening_balance_input.setMinimum(-999999)
        self.opening_balance_input.setMaximum(999999)
        
        if self.account:
            self.number_input.setText(self.account['account_number'])
            self.number_input.setReadOnly(True)
            self.name_input.setText(self.account['name'])
            type_idx = self.type_combo.findText(self.account['account_type'])
            self.type_combo.setCurrentIndex(type_idx)
            self.opening_balance_input.setValue(self.account['opening_balance'])
        
        layout.addRow(t('account_number') + ':', self.number_input)
        layout.addRow(t('name') + ':', self.name_input)
        layout.addRow(t('account_type') + ':', self.type_combo)
        layout.addRow(t('opening_balance') + ':', self.opening_balance_input)
        
        save_btn = QPushButton(t('save'))
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)
        
        self.setLayout(layout)

    def save(self):
        try:
            if not self.number_input.text() or not self.name_input.text():
                QMessageBox.warning(self, t('warning'), t('fill_all_fields'))
                return
            
            if self.account:
                self.db.update('accounts', {
                    'name': self.name_input.text(),
                    'account_type': self.type_combo.currentText(),
                    'opening_balance': self.opening_balance_input.value()
                }, {'id': self.account['id']})
            else:
                self.db.insert('accounts', {
                    'account_number': self.number_input.text(),
                    'name': self.name_input.text(),
                    'account_type': self.type_combo.currentText(),
                    'opening_balance': self.opening_balance_input.value(),
                    'current_balance': self.opening_balance_input.value()
                })
            
            QMessageBox.information(self, t('success'), t('account_saved'))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')

class TransactionDialog(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(t('new_transaction'))
        layout = QFormLayout()
        
        self.account_combo = QComboBox()
        accounts = self.db.fetchall('SELECT * FROM accounts')
        for acc in accounts:
            self.account_combo.addItem(acc['name'], acc['id'])
        
        self.type_combo = QComboBox()
        self.type_combo.addItem(t('debit'), 'Debit')
        self.type_combo.addItem(t('credit'), 'Credit')
        
        self.amount_input = QDoubleSpinBox()
        self.amount_input.setMaximum(999999)
        
        self.reference_input = QLineEdit()
        self.description_input = QLineEdit()
        
        layout.addRow(t('accounts') + ':', self.account_combo)
        layout.addRow(t('debit_credit') + ':', self.type_combo)
        layout.addRow(t('amount') + ':', self.amount_input)
        layout.addRow(t('reference_doc') + ':', self.reference_input)
        layout.addRow(t('description') + ':', self.description_input)
        
        save_btn = QPushButton(t('save'))
        save_btn.clicked.connect(self.save)
        layout.addRow(save_btn)
        
        self.setLayout(layout)

    def save(self):
        try:
            if self.amount_input.value() <= 0:
                QMessageBox.warning(self, t('warning'), t('invalid_price'))
                return
            
            account_id = self.account_combo.currentData()
            amount = self.amount_input.value()
            trans_type = self.type_combo.currentData()
            
            account = self.db.fetchone('SELECT * FROM accounts WHERE id = ?', (account_id,))
            
            if trans_type == 'Debit':
                new_balance = account['current_balance'] + amount
            else:
                new_balance = account['current_balance'] - amount
            
            self.db.insert('transactions', {
                'account_id': account_id,
                'transaction_type': trans_type,
                'amount': amount,
                'reference_doc': self.reference_input.text(),
                'description': self.description_input.text()
            })
            
            self.db.update('accounts', {'current_balance': new_balance}, {'id': account_id})
            
            QMessageBox.information(self, t('success'), t('transaction_saved'))
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, t('error'), f'{t("error")}: {str(e)}')
