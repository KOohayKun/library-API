from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Library.models.reader_model import ReaderCreate, Reader as ReaderModel
from Library.datab.dbmodels import Reader as ReaderDB
from Library.datab.database import get_db
from Library.utils.security import get_current_user, hash_password
from Library.models.user_model import User
from typing import List
from Library.models.reader_model import ReaderUpdate

router = APIRouter(prefix="/readers", tags=["reader"])

@router.post("/", response_model=ReaderModel)
def create_reader(reader: ReaderCreate, db: Session = Depends(get_db)):
    new_reader = ReaderDB(
        name=reader.name,
        email=reader.email,
        hashed_password=hash_password(reader.password)
    )
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    return ReaderModel(
        id=new_reader.id,
        name=new_reader.name,
        email=new_reader.email
    )

@router.get("/{id}", response_model=ReaderModel)
def get_reader(id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    reader = db.query(ReaderDB).filter(ReaderDB.id == id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    return ReaderModel(
        id=reader.id,
        name=reader.name,
        email=reader.email_librarian
    )

@router.get("/", response_model=List[ReaderModel])
def get_all_readers(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    readers = db.query(ReaderDB).all()
    return [
        ReaderModel(
            id=R.id,
            name=R.name,
            email=R.email
        ) for R in readers
    ]

@router.put("/{id}", response_model=ReaderModel)
def update_reader(id: int, reader_update: ReaderUpdate,
                  db: Session = Depends(get_db),
                  _: User = Depends(get_current_user)):
    reader = db.query(ReaderDB).filter(ReaderDB.id == id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    update_data = reader_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(reader, key, value)

    db.commit()
    db.refresh(reader)

    return ReaderModel(
        id=reader.id,
        name=reader.name,
        email=reader.email_librarian
    )

@router.delete("/{id}")
def delete_reader(id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    reader = db.query(ReaderDB).filter(ReaderDB.id == id).first()
    if reader is None:
        raise HTTPException(status_code=404, detail="Читатель не найден")

    db.delete(reader)
    db.refresh()
    return {"message": "Читатель удалён"}
