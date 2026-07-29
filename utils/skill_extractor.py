import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_skills(text):
    prompt = f"""
You are an expert Technical Recruiter.
Analyze the following resume text and extract all notable technical and soft skills.
Return ONLY a JSON list of strings representing the skills found. 
Do not include any other text, markdown, or backticks.

Resume:
{text}

Example format:
[
  "Python",
  "React",
  "Project Management",
  "AWS",
  "Communication"
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
            temperature=0.2,
            max_tokens=300
        )
        content = response.choices[0].message.content
        match = re.search(r'\[.*\]', content, re.DOTALL)
        if match:
            content = match.group(0)
        
        data = json.loads(content)
        return data if isinstance(data, list) else []
    except Exception as e:
        print(f"Skill Extraction Error: {e}")
        return []