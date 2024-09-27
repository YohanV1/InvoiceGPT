import streamlit as st
from database_files.invoice_s3_db import remove_user_files_from_s3
from database_files.sqlite_db import delete_user_tables
from utilities.authentication import google_auth
import time

if 'flag' not in st.session_state:
    st.session_state.flag = False

@st.dialog(title="Account Closure Confirmation", width="small")
def delete_account():
    st.warning("Closing your account will permanently delete all your data. Close account?")
    col1, col2, col3 = st.columns([1,1,5])
    with col1:
        if st.button("Yes"):
            st.session_state.flag = True
            st.rerun()
    with col2:
        if st.button("No"):
            st.rerun()
    with col3:
        pass

st.header("Settings")

user_picture = st.session_state['user_info'].get('picture')
user_name = st.session_state['user_info'].get('name')
user_email = st.session_state['user_info'].get('email')

st.write(f"Name: {user_name}")
st.write(f"Email: {user_email}")

if st.button("Close Account"):
    delete_account()
    remove_user_files_from_s3(st.session_state['user_info'].get('email'))

if st.session_state.flag:
    delete_user_tables(st.session_state['user_info'].get('email'))
    with st.spinner("Redirecting..."):
        time.sleep(5)
        google_auth()
