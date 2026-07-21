import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_career_fit(resume_text):
    prompt = f"""
You are an expert Technical Recruiter and Career Counselor.
Your task is to provide an ACCURATE, EVIDENCE-BASED career fit analysis. Do NOT blindly assign arbitrary percentages. 
You must critically analyze the explicit skills, tools, and years of experience actually present in the resume. 
Identify the top 4 job roles the candidate is highly suited for, and calculate a realistic match percentage (0-100) based strictly on how their current skillset maps to the standard industry requirements for those roles.

Resume:
{resume_text}

IMPORTANT: You must generate REAL roles derived directly from the candidate's skills. The percentages must reflect true readiness (e.g., if they lack a critical core skill for a role, the percentage should be lower). Do NOT just copy the example below.

Return the data STRICTLY in this JSON format. Do not include any other text, markdown, or backticks.

Example of the EXACT JSON structure you must use (this example is for a fictional Astronaut, you must generate content relevant to the uploaded resume!):
[
  {{"role": "Space Station Commander", "match_percentage": 96}},
  {{"role": "Lunar Rover Pilot", "match_percentage": 82}},
  {{"role": "Astrophysicist", "match_percentage": 75}},
  {{"role": "Zero-G Botanist", "match_percentage": 60}}
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
            max_tokens=300
        )
        content = response.choices[0].message.content
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            content = match.group(0)
        
        data = json.loads(content)
        return data
    except Exception as e:
        print(f"Career Fit Error: {e}")
        return []
