from pydantic import BaseModel, EmailStr
from typing import Optional

class ReaderBase(BaseModel):
    name: str
    email: EmailStr

class ReaderCreate(ReaderBase):
    password: str

class Reader(ReaderBase):
    id: int
    is_active: Optional[bool] = True

