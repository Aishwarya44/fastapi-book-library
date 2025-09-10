from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

router = APIRouter()

BOOKS = [
    {"id": 1, "title": "Book 1", "author": "author one", "published_year": 2000 , "available": True},
    {"id": 2, "title": "Book 2", "author": "author two", "published_year": 2001 , "available": True},
    {"id": 3, "title": "Book 3", "author": "author three", "published_year": 2002 , "available": True},
    {"id": 4, "title": "Book 4", "author": "author four", "published_year": 2003 , "available": True},
    {"id": 5, "title": "Book 5", "author": "author five", "published_year": 2004 , "available": True},
]

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: int
    available: bool

class BookCreate(Book):
    pass

class BookUpdate(Book):
    pass

class BookDelete(Book):
    pass


@router.get("/books")
def read_books():
    return BOOKS


@router.post("/create-book")
def create_book(b1: BookCreate):
    found_book = False
    for book in BOOKS:
        if b1.title == book["title"]:
            found_book = True
            return HttpResponse(f"Book {book.id} already exists")

    if not found_book:
        BOOKS.append(b1)

    return b1


@router.put("/update-book/{title}")
def update_book(title: str, b1: BookCreate):
    book_updated = False
    for book in BOOKS:
        if book["title"] == title:
            book["title"] = b1.title
            book["author"] = b1.author
            book["published_year"] = b1.published_year
            book["available"] = b1.available
            book_updated = True

    if not book_updated:
        return HTMLResponse(f"Book {title} not found")
    else:
        return HTMLResponse(f"Book Updated")