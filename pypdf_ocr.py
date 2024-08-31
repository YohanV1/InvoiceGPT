import PyPDF2
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
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


# Open the PDF file
with open('invoices/Amazon_Invoice.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)

    # Initialize text container
    text = ''

    # Loop through all the pages
    for page in reader.pages:
        text += page.extract_text()

# Initialize the ChatOpenAI model
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")  # or "gpt-4" if you have access

# Create a ChatPromptTemplate
prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

# Format the prompt with the invoice text
formatted_prompt = prompt_template.format_messages(invoice_text=text)

# Get the response from the LLM
response = llm(formatted_prompt)

# Parse the JSON response
print(response.content)


# what is domain and project?
#
# existing work? what exists?
#
# how are your methods better?