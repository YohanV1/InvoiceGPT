import streamlit as st
import os
from datetime import datetime
from streamlit_pdf_viewer import pdf_viewer

directory = 'uploaded_invoices'
supported_extensions = ('.jpg', '.jpeg', '.png', '.pdf')

c = st.container(border=False)
c.title("Recently Uploaded Invoices")
c.write("\n\n\n")

@st.dialog(title="File Preview", width="large")
def preview(path):
    if path.lower().endswith('.pdf'):
        pdf_viewer(path)
    else:
        st.image(path)

@st.dialog(title="Invoice Attributes", width="large")
def invoice_attributes():



col1, col2, col3 = st.columns([3, 1.5, 3.5])

with col1:
    st.caption("Invoice Name")
with col2:
    st.caption("Date Uploaded")
with col3:
    st.caption("Actions")

# st.divider()

for filename in sorted(os.listdir(directory), key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True):
    if filename.lower().endswith(supported_extensions):
        file_path = os.path.join(directory, filename)

        col1, col2, col3 = st.columns([3, 1.5, 3.5], vertical_alignment='center')

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
            date_uploaded = datetime.fromtimestamp(mod_time).strftime('%d-%m-%Y, %H:%M')
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
                    st.write("Delete functionality to be implemented")