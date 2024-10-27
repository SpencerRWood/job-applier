import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

Base = declarative_base()
engine = create_engine('sqlite:///job_applications.db')
SessionLocal = sessionmaker(bind=engine)

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    
    description_id = Column(Integer, primary_key=True, autoincrement=True)
    job_posting_link = Column(String, nullable=False)

class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    application_id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    job_description_id = Column(Integer, ForeignKey('job_descriptions.description_id'))
    applied = Column(Boolean, default=False)
    application_date = Column(Date, default=datetime.utcnow)
    resume_used = Column(String)  # Path to the uploaded resume file
    referred = Column(Boolean, default=False)
    status = Column(String)
    notes = Column(Text)
    
    job_description = relationship("JobDescription", backref="applications")

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class JobApplicationCreate(BaseModel):
    company: str
    job_title: str
    job_posting_link: str
    applied: Optional[bool] = False
    application_date: Optional[str] = None
    referred: Optional[bool] = False
    status: Optional[str] = ""
    notes: Optional[str] = ""

@app.post("/applications/")
async def create_job_application(
    company: str = Form(...),
    job_title: str = Form(...),
    job_posting_link: str = Form(...),
    applied: bool = Form(False),
    application_date: Optional[str] = Form(None),
    referred: bool = Form(False),
    status: str = Form(""),
    notes: str = Form(""),
    resume: UploadFile = File(None),
):
    # Open a new database session
    session = SessionLocal()

    # Save job description
    job_description = JobDescription(job_posting_link=job_posting_link)
    session.add(job_description)
    session.commit()
    
    # Handle resume file upload
    resume_filename = None
    if resume:
        resume_filename = os.path.join(UPLOAD_FOLDER, resume.filename)
        with open(resume_filename, "wb") as f:
            f.write(await resume.read())

    # Convert application_date to datetime
    application_date_parsed = None
    if application_date:
        application_date_parsed = datetime.strptime(application_date, "%Y-%m-%d")

    # Save job application
    job_application = JobApplication(
        company=company,
        job_title=job_title,
        job_description_id=job_description.description_id,
        applied=applied,
        application_date=application_date_parsed,
        resume_used=resume_filename,
        referred=referred,
        status=status,
        notes=notes
    )
    session.add(job_application)
    session.commit()
    
    # Close session
    session.close()
    
    return {"message": "Job application created successfully"}
