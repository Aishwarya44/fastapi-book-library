from fastapi import APIRouter
from pydantic import BaseModel
from models import Book
from database import SessionLocal


router = APIRouter()


class Book_Schema(BaseModel):
    id: int
    title: str
    author: str
    published_year: int
    available: bool

@router.get("/books")
def read_books():
    db: SessionLocal = SessionLocal()
    books = db.query(Book).all()
    return books


@router.post("/create-book")
def create_book(b1: Book_Schema):
    db: SessionLocal = SessionLocal()

    existing_book = db.query(Book).filter(Book.title == b1.title).first()
    if existing_book:
        return {"message": "Book already exists"}

    new_book = Book(id=b1.id, title=b1.title, author=b1.author, published_year=b1.published_year, available=True)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.put("/update-book/{title}")
def update_book(title: str, b1: Book_Schema):
    db: SessionLocal = SessionLocal()
    existing_book = db.query(Book).filter(Book.title == title).first()
    if not existing_book:
        return {"message": "Book not found"}
    existing_book.title = b1.title
    existing_book.author = b1.author
    existing_book.published_year = b1.published_year
    existing_book.id = b1.id
    existing_book.available = b1.available
    db.add(existing_book)
    db.commit()
    db.refresh(existing_book)
    return existing_book


@router.delete("/delete-book/{title}")
def delete_book(title: str):
    db: SessionLocal = SessionLocal()
    existing_book = db.query(Book).filter(Book.title == title).first()
    if not existing_book:
        return {"message": "Book not found"}

    db.delete(existing_book)
    db.commit()
    return {"message": "Book deleted"}