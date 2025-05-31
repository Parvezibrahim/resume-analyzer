# src/suggest_feedback.py

def generate_feedback(match_score, matched_keywords, missing_keywords):
    feedback = []

    if match_score > 80:
        feedback.append("Excellent match! Your resume aligns well with the job requirements.")
    elif match_score > 50:
        feedback.append("Good match, but there is room for improvement.")
    else:
        feedback.append("Low match score. Consider improving your resume based on missing keywords.")

    if missing_keywords:
        feedback.append(f"Focus on including these important keywords: {', '.join(missing_keywords)}.")

    if matched_keywords:
        feedback.append(f"You already have strong keywords like: {', '.join(matched_keywords)}.")

    return "\n\n".join(feedback)
