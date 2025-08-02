import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# Load Response.json (make sure it's in same directory or correct path)
try:
    with open('Response.json', 'r') as file:
        Response_Json = json.load(file)
except FileNotFoundError:
    st.error("❌ Response.json file not found. Please ensure it exists in your working directory.")
    st.stop()

st.title("🧠 MCQs Creator Application using LangChain")

# File upload and inputs
with st.form("User_inputs"):
    uploaded_file = st.file_uploader("📄 Upload a PDF or TXT file")
    mcq_count = st.number_input("📝 No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("📚 Subject", max_chars=20)
    tone = st.text_input("🎯 Complexity level of questions", max_chars=20, placeholder="Simple | Normal | Hard")
    button = st.form_submit_button("⚙️ Create MCQs")

df = None  # Declare df globally for access outside form

# Main logic
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner('⏳ Processing...'):
        try:
            text = read_file(uploaded_file)

            with get_openai_callback() as cb:
                response = generate_evaluate_chain({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "Response_Json": json.dumps(Response_Json)
                })

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__)
            st.error("⚠️ Something went wrong.")
        else:
            # Token info
            st.markdown(f"""
                **Token Usage:**
                - Total Tokens: `{cb.total_tokens}`
                - Prompt Tokens: `{cb.prompt_tokens}`
                - Completion Tokens: `{cb.completion_tokens}`
                - Estimated Cost: `${cb.total_cost:.6f}`
            """)

            if isinstance(response, dict):
                quiz = response.get("quiz", None)
                if quiz is not None:
                    table_data = get_table_data(quiz)
                    if table_data is not None:
                        df = pd.DataFrame(table_data)
                        df.index = df.index + 1
                        st.table(df)
                        st.text_area(label="📋 Review", value=response['review'], height=200)
                    else:
                        st.error("❌ Error in table data.")
                else:
                    st.write(response)
            else:
                st.write(response)

# Download button — browser download, not server save
if df is not None:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download MCQs as CSV",
        data=csv_data,
        file_name=f"Generated_MCQs_{subject}.csv",
        mime='text/csv'
    )
