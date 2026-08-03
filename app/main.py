from fastapi import FastAPI
from app.database import engine, Base
from app.models import models
from app.routers import api
from fastapi import BackgroundTasks, HTTPException
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Screener & Candidate Ranking System",
    description="Automated resume parsing, semantic matching, and candidate shortlisting API.",
    version="1.0.0"
)

app.include_router(api.router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "AI Resume Screening API is running."
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}