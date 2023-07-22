# Author: Michael Suliot (Michael AI)
# Date: 7/15/2023
# Version: 1.0
# Description: This application will take a job description and a resume generate a score based on a match.
# Project: ResumeSync

import json
import openai
import Helper
import key.open_ai_key as open_api_key
from PyPDF2 import PdfReader
from datetime import datetime
import random

openai.api_key = open_api_key.get_api_key()
current_date = datetime.now().date()
random_number = random.randint(10000000, 99999999)

Helper.clear_screen()

messages = []
app_data = {}
res_jd_data = {}
all_data = {}

# report title and date
app_data["report_title"] = "ResumeSync: Intelligent Job Alignment Platform"
app_data["date"] = str(current_date)

# set the job description and resume file names
app_data["job_description_file_name"] = "chief_tech_ASC.txt" # in job_description folder
app_data["resume_file_name"] = "michael1.pdf" # in resume folder

# set the minimum score to continue
app_data["minimum_score"] = 75.0 # minimum match score to continue

# Set the openai details - model and temperature
app_data["openai_model"] = "gpt-3.5-turbo-16k"
app_data["temperature"] = 0.1 # 0.0 - 2.0 (higher = more creative)

# set default values
app_data["number_of_questions"] = 40
app_data["number_of_resume_improvements"] = 10
app_data["number_of_pro_con"] = 5

print("=" * 100)
print(app_data["report_title"])
print("=" * 100)

# get job description and resume
job_description_data, resume_data = Helper.get_resume_and_job_description(
     app_data["job_description_file_name"], 
     app_data["resume_file_name"])

res_jd_data["job_description"] = job_description_data
res_jd_data["resume"] = resume_data

# create a system prompt
system_prompt = Helper.create_system_prompt()
messages = Helper.add_prompt_messages("system", system_prompt , messages)

# Score and reasoning
print("Adding score and reasoning")
user_prompt = Helper.create_prompt_job_match_v2(job_description_data, resume_data)
messages = Helper.add_prompt_messages("user", user_prompt , messages)
response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"]) 
Helper.add_prompt_messages("assistant",response, messages)

data = Helper.validate_json(response)
app_data["score"] = int(data["score"])
app_data["reasoning"] = data["reasoning"]
app_data["missing_requirements"] = data["missing_requirements"]


# ############# create pros and cons of the applicant
print("Adding pros and cons of the applicant")
user_prompt = Helper.create_prompt_pro_con(app_data["number_of_pro_con"])
messages = Helper.add_prompt_messages("user", user_prompt , messages)
response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"])
Helper.add_prompt_messages("assistant",response, messages)

data = Helper.validate_json(response)

pros_and_cons = {}
pros = []
cons = []

for p in data["pros"]:
    pros.append(p)

for c in data["cons"]:  
    cons.append(c)

pros_and_cons["pros"]= pros
pros_and_cons["cons"]= cons

app_data["pros_and_cons"] = pros_and_cons

# create resume improvements
print("Adding resume improvements")
user_prompt = Helper.create_prompt_to_improve_resume(app_data["number_of_resume_improvements"])
messages = Helper.add_prompt_messages("user", user_prompt, messages)
response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"])
Helper.add_prompt_messages("assistant",response, messages)

data = Helper.validate_json(response)

improvements = []

improvements_data = data["improvements"]
for improvement in improvements_data:
    improvements.append(improvement["improvement"])

app_data["improvements"] = improvements

# # create interview questions
print("Adding interview questions")
user_prompt = Helper.create_prompt_job_interview_questions(app_data["number_of_questions"])
messages = Helper.add_prompt_messages("user", user_prompt , messages) 
response = Helper.get_chat_completion_messages(messages, model=app_data["openai_model"], temperature=app_data["temperature"])
Helper.add_prompt_messages("assistant",response, messages)

data = Helper.validate_json(response)

questions = []

questions_data = data["questions"]
for question in questions_data:
    questions.append(question["category"])
    questions.append(question["question"])
    # questions.append(question["reason"])
    # questions.append(question["best_response"])

app_data["questions"] = questions

print("Creating ResumeSync Report")

html_messages = []
html_system_prompt = Helper.create_system_prompt_html()
html_messages = Helper.add_prompt_messages("system", html_system_prompt , html_messages)
html_prompt = Helper.create_prompt_html_report(app_data)
html_messages = Helper.add_prompt_messages("user", html_prompt , html_messages)

html_page = Helper.get_chat_completion_messages(html_messages, model=app_data["openai_model"], temperature=app_data["temperature"]) 

html_file = 'html/' + str(random_number) + ".html"
with open(html_file, 'w') as file:
        file.write(html_page)
        # your path to the html file will be different
        Helper.open_web_page("file:///Users/msuliot/Documents/code/getting-interviewed-by-ai/" + html_file)

print("DONE:")



# def display_json(data, indent=0):
#     for key, value in data.items():
#         print('  ' * indent + str(key))
#         if isinstance(value, dict):
#             display_json(value, indent + 1)
#         elif isinstance(value, list):
#             for i in value:
#                 if isinstance(i, dict):
#                     display_json(i, indent + 1)
#                 else:
#                     print('  ' * (indent + 1) + str(i))
#         else:
#             print('  ' * (indent + 1) + str(value))


# display_json(app_data)

# json_data = json.dumps(app_data, indent=4)
# print(json_data) 