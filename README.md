# AWS Deployment Process Helper guide

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
		vi .env85
### press insert
### copy your api key and paste it there
### press esc and type :wq and hit enter

## In your launched instance
### go with the security tab and click security groups and 
### then edit edit inbound rule then click add rule and add port 8501
