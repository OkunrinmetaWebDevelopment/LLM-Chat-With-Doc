from pydantic import BaseModel, Field
from typing import List
from uuid import UUID



class UserBase(BaseModel):
    email: str
    hashed_password: str

    class Config:
        orm_mode = True
        schema_extra={
            "example":{
                "email": "john@gmail.com",
                "hashed_password": "pass"
            }
        }


class UserCreate(UserBase):
    pass


class ShowCurrentUser(UserBase):
    id:int
    class Config:
        orm_mode = True


class SessionData(BaseModel):
    username: str
    conversation_chain_data: list[dict]


class UUIDData(SessionData):
    iuuid:UUID


class Message(BaseModel):
    user_id: str
    text: str