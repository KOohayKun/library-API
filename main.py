from fastapi import FastAPI
from Library.datab.database import init_db
from Library.routes import users, books, readers, borrowing

app = FastAPI()
init_db()

app.include_router(users.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrowing.router)
