import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_chat_response(resume_text, score, question):
    prompt = f"""
You are an AI Recruiter analyzing a candidate's resume.

Resume Text:
{resume_text}

Current ATS Score: {score}%

The candidate asks: "{question}"

Provide a direct, specific, and highly concise answer to the candidate's question based ONLY on the provided resume text and score. 
CRITICAL RULE: LIMIT YOUR RESPONSE TO A MAXIMUM OF 2 SENTENCES. DO NOT EXCEED THIS LIMIT. Do not write paragraphs.
Do not include any conversational filler, greetings, or generic advice. Answer dynamically and get straight to the point.
Do NOT use markdown. Return plain text or simple HTML (like <br> for newlines if needed).
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
            temperature=0.5,
            max_tokens=80
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
