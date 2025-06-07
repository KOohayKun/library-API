from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class User:
    def __init__(self, username: str, hashed_password: str):
        self.username = username
        self.hashed_password = hashed_password