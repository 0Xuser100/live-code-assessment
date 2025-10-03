from datetime import datetime
from typing import Dict

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    topic: str
    location: str
    language: str


class TweetResponse(BaseModel):
    id: int
    context: Dict[str, str]
    tweet: str
    author_name: str
    author_email: str
    created_at: datetime

    class Config:
        orm_mode = True
