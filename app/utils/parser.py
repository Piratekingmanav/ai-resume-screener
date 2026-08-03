import io
import re
from PyPDF2 import PdfReader
import docx

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Reads a PDF file from bytes and extracts all text."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Reads a DOCX file from bytes and extracts all text."""
    doc = docx.Document(io.BytesIO(file_bytes))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def extract_email(text: str) -> str:
    """Uses Regular Expressions (Regex) to find an email address in the text."""
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    match = re.search(email_regex, text)
    return match.group(0) if match else None



# quick explanation 

#We are using bytes because when users upload resumes through our API later, the files will arrive as a stream of bytes in memory (we don't want to save them to the hard drive if we don't have to).
# extract_email uses a pattern-matching technique (Regex) to instantly scan the entire resume and pull out the email address.


# A robust dictionary/list of skills to scan for. 
# You can easily add more skills to this list later!
COMMON_SKILLS = [
    "Python", "FastAPI", "Machine Learning", "AI", "NLP", 
    "Docker", "PostgreSQL", "MySQL", "SQL", "Java", 
    "C++", "React", "JavaScript", "AWS", "Git", "REST API"
]

def extract_skills(text: str) -> str:
    """Scans the text for predefined skills and returns a comma-separated string."""
    found_skills = []
    text_lower = text.lower()
    
    for skill in COMMON_SKILLS:
        if skill.lower() in text_lower:
            found_skills.append(skill)
            
    return ", ".join(found_skills) if found_skills else "No skills identified"

def extract_education(text: str) -> str:
    """Basic keyword matching for education levels."""
    edu_keywords = ["b.tech", "bachelor", "master", "phd", "university", "college", "degree"]
    found = [word.capitalize() for word in edu_keywords if word in text.lower()]
    return ", ".join(found) if found else "Not specified"

def extract_experience(text: str) -> str:
    """Checks if work experience is mentioned."""
    if "experience" in text.lower() or "work history" in text.lower() or "intern" in text.lower():
        return "Experience identified (Manual review recommended)"
    return "Not specified"

def extract_certifications(text: str) -> str:
    """Basic keyword matching for common certifications."""
    cert_keywords = ["aws", "azure", "gcp", "cisco", "certified", "certification"]
    found = [word.capitalize() for word in cert_keywords if word in text.lower()]
    return ", ".join(found) if found else "None found"
            