from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

app = FastAPI()


class Talk(BaseModel):
    title: str
    description: str
    abstract: Optional[str] = None
    type_id: Optional[int] = None
    topics: Optional[str] = None
    tags: Optional[str] = None
    level: Optional[str] = None
    comments: Optional[str] = None
    link_slides: Optional[str] = None
    link_video: Optional[str] = None
    desired: Optional[bool] = False
    sponsor: Optional[bool] = False
    rating_committee: Optional[int] = None
    favorite_committee: Optional[bool] = False
    selected_committee: Optional[bool] = False
    comments_committee: Optional[str] = None
    user_id: int
    published: Optional[bool] = False
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


while True:

    try:
        conn = psycopg2.connect(host=settings.DATABASE_HOST, port=settings.DATABASE_PORT,
                                database=settings.DATABASE_NAME, user=settings.DATABASE_USERNAME,
                                password=settings.DATABASE_PASSWORD, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failure")
        print("Error: ", error)
        time.sleep(3)

my_talks = [{"title": "title of talk 1", "content": "content of talk 1", "id": 1},
            {"title": "title of talk 2", "content": "content of talk 2", "id": 2}]


def find_talk(id):
    for t in my_talks:
        if t["id"] == id:
            return t


def find_index_talk(id):
    for i, t in enumerate(my_talks):
        if t["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World"}

## @desc    Get talks
## @route   GET /api/v1/talks
## @access  Public

@app.get("/api/v1/talks")
def get_talks():
    cursor.execute("""SELECT * FROM public.talks ORDER BY id ASC""")
    talks = cursor.fetchall()
    return {"data": talks}


# @desc    Add talk
# @route   POST /api/v1/talks/:bootcampId/courses
# @access  Private

@app.post("/api/v1/talks", status_code=status.HTTP_201_CREATED)
def create_posts(talk: Talk):
    cursor.execute("""INSERT INTO talks (title, description, abstract, type_id, topics, tags, level, comments, 
    link_slides, link_video, desired, sponsor, rating_committee, favorite_committee, selected_committee, 
    comments_committee, user_id, published) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
    %s, %s) RETURNING * """,
                   (talk.title, talk.description, talk.abstract, talk.type_id, talk.topics, talk.tags, talk.level,
                    talk.comments, talk.link_slides, talk.link_video, bool(talk.desired), bool(talk.sponsor),
                    talk.rating_committee, bool(talk.favorite_committee), bool(talk.selected_committee),
                    talk.comments_committee, talk.user_id, bool(talk.published)))

    new_talk = cursor.fetchone()
    conn.commit()
    return {"data": new_talk}


@app.get("/talks/{id}")
def get_talk(id: int, response: Response):
    talk = find_talk(id)
    if not talk:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} was not found")
    return {"talk_details": talk}


@app.delete("/talks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_talk(id: int):
    index = find_index_talk(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} does not exist")

    my_talks.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/talks/{id}")
def update_talks(id: int, talk: Talk):
    index = find_index_talk(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} does not exist")

    talk_dict = talk.dict()
    talk_dict['id'] = id
    my_talks[index] = talk_dict
    return {"data": talk_dict}
