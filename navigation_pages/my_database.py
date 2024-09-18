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


st.subheader("My Invoice Database")
st.caption("View extracted invoice data.")

tab1, tab2 = st.tabs(["Invoices", "Line Items"])

with tab1:
    invoices_df = get_invoices()
    if invoices_df.empty:
        st.info("No invoices found in the database.")
    else:
        st.dataframe(invoices_df)

with tab2:
    line_items_df = get_line_items()
    if line_items_df.empty:
        st.info("No line items found in the database.")
    else:
        st.dataframe(line_items_df)

col1, col2, col3 = st.columns([1,1,4.8])

if not invoices_df.empty and not line_items_df.empty:
    with col1:
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            invoices_csv = invoices_df.to_csv(index=False).encode('utf-8')
            zf.writestr("invoices.csv", invoices_csv)

            line_items_csv = line_items_df.to_csv(index=False).encode('utf-8')
            zf.writestr("line_items.csv", line_items_csv)

        buffer.seek(0)
        st.download_button(
            label="Download Data",
            data=buffer,
            file_name="invoices_and_line_items.zip",
            mime="application/zip"
        )

    with col2:
        if st.button('Refresh'):
            st.rerun()

    with col3:
        pass
else:
    with col1:
        if st.button('Refresh'):
            st.rerun()
    with col2:
        pass
    with col3:
        pass

