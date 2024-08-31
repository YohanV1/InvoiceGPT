import streamlit as st

st.set_page_config(layout="wide", page_title='BillBot')

st.title("BillBot: AI-Powered Invoice Processing")

container1 = st.container(border=True)
container1.subheader("Upload Invoice")
container1.caption("Upload an image or PDF of your invoice.")
uploaded_file = container1.file_uploader("Choose an invoice file (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])

container2 = st.container(border=True)
container2.subheader("Recent Invoices")
container2.caption("View your recently uploaded invoices.")
container2.write("Feature coming soon..")

container3 = st.container(border=True)
container3.subheader("Invoice Database")
container3.caption("View invoices from the database.")
container3.write("Feature coming soon..")

container4 = st.container(border=True)
container4.subheader("Chat with AI")
container4.caption("Ask questions about your invoice data.")
user_input = container4.text_input("Ask a question about invoices:")
if user_input:
    container4.write(f"LLM Response: This is a placeholder for LLM's response to '{user_input}'")
container4.write("Feature coming soon..")

st.sidebar.button("Login with Google")
st.sidebar.divider()
with st.sidebar.expander("About"):
    st.write("BillBot: Smart Invoice Processing with GPT-4 Vision is an AI-driven application designed to streamline bill and invoice management. Utilizing GPT-4 Vision, BillBot accurately extracts "
             "and contextualizes text from images, addressing the inefficiencies and errors of manual data entry. BillBot also offers interactive querying capabilities, enabling users to "
             "obtain precise answers about their bills.")