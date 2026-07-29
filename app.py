from flask import Flask, render_template, request, send_file, jsonify, session
import os
import io
import uuid
import pdfplumber
import concurrent.futures

from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from utils.matcher import calculate_match
from utils.ai_feedback import generate_ai_feedback
from utils.ai_rewriter import rewrite_resume_point
from utils.ai_cover_letter import generate_cover_letter
from utils.ai_interview import generate_interview_questions
from utils.ai_roadmap import generate_learning_roadmap
from utils.ai_career_fit import generate_career_fit
from utils.ai_chat import generate_chat_response

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Store latest analysis per user
user_results = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "resume" not in request.files:
        return "No file uploaded."

    resume = request.files["resume"]

    if resume.filename == "":
        return "Please select a PDF."

    job_description = request.form.get("job_description", "")

    text = ""

    try:
        with pdfplumber.open(io.BytesIO(resume.read())) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        return f"Error reading PDF: {e}"

    # Calculate ATS Score and Extract Skills dynamically
    score, matched_skills, missing_skills, resume_skills = calculate_match(
        text,
        job_description
    )


    # Resume Strength
    if score >= 80:
        strength = "🟢 Excellent"
    elif score >= 60:
        strength = "🔵 Good"
    elif score >= 40:
        strength = "🟡 Average"
    else:
        strength = "🔴 Needs Improvement"

    # Resume Rating
    rating = round((score / 100) * 5, 1)

    company_name = request.form.get("company_name", "")
    job_title = request.form.get("job_title", "")

    # Run AI generation tasks in parallel to reduce loading time
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_feedback = executor.submit(generate_ai_feedback, text, job_description, score)
        future_interview = executor.submit(generate_interview_questions, text, job_description)
        future_roadmap = executor.submit(generate_learning_roadmap, text, job_description)
        future_career_fit = executor.submit(generate_career_fit, text)
        
        future_cover_letter = None
        if company_name and job_title:
            future_cover_letter = executor.submit(generate_cover_letter, text, job_description, company_name, job_title)

        feedback = future_feedback.result()
        interview_questions = future_interview.result()
        learning_roadmap = future_roadmap.result()
        career_fit = future_career_fit.result()
        cover_letter = future_cover_letter.result() if future_cover_letter else ""

    # Resume Statistics (Total & Matched skills)
    total_skills = len(resume_skills)
    matched_count = len(matched_skills)

    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    user_id = session["user_id"]

    user_results[user_id] = {
        "text": text,
        "score": score,
        "matched_skills": matched_skills,
        "strength": strength,
        "rating": rating,
        "feedback": feedback,
        "interview_questions": interview_questions,
        "learning_roadmap": learning_roadmap,
        "career_fit": career_fit,
        "cover_letter": cover_letter,
        "total_skills": total_skills,
        "matched_count": matched_count
    }

    return render_template(
        "result.html",
        score=score,
        matched_skills=matched_skills,
        strength=strength,
        rating=rating,
        feedback=feedback,
        interview_questions=interview_questions,
        learning_roadmap=learning_roadmap,
        career_fit=career_fit,
        cover_letter=cover_letter,
        total_skills=total_skills,
        matched_count=matched_count
    )


@app.route("/download")
def download():

    user_id = session.get("user_id")
    latest_result = user_results.get(user_id) if user_id else None

    if not latest_result:
        return "No analysis available."

    filename = "Resume_Analysis_Report.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Resume Analyzer Report", styles["Title"]))
    elements.append(Paragraph(f"ATS Score: {latest_result['score']}%", styles["Normal"]))
    elements.append(Paragraph(f"Resume Strength: {latest_result['strength']}", styles["Normal"]))
    elements.append(Paragraph(f"Resume Rating: {latest_result['rating']}/5", styles["Normal"]))



    elements.append(Paragraph("Overall Feedback", styles["Heading2"]))
    elements.append(Paragraph(latest_result["feedback"], styles["Normal"]))

    if "interview_questions" in latest_result:
        elements.append(Paragraph("AI Interview Questions", styles["Heading2"]))
        iq_text = latest_result["interview_questions"]
        iq_text = iq_text.replace("<h3>", "<br/><br/><b>").replace("</h3>", "</b><br/>")
        iq_text = iq_text.replace("<li>", "<br/>• ").replace("</li>", "")
        iq_text = iq_text.replace("<ol>", "").replace("</ol>", "").replace("<ul>", "").replace("</ul>", "")
        elements.append(Paragraph(iq_text, styles["Normal"]))

    if "learning_roadmap" in latest_result:
        elements.append(Paragraph("AI Learning Roadmap", styles["Heading2"]))
        lr_text = latest_result["learning_roadmap"]
        lr_text = lr_text.replace("<h3>", "<br/><br/><b>").replace("</h3>", "</b><br/>")
        lr_text = lr_text.replace("<li>", "<br/>• ").replace("</li>", "")
        lr_text = lr_text.replace("<ol>", "").replace("</ol>", "").replace("<ul>", "").replace("</ul>", "")
        elements.append(Paragraph(lr_text, styles["Normal"]))

    doc.build(elements)

    return send_file(filename, as_attachment=True)

@app.route("/rewrite", methods=["GET", "POST"])
def rewrite():

    rewritten_text = ""

    if request.method == "POST":

        resume_point = request.form.get("resume_point", "")

        if resume_point.strip():
            rewritten_text = rewrite_resume_point(resume_point)

    return render_template(
        "rewrite.html",
        rewritten_text=rewritten_text
    )

@app.route("/chat", methods=["POST"])
def chat():
    user_id = session.get("user_id")
    latest_result = user_results.get(user_id) if user_id else None

    if not latest_result or "text" not in latest_result:
        return jsonify({"error": "No resume context available. Please upload a resume first."}), 400
    
    data = request.get_json()
    question = data.get("question", "")
    
    if not question:
        return jsonify({"error": "Question is required."}), 400
        
    answer = generate_chat_response(latest_result["text"], latest_result["score"], question)
    return jsonify({"answer": answer})


@app.route("/editor")
def editor():
    return render_template("cover_letter_editor.html")

@app.route("/api/generate-cover-letter", methods=["POST"])
def api_generate_cover_letter():
    data = request.get_json()
    resume_text = data.get("resume", "")
    job_desc = data.get("job_description", "")
    company = data.get("company_name", "")
    title = data.get("job_title", "")
    
    if not job_desc:
        return jsonify({"error": "Job Description is required."}), 400
        
    cover_letter_html = generate_cover_letter(resume_text, job_desc, company, title)
    return jsonify({"cover_letter": cover_letter_html})


if __name__ == "__main__":
    app.run(debug=True)