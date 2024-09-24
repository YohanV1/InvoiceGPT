import sqlite3
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def create_connection():
    return sqlite3.connect('invoicegpt_db.db')

def sanitize_email(email):
    return email.replace('@', '_at_').replace('.', '_dot_')

def create_user_tables(user_email):
    sanitized_email = sanitize_email(user_email)
    conn = create_connection()
    c = conn.cursor()
    c.execute(f'''
            CREATE TABLE IF NOT EXISTS invoices_{sanitized_email} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_file_name TEXT,
                invoice_number TEXT,
                invoice_date TEXT,
                due_date TEXT,
                seller_information TEXT,
                buyer_information TEXT,
                purchase_order_number TEXT,
                subtotal REAL,
                service_charges REAL,
                net_total REAL,
                discount REAL,
                tax REAL,
                tax_rate REAL,
                shipping_costs REAL,
                grand_total REAL,
                currency TEXT,
                payment_terms TEXT,
                payment_method TEXT,
                bank_information TEXT,
                invoice_notes TEXT,
                shipping_address TEXT,
                billing_address TEXT
            )
        ''')

    c.execute(f'''
            CREATE TABLE IF NOT EXISTS line_items_{sanitized_email} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_file_name TEXT,
                invoice_id INTEGER,
                product_service TEXT,
                quantity INTEGER,
                unit_price REAL,
                FOREIGN KEY (invoice_id) REFERENCES invoices_{user_email.replace('@', '_at_').replace('.', '_dot_')}(id)
            )
        ''')

    conn.commit()
    conn.close()

def insert_invoice_and_items(invoice_dict, s3_path, items, quantities, prices, user_email):
    conn = create_connection()
    c = conn.cursor()

    sanitized_email = sanitize_email(user_email)

    c.execute(f'''
    INSERT INTO invoices_{sanitized_email} (
        invoice_file_name, invoice_number, invoice_date, due_date, seller_information, buyer_information,
        purchase_order_number, subtotal, service_charges, net_total, discount, tax,
        tax_rate, shipping_costs, grand_total, currency, payment_terms, payment_method,
        bank_information, invoice_notes, shipping_address, billing_address
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        s3_path.split('/')[2],
        invoice_dict.get('Invoice Number', 'NULL'),
        invoice_dict.get('Invoice Date', 'NULL'),
        invoice_dict.get('Due Date', 'NULL'),
        invoice_dict.get('Seller Information', 'NULL'),
        invoice_dict.get('Buyer Information', 'NULL'),
        invoice_dict.get('Purchase Order Number', 'NULL'),
        invoice_dict.get('Subtotal', 0),
        invoice_dict.get('Service Charges', 0),
        invoice_dict.get('Net Total', 0),
        invoice_dict.get('Discount', 0),
        invoice_dict.get('Tax', 0),
        invoice_dict.get('Tax Rate', 0),
        invoice_dict.get('Shipping Costs', 0),
        invoice_dict.get('Grand Total', 0),
        invoice_dict.get('Currency', 'NULL'),
        invoice_dict.get('Payment Terms', 'NULL'),
        invoice_dict.get('Payment Method', 'NULL'),
        invoice_dict.get('Bank Information', 'NULL'),
        invoice_dict.get('Invoice Notes', 'NULL'),
        invoice_dict.get('Shipping Address', 'NULL'),
        invoice_dict.get('Billing Address', 'NULL')
    ))

    invoice_id = c.lastrowid

    for item, quantity, price in zip(items, quantities, prices):
        c.execute(f'''
        INSERT INTO line_items_{sanitized_email} (invoice_file_name, invoice_id, product_service, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            s3_path.split('/')[2],
            invoice_id,
            item,
            quantity,
            price
        ))

    conn.commit()
    st.cache_data.clear()
    conn.close()

@st.cache_data
def query_db(filename, user_email):
    conn = create_connection()
    c = conn.cursor()

    sanitized_email = sanitize_email(user_email)

    c.execute(f"SELECT * FROM invoices_{sanitized_email} WHERE invoice_file_name = ?", (filename,))
    invoice_data = c.fetchone()

    c.execute(f"SELECT * FROM line_items_{sanitized_email} WHERE invoice_file_name = ?", (filename,))
    line_items_data = c.fetchall()

    conn.close()
    return invoice_data, line_items_data

def delete_data(name, user_email):
    conn = create_connection()
    c = conn.cursor()

    sanitized_email = sanitize_email(user_email)

    c.execute(f"DELETE FROM line_items_{sanitized_email} WHERE invoice_file_name = ?", (name,))
    c.execute(f"DELETE FROM invoices_{sanitized_email} WHERE invoice_file_name = ?", (name,))

    conn.commit()
    st.cache_data.clear()
    conn.close()

@st.cache_data
def get_row_items(user_email):
    conn = create_connection()
    c = conn.cursor()

    sanitized_email = sanitize_email(user_email)

    c.execute(f"SELECT * FROM invoices_{sanitized_email}")
    df1 = pd.DataFrame(c.fetchall(), columns=[column[0] for column in c.description])

    c.execute(f"SELECT * FROM line_items_{sanitized_email}")
    df2 = pd.DataFrame(c.fetchall(), columns=[column[0] for column in c.description])

    conn.close()
    return df1, df2