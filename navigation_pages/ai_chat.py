import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.vectorstores import FAISS
from database_files.sqlite_db import sanitize_email, check_empty_db
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents.agent_toolkits import create_retriever_tool
from dotenv import load_dotenv
from PIL import Image
import time
import os
import re
import ast

load_dotenv()

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"Hi {st.session_state['user_info'].get('name')}, how can I help you today?"
    })

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

# FOR AWS CONNECTION - connection_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}"
# FOR AWS CONNECTION - db = SQLDatabase.from_uri(connection_uri)

sanitized_email = sanitize_email(st.session_state['user_info'].get('email'))
invoices_table = f"invoices_{sanitized_email}"
line_items_table = f"line_items_{sanitized_email}"

db = SQLDatabase.from_uri(
    'sqlite:///invoicegpt_db.db',
    include_tables=[invoices_table, line_items_table]
)

img_avatar = Image.open('logo_images/invoicegpt_icon.png')


for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=img_avatar if message["role"]=="assistant" else None):
        st.markdown(message["content"])



def query_as_list(db, query):
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return list(set(res))

@st.cache_data
def proper_nouns():
    sanitized_email = sanitize_email(st.session_state['user_info'].get('email'))

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

    return all_proper_nouns_combined

@st.cache_resource
def initialize_agent():
    extra_tools = []
    if not check_empty_db(st.session_state['user_info'].get('email')):
        vector_db = FAISS.from_texts(proper_nouns(), OpenAIEmbeddings())
        retriever = vector_db.as_retriever(search_kwargs={"k": 5})
        description = """Used to look up values to filter on. Input is an approximate spelling of the proper noun, output is \
        valid proper nouns. Use the noun most similar to the search."""
        retriever_tool = create_retriever_tool(
            retriever,
            name="search_proper_nouns",
            description=description,
        )
        extra_tools.append(retriever_tool)

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    system = """You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
    
    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database. 
    
    If you need to filter on a proper noun, you must ALWAYS first look up the filter value using the "search_proper_nouns" tool! 
    
    You have access to the following tables: {table_names}
    """

    prompt = ChatPromptTemplate.from_messages(
        [("system", system), ("human", "{input}"), MessagesPlaceholder("agent_scratchpad"), ]
    )
    agent = create_sql_agent(
        llm=llm,
        db=db,
        extra_tools=extra_tools,
        prompt=prompt,
        agent_type="openai-tools",
        verbose=False,
    )
    return agent

agent = initialize_agent()

def make_output(prompt):

    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

    conversation_history += f"\nuser: {prompt}"

    output = agent.invoke({"input": conversation_history})

    return output['output']

def modify_output(input):
    for text in input.split():
        yield text + " "
        time.sleep(0.1)


if prompt := st.chat_input("What is your question?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = make_output(prompt)

    with st.chat_message("assistant", avatar=img_avatar):
        st.write_stream(modify_output(response))
        # st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()