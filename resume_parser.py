import pdfplumber
import re

# Optional: define a skills list for matching
SKILLS = ["python", "sql", "aws", "excel", "java", "data analysis", "power bi"]

def extract_text(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.lower()

def parse_resume(path):
    text = extract_text(path)

    email = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone = re.search(r"(\+91)?[6-9]\d{9}", text)
    found_skills = [s for s in SKILLS if s in text]

    exp_match = re.search(r"(\d+)\+?\s*years", text)
    experience = int(exp_match.group(1)) if exp_match else 0

    return {
        "email": email.group(0) if email else None,
        "mobile": phone.group(0) if phone else None,
        "skills": found_skills,
        "experience": experience
    }
