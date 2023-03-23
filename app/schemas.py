from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


# these are pydantic models

# THIS IS OUR RESEPONSE MODEL, so we dont eant to show user password in the response
# # the response will be sql alchemy model, so we need pydantic to be able to convert it into ,,his'' model, so we need this option with orm_mode
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


# if we define only these fields, in the response created_at, id wont be visible

# pydantic only knows how to deal with python dictionaries, so in order to override
# that we have to insert additional option class Config: orm_mode = True. Then, the SQLAlchemy model will be valid pydantic model,

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

# the user input will be validated wth this pydantic model
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

# we need to add this schema, because while doing inner join our schema has changed to:
"""
from:
{
        "title": "fsdfdsfdsfsdfsdf",
        "content": "cdasdsadsadasdasdssadass",
        "published": true,
        "id": 1,
        "created_at": "2023-03-19T20:30:24.505700+01:00",
        "owner_id": 1,
        "owner": {
            "id": 1,
            "email": "ab@gmail.com",
            "created_at": "2023-03-19T20:29:54.643109+01:00"
        }
    }

to:

{
        "Post": {
            "title": "fsdfdsfdsfsdfsdf",
            "content": "cdasdsadsadasdasdssadass",
            "published": true,
            "id": 22,
            "created_at": "2023-03-19T23:38:15.759464+01:00",
            "owner_id": 1,
            "owner": {
                "id": 1,
                "email": "ab@gmail.com",
                "created_at": "2023-03-19T20:29:54.643109+01:00"
            }
        },
        "votes": 0
    },

"""

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True