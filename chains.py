import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

import os
print("GROQ_API_KEY from .env:", repr(os.getenv("GROQ_API_KEY")))

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        temperature=0,
        groq_api_key=os.getenv("GROQ_API_KEY"),
    )
    def extract_jobs(self,cleaned_text):
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
        chain_extract = prompt_extract | self.llm
        result = chain_extract.invoke(input={"page_data": cleaned_text})
        str_parser = StrOutputParser()

        # json_result = json_parser.parse(result.content)
        parsed_str = str_parser.invoke(result)
        # Now convert the string to JSON
        try:
            json_result = json.loads(parsed_str)
            # print(json_result)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            print("Raw response was:", parsed_str)
        return json_result if isinstance(json_result,list) else [json_result]

    def write_mail(self, json_result, links):
        prompt_cold_email = PromptTemplate.from_template(
                                """
            ### JOB POSTING:
            {job_description}

            ### CANDIDATE INFO:
            - Name: Anushka Kamalja  
            - Education: MSIM Graduate Student, University of Washington  
            - Graduation: June 2025  
            - Resume Link: {resume_link}  
            - Matched Skills: {matched_skills}

            ### INSTRUCTIONS:
            You are an assistant helping a graduate student write a short, personalized cold email to a recruiter or hiring manager regarding a specific job posting.

            Your task is to write a concise, compelling email (maximum 5 sentences) that:

            1. Uses a neutral greeting (e.g., "Hi there" or "Hi [Hiring Team]") — **never greet Anushka herself**.
            2. Introduces Anushka Kamalja as a current MSIM graduate student at the University of Washington, graduating in June 2025.
            3. Expresses genuine enthusiasm for the specific role and company.
            4. Highlights **2–3 technical or domain-specific skills** from the `matched_skills` list that are relevant to the job.
            5. References her attached resume and politely offers to discuss her fit.
            6. Maintains a confident, respectful, and warm tone (avoid overly formal or robotic language).
            7. Uses clear paragraph formatting — insert **double line breaks between paragraphs**.
            8. Ends the email with the following signature:

            Best regards,  
            Anushka Kamalja  
            Phone: +1 (206)-228-7417  
            LinkedIn: https://www.linkedin.com/in/anushka-kamalja/  
            Portfolio: https://anushka-kamalja-portfolio.netlify.app/

            ### OUTPUT FORMAT:
            Cold Email:

            [Insert the email body here — do not include subject line or markdown/code formatting.]
            """


        )

        chain_cold_email = prompt_cold_email | self.llm

        result = chain_cold_email.invoke({
            "job_description": json_result["description"],
            "resume_link": links,  # This now contains your correct resume link
            "matched_skills": ", ".join(json_result["skills"])  # Format nicely
        })
        return result.content
    
if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))