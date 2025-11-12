from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    number: str
    email: str
    cnic: str
    result: int | None = None
    total: int | None = None

class userresult(BaseModel):
    username: str | None = None
    number: str | None = None
    email: str | None = None
    cnic: str 
    result: int
    total: int

class config(BaseModel):
    subject: str
    type: str
    level: str
    count: int

