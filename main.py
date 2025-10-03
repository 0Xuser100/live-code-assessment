from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, Header, HTTPException, status
from sqlalchemy.orm import Session

from ai import FakeAI
from config import settings
from models import Tweet, create_tables, get_db
from schemas import GenerateRequest, TweetResponse


ai_client = FakeAI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


def authenticate(x_api_key: str = Header(...)) -> None:
    if x_api_key != settings.X_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to INTO AI Assessment"}


@app.post("/generate", response_model=TweetResponse, dependencies=[Depends(authenticate)])
async def generate_tweet(payload: GenerateRequest, db: Session = Depends(get_db)):
    result = await ai_client.generate_response(payload.dict())
    tweet_text = (result or {}).get("tweet") or ""
    author = (result or {}).get("author") or {}
    author_name = author.get("name") or ""
    author_email = author.get("email") or ""

    if not tweet_text or not author_name or not author_email:
        raise HTTPException(status_code=500, detail="AI did not return a valid tweet")

    tweet_obj = Tweet(
        context=payload.dict(),
        tweet=tweet_text,
        author_name=author_name,
        author_email=author_email,
    )
    db.add(tweet_obj)
    db.commit()
    db.refresh(tweet_obj)
    return tweet_obj


@app.get("/tweets", response_model=List[TweetResponse], dependencies=[Depends(authenticate)])
def get_tweets(db: Session = Depends(get_db)):
    return (
        db.query(Tweet)
        .order_by(Tweet.author_name.asc(), Tweet.created_at.desc())
        .all()
    )
