from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()


@app.get("/")
def home() -> dict[str, str]:
    return {"message": "Hello, FastAPI!"}


class BookIn(BaseModel):
    title: str
    author: str
    pages: int


class BookOut(BookIn):
    id: int


class BooksResponse(BaseModel):
    books: List[BookOut]


books: list[BookOut] = [
    BookOut(id=1, title="Python Basics", author="Real P.", pages=635),
    BookOut(id=2, title="Breaking the Rules", author="Stephen G.", pages=99),
]


@app.get("/books", response_model=BooksResponse)
def get_books(limit: Optional[int] = None) -> BooksResponse:
    """Get all books, optionally limited by count."""
    items: List[BookOut] = books[:limit] if limit else books
    return BooksResponse(books=items)


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int) -> BookOut:
    """Get a specific book by ID."""
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=BookOut)
def create_book(book: BookIn) -> BookOut:
    """Create a new book entry."""
    new_book = BookOut(
        id=len(books) + 1, title=book.title, author=book.author, pages=book.pages
    )
    books.append(new_book)
    return new_book
