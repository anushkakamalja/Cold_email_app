import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from resume import Resume
from utils import clean_text



def create_streamlit_app(llm, resume, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.cisco.com/jobs/ProjectDetail/Machine-Learning-Engineer/1441248?source=LinkedIn")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            resume.load_resume()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = resume.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    resume = Resume()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, resume, clean_text)