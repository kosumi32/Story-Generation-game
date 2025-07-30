import uuid
from typing import Optional
from datetime import datetime
from fastapi import Depends, APIRouter, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.story import Story, StoryNode
from models.job import StoryJob
from schemas.story import CompleteStoryNodeResponse, CompleteStoryResponse, CreateStoryRequest

from schemas.job import StoryJobResponse


router = APIRouter(
    prefix="/stories",
    tags=["stories"],   # for doc
    responses={404: {"description": "Not found"}}
)

# 1. Session identify your browser when interacting with a website
def get_session_id(session_id: Optional[str] = Cookie(None)):
    
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id

# 2. POST- Create something new
@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest,
    background_tasks: BackgroundTasks,
    response: Response,

    session_id: str = Depends(get_session_id),  # Depends on these functions
    db: Session = Depends(get_db)
):
    # 3. Store session id for later (Not secure)
    response.set_cookie(key="session_id", value=session_id, httponly=True)


    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id= job_id,
        session_id=session_id,
        theme=request.theme,     # from CreateStoryRequest
        status="pending"
        )
    db.add(job)
    db.commit()

    # 4. TODO: add background task to create story
    background_tasks.add_task(
        generate_story_task, job_id, session_id, request.theme
        )

    return job  # Able to check status


def generate_story_task(job_id: str, session_id: str, theme: str):
    # 5. Avoid session hanging (background task running, API unable to use DB), use a new session
    db = SessionLocal()     # necessary to have a new instance of DB (2 active at the same time)

    try:
        # 6. Look for the above job, once created
        job= db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status= "processing"
            db.commit()

            story= {}   # TODO: generate story

            job.story_id = 1
            job.status = "completed"
            job.completed_at = datetime.now()

            db.commit()
        
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()


@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
# story_id- Dynamic value in FastAPI (Need same name)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()

    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    # TODO: Parse Story
    complete_story = build_complete_story_tree(db, story)
    
    return complete_story


def build_complete_story_tree(db: Session, story: Story) -> CompleteStoryResponse:
    # 7. Build the complete story tree
    nodes = db.query(StoryNode).filter(StoryNode.story_id == story.id).all()

    complete_nodes = []
    for node in nodes:
        complete_node = CompleteStoryNodeResponse(
            id=node.id,
            content=node.content,
            choices=node.choices,  # Assuming choices is a list of strings
            next_node_id=node.next_node_id
        )
        complete_nodes.append(complete_node)

    return CompleteStoryResponse(
        id=story.id,
        title=story.title,
        theme=story.theme,
        nodes=complete_nodes
    )

# As user wants to create a story, we create a job
# Once made job (trigger background task to run OpenAI to make story)


# frontend submit jobs
# backend return job

# fronted ask if job is done
# backend return job status

# if job is done, backend can send story


# In short Job.py tells us the status of creation