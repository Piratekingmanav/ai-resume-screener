from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import models
from app.services.matcher import calculate_match_score
from app.utils.parser import extract_text_from_pdf, extract_text_from_docx, extract_email, extract_skills, extract_education, extract_experience, extract_certifications
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pytesseract
from pdf2image import convert_from_bytes
import io
import PyPDF2
from fastapi import BackgroundTasks, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load the embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')


router = APIRouter()

@router.post("/jobs/")
def create_job(title: str, description: str, required_skills: str,required_education: str = "Not specified",required_experience: str = "Not specified", db: Session = Depends(get_db)):
    """Creates a new Job Description in the database."""
    new_job = models.JobDescription(
        title=title, 
        description=description, 
        required_skills=required_skills,
        required_education=required_education,
        required_experience=required_experience
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "Job created successfully", "job": new_job}

@router.post("/upload-resume/{job_id}")
def upload_resume(job_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploads a resume, parses text, scores it, and saves to the database."""
    
    # 1. Check if job exists
    job = db.query(models.JobDescription).filter(models.JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # 2. Read file content
    content = file.file.read()

    # 3. Extract raw text
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(content)
    elif file.filename.endswith(".docx"):
        text = extract_text_from_docx(content)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX are supported")

    # 4. Extract data using our NLP functions
    email = extract_email(text)
    extracted_skills = extract_skills(text)
    extracted_edu = extract_education(text)
    extracted_exp = extract_experience(text)
    extracted_certs = extract_certifications(text)

    # 5. Calculate AI Match Score
    score = calculate_match_score(text, job.description)

    # 6. Save the Candidate to the Database
    candidate = models.Candidate(
        name=file.filename,
        email=email,
        education=extracted_edu,
        experience=extracted_exp,
        skills=extracted_skills,
        certifications=extracted_certs,
        match_score=score,
        job_id=job_id
    )
    
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return {
        "filename": file.filename,
        "email_found": email,
        "match_score": score,
        "raw_text": text
    }

@router.get("/candidates/{job_id}")
def get_candidates(job_id: int, db: Session = Depends(get_db)):
    """Fetches all candidates for a specific job, sorted by highest match score."""
    candidates = db.query(models.Candidate)\
        .filter(models.Candidate.job_id == job_id)\
        .order_by(models.Candidate.match_score.desc())\
        .all()
    return candidates

def calculate_match_score(resume_text: str, job_skills: str) -> int:
    """
    Calculates semantic similarity using vector embeddings.
    """
    if not resume_text or not job_skills:
        return 0
        
    # 1. Convert text to vector embeddings
    embeddings = embedding_model.encode([resume_text, job_skills])
    
    # 2. Calculate Cosine Similarity between the two vectors
    resume_vector = embeddings[0].reshape(1, -1)
    job_vector = embeddings[1].reshape(1, -1)
    similarity = cosine_similarity(resume_vector, job_vector)[0][0]
    
    # 3. Convert mathematical similarity to a percentage (0 to 100)
    score = round(float(similarity) * 100)
    
    # Prevent negative scores if vectors are completely opposite
    return max(0, min(score, 100))

def extract_text_from_pdf(file_bytes: bytes) -> str:
    text = ""
    
    # 1. Try standard text extraction first (fastest)
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"Standard extraction failed: {e}")

    # 2. Fallback to OCR if it's a scanned image (less than 50 chars found)
    if len(text.strip()) < 50:
        print("Scanned document detected. Engaging OCR fallback...")
        try:
            # Convert PDF bytes into a list of images
            images = convert_from_bytes(file_bytes)
            for image in images:
                # Extract text from each image
                text += pytesseract.image_to_string(image) + "\n"
        except Exception as e:
            print(f"OCR processing failed: {e}")
            
    return text


# --- EMAIL NOTIFICATION WORKER ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "manavlabana2003@gmail.com"      # Replace with your email
SENDER_PASSWORD = "Satoro@gojo17"       # Replace with your App Password

def send_interview_email_task(to_email: str, candidate_name: str):
    """
    Background worker function that sends a formal interview invitation email.
    """
    subject = "Interview Invitation - AI Resume Screener Selection"
    body = f"""
    Hi {candidate_name},

    Great news! Your resume was reviewed and highly rated by our screening system.

    We would love to invite you for an initial interview round to discuss your experience and skill alignment. 
    Please reply to this email with your availability for this coming week.

    Best regards,
    Recruiting Team
    """

    try:
        # Create message container
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to server and send
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"[SUCCESS] Interview invite email sent to {to_email}")
    except Exception as e:
        print(f"[EMAIL LOG / MOCK] Could not dispatch real email (Check SMTP settings): {e}")
        print(f"[MOCK DISPATCH] Intended recipient: {to_email} | Candidate: {candidate_name}")


@router.post("/send-invite/{candidate_id}")
def send_interview_invite(candidate_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Retrieve candidate from database
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    if not candidate.email or candidate.email == "N/A":
        raise HTTPException(status_code=400, detail="Candidate has no valid email address on record")

    # Queue the email dispatch task in the background
    background_tasks.add_task(send_interview_email_task, candidate.email, candidate.name)

    return {"status": "success", "message": f"Interview invite queued for {candidate.name} ({candidate.email})"}