import streamlit as st
import os
from PIL import Image

UPLOAD_DIR = "uploaded_invoices"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

with st.form("my-form", clear_on_submit=True):
    st.subheader("Upload Invoice")
    st.caption("Upload an image or PDF of your invoice.")
    uploaded_file = st.file_uploader("Choose an invoice file (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"],
                                     accept_multiple_files=False, label_visibility="collapsed")
    submitted = st.form_submit_button("Upload invoice")
    if submitted and uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
            image = Image.open(uploaded_file)
            image.save(file_path)
            st.success("Image invoice successfully uploaded!")
        elif uploaded_file.type == "application/pdf":
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("PDF invoice successfully uploaded!")
        else:
            st.error("Unsupported file type. Please upload a PDF or image file.")