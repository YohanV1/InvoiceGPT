import mysql.connector
import mysql.connector
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import os

load_dotenv()

connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    host=os.getenv('DB_HOST'),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)

def get_connection():
    return connection_pool.get_connection()

def sanitize_email(email):
    return email.replace('@', '_at_').replace('.', '_dot_')

def create_user_tables(user_email):
    sanitized_email = sanitize_email(user_email)

    try:
        connection = get_connection()

        if connection and connection.is_connected():
            cursor = connection.cursor()

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS invoices_{sanitized_email} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    invoice_file_name VARCHAR(255),
                    invoice_number VARCHAR(255),
                    invoice_date DATE,
                    due_date DATE,
                    seller_information TEXT,
                    buyer_information TEXT,
                    purchase_order_number VARCHAR(255),
                    subtotal DECIMAL(10, 2),
                    service_charges DECIMAL(10, 2),
                    net_total DECIMAL(10, 2),
                    discount DECIMAL(10, 2),
                    tax DECIMAL(10, 2),
                    tax_rate DECIMAL(5, 2),
                    shipping_costs DECIMAL(10, 2),
                    grand_total DECIMAL(10, 2),
                    currency VARCHAR(50),
                    payment_terms TEXT,
                    payment_method VARCHAR(50),
                    bank_information TEXT,
                    invoice_notes TEXT,
                    shipping_address TEXT,
                    billing_address TEXT
                )
            ''')

            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS line_items_{sanitized_email} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    invoice_file_name VARCHAR(255),
                    invoice_id INT,
                    product_service TEXT,
                    quantity INT,
                    unit_price DECIMAL(10, 2),
                    FOREIGN KEY (invoice_id) REFERENCES invoices_{sanitized_email} (id)
                )
            ''')

            connection.commit()

    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

def make_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD')
        )

        if connection.is_connected():

            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE invoicegpt_db;")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



def insert_invoice_and_items(invoice_dict, s3_path, items, quantities, prices, user_email):
    connection = get_connection()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        sanitized_email = sanitize_email(user_email)

        cursor.execute(f'''
        INSERT INTO invoices_{sanitized_email} (
            invoice_file_name, invoice_number, invoice_date, due_date, seller_information, buyer_information,
            purchase_order_number, subtotal, service_charges, net_total, discount, tax,
            tax_rate, shipping_costs, grand_total, currency, payment_terms, payment_method,
            bank_information, invoice_notes, shipping_address, billing_address
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

        invoice_id = cursor.lastrowid

        for item, quantity, price in zip(items, quantities, prices):
            cursor.execute(f'''
            INSERT INTO line_items_{sanitized_email} (invoice_file_name, invoice_id, product_service, quantity, unit_price)
            VALUES (%s, %s, %s, %s, %s)
            ''', (
                s3_path.split('/')[2],
                invoice_id,
                item,
                quantity,
                price
            ))

        connection.commit()
        st.cache_data.clear()


    except mysql.connector.Error:
        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@st.cache_data
def query_db(filename, user_email):
    connection = get_connection()

    if connection is None:

        return None, None

    try:
        cursor = connection.cursor()

        sanitized_email = sanitize_email(user_email)

        query1 = f"SELECT * FROM invoices_{sanitized_email} WHERE invoice_file_name = %s"
        cursor.execute(query1, (filename,))
        invoice_data = cursor.fetchone()

        query2 = f"SELECT * FROM line_items_{sanitized_email} WHERE invoice_file_name = %s"
        cursor.execute(query2, (filename,))
        line_items_data = cursor.fetchall()

        return invoice_data, line_items_data

    except mysql.connector.Error:

        return None, None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete_data(name, user_email):
    connection = get_connection()

    if connection is None:

        return

    try:
        cursor = connection.cursor()

        sanitized_email = sanitize_email(user_email)

        query2 = f"DELETE FROM line_items_{sanitized_email} WHERE invoice_file_name = %s"
        cursor.execute(query2, (name,))

        query1 = f"DELETE FROM invoices_{sanitized_email} WHERE invoice_file_name = %s"
        cursor.execute(query1, (name,))

        connection.commit()
        st.cache_data.clear()


    except mysql.connector.Error:

        connection.rollback()

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@st.cache_data
def get_row_items(user_email):
    connection = get_connection()

    if connection is None:

        return None, None

    try:
        sanitized_email = user_email.replace('@', '_at_').replace('.', '_dot_')

        query1 = f"SELECT * FROM invoices_{sanitized_email}"
        query2 = f"SELECT * FROM line_items_{sanitized_email}"

        df1 = pd.read_sql(query1, connection)
        df2 = pd.read_sql(query2, connection)

        return df1, df2

    except mysql.connector.Error:
        return None, None

    finally:
        if connection.is_connected():
            connection.close()