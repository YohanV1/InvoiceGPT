import streamlit as st
from database_files.sqlite_db import query_db, delete_data
from streamlit_pdf_viewer import pdf_viewer
from database_files.local_storage import get_file, list_user_files, delete_file
import pandas as pd
from datetime import datetime
import pytz
import os

directory = 'uploaded_invoices'
supported_extensions = ('.jpg', '.jpeg', '.png', '.pdf')

st.header("Invoice History")
st.caption("Access all your past invoice uploads and their individual data.")

@st.dialog(title="File Preview", width="large")
def preview(file_path):
    file_content = get_file(file_path)
    if file_content:
        if file_path.lower().endswith('.pdf'):
            pdf_viewer(file_content)
        else:
            st.image(file_content)

@st.dialog(title="Invoice Attributes", width="large")
def invoice_attributes(filename):
    invoice_data, line_items_data = query_db(filename, st.session_state['user_info'].get('email'))

    if invoice_data:
        st.subheader("Invoice Details")
        invoice_columns = ['ID', 'Invoice File Name', 'Invoice Number', 'Invoice Date', 'Due Date', 'Seller Information',
                           'Buyer Information', 'Purchase Order Number', 'Subtotal', 'Service Charges', 'Net Total',
                           'Discount', 'Tax', 'Tax Rate', 'Shipping Costs', 'Grand Total', 'Currency', 'Payment Terms',
                           'Payment Method', 'Bank Information', 'Invoice Notes', 'Shipping Address', 'Billing Address']

        invoice_df = pd.DataFrame([invoice_data], columns=invoice_columns)
        st.dataframe(invoice_df)
    else:
        st.write("No invoice found for the given filename.")

    if line_items_data:
        st.subheader("Line Items")
        line_items_columns = ['ID', 'Invoice File Name', 'Invoice ID', 'Product/Service', 'Quantity', 'Unit Price']
        line_items_df = pd.DataFrame(line_items_data, columns=line_items_columns)
        st.dataframe(line_items_df)
    else:
        st.write("No line items found for the given invoice.")

@st.dialog(title="Deletion Confirmation", width="small")
def delete_invoice(file_path, name):
    st.warning(f"Are you sure you want to delete '{name}' and its attributes from the database?")
    col1, col2, col3 = st.columns([1,1,5])
    with col1:
        if st.button("Yes"):
            delete_data(name, st.session_state['user_info'].get('email'))
            delete_file(file_path)
            st.rerun()
    with col2:
        if st.button("No"):
            st.rerun()
    with col3:
        pass

files = list_user_files(st.session_state['user_info'].get('email'))

if files:
    col1, col2, col3 = st.columns([3, 2, 4.5])

    with col1:
        st.caption("Invoice Name")
    with col2:
        st.caption("Date Uploaded")
    with col3:
        st.caption("Actions")

    sorted_files = sorted(files, key=lambda x: x['LastModified'], reverse=True)

    for file in sorted_files:
        filename = file['Key'].split('/')[-1]
        if filename.lower().endswith(supported_extensions):
            col1, col2, col3 = st.columns([3, 2, 4.5], vertical_alignment='center')

            with col1:
                base_name, extension = filename.rsplit('.', 1)
                if len(filename) > 25:
                    start_length = 12
                    end_length = 4
                    fname = f"{base_name[:start_length]}..{base_name[-end_length:]}.{extension}"
                    st.write(fname)
                else:
                    st.write(filename)

            with col2:
                timestamp = datetime.fromtimestamp(file['LastModified'])
                utc_zone = pytz.timezone('UTC')
                ist_zone = pytz.timezone('Asia/Kolkata')
                ist_time = utc_zone.localize(timestamp).astimezone(ist_zone)
                date_uploaded = ist_time.strftime('%H:%M, %d %b. %Y')
                st.write(date_uploaded)

            with col3:
                col3_1, col3_2, col3_3, col3_4 = st.columns(4)
                with col3_1:
                    if st.button("Preview", key=f"preview_{filename}"):
                        preview(file['Key'])
                with col3_2:
                    if st.button("View Data", key=f"details_{filename}"):
                        invoice_attributes(filename)
                with col3_3:
                    file_content = get_file(file['Key'])
                    if file_content:
                        st.download_button(
                            label="Download",
                            data=file_content,
                            file_name=filename,
                            mime=f"application/{filename.split('.')[-1]}"
                        )
                with col3_4:
                    if st.button("️Delete", key=f"delete_{filename}"):
                        delete_invoice(file['Key'], filename)
else:
    st.info("There is no invoice data to display at this moment. Upload an invoice and come back.")