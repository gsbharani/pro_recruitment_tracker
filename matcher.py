# matcher.py
from sentence_transformers import SentenceTransformer, util

# Load a lightweight model for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_score(jd_text: str, resume_text: str) -> float:
    """
    Calculate semantic similarity score between JD and resume.
    Returns a percentage (0-100).
    """
    jd_emb = model.encode(jd_text, convert_to_tensor=True)
    resume_emb = model.encode(resume_text, convert_to_tensor=True)

    similarity = util.cos_sim(jd_emb, resume_emb).item()
    return round(similarity * 100, 2)


def skill_score(resume_text: str, required_skills: list) -> float:
    """
    Check how many skills from required_skills appear in resume_text.
    Returns percentage of skills matched (0-100).
    """
    if not required_skills:
        return 0.0

    resume_text_lower = resume_text.lower()
    matched = sum(1 for skill in required_skills if skill.lower() in resume_text_lower)

    return round((matched / len(required_skills)) * 100, 2)
