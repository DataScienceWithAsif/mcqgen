# AWS Deployment Process Helper guide

## Project overview

This project is an AI-powered **MCQ Generator** built with **Python, Streamlit, and LangChain**.
It helps users generate multiple-choice questions from uploaded study material (PDF or TXT),
and then provides a short quality review of the generated quiz.

### What this project does

- Accepts a **PDF** or **TXT** file as input content.
- Lets the user choose:
  - Number of questions
  - Subject
  - Difficulty/tone (for example: Simple, Normal, Hard)
- Uses an OpenAI model through LangChain to:
  1. Generate MCQs in a structured JSON format.
  2. Evaluate the quiz for language quality and level suitability.
- Displays questions in a table inside Streamlit.
- Allows downloading generated MCQs as a **CSV** file.
- Shows token usage and estimated API cost for transparency.

### Main project components

- `StreamlitApp.py`  
  UI entry point. Handles user input, file upload, chain execution, and CSV download.

- `src/mcqgenerator/MCQGenerator.py`  
  Contains the LangChain prompt templates and sequential chain used for quiz generation + review.

- `src/mcqgenerator/utils.py`  
  Utility helpers for reading uploaded files and converting generated quiz JSON into tabular data.

- `Response.json`  
  Reference output schema used to guide the model’s quiz JSON format.

### End-to-end flow

1. User uploads a file and provides quiz settings.
2. Text is extracted from the uploaded file.
3. AI generates MCQs from the extracted text.
4. A second AI pass reviews/evaluates the generated quiz.
5. Results are shown in table format and can be exported as CSV.

### Requirements to run

- Python environment with dependencies from `requirements.txt`
- OpenAI API key available in environment (for example through `.env`)
- Streamlit app execution:
  `python3 -m streamlit run StreamlitApp.py`

## Ubuntu terminal working steps and commands:

 ## First login to aws/console --> https://aws.amazon.com/

## search about EC2

## You need to Config Ubuntu Machine

## Launch the Instance

## Update the machine:
	sudo apt update
	sudo apt-get update
	sudo apt upgrade -y
	sudo apt install git curl unzip tar make sudo vim wget
	
###  git clone " Your-Repo-Link "

	sudo apt install python3-pip
	
 ## (optional and recommended)
	python -m venv venv
	source venv/bin/activate
	pip3 install -r requirements.txt 
	
	python3 -m streamlit run StreamlitApp.py (Your streamlit file name)

## if you want to add openai api key in your project
### create .env file in your server
	touch .env
	vi .env
### press insert
### copy your api key and paste it there
### press esc and type 
	:wq
### and hit enter

## In your launched instance
### go with the security tab and click security groups and 
### then edit edit inbound rule then click add rule and add port 8501


