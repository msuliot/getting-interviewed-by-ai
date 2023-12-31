# Getting Interviewed by AI

## YouTube Video Tutorial for this GitHub Repository
[Mastering AI Interviews](https://youtu.be/lAEvvGosJ20)

## The basics

1. Must have Python3.
2. Get repository
```bash
git clone https://github.com/msuliot/getting-interviewed-by-ai.git 
```
3. use pip3 to install any dependencies.
```bash
pip3 install -r requirements.txt
```

## Open AI / ChatGPT

Make sure to get an OpenAI key from https://platform.openai.com/account/api-keys

Create a ".env" file and put your OpenAI key in that file
```bash
OPENAI_API_KEY='your key here'
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
   - app_data["job_description_file_name"] = "THE_FILE_NAME.txt" # in job_description folder
   - app_data["resume_file_name"] = "THE_RESUME.pdf" # in resume folder

4. ** Run the app.py **
    ```bash
    python3 app.py
    ``` 
