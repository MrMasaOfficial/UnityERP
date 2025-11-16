from database import Database

def seed_database():
    db = Database()
    
    categories = [
        {'name': 'الإلكترونيات', 'description': 'أجهزة إلكترونية'},
        {'name': 'الملابس', 'description': 'ملابس وإكسسوارات'},
        {'name': 'الغذاء', 'description': 'منتجات غذائية'},
        {'name': 'الأثاث', 'description': 'أثاث وديكور'},
    ]
    
    for cat in categories:
        try:
            db.insert('categories', cat)
        except:
            pass
    
    items = [
        {'code': 'ELEC-001', 'name': 'هاتف ذكي', 'category_id': 1, 'unit': 'قطعة', 'price': 2000, 'quantity_on_hand': 50, 'min_quantity': 10},
        {'code': 'ELEC-002', 'name': 'شاشة', 'category_id': 1, 'unit': 'قطعة', 'price': 1500, 'quantity_on_hand': 30, 'min_quantity': 5},
        {'code': 'CLTH-001', 'name': 'قميص', 'category_id': 2, 'unit': 'قطعة', 'price': 150, 'quantity_on_hand': 100, 'min_quantity': 20},
        {'code': 'FOOD-001', 'name': 'زيت', 'category_id': 3, 'unit': 'لتر', 'price': 50, 'quantity_on_hand': 200, 'min_quantity': 50},
        {'code': 'FURN-001', 'name': 'طاولة', 'category_id': 4, 'unit': 'قطعة', 'price': 500, 'quantity_on_hand': 15, 'min_quantity': 3},
    ]
    
    for item in items:
        try:
            db.insert('items', item)
        except:
            pass
    
    suppliers = [
        {'name': 'الموردين المتحدة', 'contact_person': 'محمد علي', 'phone': '0501234567', 'email': 'info@suppliers.sa', 'address': 'شارع النيل', 'city': 'الرياض', 'balance': 0},
        {'name': 'شركة التوزيع', 'contact_person': 'فاطمة أحمد', 'phone': '0559876543', 'email': 'contact@distribution.sa', 'address': 'شارع الخليج', 'city': 'جدة', 'balance': 0},
    ]
    
    for supp in suppliers:
        try:
            db.insert('suppliers', supp)
        except:
            pass
    
    customers = [
        {'name': 'أحمد محمد', 'contact_person': 'أحمد', 'phone': '0561234567', 'email': 'ahmad@email.com', 'address': 'شارع السلام', 'city': 'الرياض', 'balance': 0},
        {'name': 'فاطمة خالد', 'contact_person': 'فاطمة', 'phone': '0569876543', 'email': 'fatima@email.com', 'address': 'شارع الأمل', 'city': 'جدة', 'balance': 0},
        {'name': 'سارة علي', 'contact_person': 'سارة', 'phone': '0505555555', 'email': 'sarah@email.com', 'address': 'شارع النور', 'city': 'الدمام', 'balance': 0},
    ]
    
    for cust in customers:
        try:
            db.insert('customers', cust)
        except:
            pass
    
    accounts = [
        {'account_number': '1001', 'account_type': 'Assets', 'name': 'البنك', 'opening_balance': 10000, 'current_balance': 10000},
        {'account_number': '2001', 'account_type': 'Liabilities', 'name': 'حسابات المستحقات', 'opening_balance': 0, 'current_balance': 0},
        {'account_number': '3001', 'account_type': 'Revenue', 'name': 'الإيرادات', 'opening_balance': 0, 'current_balance': 0},
        {'account_number': '4001', 'account_type': 'Expenses', 'name': 'المصروفات', 'opening_balance': 0, 'current_balance': 0},
    ]
    
    for acc in accounts:
        try:
            db.insert('accounts', acc)
        except:
            pass
    
    print('[OK] Initial data added successfully!')
    db.close()

if __name__ == '__main__':
    seed_database()
