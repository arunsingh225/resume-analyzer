def generate_feedback(text, skills, score):
    feedback = []

    if len(text.split()) < 200:
        feedback.append("Add more content to your resume.")

    if len(skills) < 3:
        feedback.append("Include more technical skills.")

    if "project" not in text.lower():
        feedback.append("Add project section.")

    if score < 60:
        feedback.append("Improve ATS keywords and formatting.")
    else:
        feedback.append("Good resume, improve formatting slightly.")

    return feedback