import streamlit as st

if "status" not in st.session_state:
    st.session_state.status = False

def about():
    st.title("InvoiceGPT")
    st.subheader("AI for Your Purchase Data!")
    st.write("BillBot: Smart Invoice Processing with GPT-4 Vision is an AI-driven application designed to streamline bill and invoice management. Utilizing GPT-4 Vision, BillBot accurately extracts "
             "and contextualizes text from images, addressing the inefficiencies and errors of manual data entry. BillBot also offers interactive querying capabilities, enabling users to "
             "obtain precise answers about their bills.")
    if not st.session_state.status:
        if st.button("Login"):
            st.session_state.status = True
            st.rerun()

def logout():
    st.session_state.status = False
    st.rerun()

st.set_page_config(layout="wide", page_title='InvoiceGPT', page_icon='logo_images/invoicegpt_icon.png')
st.logo("logo_images/invoicegpt_logo.png", icon_image="logo_images/invoicegpt_icon.png")

value = st.session_state.status

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
settings = st.Page("navigation_pages/settings.py", title="Settings", icon=":material/settings:")
view_invoices = st.Page("navigation_pages/view_invoices.py", title="View Invoices")
view_invoice_database = st.Page("navigation_pages/view_invoice_database.py", title="View Database")
upload_invoice = st.Page("navigation_pages/upload_invoice.py", title="Upload Invoice")
chat_with_ai = st.Page("navigation_pages/ai_chat.py", title="Chat with AI")
about_page = st.Page(about, title="About")

about_pages = [about_page]
account_pages = [logout_page, settings]
invoice_pages = [upload_invoice, view_invoices, view_invoice_database, chat_with_ai]

page_dict = {}
if st.session_state.status:
    page_dict[""] = invoice_pages
    pg = st.navigation({"Home": about_pages} | page_dict | {"Account": account_pages})
else:
    pg = st.navigation([st.Page(about)])

pg.run()