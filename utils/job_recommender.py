import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def recommend_jobs(resume_text):
    prompt = f"""
You are an expert Technical Recruiter and Career Counselor.
Based on the following resume text, suggest the top 5 most realistic job titles the candidate is highly suited for. 
Take into account their skills, experience, and the tools they know.

Resume:
{resume_text}

Return the data STRICTLY as a JSON list of strings representing the job titles. Do not include any other text, markdown, or backticks.

Example of the EXACT JSON structure you must use:
[
  "Python Developer",
  "Data Engineer",
  "Backend Developer",
  "Cloud Engineer",
  "Software Engineer"
]
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=150
        )
        content = response.choices[0].message.content
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            content = match.group(0)
        
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Job Recommendation Error: {e}")
        return ["Software Developer"]