def extract_skills(text):

    skills_database = {
        "python": "Python",
        "java": "Java",
        "c": "C",
        "c++": "C++",
        "html": "HTML",
        "css": "CSS",
        "javascript": "JavaScript",
        "flask": "Flask",
        "django": "Django",
        "sql": "SQL",
        "mysql": "MySQL",
        "mongodb": "MongoDB",
        "react": "React",
        "node.js": "Node.js",
        "git": "Git",
        "github": "GitHub",
        "aws": "AWS",
        "docker": "Docker",
        "linux": "Linux",
        "machine learning": "Machine Learning",
        "data analysis": "Data Analysis",
        "excel": "Excel"
    }

    text = text.lower()

    found_skills = []

    for key, value in skills_database.items():
        if key in text:
            found_skills.append(value)

    return found_skills