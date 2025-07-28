# Define python classes that specify the structure of the data

from typing import List, Optional,Dict
from datetime import datetime
from pydantic import BaseModel

# 1. All schema needs to inherit from BaseModel, pydantic can do automatic data validation
class StoryOptionsSchema(BaseModel):
    # 2. Define the fields of the schema
    title: str
    description: Optional[str] = None


# 2. Not directly use in API, but gonna use it as a parent class for other schemas
class StoryNodeBase(BaseModel):
    content: str
    is_ending: bool = False
    is_winning: bool = False

# 3. Response from API gonna be
class CompleteStoryNodeResponse(StoryNodeBase): # Inherite from StoryNodeBase
    id: int
    options: List[StoryOptionsSchema] = []


    # build this response model directly from a database object’s fields
    class Config:
        from_attributes = True


class StoryBase(BaseModel):
    title: str
    session_id: Optional[str] = None

    class Config:
        from_attributes = True


class CreateStoryRequest(BaseModel):
    theme: str


class CompleteStoryResponse(StoryBase):
    id: int
    created_at: datetime
    root_node: CompleteStoryNodeResponse
    all_nodes: Dict[int, CompleteStoryNodeResponse]

    class Config:
        from_attributes = True