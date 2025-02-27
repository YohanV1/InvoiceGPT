import streamlit as st
from utilities.home import home_page
from utilities.authentication import google_auth

st.set_page_config(layout="wide", page_title='InvoiceGPT', page_icon='images/invoicegpt_icon.png')
st.logo("images/invoicegpt_logo.png", icon_image="images/invoicegpt_icon.png")

def about():
    home_page()

def exit_app():
    google_auth()

logout_page = st.Page(exit_app, title="Log out", icon=":material/logout:")
settings = st.Page("navigation_pages/settings.py", title="Settings", icon=":material/settings:")
view_invoices = st.Page("navigation_pages/invoice_history.py", title="Recent Invoices", icon=":material/folder:")
view_invoice_database = st.Page("navigation_pages/my_database.py", title="My Database", icon=":material/visibility:")
view_graphs = st.Page("navigation_pages/graphs_dashboard.py", title="Analytics Dashboard", icon=":material/dashboard:")
chat_with_ai = st.Page("navigation_pages/ai_chat.py", title="Chat with AI", icon=":material/chat:")
about_page = st.Page(about, title="Home", icon=":material/home:")
manual_entry_page = st.Page("navigation_pages/manual_entry.py", title="Insert & Update Data", icon=":material/edit:")

about_us_page = st.Page("navigation_pages/about_us.py", title="About", icon=":material/help:")
contact_us_page = st.Page("navigation_pages/contact_us.py", title="Get in Touch!", icon=":material/contact_mail:")

account_pages = [settings, logout_page]
invoice_pages = [about_page, view_invoices, view_invoice_database, chat_with_ai, view_graphs, manual_entry_page]
learn_more_pages = [about_us_page, contact_us_page]

page_dict = {}

if st.session_state.get('connected', False):
    page_dict["Explore"] = invoice_pages
    first_name = st.session_state['user_info'].get('name').split()[0]
    pg = st.navigation(page_dict | {"Have Questions?": learn_more_pages} | {f"Account (Logged in as {first_name})": account_pages})
else:
    pg = st.navigation([st.Page(about)])

pg.run()