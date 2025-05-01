from langchain_groq import ChatGroq

llm = ChatGroq(
    model_name="llama-3.1-8b-instant",
    temperature=0,
    # max_tokens=8192,
    # timeout=10,
    # max_retries=3,
    groq_api_key="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",
)

from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://jobs.cisco.com/jobs/ProjectDetail/Machine-Learning-Engineer/1441248?source=LinkedIn")
page_data =loader.load().pop().page_content



# print(page_data)

from langchain_core.prompts import PromptTemplate

prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM WEBSITE:
    {page_data}
    ### INSTRUCTIONS:
    The scraped text is form the career page of a company.
    Your job is to extract the job postings and return them in JSON format containing the following keys:
    `role`, `company`, `location`, `experience`, `skills`, `description`, `link`
    Only return the valid JSON object, nothing else.
    ### VALID JASON (NO OTHER TEXT AT ALL, NO BACKTICKS, NO PREAMBLE)
    """
)

chain_extract = prompt_extract | llm

result = chain_extract.invoke(input={"page_data": page_data})

# print(result.content)


# from langchain_core.output_parsers.json import JSONOutputParser
from langchain_core.output_parsers import StrOutputParser
import json

# json_parser = JSONOutputParser()
str_parser = StrOutputParser()

# json_result = json_parser.parse(result.content)
parsed_str = str_parser.invoke(result)
# Now convert the string to JSON
try:
    json_result = json.loads(parsed_str)
    print(json_result)
except json.JSONDecodeError as e:
    print("Failed to parse JSON:", e)
    print("Raw response was:", parsed_str)

# print(json_result)
import pandas as pd

df = pd.read_csv("tech_stack_resume_mapping.csv")

import chromadb
import uuid

client = chromadb.PersistentClient("vector_store")

collection = client.get_or_create_collection("tech_stack_resume_mapping")

if not collection.count():  
    for index, row in df.iterrows():
        collection.add(
            documents=[row["Tech_Stack"]],
            metadatas= {'links': row["Resume_Link"]},
            ids=[str(uuid.uuid4())],
        )

print(collection.count())

#Prompt for writing a cold email

prompt_cold_email = PromptTemplate.from_template(
    """
    ### JOB POSTING:
    {job_description}
    
    ### CANDIDATE INFO:
    Name: Anushka Kamalja  
    Education: MSIM Graduate Student, University of Washington  
    Graduation: June 2025  
    Resume Link: {resume_link}  
    Matched Skills: {matched_skills}

    ### INSTRUCTIONS:
    You are an assistant helping a graduate student write a short, compelling cold email to a recruiter or hiring manager based on a job posting.

    Your task is to write a concise and personalized cold email (max 5 sentences) that:
    - Starts by introducing Anushka Kamalja as a current MSIM student at the University of Washington graduating in June 2025.
    - Expresses enthusiasm for the specific role and company.
    - Highlights 2–3 relevant technical or domain-specific skills matched to the job.
    - References her attached resume and politely offers to discuss her fit.
    - Maintains a confident, respectful, and warm tone (not overly formal or robotic).

    ### OUTPUT FORMAT:
    Cold Email:
    [Insert the email body here—no subject line or signature needed.]
    """
)

chain_cold_email = prompt_cold_email | llm

result = chain_cold_email.invoke(input={"job_description": json_result["description"], "resume_link": json_result["link"], "matched_skills": json_result["skills"]})

print(result.content)