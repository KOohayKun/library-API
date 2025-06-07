from fastapi import APIRouter, HTTPException
from typing import List
from uuid import uuid4
from fastapi.params import Depends
from Library.models.book_model import Book, BookCreate, BookUpdate
from Library.utils.security import get_current_user
from Library.models.user_model import User
from sqlalchemy.orm import Session
from Library.datab.database import get_db
from Library.datab.dbmodels import BookDB

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book)
def create_book(book_data: BookCreate, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    isbn = str(uuid4())[:8]

    new_book = BookDB(
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        ISBN=isbn,
        num_of_books=book_data.num_of_books
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return Book(
        book_id=new_book.id,
        title=new_book.title,
        author=new_book.author,
        year=new_book.year,
        ISBN=new_book.ISBN,
        num_of_books=new_book.num_of_books
    )

@router.get("/{book_id}", response_model=Book)
def get_book_by_id(book_id: int,_: User = Depends(get_current_user),db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="книга не найдена")

    return Book(
        book_id=book.id,
        title=book.title,
        author=book.author,
        year=book.year,
        ISBN=book.ISBN,
        num_of_books=book.num_of_books
    )


@router.delete("/{book_id}")
def delete_book(book_id: int, _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    db.delete(book)
    db.commit()
    return {"message":"Книга успешно удалена"}

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate,
                _: User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    update_data = book_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)


    return Book(
        book_id=book.id,
        title=book.title,
        author=book.author,
        year=book.year,
        ISBN=book.ISBN,
        num_of_books=book.num_of_books
    )


@router.get("/", response_model=List[Book])
def get_book_list(db: Session = Depends(get_db)):
    books_2 = db.query(BookDB).all()

    return [
        Book(
            book_id=book.id,
            title=book.title,
            author=book.author,
            year=book.year,
            ISBN=book.ISBN,
            num_of_books=book.num_of_books
        )
        for book in books_2
    ]