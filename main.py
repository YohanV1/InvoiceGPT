import streamlit as st
from home import home_page
from authentication import google_auth

st.set_page_config(layout="wide", page_title='InvoiceGPT', page_icon='logo_images/invoicegpt_icon.png')
st.logo("logo_images/invoicegpt_logo.png", icon_image="logo_images/invoicegpt_icon.png")

def about():
    home_page()

def exit():
    google_auth()

logout_page = st.Page(exit, title="Log out", icon=":material/logout:")
settings = st.Page("navigation_pages/settings.py", title="Settings", icon=":material/settings:")
view_invoices = st.Page("navigation_pages/invoice_history.py", title="Recent Invoices", icon=":material/folder:")
view_invoice_database = st.Page("navigation_pages/my_database.py", title="My Database", icon=":material/visibility:")
chat_with_ai = st.Page("navigation_pages/ai_chat.py", title="Chat with AI", icon=":material/chat:")
about_page = st.Page(about, title="Home", icon=":material/home:")

account_pages = [logout_page, settings]
invoice_pages = [about_page, view_invoices, view_invoice_database, chat_with_ai]

page_dict = {}
if st.session_state.get('connected', False):
    page_dict["Explore"] = invoice_pages
    pg = st.navigation(page_dict | {"Account": account_pages})
else:
    pg = st.navigation([st.Page(about)])

pg.run()