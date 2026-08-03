from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from app.database import Base

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    required_skills = Column(Text)
    required_education = Column(String)
    required_experience = Column(String) 

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    education = Column(Text)
    experience = Column(Text)
    skills = Column(Text)
    certifications = Column(Text) # <-- This is the new one!
    match_score = Column(Float, default=0.0) 
    
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))