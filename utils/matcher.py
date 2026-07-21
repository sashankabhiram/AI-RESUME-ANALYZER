def calculate_match(resume_skills, job_description):

    job_description = job_description.lower()

    matched_skills = []
    missing_skills = []

    for skill in resume_skills:

        if skill.lower() in job_description:
            matched_skills.append(skill)

    skills_database = [
        "Python",
        "Java",
        "C",
        "C++",
        "HTML",
        "CSS",
        "JavaScript",
        "Flask",
        "Django",
        "SQL",
        "MySQL",
        "MongoDB",
        "React",
        "Node.js",
        "Git",
        "GitHub",
        "AWS",
        "Docker",
        "Linux",
        "Machine Learning",
        "Data Analysis",
        "Excel"
    ]

    for skill in skills_database:
        if skill.lower() in job_description and skill not in matched_skills:
            missing_skills.append(skill)

    if len(matched_skills) + len(missing_skills) == 0:
        score = 0
    else:
        score = int(
            (len(matched_skills) /
            (len(matched_skills) + len(missing_skills))) * 100
        )

    return score, matched_skills, missing_skills