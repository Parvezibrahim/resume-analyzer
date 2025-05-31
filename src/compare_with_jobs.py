import json
import os
from src.extract_keywords import extract_keywords_from_text

INDUSTRY_JOB_PATH = os.path.join("data", "industry_job_roles.json")

def get_industries():
    with open(INDUSTRY_JOB_PATH) as f:
        data = json.load(f)
    return list(data.keys())

def get_roles_for_industry(industry):
    with open(INDUSTRY_JOB_PATH) as f:
        data = json.load(f)
    return [role["title"] for role in data.get(industry, [])]

def get_keywords_for_role(industry, role):
    with open(INDUSTRY_JOB_PATH) as f:
        data = json.load(f)
    roles = data.get(industry, [])
    for r in roles:
        if r["title"] == role:
            return r["keywords"]
    return []

def compare_keywords(resume_keywords, job_keywords):
    matched = [kw for kw in resume_keywords if kw in job_keywords]
    missing = [kw for kw in resume_keywords if kw not in job_keywords]
    match_score = round((len(matched) / len(resume_keywords)) * 100, 2) if resume_keywords else 0.0
    return {
        "match_score": match_score,
        "matched_keywords": matched,
        "missing_keywords": missing
    }

def compare_with_custom_jd(resume_keywords, jd_text):
    jd_keywords = extract_keywords_from_text(jd_text)
    return compare_keywords(resume_keywords, jd_keywords)
