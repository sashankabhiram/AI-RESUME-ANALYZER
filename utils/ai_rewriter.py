import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def rewrite_resume_point(text):

    prompt = f"""
You are a professional resume writer.

Rewrite the following resume bullet point to make it highly ATS-friendly, professional, and impactful. 

Instead of giving multiple confusing variations, I want you to provide:
1. One single, highly polished, ATS-optimized version of the bullet point.
2. A very simple, beginner-friendly explanation (1-2 sentences) of WHY this new version is better and what ATS keywords were added.

Resume Bullet Point:
{text}

Return ONLY clean HTML. Do NOT use Markdown, **, or triple backticks.

Example of the EXACT HTML structure you must use (this example is for a fictional Chef, you must generate content relevant to the user's bullet point!):

<h3>✨ ATS-Optimized Version</h3>
<ul>
<li>Spearheaded the redesign of the kitchen layout, streamlining workflow and drastically reducing meal prep time by 20%.</li>
</ul>

<h3>💡 Why this is better</h3>
<p>We added strong action words like "Spearheaded" and included a measurable result (20%) which applicant tracking systems (ATS) and recruiters love to see because it proves your direct impact.</p>
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

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"