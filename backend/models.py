from pydantic import BaseModel
from typing import List, Optional

class StoryRequest(BaseModel):
    character: str
    plot: str
    page_count: int = 3

class Panel(BaseModel):
    panel_number: int
    text: Optional[str] = None
    dialogue: Optional[str] = None
    scene: Optional[str] = None
    shot: Optional[str] = None

class Page(BaseModel):
    page_number: int
    panels: List[Panel]
    prompt: str # Combined prompt for the whole page
    image_url: Optional[str] = None
    status: str = "pending" # pending, generating, done, error

class StoryResponse(BaseModel):
    title: str
    character_design: Optional[str] = None # Detailed visual description of the character
    pages: List[Page]

class ImageRequest(BaseModel):
    prompt: str
    character_design: Optional[str] = None # To ensure consistency
    page_number: int
    story_title: str

# Auth Models
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    points: int
    is_admin: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserUpdatePoints(BaseModel):
    points: int
