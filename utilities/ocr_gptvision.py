import base64
import requests
from database_files.sqlite_db import insert_invoice_and_items
import boto3
from pdf2image import convert_from_bytes
from io import BytesIO
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

BUCKET_NAME = 'invoicegpt-bucket'
s3_client = boto3.client('s3')

api_key = os.getenv("OPENAI_API_KEY")

def ocr_gpt(s3_path):
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=s3_path)
    file_content = response['Body'].read()
    if s3_path.lower().endswith('.pdf'):
        images = convert_from_bytes(file_content, dpi=500)
        img_byte_arr = BytesIO()
        images[0].save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
    else:
        base64_image = base64.b64encode(file_content).decode('utf-8')

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Perform OCR on the given image and extract the following key invoice attributes. 
                    Format your response as [serial no.]. [key]: [value]. If an attribute is not present, use 'NULL'. 
                    Convert any percentages to numeric (Example: 20% = 0.2). Provide prices only as numerics, without currency. 
                    Do not provide any additional text or explanations.

1. invoice_number: The unique identifier for this invoice. (TEXT)
2. invoice_date: The date the invoice was issued (format: YYYY-MM-DD). (DATE)
3. due_date: The date by which payment is expected (format: YYYY-MM-DD). (DATE)
4. seller_information: Full name, address, and contact details of the seller. (TEXT)
5. buyer_information: Full name, address, and contact details of the buyer. (TEXT)
6. purchase_order_number: The buyer's purchase order number, if available. (TEXT)
7. products_services: Comma-separated list of all items or services billed. Do not include services like shipping. (TEXT)
8. quantities: Comma-separated list of quantities for each item, in the same order as the products/services. Do not include commas in each quantity itself. (INTEGER)
9. unit_prices: Comma-separated list of unit prices for each item, in the same order as the products/services. Do not include commas in each unit price itself. (NUMERIC)
10. subtotal: The sum of all line items before taxes and discounts. Do not include any commas in the subtotal. (NUMERIC)
11. service_charges: Any additional charges that may be applied. Do not include shipping costs here. Do not include any commas in the service charge. (NUMERIC)
12. net_total: Sum of subtotal and service charges. Do not include any commas in the net total. (NUMERIC)
13. discount: Any discounts applied to the invoice. Do not include any commas in the discount. (TEXT)
14. tax: The total amount of tax charged. Do not include any commas in the tax. (NUMERIC)
15. tax_rate: The percentage rate at which tax is charged. Do not include any commas in the tax rate. (TEXT)
16. shipping_costs: Any shipping or delivery charges. Do not include any commas in the shipping costs. (NUMERIC)
17. grand_total: The final amount to be paid, including all taxes and fees. Do not include any commas in the grand total. (NUMERIC)
18. currency: The currency in which the invoice is issued (INR, USD, SGD, AUD, etc). (TEXT)
19. payment_terms: The terms of payment (e.g., "Net 30", "Due on Receipt"). (TEXT)
20. payment_method: Accepted or preferred payment methods. (TEXT)
21. bank_information: Seller's bank details for payment, if provided. (TEXT)
22. invoice_notes: Any additional notes or terms on the invoice. (TEXT)
23. shipping_address: The delivery address. (TEXT)
24. billing_address: The billing address. (TEXT)"""
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
}

    response1 = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response_json1 = response1.json()
    invoice_data = response_json1['choices'][0]['message']['content']

    invoice_dict = {}
    for line in invoice_data.split('\n'):
        if ": " in line:
            substring = line[line.find(" ") + 1:]
            key, value = substring.split(': ', 1)
            invoice_dict[key.strip()] = value.strip()

    items = [item.strip() for item in invoice_dict['products_services'].split(',')]
    quantities = [quantity.strip() for quantity in invoice_dict['quantities'].split(',')]
    prices = [price.strip() for price in invoice_dict['unit_prices'].split(',')]
    insert_invoice_and_items(invoice_dict, s3_path, items, quantities, prices, st.session_state['user_info'].get('email'))
    return
