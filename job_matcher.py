def extract_skills_from_analysis(analysis_text):

    skills = []

    lines = analysis_text.split("\n")

    for line in lines:
        if "-" in line:
            skill = line.replace("-", "").strip()
            if len(skill) > 2:
                skills.append(skill)

    return skills


def recommend_keywords(skills):

    roles = []

    for skill in skills:

        s = skill.lower()

        if "python" in s:
            roles.append("Python Developer")

        if "java" in s:
            roles.append("Java Developer")

        if "sql" in s or "database" in s:
            roles.append("Database Developer")

        if "html" in s or "css" in s or "javascript" in s:
            roles.append("Frontend Developer")

        if "react" in s or "web" in s:
            roles.append("Web Developer")

        if "machine learning" in s or "ai" in s:
            roles.append("AI Engineer")

    if len(roles) == 0:
        roles = ["Software Developer"]

    return list(set(roles))[:3]