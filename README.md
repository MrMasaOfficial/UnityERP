# Integrated ERP System

An integrated resource management system (ERP) built with Python, PyQt5, and SQLite3

**Current Version**: 1.0 🚀 With language and theme support!


## Key Features

### 🌍 Languages ​​and Themes (New!)
- **Multilingual**: Full Arabic and English
- **Themes**: Day (Light) and Night (Dark) Mode
- **Save Settings**: User preferences are saved automatically
- **Instant Switch**: Change language or theme with one click

### Essential Features

### 1. Inventory Management
- Item table with codes, categories, and prices
- Inventory transactions (purchase, sale, modification)
- Automatic alerts when stock is low
- Filter items by category

### 2. Purchasing
- Create purchase orders
- Manage suppliers
- Link invoices to orders
- Audit Trail
- Print PDF

### 3. Sales
- Create invoices with total, discount, and tax calculations
- Manage customers
- Automatically update inventory
- Print invoices as PDF

### 4. Accounts (Accounting)
- Account Management
- Transaction Recording
- Customer and Supplier Accounts
- Financial Reports

### 5. Reports
- Sales Report
- Purchases Report
- Inventory Report
- Financial Reports (Profit and Loss, Balance Sheet)
- Export to PDF

## Installation

### Requirements
- Python 3.7+
- pip

### Installation Steps

1. Clone or download the project

2. Install the required libraries:
```bash
pip install -r requirements.txt
```

3. Add the initial data (optional):
```bash
python seed_data.py
```

## Running

Run the application:
```bash
python main.py
```

## Using Languages ​​and Themes 🎨

### Switching Language
1. Click on **Settings** in the top menu
2. Choose the language: **Arabic** or **English**
3. Click **Save**
4. All text will be updated automatically.

### Switch Appearance
1. Click **Settings** in the top menu.
2. Choose Appearance: **Light Mode** or **Dark Mode**.
3. Click **Save**.
4. The new colors will be applied immediately.

## New Documentation Files

- **QUICK_START.md** - Quick Start Guide
- **LANGUAGE_THEME_GUIDE.md** - Detailed Language and Theme Guide
- **UPDATES.md** - Technical Update Details
- **VERSION_HISTORY.md** - Release History
- **PROJECT_SUMMARY.md** - Project Summary

## Project Structure

```
erp_system/
├── main.py # Starting Point
├── database.py # Database Management
├── seed_data.py # Data Initials
├── requirements.txt # Required Libraries
├── ui/ # Graphical Interfaces
│ ├── inventory.py # Inventory Management
│ ├── sales.py # Sales Management
│ ├── purchasing.py # Purchasing Management
│ ├── accounting.py # Accounts Management
│ └── reports.py # Reports
├── utils/ # Utilities
│ └── pdf_generator.py # PDF Generation
└── erp_system.db # Database

```

## Database Tables

### Categories
- id: Unique Identifier
- name: Category Name
- description: Description

### Items
- ID: Unique ID
- Code: Code
- Name: Name
- Category_ID: Category ID
- Unit: Unit of Measurement
- Price: Price
- Quantity_on_hand: Quantity available
- Min_quantity: Minimum quantity

### Stock_movements
- ID: Unique ID
- Item_ID: Item ID
- Movement_type: Movement type (Buy, Sell, Modify)
- Quantity: Quantity
- Reference_doc: Reference
- Created_at: Date

### Customers
- ID: Unique ID
- Name: Name
- Contact_person: Contact person
- Phone: Phone
- Email: Email
- Address: Address
- City: City
- Balance: Balance

### Suppliers
- ID: Unique ID
- Name: Name
- Contact_person: Contact person
- Phone: Phone
- Email: Email
- Address: Address
- City: City
- Balance: Balance

### Invoices
- id: Unique ID
- invoice_number: Invoice number
- customer_id: Customer ID
- subtotal: Subtotal
- discount: Discount
- tax: Tax
- total_amount: Total
- paid_amount: Amount paid
- status: Status

### Purchase Orders
- id: Unique ID
- po_number: Order number
- supplier_id: Supplier ID
- total_amount: Total
- status: Status

### Accounts
- id: Unique ID
- account_number: Account number
- name: Name
- account_type: Account type
- opening_balance: Opening balance
- current_balance: Current balance

### Transactions
- id: Unique ID
- account_id: Account ID
- transaction_type: Transaction type
- amount: Amount
- created_at: Date

## Notes

- Data is Save them in an SQLite file named `erp_system.db`
- Invoices and purchase orders are saved as PDFs in separate folders
- Reports are saved in the `reports` folder
- The system fully supports Arabic

## Future Features

- User and permission support
- Advanced search and filtering
- Excel export
- Multi-currency support
- Recurring invoice system
- Human resources system