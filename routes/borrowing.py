from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from Library.datab.database import get_db
from Library.datab.dbmodels import BookDB, Reader, BorrowedBook
from pydantic import BaseModel

router = APIRouter(prefix="/library", tags=["borrowing"])

class BorrowRequest(BaseModel):
    book_id: int
    reader_id: int

class ReturnRequest(BaseModel):
    borrow_id: int

@router.post("/borrow")
def borrow_book(request: BorrowRequest, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == request.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    reader = db.query(Reader).filter(Reader.id == request.reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    if book.num_of_books < 1:
        raise HTTPException(status_code=400, detail="Нет доступных экземпляров книги")

    active_borrows = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == request.reader_id,
        BorrowedBook.return_date is None
    ).count()
    if active_borrows >= 3:
        raise HTTPException(status_code=400, detail="Читатель уже имеет максимум книг (3шт.)")

    borrow = BorrowedBook(book_id=request.book_id, reader_id=request.reader_id)
    book.num_of_books -= 1

    db.add(borrow)
    db.commit()
    db.refresh(borrow)

    return {"message": "Книга успешно выдана", "borrow_id": borrow.id }

@router.put("/return")
def return_book(request: ReturnRequest , db: Session = Depends(get_db)):
    borrow = db.query(BorrowedBook).filter(BorrowedBook.id == request.borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Запись о выдаче не найдена")

    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Книга уже возвращена")

    book = db.query(BookDB).filter(BookDB.id == borrow.book.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    book.num_of_books += 1

    borrow.return_date = datetime.now(timezone.utc)
    db.commit()

    return {"message": "Книга успешно возвращена"}

@router.get("/reader/{reader_id}/active")
def get_active_books_for_reader(reader_id: int, db: Session = Depends(get_db)):
    active_borrows = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date is None).all()

    results = []
    for borrow in active_borrows:
        book = db.query(BookDB).filter(BookDB.id == borrow.book_id).first()
        if book:
            results.append({
                "book_id": book.id,
                "title": book.title,
                "author": book.author,
                "borrow_date": borrow.borrow_date
            })
    return results