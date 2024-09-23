import streamlit as st
import os
from datetime import datetime
from database_files.db import query_db, delete_data
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd

directory = 'uploaded_invoices'
supported_extensions = ('.jpg', '.jpeg', '.png', '.pdf')

st.subheader("Invoice History")
st.caption("Access all your past invoice uploads and their individual data.")

@st.dialog(title="File Preview", width="large")
def preview(path):
    if path.lower().endswith('.pdf'):
        pdf_viewer(path)
    else:
        st.image(path)

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
def delete_invoice(path, name):
    st.warning(f"Are you sure you want to delete '{name}' and its attributes from the database?")
    col1, col2, col3 = st.columns([1,1,5])
    with col1:
        if st.button("Yes"):
            delete_data(name, st.session_state['user_info'].get('email'))
            os.remove(path)
            st.rerun()
    with col2:
        if st.button("No"):
            st.rerun()
    with col3:
        pass


if len(os.listdir(directory)) != 0:
    col1, col2, col3 = st.columns([3, 2, 4.5])

    with col1:
        st.caption("Invoice Name")
    with col2:
        st.caption("Date Uploaded")
    with col3:
        st.caption("Actions")


    for filename in sorted(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True):
        if filename.lower().endswith(supported_extensions):
            file_path = os.path.join(directory, filename)

            col1, col2, col3 = st.columns([3, 2, 4.5], vertical_alignment='center')

            with col1:
                base_name, extension = os.path.splitext(filename)
                if len(filename) > 25:
                    start_length = 12
                    end_length = 4

                    fname = f"{base_name[:start_length]}..{base_name[-end_length:]}{extension}"
                    st.write(fname)
                else:
                    st.write(filename)

            with col2:

                mod_time = os.path.getmtime(file_path)
                date_uploaded = datetime.fromtimestamp(mod_time).strftime('%H:%M, %d %b. %Y')
                st.write(date_uploaded)

            with col3:
                col3_1, col3_2, col3_3, col3_4 = st.columns(4)
                with col3_1:
                    if st.button("Preview", key=f"preview_{filename}"):
                        preview(file_path)
                with col3_2:
                    if st.button("View Data", key=f"details_{filename}"):
                        invoice_attributes(filename)
                with col3_3:
                    with open(file_path, 'rb') as f:
                        st.download_button(
                            label="️Download",
                            data=f,
                            file_name=filename,
                            mime="application/pdf" if filename.lower().endswith('.pdf') else f"image/{filename.split('.')[-1]}",
                            key=f"download_{filename}"
                        )
                with col3_4:
                    if st.button("️Delete", key=f"delete_{filename}"):
                        st.write(filename)
                        delete_invoice(file_path, filename)
else:
    st.info("There is no invoice data to display at this moment. Upload an invoice and come back.")