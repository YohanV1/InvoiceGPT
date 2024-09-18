import streamlit as st
from database_files.db_create import create_tables
from ocr_gptvision import ocr_gpt
from PIL import Image
import os

if "status" not in st.session_state:
    st.session_state.status = False

st.set_page_config(layout="wide", page_title='InvoiceGPT', page_icon='logo_images/invoicegpt_icon.png')
st.logo("logo_images/invoicegpt_logo.png", icon_image="logo_images/invoicegpt_icon.png")

def about():
    st.image("logo_images/invoicegpt_logo_full.png", width=400)
    st.write("BillBot: Smart Invoice Processing with GPT-4 Vision is an AI-driven application designed to streamline bill and invoice management. Utilizing GPT-4 Vision, BillBot accurately extracts "
             "and contextualizes text from images, addressing the inefficiencies and errors of manual data entry. BillBot also offers interactive querying capabilities, enabling users to "
             "obtain precise answers about their bills.")
    if not st.session_state.status:
        if st.button("Login"):
            st.session_state.status = True
            st.rerun()
    if st.session_state.status:
        UPLOAD_DIR = "uploaded_invoices"
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        with st.form("my-form", clear_on_submit=True):
            st.subheader("Upload Invoice")
            st.caption("Upload an image or PDF of your invoice and automatically extract its data!")
            uploaded_files = st.file_uploader("Choose an invoice file (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"],
                                              accept_multiple_files=True, label_visibility="collapsed")
            submitted = st.form_submit_button("Upload invoice")
            for uploaded_file in uploaded_files:
                if submitted and uploaded_file is not None:
                    st.session_state.file_key += 1
                    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
                    if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
                        image = Image.open(uploaded_file)
                        image.save(file_path)
                        ocr_gpt(file_path)
                        st.success("Image invoice successfully uploaded!")

                    elif uploaded_file.type == "application/pdf":
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        ocr_gpt(file_path)
                        st.success("PDF invoice successfully uploaded!")
        create_tables()

def logout():
    st.session_state.status = False
    st.rerun()

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("navigation_pages/settings.py", title="Settings", icon=":material/settings:")
view_invoices = st.Page("navigation_pages/view_invoices.py", title="Recent Invoices", icon=":material/folder:")
view_invoice_database = st.Page("navigation_pages/view_invoice_database.py", title="My Database", icon=":material/visibility:")
chat_with_ai = st.Page("navigation_pages/ai_chat.py", title="Chat with AI", icon=":material/chat:")
about_page = st.Page(about, title="Home", icon=":material/home:")

account_pages = [logout_page, settings]
invoice_pages = [about_page, view_invoices, view_invoice_database, chat_with_ai]

page_dict = {}
if st.session_state.status:
    page_dict["Explore"] = invoice_pages
    pg = st.navigation(page_dict | {"Account": account_pages})
else:
    pg = st.navigation([st.Page(about)])

pg.run()