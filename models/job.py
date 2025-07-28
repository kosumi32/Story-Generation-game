# frontend submit jobs
# backend return job

# fronted ask if job is done
# backend return job status

# if job is done, backend can send story


# In short Job.py tells us the status of creation

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base


class StoryJob(Base):
    __tablename__ = "story_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)  
    session_id = Column(String, index=True)  
    theme= Column(String)
    status = Column(String, default="pending")  # pending, in_progress, completed, failed
    
    story_id= Column(Integer, nullable=True)  # ID of the story created by this job
    error= Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)  # how long the job took
    