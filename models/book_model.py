from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    book_id: int
    title: str
    author: str
    year: Optional[int] = None
    ISBN: str
    num_of_books: int

class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    num_of_books: int = Field(default=1, ge=0)

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    num_of_books: Optional[int] = Field(default=None, ge=0)

