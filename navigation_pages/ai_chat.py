import streamlit as st

container4 = st.container(border=True)
container4.subheader("Chat with AI")
container4.caption("Ask questions about your invoice data.")
user_input = container4.text_input("Ask a question about invoices:")
if user_input:
    container4.write(f"LLM Response: This is a placeholder for LLM's response to '{user_input}'")
container4.write("Feature coming soon..")