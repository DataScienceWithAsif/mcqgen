import os
import json
import pandas as pd
import traceback

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI
from langchain_community.callbacks.manager import get_openai_callback

import PyPDF2

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.logger import logging


# load environment variables from .env file
load_dotenv()
# access env variables just like with os.environ
key=os.getenv('openai_api_key')

llm=ChatOpenAI(openai_api_key=key, model_name='gpt-3.5-turbo', temperature=0.5)

TEMPLATE="""
Text : {text}
You are an expert mcq maker. Given the above text, it is your job to \
create a quiz of {number} multiple choices questions for {subject} students in {tone} tone.
make sure the questions are not repeated and check all the questions to be conforming the text as well.
make sure to format your response like RESPONSE_JSON below and use it as guide. \
Ensure to make {number} mcqs.
### RESPONSE_JSON
{Response_Json}

"""
quiz_generation_prompt = PromptTemplate(
    input_variables=['text','number', 'subject', 'tone', 'Response_Json'],
    template=TEMPLATE
)

quiz_chain=LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key='quiz')

TEMPLATE2="""
you are an expert English grammarian and writer. Given a multiple choice quiz for {subject} students. \
you need to evaluate the complexity of questions and give a complete analysis of quiz.only use at max 50 words for complexity.
if the quiz is not as per with the cognitive and analytical abilities of the students. \
Update the quiz questions wich needs to be changed and change the tone such that it perfectly fits the students ability.
Quiz_MCQs.
{quiz}

Check from an expert English Writer of the above quiz:
"""
quiz_evaluation_prompt=PromptTemplate(
    input_variables=['subject','quiz'],
    template=TEMPLATE2
)

review_chain=LLMChain(llm=llm, prompt=quiz_evaluation_prompt, output_key='review')

generate_evaluate_chain=SequentialChain(chains=[quiz_chain,review_chain],input_variables=['text','number', 'subject', 'tone', 'Response_Json'],
                                        output_variables=['quiz','review'], verbose=True)