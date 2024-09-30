import sqlite3
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import datetime

load_dotenv()

def create_connection():
    return sqlite3.connect('invoicegpt_db.db')

def sanitize_email(email):
    return email.replace('@', '_at_').replace('.', '_dot_')

def validate_date(date_str):
    if date_str == 'NULL':
        return None
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

def validate_numeric(value):
    if value == 'NULL':
        return 0
    return float(str(value))


def validate_text(value):
    return str(value) if value != 'NULL' else None

def validate_integer(value):
    if value == 'NULL':
        return 0
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

def create_user_tables(user_email):
    sanitized_email = sanitize_email(user_email)
    conn = create_connection()
    c = conn.cursor()
    c.execute(f'''
            CREATE TABLE IF NOT EXISTS invoices_{sanitized_email} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_file_name TEXT,
                invoice_number TEXT,
                invoice_date DATE,
                due_date DATE,
                seller_information TEXT,
                buyer_information TEXT,
                purchase_order_number TEXT,
                subtotal NUMERIC,
                service_charges NUMERIC,
                net_total NUMERIC,
                discount TEXT,
                tax NUMERIC,
                tax_rate TEXT,
                shipping_costs NUMERIC,
                grand_total NUMERIC,
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
                unit_price NUMERIC,
                FOREIGN KEY (invoice_id) REFERENCES invoices_{sanitized_email}(id)
            )
        ''')

    conn.commit()
    conn.close()

def insert_invoice_and_items(invoice_dict, s3_path, items, quantities, prices, user_email):
    conn = create_connection()
    c = conn.cursor()

    sanitized_email = sanitize_email(user_email)

    invoice_data = (
        validate_text(s3_path.split('/')[2]),
        validate_text(invoice_dict.get('invoice_number')),
        validate_date(invoice_dict.get('invoice_date')),
        validate_date(invoice_dict.get('due_date')),
        validate_text(invoice_dict.get('seller_information')),
        validate_text(invoice_dict.get('buyer_information')),
        validate_text(invoice_dict.get('purchase_order_number')),
        validate_numeric(invoice_dict.get('subtotal', 0)),
        validate_numeric(invoice_dict.get('service_charges', 0)),
        validate_numeric(invoice_dict.get('net_total', 0)),
        validate_text(invoice_dict.get('discount', 0)),
        validate_numeric(invoice_dict.get('tax', 0)),
        validate_text(invoice_dict.get('tax_rate', 0)),
        validate_numeric(invoice_dict.get('shipping_costs', 0)),
        validate_numeric(invoice_dict.get('grand_total', 0)),
        validate_text(invoice_dict.get('currency')),
        validate_text(invoice_dict.get('payment_terms')),
        validate_text(invoice_dict.get('payment_method')),
        validate_text(invoice_dict.get('bank_information')),
        validate_text(invoice_dict.get('invoice_notes')),
        validate_text(invoice_dict.get('shipping_address')),
        validate_text(invoice_dict.get('billing_address'))
    )

    # Execute the SQL query with the validated data
    c.execute(f'''
    INSERT INTO invoices_{sanitized_email} (
        invoice_file_name, invoice_number, invoice_date, due_date, seller_information, buyer_information,
        purchase_order_number, subtotal, service_charges, net_total, discount, tax,
        tax_rate, shipping_costs, grand_total, currency, payment_terms, payment_method,
        bank_information, invoice_notes, shipping_address, billing_address
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', invoice_data)

    invoice_id = c.lastrowid

    for item, quantity, price in zip(items, quantities, prices):
        line_item_data = (
            validate_text(s3_path.split('/')[2]),
            invoice_id,
            validate_text(item),
            validate_integer(quantity),
            validate_numeric(price)
        )

        c.execute(f'''
        INSERT INTO line_items_{sanitized_email} (invoice_file_name, invoice_id, product_service, quantity, unit_price)
        VALUES (?, ?, ?, ?, ?)
        ''', line_item_data)

    conn.commit()
    st.cache_data.clear()
    st.cache_resource.clear()
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
    st.cache_resource.clear()
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

def check_empty_db(user_email):
    conn = create_connection()
    c = conn.cursor()
    sanitized_email = sanitize_email(user_email)
    c.execute(f"SELECT COUNT(*) FROM invoices_{sanitized_email}")
    result = c.fetchone()
    count = result[0]
    conn.close()
    return count==0

def delete_user_tables(email):
    sanitized_email = sanitize_email(email)
    conn = sqlite3.connect('invoicegpt_db.db')
    cursor = conn.cursor()

    tables = [f"invoices_{sanitized_email}", f"line_items_{sanitized_email}"]

    for table in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table}")

    conn.commit()
    conn.close()