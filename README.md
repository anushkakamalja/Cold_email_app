# 📧 Cold Email Generator

This app helps you generate personalized cold emails for job applications by scraping job postings, matching your resume skills, and composing a tailored email using LLMs.

## Features
- Scrapes job postings from a provided URL
- Extracts job details using LLMs (Groq API)
- Matches your resume skills to job requirements
- Generates a personalized cold email for each job
- Simple Streamlit web interface

## Requirements
- Python 3.8+
- A valid Groq API key

## Installation
1. **Clone the repository:**
   ```sh
   git clone https://github.com/anushkakamalja/Cold_email_app.git
   cd cold_email
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the project root:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

## Usage
1. **Run the app:**
   ```sh
   streamlit run main.py
   ```
2. **Open your browser:**
   - Go to the local URL provided by Streamlit (usually http://localhost:8501)
3. **Enter a job posting URL** and click Submit to generate a cold email.

## Notes
- Your `.env` file should never be committed to version control (see `.gitignore`).
- Make sure your Groq API key is valid and has access to the required models.

## License
MIT

🛠️ Technologies Used
    - Python

    - ChromaDB

    - OpenAI / LLMs

    - Pandas

✨ Future Improvements
1. Parse actual resume text to extract real-time matching skills

2. Extract hiring manager details.

3. Store a table of all applications submitted

