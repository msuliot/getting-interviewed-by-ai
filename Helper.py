import openai
import json
import os
import sys
import key.open_ai_key as open_api_key
from PyPDF2 import PdfReader
import webbrowser

def open_web_page(url):
    webbrowser.open(url)

def clear_screen():
    _ = os.system('clear')

def add_prompt_messages(role, content, messages):
    json_message = {
        "role": role, 
        "content": content
    }
    messages.append(json_message)
    return messages

def parse_file_name(file_name: str):
    name, extension = os.path.splitext(file_name)
    # Since splitext returns extension with dot, we remove it
    extension = extension.lstrip('.')
    return name, extension


def get_chat_completion_messages(messages, model="gpt-3.5-turbo", temperature=0.0): 
    try:
        response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    except openai.error.AuthenticationError as e:
        #Handle authentication error (e.g. invalid credentials)
        print(f"OpenAI API request failed due to invalid credentials: {e}")
        pass
    except openai.error.InvalidRequestError as e:
        #Handle invalid request error (e.g. required parameter missing)
        print(f"OpenAI API request failed due to invalid parameters: {e}")
        pass
    except openai.error.ServiceUnavailableError as e:
        #Handle service unavailable error
        print(f"OpenAI API request failed due to a temporary server error: {e}")
        pass
    else:
        # code to execute if no exception was raised
        # print(response)
        return response.choices[0].message["content"]
        # return response.choices[0].message


def create_prompt_job_interview_questions(number_of_questions):
    prompt = f"""
        Your task is to generate a list of {number_of_questions} questions for job interview between a hiring manager, and a job candidate.
        The quesiton should be relevant to the job posting, and the resume of the candidate.
        Very important to only respond in JSON format, with the following keys:
        id:
        question:

        double check your response is in JSON format.
        """
    return prompt


def create_prompt_to_improve_resume(number_of_items):
    prompt = f"""
        i really want to improve my resume You better align with the job description and improve my score, create me a list of {number_of_items} things to improve my resume.
        Very important to only respond in JSON format, with the following keys:
        id:
        improvement:

        double check your response is in JSON format.
        """
    return prompt


def create_prompt_pro_con(number_of_items):
    prompt = f"""
        You are a hiring manager. Your task is to generate a list of {number_of_items} pros and cons for a job candidate.

        Very important to only respond in JSON format, with the following keys:
        pros:
        cons:

        double check your response is in JSON format.
        """
    return prompt

def create_default_system_prompt():
    DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
"""

    return DEFAULT_SYSTEM_PROMPT

def create_prompt_base(data):
    prompt = f"""
        You are a data scientist. Your task is to summary of the data and provide 500 word summary and bullet point list or 20 items what are important.
        Here is your data enclosed in 3 backticks: ```{data}```.
        """
    return prompt


def create_system_prompt():
    system_prompt = f"""
    You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

    If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.

    As a hiring manager, your responsibility is to evaluate the qualifications and skills of candidates for a specific job opening. Your task is to generate a relevance score that indicates how closely the candidate's resume matches the job description. The scoring scale ranges from 0 to 100, with 100 representing a perfect match and 0 indicating no match.

    To calculate the relevance score, compare the job description with the candidate's resume and assess the alignment of their qualifications and skills. Consider factors such as relevant work experience, education, certifications, and any specific requirements mentioned in the job description.

    Also, include your reasoning for the score.

    double check your score, reasoning and resume facts before submitting it to the hiring manager.
    """
    return system_prompt


def create_prompt_job_match(job_description, resume):
    prompt = f"""
    Here's a template you can use to generate the relevance score:
    job_description = ```{job_description}```

    resume = ```{resume}```

    # Perform relevance assessment
    score = calculate_relevance_score(job_description, resume)

    # Round the score to two decimal places
    rounded_score = round(score, 2)

    # Output the relevance score
    responed with ONLY floating-point number rounded to 2 decimal places between 0 and 100.

    # job_description requirements
    If there are any job descriptions that resume does not have, respond with a list of missing requirements and take 20 points off the score.

    Very important to only respond in JSON format, with the following keys:
        reasoning:
        score:
        missing_requirements:

    double check your response is in JSON format.
    """
    return prompt

def create_prompt_job_match_v2(job_description, resume):
    prompt = f"""
Here's a template you can use to generate the relevance score:
Here's are some examples way to do it:

1. Identify the key requirements in the job description.
2. Compare these requirements with the candidate's resume.
3. Assign points based on the alignment.
4. Add up the points to get the total score. In this case
5. Make sure to point out missing requirements in education, job duties or any others

Very important to only respond in JSON format, with the following keys:
    reasoning:
    score:
    missing_requirements:

    job_description = ```{job_description}```

    resume = ```{resume}```

    double check your response is in JSON format.
    """
    return prompt

def create_system_prompt_job_description():
    system_prompt = f"""
    As a hiring manager, your responsibility is to create job descriptions.

    When creating a job description, it's important to provide clear and concise information about the position to attract the best candidates. Here are some main bullet points to consider:

1. Job Title: Clearly state the job title that accurately reflects the role.

2. Company Overview: Provide a brief overview of your company, its mission, values, and culture.

3. Job Summary/Objective: Summarize the primary purpose of the role and what the candidate will be responsible for achieving.

4. Responsibilities: Outline the specific duties, tasks, and responsibilities the candidate will be expected to fulfill. Use action verbs to describe each responsibility.

5. Qualifications: Specify the essential qualifications, skills, experience, and education required for the position. Differentiate between "required" and "preferred" qualifications.

6. Competencies: Identify the key competencies, both technical and soft skills, that the candidate should possess to excel in the role. This may include communication skills, problem-solving abilities, teamwork, leadership, etc.

7. Reporting Structure: Clarify the position's place within the company hierarchy and to whom the candidate will report.

8. Work Environment: Briefly describe the work environment, including the office setup, remote work possibilities, or any other relevant information.

9. Compensation and Benefits: Provide a general idea of the salary range and benefits package, or mention that it will be discussed during the interview process.

10. Application Process: Explain how candidates should apply (e.g., online application, email, or physical submission) and include any required materials such as resumes, portfolios, or references.

11. Deadline: Specify the deadline for applications or mention that the position will remain open until filled.

12. Equal Opportunity Employer Statement: Include a statement affirming your commitment to equal opportunity employment and diversity.

13. Company Contact Information: Provide relevant contact information for candidates to reach out with questions or inquiries.

Remember, it's essential to tailor the job description to the specific role and your company's needs while being transparent and informative to attract the most qualified candidates.
    """
    return system_prompt

def create_prompt_job_description(resume):
    prompt = f"""
    Your task is to generate a job description based on this resume ```{resume}```. 
    The job description should be The ideal job for the resume you have. 
    """
    return prompt


def create_system_prompt_resume():
    system_prompt = f"""
    As a person looking for a job, your responsibility is to create a resume.
    When creating a résumé for the technology field with many years of experience, there are several key items you should include to highlight your skills, accomplishments, and expertise. Here are the top elements to consider:

1. Contact Information: Include your full name, professional title, phone number, email address, and optionally, your LinkedIn profile URL.

2. Professional Summary/Objective: Write a concise statement at the beginning of your résumé that summarizes your experience, skills, and areas of expertise. Tailor this section to the specific job you're applying for.

3. Work Experience: List your work history in reverse chronological order, starting with your most recent position. Include the following details for each role:
   - Job title, company name, and location.
   - Employment dates (month and year).
   - Key responsibilities and accomplishments.
   - Technological tools, programming languages, or frameworks you used.
   - Any notable projects you worked on and their outcomes.
   - Any leadership or managerial roles you held.

4. Skills: Highlight your technical skills, software proficiencies, programming languages, and any relevant certifications or training you have acquired over the years. Be specific and mention both your foundational skills and any advanced or specialized expertise you possess.

5. Education: Include your educational background, starting with your highest degree. Provide the institution name, degree earned, major or field of study, and graduation year. If you have attended any relevant workshops, conferences, or obtained additional certifications, mention them here.

6. Professional Achievements: Showcase any notable achievements, awards, or recognition you have received throughout your career. This could include accolades for innovative projects, patents, publications, or industry-related honors.

7. Professional Associations and Affiliations: Mention any memberships or affiliations with relevant professional organizations, such as IEEE, ACM, or industry-specific associations. Also, include any leadership positions you held within these organizations.

8. Continuing Education and Training: Highlight any ongoing professional development activities you have pursued, such as attending conferences, completing online courses, or participating in workshops. This demonstrates your commitment to staying current in the field.

9. Publications and Presentations: If you have authored technical papers, published articles, or delivered presentations at conferences or industry events, list them in a separate section.

10. References: Optionally, you can provide references from individuals who can vouch for your professional capabilities and character. Include their names, titles, contact information, and their relationship to you (e.g., former supervisor, colleague, or client). Make sure to seek their permission before including their details.

Remember to tailor your résumé to each job application by highlighting the skills and experiences that align with the specific position you are seeking. Use action verbs, quantify your achievements when possible, and keep the document concise and easy to read.
   
    
      """
    return system_prompt


def create_prompt_resume(task, data):
    prompt = f"""
    you have received a {task} for the data needed to create or improve a resume.
    Your task is to create or improve a resume based on the 
    {task} enclosed with three backticks ```{data}```. 
    The resume should be the ideal candidate for the {task} you have. 
    The resume should have all necessary requirements, skills and experience expected based on the {task}.
    Remember to tailor your resume to match the requirements and responsibilities mentioned in the {task}. 
    Use action verbs, quantify your achievements when possible, and keep the document concise and easy to read.
    Remember to fill in all information.

    Professional summary is the most important part of this resume make it at least three paragraphs long and include highlights of career and goals.

    Here's some contact information to include, if not provided by the {task}:
    Make sure to display the contact information in a professional manner as needed:
    [full name: "Michael AI"]
    [professional title: "AI Enthusiast"]
    [phone number: "480-555-1212"]
    [email address: "michael-ai@email.com"]
    [LinkedIn profile URL: "https://www.linkedin.com/in/suliot"]
    [address: "1234 Main St, Anytown, AZ 12345"]
    [website: "https://www.michael-ai.com"]
    [github: "https://github.com/msuliot"]
    [youtube: "https://www.youtube.com/@michael-ai"]

    Work experience should also have five bullet points of achievements for each job in quantitative results. 
    Quantitative results example, "Increased sales by 20% in 2019" or "Reduced costs by 10% by implementing a new process". 
    
    Make sure the output has all the recommended sections and information.
    output should be in a text format.
    """
    return prompt   
# Output your results in HTML format 12 point font and single spaced.

def create_system_prompt_html():
    system_prompt = f"""
    You are a html web designer with outstanding design skills and a passion for creating websites for resumes.
    """
    return system_prompt

def create_prompt_html(data):
    prompt = f"""
    Your task is to take the data and create a fantasic HTML resume.

    You will receive the data in the format of a JSON object.

    Here is your data enclosed and three backticks: ```{data}```

    you must output your results in HTML format and only the report you have created and nothing more.
    """
    return prompt

def is_json(json_string):
    try:
        # Attempt to parse the JSON string
        json_data = json.loads(json_string)
        # If parsing is successful, the JSON is valid
        return True
    except ValueError as e:
        # Catch any ValueError, indicating invalid JSON
        print("Invalid JSON:", e)
        return False


def get_resume_and_job_description(job_description_file_name, resume_file_name):

    resume_name, resume_format = parse_file_name(resume_file_name)

    # print(f'File name: {name}')
    # print(f'File extension: {extension}')

    # import job description, convert to text and save to file
    print("***** Importing job description: " + job_description_file_name)
    job_description = import_text_file("job_description/" + job_description_file_name)
    if job_description:
        print("+++++ Job description was imported.")
        #print(file_content)
    else:
        print("----- No job description was imported.")

    print("***** Importing resume: " + resume_file_name)
    if resume_format == "pdf":
        resume = convert_pdf_to_text("resume/" + resume_file_name)
        if resume:
            print("+++++ Resume was imported.")
            #print(file_content)
        else:
            print("----- No PDF resume was imported.")
    elif resume_format == "txt":
        # import resume, convert to text and save to file
        resume = import_text_file("resume/" + resume_file_name)
        if resume:
            print("+++++ Resume was imported.")

    #print(text)
    # write_text_to_file('resume/resume.txt', resume)
        else:
            print("----- No TXT resume was imported.")
    else:  
        print("----- Resume format is not supported. Exiting.")

    if not job_description or not resume:
        print("!!!!! No job description or resume was imported. Exiting.")
        sys.exit()

    return job_description, resume

# import a pdf and convert to text
def convert_pdf_to_text(path):
    try:
        with open(path, "rb") as filehandle:
            pdf = PdfReader(filehandle)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except FileNotFoundError:
        print(f"The file {path} does not exist.")
    except:
        print("An unexpected error occurred.")

# import a text file
def import_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except IOError:
        print(f"Error: Unable to read file '{file_path}'.")

# write text to a file
def write_text_to_file(filename, text):
    try:
        with open(filename, 'w') as f:
            f.write(text)
        print(f"Text successfully written to {filename}")
    except:
        print("An error occurred while writing the file.")
