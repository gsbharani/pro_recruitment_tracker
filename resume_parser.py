import re
from text_utils import extract_text

def parse_resume(path, required_skills=[]):
    text = extract_text(path).lower()

    email = re.search(r"[\w.-]+@[\w.-]+", text)
    phone = re.search(r"(\+91)?[6-9]\d{9}", text)
    dob = re.search(r"\d{2}/\d{2}/\d{4}", text)

    experience_match = re.search(r"(\d+)\+?\s*years", text)
    experience = int(experience_match.group(1)) if experience_match else 0

    found_skills = [s for s in required_skills if s in text]

    return {
        "email": email.group(0) if email else None,
        "mobile": phone.group(0) if phone else None,
        "dob": dob.group(0) if dob else None,
        "experience": experience,
        "skills": found_skills,
        "name": text.split("\n")[0]  # first line as name (simplistic)
    }
