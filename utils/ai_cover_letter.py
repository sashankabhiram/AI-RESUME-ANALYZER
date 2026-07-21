import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_cover_letter(resume_text, job_description, company_name, job_title):

    resume_context = f"Resume:\n{resume_text}" if resume_text else "Note: No specific resume provided. Write a strong, compelling cover letter relying heavily on the Job Description and standard professional achievements for this role."

    prompt = f"""
You are an expert HR recruiter and professional resume writer.

Write a personalized cover letter using the following information.

{resume_context}

Job Description:
{job_description}

Company:
{company_name}

Job Title:
{job_title}

Requirements:

To ensure the best reading experience, a cover letter should be 20 to 25 lines of text in total (excluding headers).
In terms of layout, this translates to 3 to 4 paragraphs spread across roughly 250 to 350 words.

Line-by-Line Breakdown for UX:
- 1-2 lines: A professional, personalized salutation.
- 3-4 lines: The opening hook stating the target role.
- 6-8 lines: The core value paragraph with quantified achievements.
- 4-5 lines: The company connection paragraph showing cultural fit.
- 3-4 lines: The call-to-action closing and professional sign-off.

Best UX Rules for Readability:
- Keep sentences short: Aim for under 15 words per sentence.
- Use white space: Leave a full blank line between every paragraph (use <br/><br/> or separate <p> tags).
- Never exceed one page: A user should never have to scroll endlessly or print a second page.
- Limit paragraph depth: No single paragraph should be more than 4 to 5 lines long.

Return ONLY clean HTML.

Use:
<h2>Cover Letter</h2>
<p>...</p>

Do NOT use Markdown.
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
            max_tokens=700
        )

        content = response.choices[0].message.content
        content = content.replace("```html", "").replace("```", "").strip()
        return content

    except Exception as e:
        return f"Cover Letter Error: {str(e)}"