import streamlit as st
from database_files.sqlite_db import insert_invoice_and_items
from PIL import Image
from database_files.invoice_s3_db import upload_to_s3
import io

if "input_count" not in st.session_state:
    st.session_state.input_count = 1

if "input_values" not in st.session_state:
    st.session_state.input_values = [{"text": "", "num1": 0, "num2": 0}]

def add_input():
    st.session_state.input_count += 1
    st.session_state.input_values.append({"text": "", "num1": 0, "num2": 0})

def remove_input(index):
    if st.session_state.input_count > 1:
        st.session_state.input_count -= 1
        st.session_state.input_values.pop(index)

def prepare_data_for_insertion():
    invoice_dict = {
        'Invoice Number': st.session_state.get('invoice_number'),
        'Invoice Date': st.session_state.get('invoice_date'),
        'Due Date': st.session_state.get('due_date'),
        'Seller Information': st.session_state.get('seller_information'),
        'Buyer Information': st.session_state.get('buyer_information'),
        'Purchase Order Number': st.session_state.get('purchase_order_number'),
        'Subtotal': st.session_state.get('subtotal'),
        'Service Charges': st.session_state.get('service_charges'),
        'Net Total': st.session_state.get('net_total'),
        'Discount': st.session_state.get('discount'),
        'Tax': st.session_state.get('tax'),
        'Tax Rate': st.session_state.get('tax_rate'),
        'Shipping Costs': st.session_state.get('shipping_costs'),
        'Grand Total': st.session_state.get('grand_total'),
        'Currency': st.session_state.get('currency'),
        'Payment Terms': st.session_state.get('payment_terms'),
        'Payment Method': st.session_state.get('payment_method'),
        'Bank Information': st.session_state.get('bank_information'),
        'Invoice Notes': st.session_state.get('invoice_notes'),
        'Shipping Address': st.session_state.get('shipping_address'),
        'Billing Address': st.session_state.get('billing_address')
    }

    items = [item['text'] for item in st.session_state.input_values]
    quantities = [item['num1'] for item in st.session_state.input_values]
    prices = [item['num2'] for item in st.session_state.input_values]

    return invoice_dict, items, quantities, prices

st.header("Insert & Update Data")
st.caption("If your invoice is blurry, or the data extracted is not completely accurate!")

tab1, tab2 = st.tabs(["New Entry", "Edit Existing"])

with tab1:
    st.subheader("Invoice Entry")

    uploaded_file = st.file_uploader("Upload an image or PDF of the invoice for secure storage.", type=["pdf", "jpg", "jpeg", "png"],
                                      accept_multiple_files=False, label_visibility="visible")


    col0_1, col0_2 = st.columns([7, 1], vertical_alignment="bottom")
    with col0_2:
        invoice_number_toggle = st.toggle('NA', key='ino')
    with col0_1:
        invoice_number = st.text_input("Invoice Number", disabled=invoice_number_toggle)
        invoice_number = invoice_number if not invoice_number_toggle else None

    col1, col2 = st.columns([7,1], vertical_alignment="bottom")
    with col2:
        invoice_checkbox = st.toggle('NA', key='id')
    with col1:
        invoice_date = st.date_input("Invoice Date", disabled=invoice_checkbox)
        invoice_date = invoice_date if not invoice_checkbox else None

    col3, col4 = st.columns([7, 1], vertical_alignment="bottom")
    with col4:
        due_date_checkbox = st.toggle('NA', key='dd')
    with col3:
        due_date = st.date_input("Due Date", disabled=due_date_checkbox)
        due_date = due_date if not due_date_checkbox else None

    col5, col6 = st.columns([7, 1], vertical_alignment="bottom")
    with col6:
        seller_info_toggle = st.toggle('NA', key='si')
    with col5:
        seller_information = st.text_area("Seller Information", disabled=seller_info_toggle)
        seller_information = seller_information if not seller_info_toggle else None

    col7, col8 = st.columns([7, 1], vertical_alignment="bottom")
    with col8:
        buyer_info_toggle = st.toggle('NA', key='b')
    with col7:
        buyer_information = st.text_area("Buyer Information", disabled=buyer_info_toggle)
        buyer_information = buyer_information if not buyer_info_toggle else None

    col9, col10 = st.columns([7, 1], vertical_alignment="bottom")
    with col10:
        po_number_toggle = st.toggle('NA', key='pon')
    with col9:
        purchase_order_number = st.text_input("Purchase Order Number", disabled=po_number_toggle)
        purchase_order_number = purchase_order_number if not po_number_toggle else None

    col11, col12 = st.columns([7, 1], vertical_alignment="bottom")
    with col12:
        subtotal_toggle = st.toggle('NA', key='st')
    with col11:
        subtotal = st.number_input("Subtotal", min_value=0.0, disabled=subtotal_toggle)
        subtotal = subtotal if not subtotal_toggle else None

    col13, col14 = st.columns([7, 1], vertical_alignment="bottom")
    with col14:
        service_charges_toggle = st.toggle('NA', key='sc')
    with col13:
        service_charges = st.number_input("Service Charges", min_value=0.0, disabled=service_charges_toggle)
        service_charges = service_charges if not service_charges_toggle else None

    col15, col16 = st.columns([7, 1], vertical_alignment="bottom")
    with col16:
        net_total_toggle = st.toggle('NA', key='nt')
    with col15:
        net_total = st.number_input("Net Total", min_value=0.0, disabled=net_total_toggle)
        net_total = net_total if not net_total_toggle else None

    col17, col18 = st.columns([7, 1], vertical_alignment="bottom")
    with col18:
        discount_toggle = st.toggle('NA', key='dis')
    with col17:
        discount = st.number_input("Discount", min_value=0.0, disabled=discount_toggle)
        discount = discount if not discount_toggle else None

    col19, col20 = st.columns([7, 1], vertical_alignment="bottom")
    with col20:
        tax_toggle = st.toggle('NA', key='tax')
    with col19:
        tax = st.number_input("Tax", min_value=0.0, disabled=tax_toggle)
        tax = tax if not tax_toggle else None

    col21, col22 = st.columns([7, 1], vertical_alignment="bottom")
    with col22:
        tax_rate_toggle = st.toggle('NA', key='tr')
    with col21:
        tax_rate = st.number_input("Tax Rate", min_value=0.0, disabled=tax_rate_toggle)
        tax_rate = tax_rate if not tax_rate_toggle else None

    col23, col24 = st.columns([7, 1], vertical_alignment="bottom")
    with col24:
        shipping_costs_toggle = st.toggle('NA', key='shc')
    with col23:
        shipping_costs = st.number_input("Shipping Costs", min_value=0.0, disabled=shipping_costs_toggle)
        shipping_costs = shipping_costs if not shipping_costs_toggle else None

    col25, col26 = st.columns([7, 1], vertical_alignment="bottom")
    with col26:
        grand_total_toggle = st.toggle('NA', key='gt')
    with col25:
        grand_total = st.number_input("Grand Total", min_value=0.0, disabled=grand_total_toggle)
        grand_total = grand_total if not grand_total_toggle else None

    col27, col28 = st.columns([7, 1], vertical_alignment="bottom")
    with col28:
        currency_toggle = st.toggle('NA', key='cur')
    with col27:
        currency = st.text_input("Currency", disabled=currency_toggle)
        currency = currency if not currency_toggle else None

    col29, col30 = st.columns([7, 1], vertical_alignment="bottom")
    with col30:
        payment_terms_toggle = st.toggle('NA', key='pt')
    with col29:
        payment_terms = st.text_input("Payment Terms", disabled=payment_terms_toggle)
        payment_terms = payment_terms if not payment_terms_toggle else None

    col31, col32 = st.columns([7, 1], vertical_alignment="bottom")
    with col32:
        payment_method_toggle = st.toggle('NA', key='pm')
    with col31:
        payment_method = st.text_input("Payment Method", disabled=payment_method_toggle)
        payment_method = payment_method if not payment_method_toggle else None

    col33, col34 = st.columns([7, 1], vertical_alignment="center")
    with col34:
        bank_info_toggle = st.toggle('NA', key='bi')
    with col33:
        bank_information = st.text_area("Bank Information", disabled=bank_info_toggle)
        bank_information = bank_information if not bank_info_toggle else None

    col35, col36 = st.columns([7, 1], vertical_alignment="center")
    with col36:
        invoice_notes_toggle = st.toggle('NA', key='in')
    with col35:
        invoice_notes = st.text_area("Invoice Notes", disabled=invoice_notes_toggle)
        invoice_notes = invoice_notes if not invoice_notes_toggle else None

    col37, col38 = st.columns([7, 1], vertical_alignment="center")
    with col38:
        shipping_address_toggle = st.toggle('NA', key='sa')
    with col37:
        shipping_address = st.text_area("Shipping Address", disabled=shipping_address_toggle)
        shipping_address = shipping_address if not shipping_address_toggle else None

    col39, col40 = st.columns([7, 1], vertical_alignment="center")
    with col40:
        billing_address_toggle = st.toggle('NA', key='ba')
    with col39:
        billing_address = st.text_area("Billing Address", disabled=billing_address_toggle)
        billing_address = billing_address if not billing_address_toggle else None

    st.subheader("Line Item Entry")

    st.button("Add line item", on_click=add_input)

    for i in range(st.session_state.input_count):
        cols = st.columns([4, 1], vertical_alignment='center')
        with cols[0]:
            st.session_state.input_values[i]["text"] = st.text_input(f"Product/Service {i + 1}", value=st.session_state.input_values[i]["text"])
            st.session_state.input_values[i]["num1"] = st.number_input(f"Quantity {i + 1}", value=st.session_state.input_values[i]["num1"])
            st.session_state.input_values[i]["num2"] = st.number_input(f"Unit Price {i + 1}", value=st.session_state.input_values[i]["num2"])
        with cols[1]:
            if st.button(f"Remove", key=f"remove_{i}"):
                remove_input(i)
                st.rerun()

    if st.button("Submit Invoice"):
        if uploaded_file is not None:
            user_email = st.session_state['user_info'].get('email')
            if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
                with st.spinner("Uploading..."):
                    img_byte_arr = io.BytesIO()
                    image = Image.open(uploaded_file)
                    image.save(img_byte_arr, format=image.format)
                    img_byte_arr = img_byte_arr.getvalue()

                    s3_path = upload_to_s3(io.BytesIO(img_byte_arr), uploaded_file.name, user_email)
            elif uploaded_file.type == "application/pdf":
                with st.spinner("Uploading..."):
                    s3_path = upload_to_s3(uploaded_file, uploaded_file.name, user_email)

        invoice_dict = {
            'invoice_number': invoice_number,
            'invoice_date': invoice_date,
            'due_date': due_date,
            'seller_information': seller_information,
            'buyer_information': buyer_information,
            'purchase_order_number': purchase_order_number,
            'subtotal': subtotal,
            'service_charges': service_charges,
            'net_total': net_total,
            'discount': discount,
            'tax': tax,
            'tax_rate': tax_rate,
            'shipping_costs': shipping_costs,
            'grand_total': grand_total,
            'currency': currency,
            'payment_terms': payment_terms,
            'payment_method': payment_method,
            'bank_information': bank_information,
            'invoice_notes': invoice_notes,
            'shipping_address': shipping_address,
            'billing_address': billing_address,
        }
        print(invoice_dict)
        items = [item['text'] for item in st.session_state.input_values]
        quantities = [item['num1'] for item in st.session_state.input_values]
        prices = [item['num2'] for item in st.session_state.input_values]

        insert_invoice_and_items(invoice_dict, s3_path, items, quantities, prices, st.session_state['user_info'].get('email'))

with tab2:
    st.subheader("To be developed.")