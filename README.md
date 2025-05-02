# 🧠 Resume Matcher App

This is a Python-based application that matches job descriptions with the most relevant version of Anushka Kamalja's resume. It automatically identifies matching technical skills from a job post, selects the most appropriate resume based on tech stack, and generates a personalized cold outreach email to recruiters.

---

## 🔍 Features

- Extracts key technical skills from job descriptions using an LLM
- Matches those skills against a defined tech stack → resume mapping (`tech_stack_resume_mapping.csv`)
- Retrieves and links the best-matching resume
- Highlights matched skills in the cold email for personalization
- Generates a concise, custom cold email with a professional signature

---


## 💾 Setup Instructions

1. Clone the repository
   
   git clone https://github.com/anushkakamalja/Cold_email_app.git
   cd resume-matcher-app


2. Install dependencies

    pip install -r requirements.txt
3. Run teh app:

    streamlit run main.py


🛠️ Technologies Used
    - Python

    - ChromaDB

    - OpenAI / LLMs

    - Pandas

✨ Future Improvements
1. Parse actual resume text to extract real-time matching skills

2. Extract hiring manager details.

3. Store a table of all applications submitted

