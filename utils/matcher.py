import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

from utils.skill_extractor import extract_skills

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def calculate_match(resume_text, job_description):
    
    if not job_description or not job_description.strip():
        # Fallback: Just extract skills from resume
        resume_skills = extract_skills(resume_text)
        return 0, [], [], resume_skills

    prompt = f"""
You are an expert ATS (Applicant Tracking System) software.
Analyze the provided resume against the job description.

Extract all technical and soft skills present in the resume.
Extract the required skills from the job description.
Compare them to calculate a realistic match percentage (0-100).

Resume:
{resume_text}

Job Description:
{job_description}

Return ONLY valid JSON exactly matching the structure below. Do not include any other text, markdown, or backticks.

{{
  "score": 85,
  "matched_skills": ["Python", "React", "Docker"],
  "missing_skills": ["Kubernetes", "AWS"],
  "resume_skills": ["Python", "React", "Docker", "Git", "HTML"]
}}
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
            max_tokens=400
        )
        content = response.choices[0].message.content
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            content = match.group(0)
        
        data = json.loads(content)
        
        score = int(data.get("score", 0))
        matched = data.get("matched_skills", [])
        missing = data.get("missing_skills", [])
        resume_skills = data.get("resume_skills", [])
        
        return score, matched, missing, resume_skills
        
    except Exception as e:
        print(f"ATS Matcher Error: {e}")
        resume_skills = extract_skills(resume_text)
        return 0, [], [], resume_skills