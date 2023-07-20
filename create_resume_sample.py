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

#################### SET LOCAL VARS #####################
job_description_file_name = "chief_tech_ASC.txt" # in job_description folder
resume_file_name = "michael1.pdf" # in resume folder
resume_format = "pdf" # pdf, txt
openai_model = "gpt-3.5-turbo" # gpt-4, gpt-4-0613, gpt-3.5-turbo, gpt-3.5-turbo-16k, gpt-3.5-turbo-0613
temperature=1.3 # 0.0 - 2.0 (higher = more creative) 
use_as_base = "jd" # res, jd
#########################################################

messages = []

# get job description and resume
job_description, resume = Helper.get_resume_and_job_description(job_description_file_name, resume_file_name, resume_format)

system_prompt = Helper.create_system_prompt_resume()
messages = Helper.add_prompt_messages("system", system_prompt , messages)

if use_as_base == "res" :
    print("creating sample resume based on the resume you provided: " + resume_file_name)
    user_prompt = Helper.create_prompt_resume("resume", resume) 
elif use_as_base == "jd" :
    print("creating sample resume based on the job description you provided: " + job_description_file_name)
    user_prompt = Helper.create_prompt_resume("job description", job_description) 
else :  
    print("error: use_as_base must be res or jd")
    sys.exit()

messages = Helper.add_prompt_messages("user", user_prompt , messages)
custom_resume = Helper.get_chat_completion_messages(messages, model=openai_model, temperature=temperature) 
print(custom_resume)

html_messages = []
# create a system prompt
html_system_prompt = Helper.create_system_prompt_html()
html_messages = Helper.add_prompt_messages("system", html_system_prompt , html_messages)

html_prompt = Helper.create_prompt_html(custom_resume)
html_messages = Helper.add_prompt_messages("user", html_prompt , html_messages)

html_resume = Helper.get_chat_completion_messages(html_messages, model=openai_model, temperature=temperature) 

# print(custom_resume)
html_file = 'html/' + str(random_number) + ".html"
with open(html_file, 'w') as file:
        file.write(html_resume)
        webbrowser.open("file:///Users/msuliot/Documents/code/resume_sync/" + html_file)