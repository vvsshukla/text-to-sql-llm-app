from dotenv import load_dotenv
load_dotenv() ##load all env variables
import streamlit as st
import os
import google.generativeai as genai
from connect import connect
from config import load_config

## Configure Genai Key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

## Function to load Google Gemini model and provide quries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt[0], question])
    return response.text

## Function to retrieve query from the database
def read_sql_query(sql):
    config = load_config()
    conn = connect(config)
    print(sql)
    cur = conn.cursor(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows
    
## Define Your Prompt
prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database has the name studentlist and has the follwing columns - name, class,
    section\n\nFor example, \nExample 1 - How many entries of records are present?,
    the sql command will be something like this SELECT count(*) from studentlist ;
    \nExample 2 - Tell me all the students studying in data science class?,
    the sql command will be something like this SELECT * from studentlist where
    class = 'Data Science';
    also the sql code should not have ``` in beginning or end and sql word in output
    """
]

## Streamlit App
st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retieve SQL Data")
question = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit:
    response = get_gemini_response(question, prompt)
    response = read_sql_query(response)
    st.subheader("The Response is:")
    for row in response:
        st.header(row)
