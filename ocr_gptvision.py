import base64
import requests
from dotenv import load_dotenv
from pdf2image import convert_from_path
from database_files.db import insert_invoice_and_items
import streamlit as st
import os

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

def ocr_gpt(image_path):
    original = image_path
    if 'pdf' in image_path:
        image = convert_from_path(image_path)
        filename = image_path.split('/')[-1].split('.')[0]
        image_path = f'uploaded_invoices/{filename}.png'
        image[0].save(image_path, 'PNG')

    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

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
                        "text": """Perform OCR on the given image and extract the following key invoice attributes. Format your response as [serial no.]. [key]: [value]. If an attribute is not present, use 'NULL'. Do not provide any additional text or explanations.

    1. Invoice Number: The unique identifier for this invoice.
    2. Invoice Date: The date the invoice was issued (format: YYYY-MM-DD).
    3. Due Date: The date by which payment is expected (format: YYYY-MM-DD).
    4. Seller Information: Full name, address, and contact details of the seller.
    5. Buyer Information: Full name, address, and contact details of the buyer.
    6. Purchase Order Number: The buyer's purchase order number, if available.
    7. List of Products/Services: Comma-separated list of all items or services billed. Do not include services like shipping as there is a separate attribute for that below.
    8. List of Quantities: Comma-separated list of quantities for each item, in the same order as the products/services.
    9. List of Unit Prices: Comma-separated list of unit prices for each item in float format only, in the same order as the products/services.
    10. Subtotal: The sum of all line items before taxes and discounts.
    11. Service Charges: Any additional charges that may be applied. Do not include shipping costs here.
    12. Net Total: Sum of subtotal and service charges.
    13. Discount: Any discounts applied to the invoice.
    14. Tax: The total amount of tax charged.
    15. Tax Rate: The percentage rate at which tax is charged.
    16. Shipping Costs: Any shipping or delivery charges.
    17. Grand Total: The final amount to be paid, including all taxes and fees.
    18. Currency: The currency in which the invoice is issued (INR, USD, etc.).
    19. Payment Terms: The terms of payment (e.g., "Net 30", "Due on Receipt", "UPI", etc.).
    20. Payment Method: Accepted or preferred payment methods.
    21. Bank Information: Seller's bank details for payment, if provided.
    22. Invoice Notes: Any additional notes or terms on the invoice.
    23. Shipping Address: The delivery address, if different from the buyer's address.
    24. Billing Address: The billing address, if different from the buyer's address."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
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

    items = [item.strip() for item in invoice_dict['List of Products/Services'].split(',')]
    quantities = [quantity.strip() for quantity in invoice_dict['List of Quantities'].split(',')]
    prices = [price.strip() for price in invoice_dict['List of Unit Prices'].split(',')]

    insert_invoice_and_items(invoice_dict, items, quantities, prices, st.session_state['user_info'].get('email'))

    if 'pdf' in original:
        os.remove(image_path)
    return
