from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

class Talk(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_talks = [{"title": "title of talk 1", "content": "content of talk 1", "id": 1} , {"title": "title of talk 2", "content": "content of talk 2", "id": 2}]

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

@app.get("/talks")
def get_talks():
    return {"data": my_talks}

@app.post("/talks", status_code=status.HTTP_201_CREATED)
def create_posts(talk: Talk):
    talk_dict = talk.dict()
    talk_dict["id"] = randrange(0, 1000000)
    my_talks.append(talk_dict)
    return {"data": talk_dict}


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


