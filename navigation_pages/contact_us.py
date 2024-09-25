import streamlit as st
from send_email import send_email

st.header("Get in Touch")
text = """
We value your feedback and input! If you have any questions, suggestions, or concerns about the app, we'd love to hear from you.Your insights can help us improve and grow. Whether it's a bug report, a feature request, or just general feedback, every bit helps.
Interested in contributing to the project? We welcome collaborators of all skill levels. Check out our GitHub repository to get started!
"""
st.write(text)

with st.form(key="email_form", clear_on_submit=True):
    name = st.text_input("Your name")
    subject = st.text_input("Your subject")
    message = st.text_area("Your message")
    email_subject = f"{subject} - {name}, {st.session_state['user_info'].get('email')}"
    button = st.form_submit_button("Submit")
    if button:
        with st.spinner("Sending..."):
            send_email(message, email_subject)
        st.success("Thank you! Your message has been received. We'll get back to you as soon as possible.")