import sqlite3

# Connect to (or create) the database
conn = sqlite3.connect('invoices_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create invoices table
cursor.execute('''
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT,
    invoice_date TEXT,
    due_date TEXT,
    seller_information TEXT,
    buyer_information TEXT,
    purchase_order_number TEXT,
    subtotal TEXT,
    service_charges TEXT,
    net_total TEXT,
    discount TEXT,
    tax TEXT,
    tax_rate TEXT,
    shipping_costs TEXT,
    grand_total TEXT,
    currency TEXT,
    payment_terms TEXT,
    payment_method TEXT,
    bank_information TEXT,
    invoice_notes TEXT,
    shipping_address TEXT,
    billing_address TEXT
)
''')

# Create line_items table
cursor.execute('''
CREATE TABLE IF NOT EXISTS line_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    product_service TEXT,
    quantity TEXT,
    unit_price TEXT,
    FOREIGN KEY (invoice_id) REFERENCES invoices (id)
)
''')

conn.commit()
conn.close()