def recommend_jobs(skills):

    jobs = []

    if "Python" in skills:
        jobs.append("Python Developer")

    if "Java" in skills:
        jobs.append("Java Developer")

    if "HTML" in skills or "CSS" in skills or "JavaScript" in skills:
        jobs.append("Frontend Developer")

    if "Flask" in skills or "Django" in skills:
        jobs.append("Backend Developer")

    if "React" in skills:
        jobs.append("React Developer")

    if "Machine Learning" in skills:
        jobs.append("Machine Learning Engineer")

    if "Data Analysis" in skills or "Excel" in skills:
        jobs.append("Data Analyst")

    if "SQL" in skills or "MySQL" in skills or "MongoDB" in skills:
        jobs.append("Database Developer")

    if "AWS" in skills or "Docker" in skills:
        jobs.append("Cloud Engineer")

    if len(jobs) == 0:
        jobs.append("Software Developer")

    return jobs