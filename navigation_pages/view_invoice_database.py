import streamlit as st
import sqlite3
import pandas as pd
import zipfile
import io

def get_invoices():
    conn = sqlite3.connect('invoices_data.db')
    query = "SELECT * FROM invoices"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_line_items():
    conn = sqlite3.connect('invoices_data.db')
    query = "SELECT * FROM line_items"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


st.subheader("Invoice Database")
st.caption("View extracted invoice data from the database.")

tab1, tab2 = st.tabs(["Invoices", "Line Items"])

with tab1:
    st.write("Invoices")
    invoices_df = get_invoices()
    if invoices_df.empty:
        st.write("No invoices found in the database.")
    else:
        st.dataframe(invoices_df)

with tab2:
    st.write("Line Items")
    line_items_df = get_line_items()
    if line_items_df.empty:
        st.write("No line items found in the database.")
    else:
        st.dataframe(line_items_df)

col1, col2, col3 = st.columns([1,1,4.8])
with col1:
    if not invoices_df.empty and not line_items_df.empty:
        # Create an in-memory buffer to hold the zip file
        buffer = io.BytesIO()

        # Create a zip file in-memory
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add invoices CSV to zip
            invoices_csv = invoices_df.to_csv(index=False).encode('utf-8')
            zf.writestr("invoices.csv", invoices_csv)

            # Add line items CSV to zip
            line_items_csv = line_items_df.to_csv(index=False).encode('utf-8')
            zf.writestr("line_items.csv", line_items_csv)

        # Set the buffer position to the beginning so it can be read
        buffer.seek(0)

        # Create the download button for the zip file
        st.download_button(
            label="Download as Zip",
            data=buffer,
            file_name="invoices_and_line_items.zip",
            mime="application/zip"
        )

with col2:
    if st.button('Refresh Data'):
        st.rerun()

with col3:
    pass