from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os

def generate_invoice_pdf(db, invoice_number):
    invoice = db.fetchone('SELECT * FROM invoices WHERE invoice_number = ?', (invoice_number,))
    customer = db.fetchone('SELECT * FROM customers WHERE id = ?', (invoice['customer_id'],))
    items = db.fetchall('SELECT * FROM invoice_items WHERE invoice_id = ?', (invoice['id'],))
    
    filename = f"invoices/{invoice_number}.pdf"
    os.makedirs("invoices", exist_ok=True)
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        alignment=1
    )
    
    story.append(Paragraph('فاتورة بيع', title_style))
    story.append(Spacer(1, 0.2*inch))
    
    header_data = [
        ['رقم الفاتورة:', invoice_number, 'التاريخ:', invoice['invoice_date']],
        ['العميل:', customer['name'], 'الهاتف:', customer['phone'] or '-'],
        ['العنوان:', customer['address'] or '-', 'المدينة:', customer['city'] or '-'],
    ]
    
    header_table = Table(header_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.3*inch))
    
    items_data = [['الصنف', 'الكمية', 'السعر', 'الإجمالي']]
    for item in items:
        item_name = db.fetchone('SELECT name FROM items WHERE id = ?', (item['item_id'],))
        items_data.append([
            item_name['name'],
            str(item['quantity']),
            f"{item['unit_price']:.2f}",
            f"{item['total_price']:.2f}"
        ])
    
    items_table = Table(items_data, colWidths=[3*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))
    
    totals_data = [
        ['المجموع الجزئي:', f"{invoice['subtotal']:.2f}"],
        ['الخصم:', f"{invoice['discount']:.2f}"],
        ['الضريبة ({:.0f}%)'.format((invoice['tax'] / invoice['subtotal'] * 100) if invoice['subtotal'] > 0 else 0), f"{invoice['tax']:.2f}"],
        ['الإجمالي:', f"{invoice['total_amount']:.2f}"],
    ]
    
    totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
    ]))
    story.append(totals_table)
    
    doc.build(story)
    return filename

def generate_po_pdf(db, po_number):
    po = db.fetchone('SELECT * FROM purchase_orders WHERE po_number = ?', (po_number,))
    supplier = db.fetchone('SELECT * FROM suppliers WHERE id = ?', (po['supplier_id'],))
    items = db.fetchall('SELECT * FROM purchase_items WHERE purchase_order_id = ?', (po['id'],))
    
    filename = f"purchase_orders/{po_number}.pdf"
    os.makedirs("purchase_orders", exist_ok=True)
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        alignment=1
    )
    
    story.append(Paragraph('طلب شراء', title_style))
    story.append(Spacer(1, 0.2*inch))
    
    header_data = [
        ['رقم الطلب:', po_number, 'التاريخ:', po['order_date']],
        ['المورد:', supplier['name'], 'الهاتف:', supplier['phone'] or '-'],
        ['العنوان:', supplier['address'] or '-', 'المدينة:', supplier['city'] or '-'],
    ]
    
    header_table = Table(header_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.3*inch))
    
    items_data = [['الصنف', 'الكمية', 'السعر', 'الإجمالي']]
    for item in items:
        item_name = db.fetchone('SELECT name FROM items WHERE id = ?', (item['item_id'],))
        items_data.append([
            item_name['name'],
            str(item['quantity']),
            f"{item['unit_price']:.2f}",
            f"{item['total_price']:.2f}"
        ])
    
    items_table = Table(items_data, colWidths=[3*inch, 1.2*inch, 1.2*inch, 1.2*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.3*inch))
    
    totals_data = [
        ['الإجمالي:', f"{po['total_amount']:.2f}"],
    ]
    
    totals_table = Table(totals_data, colWidths=[4*inch, 1.5*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('LINEABOVE', (0, 0), (-1, 0), 2, colors.black),
    ]))
    story.append(totals_table)
    
    doc.build(story)
    return filename

def generate_sales_report_pdf(db, from_date, to_date, customer_id=None):
    filename = f"reports/sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    os.makedirs("reports", exist_ok=True)
    
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=10,
        alignment=1
    )
    
    story.append(Paragraph('تقرير المبيعات', title_style))
    story.append(Spacer(1, 0.2*inch))
    
    info_data = [
        ['من:', from_date, 'إلى:', to_date],
    ]
    info_table = Table(info_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    query = '''SELECT i.invoice_number, c.name, i.invoice_date, it.quantity,
               it.unit_price, it.total_price FROM invoices i 
               JOIN customers c ON i.customer_id = c.id
               JOIN invoice_items it ON i.id = it.invoice_id
               WHERE i.invoice_date BETWEEN ? AND ?'''
    
    params = [from_date, to_date]
    if customer_id:
        query += ' AND c.id = ?'
        params.append(customer_id)
    
    results = db.fetchall(query, tuple(params))
    
    data = [['رقم الفاتورة', 'العميل', 'التاريخ', 'الكمية', 'السعر', 'الإجمالي']]
    for res in results:
        data.append([
            res['invoice_number'],
            res['name'],
            res['invoice_date'],
            str(res['quantity']),
            f"{res['unit_price']:.2f}",
            f"{res['total_price']:.2f}"
        ])
    
    table = Table(data, colWidths=[1.2*inch, 1.5*inch, 1*inch, 0.8*inch, 0.8*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(table)
    
    doc.build(story)
    return filename
