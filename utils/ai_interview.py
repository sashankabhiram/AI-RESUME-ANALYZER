import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_interview_questions(resume_text, job_description=""):
    prompt = f"""
You are an expert Technical Recruiter and Hiring Manager.
Based on the candidate's resume and the job description, generate 5 interview questions to assess their fit for the role.

Resume:
{resume_text}

Job Description (if any):
{job_description}

Please provide 3 technical or role-specific questions and 2 behavioral/situational questions.

Return ONLY clean HTML.

Do NOT use Markdown.
Do NOT use ** or ##.
Do NOT use triple backticks.

Use this exact structure:

<h3>💻 Technical Questions</h3>
<ol>
<li>Question 1</li>
<li>Question 2</li>
<li>Question 3</li>
</ol>

<h3>🤝 Behavioral Questions</h3>
<ol>
<li>Question 1</li>
<li>Question 2</li>
</ol>

Keep the questions professional, targeted to their experience, and concise.
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
            temperature=0.4,
            max_tokens=450
        )
        content = response.choices[0].message.content
        content = content.replace("```html", "").replace("```", "").strip()
        return content
    except Exception as e:
        return f"<p>AI Interview Questions Error: {str(e)}</p>"
