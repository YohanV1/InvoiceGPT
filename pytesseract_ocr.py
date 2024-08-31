from langchain_openai import ChatOpenAI
from pdf2image import convert_from_path
import pytesseract
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
You are an AI assistant specialized in analyzing invoice data. Your task is to extract key information from the following invoice text and categorize it into specific attributes.

Invoice text:
{invoice_text}

Please extract and categorize the following information from the invoice text:

1. Invoice Number: [Extract the unique identifier for this invoice]
2. Invoice Date: [Extract the date the invoice was issued]
3. Due Date: [Extract the date by which payment is due]
4. Billing Address: [Extract the full address of the entity receiving the invoice]
5. Shipping Address: [Extract the full address where the goods or services are to be delivered]
6. Itemized List: [For each item or service on the invoice, extract a brief description and quantity]
7. Unit Price: [Extract the price per unit for each item or service]
8. Total Amount: [Extract the total amount due, including any taxes and discounts]
9. Tax Information: [Extract details about any taxes applied, such as VAT or GST]
10. Payment Terms: [Extract any information about payment terms or conditions]

Please format your response as a JSON object, with each attribute as a key. Ensure that all numeric values are represented as strings to maintain consistency. If any information is not present in the invoice, use null for that field.

Please analyze the provided invoice text and return the extracted information in the specified JSON format.
"""


def extract_text_ocr(file_path):
    images = convert_from_path(file_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text


file_path = 'invoices/Amazon_Invoice.pdf'
text = extract_text_ocr(file_path)

print("Extracted text:")
print(text)
print("\n" + "="*50 + "\n")

llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

prepared_prompt = PROMPT_TEMPLATE.format(invoice_text=text)
response = llm.invoke(prepared_prompt)

print(response.content)