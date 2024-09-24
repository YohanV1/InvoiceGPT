from dotenv import load_dotenv
import os
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import streamlit as st
from database_files.aws_db import sanitize_email
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_core.messages import SystemMessage
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import time
import ast
import re


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4o-mini")

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

connection_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"

db = SQLDatabase.from_uri(connection_uri)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

tools = toolkit.get_tools()
def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

sanitized_email = 'yohanvvinu_at_gmail_dot_com'

invoice_file_names = query_as_list(db, f"SELECT invoice_file_name FROM invoices_{sanitized_email}")
invoice_numbers = query_as_list(db, f"SELECT invoice_number FROM invoices_{sanitized_email}")
seller_information = query_as_list(db, f"SELECT seller_information FROM invoices_{sanitized_email}")
buyer_information = query_as_list(db, f"SELECT buyer_information FROM invoices_{sanitized_email}")
purchase_order_numbers = query_as_list(db, f"SELECT purchase_order_number FROM invoices_{sanitized_email}")
currencies = query_as_list(db, f"SELECT currency FROM invoices_{sanitized_email}")
payment_methods = query_as_list(db, f"SELECT payment_method FROM invoices_{sanitized_email}")
bank_information = query_as_list(db, f"SELECT bank_information FROM invoices_{sanitized_email}")
invoice_notes = query_as_list(db, f"SELECT invoice_notes FROM invoices_{sanitized_email}")
shipping_addresses = query_as_list(db, f"SELECT shipping_address FROM invoices_{sanitized_email}")
billing_addresses = query_as_list(db, f"SELECT billing_address FROM invoices_{sanitized_email}")
line_item_file_names = query_as_list(db, f"SELECT invoice_file_name FROM line_items_{sanitized_email}")
products_services = query_as_list(db, f"SELECT product_service FROM line_items_{sanitized_email}")

all_proper_nouns_combined = (
        invoice_file_names +
        invoice_numbers +
        seller_information +
        buyer_information +
        purchase_order_numbers +
        currencies +
        payment_methods +
        bank_information +
        invoice_notes +
        shipping_addresses +
        billing_addresses +
        line_item_file_names +
        products_services
)
vector_db = FAISS.from_texts(all_proper_nouns_combined, OpenAIEmbeddings())
retriever = vector_db.as_retriever(search_kwargs={"k": 5})
description = """Use to look up values to filter on. Input is an approximate spelling of the proper noun, output is \
valid proper nouns. Use the noun most similar to the search."""
retriever_tool = create_retriever_tool(
    retriever,
    name="search_proper_nouns",
    description=description,
)

system = """You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct SQLite query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most 5 results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the given tools. Only use the information returned by the tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

You have access to the following tables: {table_names}

If you need to filter on a proper noun, you must ALWAYS first look up the filter value using the "search_proper_nouns" tool!
Do not try to guess at the proper name - use this function to find similar ones.""".format(
    table_names=db.get_usable_table_names()
)



system_message = SystemMessage(content=system)

tools.append(retriever_tool)

agent = create_react_agent(llm, tools, state_modifier=system_message)
start_time = time.time()
for s in agent.stream(
    {"messages": [HumanMessage(content="what parts have I bought that could be used in an internet of things project?")]}
):
    print(s)
    print("----")
end_time = time.time()
print(end_time - start_time)