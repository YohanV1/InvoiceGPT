import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('invoices.db')

# Create a cursor object
cursor = conn.cursor()

# Create the invoices table
cursor.execute('''
CREATE TABLE IF NOT EXISTS invoices (
    invoice_number TEXT PRIMARY KEY,
    invoice_date TEXT,
    due_date TEXT,
    billing_address TEXT,
    shipping_address TEXT,
    itemized_list TEXT,
    unit_price TEXT,
    total_amount REAL,
    tax_information TEXT,
    payment_terms TEXT
)
''')

# Insert the invoice instances into the table
invoices = [
    ('INV-001', '2024-08-31', '2024-09-30', '123 Elm Street, Springfield, IL', '456 Oak Avenue, Springfield, IL', 'Laptop x1, Mouse x2', '1000.00, 20.00', 1040.00, '10% VAT', 'Net 30, Credit Card'),
    ('INV-002', '2024-08-30', '2024-09-15', '789 Pine Lane, Metropolis, NY', '789 Pine Lane, Metropolis, NY', 'Consulting Services x10 hours', '150.00', 1500.00, 'No tax', 'Net 15, Bank Transfer'),
    ('INV-003', '2024-08-28', '2024-09-28', '101 Maple Blvd, Gotham, NJ', '202 Birch Road, Gotham, NJ', 'Office Supplies x5, Printer x1', '50.00, 200.00', 450.00, '5% Sales Tax', 'Net 30, PayPal')
]

# Execute the insertions
cursor.executemany('''
INSERT INTO invoices (
    invoice_number, invoice_date, due_date, billing_address, shipping_address, 
    itemized_list, unit_price, total_amount, tax_information, payment_terms
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', invoices)

# Commit the changes
conn.commit()

# Fetch and display the inserted records
cursor.execute('SELECT * FROM invoices')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()
