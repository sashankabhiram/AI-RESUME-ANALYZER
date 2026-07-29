# AI Resume Analyzer

AI Resume Analyzer is a powerful, AI-driven web application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). By comparing a user's resume against a target job description, it provides actionable insights, scores, and various AI-generated tools to improve their chances of landing an interview.

## 🚀 Features

- **ATS Scoring & Skill Matching**: Evaluates your resume against a job description and highlights matched/missing skills.
- **Detailed AI Feedback**: Provides a strength rating and comprehensive feedback on how to improve your resume.
- **Cover Letter Generation**: Automatically generates a tailored cover letter based on your resume, the job description, and the company.
- **Interview Preparation**: Generates potential AI-curated interview questions based on your specific profile and the targeted role.
- **Learning Roadmap**: Suggests a customized learning or career roadmap to bridge the skill gap for your desired role.
- **AI Chat Assistant**: Ask questions and chat directly with an AI about your uploaded resume.
- **Resume Point Rewriter**: A dedicated tool to re-write and enhance individual bullet points in your resume.
- **Downloadable Reports**: Export your complete resume analysis (including feedback, questions, and roadmap) as a PDF report.

## 🛠️ Technology Stack

- **Backend Framework**: Python, Flask
- **PDF Processing**: `pdfplumber` (for reading resumes), `reportlab` (for generating PDF reports)
- **AI Integration**: Groq API (Configured via environment variables)
- **Frontend**: HTML, CSS, JavaScript (Jinja2 Templates)

## 📁 Project Structure

```text
AI Resume Analyzer/
│
├── app.py                   # Main Flask application
├── requirements.txt         # Project dependencies
├── .env                     # Environment variables (API Keys)
├── .venv/                   # Python Virtual Environment
│
├── templates/               # HTML Templates
│   ├── index.html           # Upload & Landing page
│   ├── result.html          # Analysis Dashboard
│   ├── cover_letter_editor.html # Cover Letter UI
│   └── rewrite.html         # Resume bullet point rewriter
│
├── static/                  # Static files (CSS, Images, Uploads)
│
└── utils/                   # AI and Core Logic Modules
    ├── ai_career_fit.py
    ├── ai_chat.py
    ├── ai_cover_letter.py
    ├── ai_feedback.py
    ├── ai_interview.py
    ├── ai_rewriter.py
    ├── ai_roadmap.py
    ├── job_recommender.py
    ├── matcher.py
    └── skill_extractor.py
```

## ⚙️ Setup Instructions

Follow these steps to run the project locally on your machine.

### 1. Prerequisites
Ensure you have Python installed on your system. 

### 2. Activate Virtual Environment
Open your terminal/command prompt and activate the virtual environment:
**Windows:**
```bash
.\.venv\Scripts\activate
```
**Mac/Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies
If you haven't already, install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Environment Variables
Ensure you have a `.env` file in the root directory containing your API Key:
```env
GROQ_API_KEY=your_api_key_here
```

### 5. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 6. Open in Browser
Once the server is running, open your web browser and go to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---
*Built to help you land your dream job!*
