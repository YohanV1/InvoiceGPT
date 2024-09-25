from streamlit_google_auth import Authenticate
import streamlit as st

def google_auth():
    authenticator = Authenticate(
        secret_credentials_path='google_creds.json',
        cookie_name='my_cookie_name',
        cookie_key='this_is_secret',
        redirect_uri='http://localhost:8501',
        cookie_expiry_days=7
    )

    authenticator.check_authentification()

    if not st.session_state.get('connected', False):
        authorization_url = authenticator.get_authorization_url()
        st.markdown(
            f'<a href="{authorization_url}" target="_self" style="text-decoration: none;">'
            f'<button style="background-color:#D1442A;color:white;border:none;padding:10px 20px;">Sign in</button>'
            '</a>',
            unsafe_allow_html=True
        )
    else:
        st.cache_data.clear()
        st.cache_resource.clear()
        authenticator.logout()