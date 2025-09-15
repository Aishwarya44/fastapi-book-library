from fastapi import FastAPI
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

from routers import books, auth

app = FastAPI()

app.include_router(books.router, tags=["books"])
app.include_router(auth.router, tags=["auth"])





