import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain_community.callbacks.manager import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open(r'Response.json','r') as file:
    Response_Json=json.load(file)
    
st.title("MCQs Creator Application using LangChain....!!!!")

with st.form("User_inputs"):
    uploaded_file=st.file_uploader("upload a pdf or txt file")
    
    mcq_count=st.number_input("No.of MCQs",min_value=3,max_value=50)
    subject=st.text_input("Insert Subject",max_chars=20)
    tone=st.text_input("Complexity level of questions",max_chars=20,placeholder="Simple | Normal | Hard")
    # Add button
    button=st.form_submit_button("Create MCQs")
    
if button and uploaded_file is not None and mcq_count and subject and tone:
    with st.spinner('loading......'):
        try:
            text=read_file(uploaded_file)
            
            with get_openai_callback() as cb:
                response=generate_evaluate_chain(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "Response_Json":json.dumps(Response_Json)
                    }
                )
            
        except Exception as e:
            traceback.print_exception(type(e),e,e.__traceback__)
            st.error("Error")
            
        else:
            print('total tokens      : ',cb.total_tokens)
            print('prompt tokens     :',cb.prompt_tokens)
            print('completion tokens :',cb.completion_tokens)
            print('total cost        :',cb.total_cost)
            
            if isinstance(response,dict):
                quiz=response.get("quiz",None)
                
                if quiz is not None:
                    table_data=get_table_data(quiz)
                    if table_data is not None:
                        df=pd.DataFrame(table_data)
                        df.index=df.index+1
                        st.table(df)
                        # display the review in a text box as well
                        st.text_area(label="review",value=response['review'])
                    else:
                        st.error("Error in the table data")
            else:
                st.write(response)
    