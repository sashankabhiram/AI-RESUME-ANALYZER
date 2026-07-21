import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_chat_response(resume_text, score, question):
    prompt = f"""
You are an AI Recruiter chatting with a candidate about their resume.

Resume Text:
{resume_text}

Current ATS Score: {score}%

The candidate asks: "{question}"

Answer the candidate's question specifically and only based on the provided resume text and their score.
Be helpful, professional, and concise. Do NOT use markdown. Return plain text or simple HTML (like <br> for newlines if needed, but plain text is fine).
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
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
