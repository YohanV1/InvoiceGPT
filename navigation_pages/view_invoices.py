from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
import os

directory = 'uploaded_invoices'

supported_extensions = ('.jpg', '.jpeg', '.png', '.pdf')

container2 = st.container(border=True)
container2.subheader("Recent Invoices")
container2.caption("View your recently uploaded invoices.")
container2.write("Feature coming soon..")

@st.dialog(title="File Preview", width="large")
def preview(path):
    pdf_viewer(path)

for filename in os.listdir(directory):
    if filename.endswith(supported_extensions):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'rb') as f:
            st.download_button(
                label=f"Download file",
                data=f,
                file_name=filename,
                mime="application/pdf" if filename.endswith('.pdf') else f"image/{filename.split('.')[-1]}"
            )

if st.button("Preview file"):
    preview("uploaded_invoices/Amazon_Invoice.pdf")