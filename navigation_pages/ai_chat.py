import streamlit as st

container4 = st.container(border=True)
container4.subheader("Chat with AI")
container4.caption("Ask questions about your invoice data.")
user_input = container4.text_input("Ask a question about invoices:")
if user_input:
    container4.write(f"LLM Response: This is a placeholder for LLM's response to '{user_input}'")
container4.write("Feature coming soon..")

# from langchain_community.utilities import SQLDatabase
# from langchain_community.agent_toolkits import create_sql_agent
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# import os
#
# load_dotenv()
#
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#
# db = SQLDatabase.from_uri("sqlite:///../invoices_data.db")
# print(db.dialect)
# print(db.get_usable_table_names())
# db.run("SELECT * FROM invoices;")
# llm = ChatOpenAI(model="gpt-4o", temperature=0)
# agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
# output = agent_executor.invoke("how much did i spend on soy soy bling?")
# print(output)