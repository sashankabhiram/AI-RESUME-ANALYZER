import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_ai_feedback(resume_text, job_description, score):

    prompt = f"""
You are a Senior Technical Recruiter with over 15 years of hiring experience.

Analyze the candidate's resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Current ATS Score:
{score}%

Return ONLY clean HTML.

Do NOT use Markdown.
Do NOT use ** or ##.
Do NOT use triple backticks.

Use this exact structure:

<h2>Resume Analysis</h2>

<h3>📝 Overall Evaluation</h3>
<p>Write 3-5 sentences explaining how well the resume matches the job.</p>

<h3>💪 Key Strengths</h3>
<ul>
<li>Strength 1</li>
<li>Strength 2</li>
<li>Strength 3</li>
</ul>

<h3>📈 Areas for Improvement</h3>
<ul>
<li>Improvement 1</li>
<li>Improvement 2</li>
<li>Improvement 3</li>
</ul>

<h3>✅ Hiring Recommendation</h3>
<p>
Mention one of these:
Strongly Recommended,
Recommended,
Recommended with Improvements,
Not Recommended.

Explain why.
</p>

Keep the response professional, concise, and under 250 words.
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
            max_tokens=450
        )

        content = response.choices[0].message.content
        content = content.replace("```html", "").replace("```", "").strip()
        return content

    except Exception as e:
        return f"AI Feedback Error: {str(e)}"