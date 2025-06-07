from fastapi import FastAPI
from Library.datab.database import init_db
from Library.routes import users, books

app = FastAPI()
init_db()

app.include_router(users.router)
app.include_router(books.router)
