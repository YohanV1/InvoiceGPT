import streamlit as st
from database_files.sqlite_db import create_user_tables
from utilities.ocr_gptvision import ocr_gpt
from utilities.authentication import google_auth
from PIL import Image
from database_files.invoice_s3_db import upload_to_s3
import io

def home_page():
    if not st.session_state.get('connected', False):
        col1, col2, col3 = st.columns([3,10,2], vertical_alignment='center')
        with col1:
            st.title("InvoiceGPT")

        with col2:
            pass

        with col3:
            if not st.session_state.get('connected', False):
                google_auth()
            else:
                pass
    else:
        st.title("InvoiceGPT")

    st.header("AI-Powered Insights for Your Invoices")
    st.write("InvoiceGPT is your intelligent solution for streamlined bill and invoice management. "
             "Harnessing the power of GPT-4 Vision, our application revolutionizes how you handle financial documents. "
             "Say goodbye to tedious manual data entry and hello to accurate, efficient, and insightful invoice processing. "
             "InvoiceGPT doesn't just digitize your bills – it understands them, providing you with actionable insights "
             "and powerful analytical capabilities to transform your financial management. You are also equipped with your"
             "own invoice chatbot to query your data for insights. Go ahead and ask it how much you spent on your last shopping trip!")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        container1 = st.container(border=True, height=200)
        col1_1, col1_2 = container1.columns([1, 7], vertical_alignment='center')
        with col1_1:
            st.image("images/Upload icon.png", width=40)
        with col1_2:
            st.subheader('Store Invoices')
        container1.write('Effortlessly upload and securely store your financial documents in one centralized location, ensuring easy access and organization.')

    with col2:
        container2 = st.container(border=True, height=200)
        col2_1, col2_2 = container2.columns([1, 7], vertical_alignment='center')
        with col2_1:
            st.image("images/Lightbulb icon.png", width=40)
        with col2_2:
            st.subheader('Smart Processing')
        container2.write('Experience cutting-edge OCR and AI technology that accurately extracts, interprets, and categorizes data from your invoices with minimal manual input.')

    with col3:
        container3 = st.container(border=True, height=200)
        col3_1, col3_2 = container3.columns([1, 7], vertical_alignment='center')
        with col3_1:
            st.image("images/Content cut 24dp.png", width=40)
        with col3_2:
            st.subheader('Auto-Splitting')
        container3.write('Save time with intelligent auto-splitting capabilities that accurately categorize and allocate invoice items across both PDF and image formats.')

    col4, col5, col6 = st.columns(3, gap="medium")

    with col4:
        container4 = st.container(border=True, height=200)
        col4_1, col4_2 = container4.columns([1, 7], vertical_alignment='center')
        with col4_1:
            st.image("images/Satisfied icon.png", width=40)
        with col4_2:
            st.subheader('User-Friendly')
        container4.write('Navigate our intuitive interface designed for users of all skill levels, making invoice management accessible and effortless for everyone.')

    with col5:
        container5 = st.container(border=True, height=200)
        col5_1, col5_2 = container5.columns([1, 7], vertical_alignment='center')
        with col5_1:
            st.image("images/Search icon.png", width=40)
        with col5_2:
            st.subheader('AI Querying')
        container5.write('Engage with our AI to ask specific questions about your bills and receive instant, accurate answers, enhancing your financial understanding.')

    with col6:
        container6 = st.container(border=True, height=200)
        col6_1, col6_2 = container6.columns([1, 7], vertical_alignment='center')
        with col6_1:
            st.image("images/Analytics icon.png", width=40)
        with col6_2:
            st.subheader('Data Insights')
        container6.write('Unlock valuable insights from your financial data with advanced analytics tools, empowering you to make informed business decisions.')

    st.divider()

    col7, col8 = st.columns(2)

    with col7:
        if st.session_state.get('connected', False):
            st.subheader('Get started.')
        else:
            st.subheader('Sign in to get started.')

    with col8:
        pass

    col9, col10 = st.columns(2, gap="large")

    with col9:
        if st.session_state.get('connected', False):
            with st.form("my-form", clear_on_submit=True, border=False):
                st.write("Upload an image or PDF of your invoice and automatically extract its data.")
                uploaded_files = st.file_uploader("Choose an invoice file (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"],
                                                  accept_multiple_files=True, label_visibility="collapsed")
                submitted = st.form_submit_button("Process invoice")
                for uploaded_file in uploaded_files:
                    if submitted and uploaded_file is not None:
                        user_email = st.session_state['user_info'].get('email')
                        if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
                            with st.spinner("Uploading..."):
                                img_byte_arr = io.BytesIO()
                                image = Image.open(uploaded_file)
                                image.save(img_byte_arr, format=image.format)
                                img_byte_arr = img_byte_arr.getvalue()

                                s3_path = upload_to_s3(io.BytesIO(img_byte_arr), uploaded_file.name, user_email)
                                if s3_path:
                                    ocr_gpt(s3_path)
                            st.success("Image invoice successfully uploaded. Navigate with the sidebar for insights.")
                        elif uploaded_file.type == "application/pdf":
                            with st.spinner("Uploading..."):
                                s3_path = upload_to_s3(uploaded_file, uploaded_file.name, user_email)
                                if s3_path:
                                    ocr_gpt(s3_path)
                            st.success("PDF invoice successfully uploaded. Navigate with the sidebar for insights.")
            create_user_tables(st.session_state['user_info'].get('email'))
        else:
            with st.form("my-form", clear_on_submit=True, border=False):
                st.caption("Upload an image or PDF of your invoice and automatically extract its data.")
                st.file_uploader("Choose an invoice file (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"],
                                                  accept_multiple_files=True, label_visibility="collapsed", disabled=True)
                st.form_submit_button("Process invoice", disabled=True)
    with col10:
        st.write("Here are some sample queries for reference.")
        st.code("How much have I spent on taxes in the past month?", language="none")
        st.code("When was the last time I got Pizza?", language="none")
        st.code("Where did I ship my last pair of shoes to?", language="none")