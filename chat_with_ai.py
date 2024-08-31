from dotenv import load_dotenv
import streamlit as st
import sqlite3
from langchain_openai import ChatOpenAI
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def get_openai_response(question, prompt):
    model = ChatOpenAI(temperature=0, model_name="gpt-4")
    messages = prompt + [{"role": "user", "content": question}]
    response = model.invoke(messages)
    return response.content


def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows


prompt = [
    {"role": "system", "content": """
    You are an expert in converting English questions to SQL queries!
    The SQL database has the name INVOICES and has the following columns - 
    INVOICE_NUMBER, INVOICE_DATE, DUE_DATE, BILLING_ADDRESS, SHIPPING_ADDRESS, 
    ITEMIZED_LIST, UNIT_PRICE, TOTAL_AMOUNT, TAX_INFORMATION, PAYMENT_TERMS.

    For example:
    Example 1 - How many invoices are present in the database?
    The SQL command will be: SELECT COUNT(*) FROM INVOICES;

    Example 2 - Show me all invoices with a total amount greater than 1000.
    The SQL command will be: SELECT * FROM INVOICES WHERE TOTAL_AMOUNT > 1000;

    Example 3 - How much have I spent in the last month?
    The SQL command will be: SELECT SUM(TOTAL_AMOUNT) FROM INVOICES WHERE INVOICE_DATE >= DATE('now', '-1 month');

    Example 4 - List all invoices that have "Consulting Services" in the itemized list.
    The SQL command will be: SELECT * FROM INVOICES WHERE ITEMIZED_LIST LIKE '%Consulting Services%';

    Example 5 - Show me the details of the invoice with the invoice number 'INV-002'.
    The SQL command will be: SELECT * FROM INVOICES WHERE INVOICE_NUMBER = 'INV-002';

    Example 6 - What are the total taxes applied across all invoices?
    The SQL command will be: SELECT SUM(TOTAL_AMOUNT * SUBSTR(TAX_INFORMATION, 1, INSTR(TAX_INFORMATION, '%')-1) / 100) FROM INVOICES WHERE TAX_INFORMATION LIKE '%VAT%' OR TAX_INFORMATION LIKE '%Sales Tax%';

    Example 7 - List all invoices that are due next week.
    The SQL command will be: SELECT * FROM INVOICES WHERE DUE_DATE BETWEEN DATE('now', 'start of day', '+1 day') AND DATE('now', 'start of day', '+8 days');

    Example 8 - Show all invoices where the billing address is in 'Springfield'.
    The SQL command will be: SELECT * FROM INVOICES WHERE BILLING_ADDRESS LIKE '%Springfield%';

    Example 9 - Display all invoices that have been paid using PayPal.
    The SQL command will be: SELECT * FROM INVOICES WHERE PAYMENT_TERMS LIKE '%PayPal%';

    Example 10 - How many invoices were issued in August 2024?
    The SQL command will be: SELECT COUNT(*) FROM INVOICES WHERE INVOICE_DATE BETWEEN '2024-08-01' AND '2024-08-31';

    Provide only the SQL query without any additional text, markdown formatting, or explanations.
    """}
]



st.set_page_config(page_title="Chat With AI")
st.header("BillBot - Text to SQL AI Chat Demo")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")

if submit:
    response = get_openai_response(question, prompt)
    results = read_sql_query(response, "invoices.db")
    st.subheader("The Response is")
    for row in results:
        st.write(row)
