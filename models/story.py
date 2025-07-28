# story name
# theme
# first option
# children: [go left, go right]

# text
# option: []

# Looks like binary tree

# Object Relational Mapping (ORM) - SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, JSON

# 1. FastAPI has modules like SQLAlchemy, allowing us to map data into Python classes without sql code

from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base

class Story(Base):  # inherit from Base, so that SQLAlchemy knows this is a model
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # index=True allows us to search for this field
    session_id = Column(String, index=True)  # track every stories created
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 每個 Story 可以有很多個 StoryNode，但每個 StoryNode 只屬於一個 Story
    nodes= relationship("StoryNode", back_populates="story")  


class StoryNode(Base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"))    # ForeignKey()- 用來連接「多的那方」回到「一的那方」
    content = Column(String)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)  
    is_winning = Column(Boolean, default=False)
    options = Column(JSON, default=list)
    
    story = relationship("Story", back_populates="nodes")  # DB relationship (many to one)