# OpenAI API Reference 

This repository contains OpenAI API reference examples. 
* [OpenAI API Reference](https://platform.openai.com/docs/api-reference)


To install the official Python bindings, run the following command:
```bash
pip3 install openai
pip3 install PyPDF2
```

## The basics

1. Must have Python3.
2. Get repository
```bash
git clone https://github.com/msuliot/simple_ai.git 
```
3. use pip3 to install any dependencies.
```bash
pip3 install openai
pip3 install PyPDF2
```

## Open AI / ChatGPT

Make sure to get an OpenAI key from https://platform.openai.com/account/api-keys

Add your OpenAI key to the open_ai_key.py file
```bash
return "OPENAI_API_KEY" 
```

# Instructions:

1. ** Resume **
   - Put your resume in the resume folder
   - Your resume must be in PDF or text format


2. ** Job description **
   - Put the job description in the job_description folder
   - Go to any online job board and copy the job description
   - Paste the job description into a text file and save it as a text file in the job_description folder

3. ** Update the app.py **
    # set the job description and resume file names
        app_data["job_description_file_name"] = "THE_FILE_NAME.txt" # in job_description folder
        app_data["resume_file_name"] = "THE_RESUME.pdf" # in resume folder

4. ** Run the app.py **
    ```bash
    python3 app.py
    ``` 
