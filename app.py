# Author: Michael Suliot (Michael AI)
# Date: 7/15/2023
# Version: 1.0
# Description: This application will take a job description and a resume Generate a score based on a match.
# Project: ResumeSync

import sys
import json
import openai
import Helper
import key.open_ai_key as open_api_key
from PyPDF2 import PdfReader
from datetime import datetime
import random
import webbrowser


openai.api_key = open_api_key.get_api_key()
current_date = datetime.now().date()
random_number = random.randint(10000000, 99999999)

Helper.clear_screen()

messages = []
app_data = {}


# report title and date
app_data["report_title"] = "ResumeSync: Intelligent Job Alignment Platform"
app_data["date"] = str(current_date)

# set the job description and resume file names
app_data["job_description_file_name"] = "chief_tech_ASC.txt" # in job_description folder
app_data["resume_file_name"] = "michael1.pdf" # in resume folder

# set the minimum score to continue
app_data["min_match"] = 80.0 # minimum match score to continue

# set the openai details
app_data["openai_model"] = "gpt-3.5-turbo"  # gpt-4, gpt-4-0613, gpt-3.5-turbo, gpt-3.5-turbo-16k, gpt-3.5-turbo-0613
app_data["temperature"] = 0.3 # 0.0 - 2.0 (higher = more creative)

# set default values
app_data["number_of_questions"] = 20 
app_data["number_of_resume_improvements"] = 7
app_data["number_of_pro_con"] = 7


# get job description and resume
job_description_data, resume_data = Helper.get_resume_and_job_description(
     app_data["job_description_file_name"], 
     app_data["resume_file_name"])

# create a system prompt
system_prompt = Helper.create_system_prompt()
messages = Helper.add_prompt_messages("system", system_prompt , messages)

# Score and reasoning
print("Adding score and reasoning")
user_prompt = Helper.create_prompt_job_match_v2(job_description_data, resume_data)
messages = Helper.add_prompt_messages("user", user_prompt , messages)
response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"]) 
Helper.add_prompt_messages("assistant",response, messages)

# check if the json is valid
json_valid = Helper.is_json(response)
if not json_valid:
    print("ChatGPT Error: Please try again.")
    print(response)
    sys.exit()

# get score and reasoning
try:
    data = json.loads(response) 
    app_data["score"] = int(data["score"])
    # app_data["reasoning"] = data["reasoning"]
    # app_data["missing_requirements"] = data["missing_requirements"]



    # print("Score: " + str(app_data["score"]))
    # print("Reasoning: " + str(app_data["reasoning"]))   
    # print("Missing Requirements: " + str(app_data["missing_requirements"]))

except Exception as e:
    print(e)
    sys.exit()

# ############# create pros and cons of the applicant
print("Adding pros and cons of the applicant")
user_prompt = Helper.create_prompt_pro_con(app_data["number_of_pro_con"])
messages = Helper.add_prompt_messages("user", user_prompt , messages)
response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"])
Helper.add_prompt_messages("assistant",response, messages)

# check if the json is valid
json_valid = Helper.is_json(response)
if not json_valid:
    print("ChatGPT Error: Please try again.")
    print(response)
    sys.exit()

# get score and reasoning
pros_and_cons = {}
pros = []
cons = []

try:
    data = json.loads(response) 
    for p in data["pros"]:
        pros.append(p)
    
    for c in data["cons"]:  
        cons.append(c)

    pros_and_cons["pros"]= pros
    pros_and_cons["cons"]= cons

    app_data["pros_and_cons"] = pros_and_cons

except Exception as e:
    print(e)
    sys.exit()


# create resume improvements
print("Adding resume improvements")
user_prompt = Helper.create_prompt_to_improve_resume(app_data["number_of_resume_improvements"])
messages = Helper.add_prompt_messages("user", user_prompt, messages)
response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"])
Helper.add_prompt_messages("assistant",response, messages)

# check if the json is valid
json_valid = Helper.is_json(response)
if not json_valid:
    print("ChatGPT Error: Please try again.")
    print(response)
    sys.exit()

# print(response)
# get score and reasoning
improvements = []

try:
    data = json.loads(response) 
    improvements_data = data["improvements"]
    for improvement in improvements_data:
        improvements.append(improvement["improvement"])

    app_data["improvements"] = improvements

except Exception as e:
    print(e)
    sys.exit()

# # create interview questions
# print("Adding interview questions")
# user_prompt = Helper.create_prompt_job_interview_questions(app_data["number_of_questions"])
# messages = Helper.add_prompt_messages("user", user_prompt , messages) 
# response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"])
# Helper.add_prompt_messages("assistant",response, messages)

# print('_' * 100)
# print("app_data")
# json_data = json.dumps(app_data, indent=4)
# print(json_data)
# print('_' * 100)
# print("messages")
# json_data = json.dumps(messages, indent=4)
# print(json_data)



# html_messages = []
# html_system_prompt = Helper.create_system_prompt_html()
# html_messages = Helper.add_prompt_messages("system", html_system_prompt , html_messages)
# html_prompt = Helper.create_prompt_html(consolidated_information)
# html_messages = Helper.add_prompt_messages("user", html_prompt , html_messages)

# html_page = Helper.get_chat_completion_messages(html_messages, model=openai_model, temperature=temperature) 

# # print(custom_resume)
# html_file = 'html/' + str(random_number) + ".html"
# with open(html_file, 'w') as file:
#         file.write(html_page)
#         # your path to the html file will be different
#         webbrowser.open("file:///Users/msuliot/Documents/code/getting-interviewed-by-ai/" + html_file)



def display_json(data, indent=0):
    for key, value in data.items():
        print('  ' * indent + str(key))
        if isinstance(value, dict):
            display_json(value, indent + 1)
        elif isinstance(value, list):
            for i in value:
                if isinstance(i, dict):
                    display_json(i, indent + 1)
                else:
                    print('  ' * (indent + 1) + str(i))
        else:
            print('  ' * (indent + 1) + str(value))


# display_json(app_data)

json_data = json.dumps(app_data, indent=4)
print(json_data)