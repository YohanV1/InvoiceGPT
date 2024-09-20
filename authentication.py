from streamlit_google_auth import Authenticate
import streamlit as st

def google_auth():
    authenticator = Authenticate(
        secret_credentials_path='google_creds.json',
        cookie_name='my_cookie_name',
        cookie_key='this_is_secret',
        redirect_uri='http://localhost:8501',
    )

    authenticator.check_authentification()

    if not st.session_state.get('connected', False):
        authorization_url = authenticator.get_authorization_url()
        st.link_button('Sign in', authorization_url)
    else:
        authenticator.logout()