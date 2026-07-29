import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_learning_roadmap(resume_text, job_description=""):
    prompt = f"""
You are an expert Career Coach and Technical Mentor.
Based on the candidate's resume and the job description, generate a structured Learning Roadmap to help them upskill for the role.

CRITICAL REQUIREMENT: The tone and language must be extremely easy to understand, as if you are explaining it to a 1st-year college student. Avoid overly complex jargon, and explain concepts simply.

Resume:
{resume_text}

Job Description (if any):
{job_description}

Identify the critical skill gaps. Create a beginner-friendly roadmap consisting of:
1. Short-Term Goals (0-1 Months) - Immediate priority skills (explained simply).
2. Medium-Term Goals (1-3 Months) - Next steps or tools to learn.
3. Recommended Resources - 3 to 4 specific beginner-friendly courses, books, or tutorials.

Return ONLY clean HTML. Do NOT use Markdown, **, or triple backticks.

IMPORTANT: You MUST generate real, highly personalized insights based entirely on the candidate's resume above.

Here is an example of the EXACT HTML structure you must use (this example is for a fictional Chef, you must generate content relevant to the uploaded resume!):

<h3> Short-Term Goals (0-1 Months)</h3>
<ul>
<li>Master basic knife skills and chopping techniques.</li>
<li>Learn the 5 fundamental mother sauces.</li>
</ul>

<h3> Medium-Term Goals (1-3 Months)</h3>
<ul>
<li>Practice advanced plating and food presentation.</li>
<li>Understand kitchen management and inventory.</li>
</ul>

<h3> Recommended Resources</h3>
<ul>
<li>Book: "The Food Lab" by J. Kenji López-Alt</li>
<li>Course: Gordon Ramsay's MasterClass on Cooking</li>
</ul>
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
            temperature=0.6,
            max_tokens=500
        )
        content = response.choices[0].message.content
        content = content.replace("```html", "").replace("```", "").strip()
        return content
    except Exception as e:
        return f"<p>AI Learning Roadmap Error: {str(e)}</p>"
