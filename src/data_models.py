from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base

class JobDescription(Base):
    __tablename__ = 'job_descriptions'
    
    description_id = Column(Integer, primary_key=True, autoincrement=True)
    job_posting_link = Column(String, nullable=False)

class JobApplication(Base):
    __tablename__ = 'job_applications'
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('job_descriptions.description_id'), nullable=False, index=True)
    company = Column(String, nullable=False)
    job_title = Column(String, nullable=False)
    applied = Column(Boolean, default=False)
    application_date = Column(Date, default=datetime.now)
    resume_used = Column(String)  # Path to the uploaded resume file
    referred = Column(Boolean, default=False)
    status = Column(String)
    notes = Column(Text)

    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)

    current_indicator = Column(Boolean, default=True)
    
    job_description = relationship("JobDescription", backref="applications")