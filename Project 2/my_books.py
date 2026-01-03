from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithbakr",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2029,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "codingwithroby", "A very nice book!", 5, 2030),
    Book(2, "Be Fast with FastAPI", "codingwithroby", "A great book!", 5, 2030),
    Book(3, "Master Endpoints", "codingwithroby", "A awesome book!", 5, 2029),
    Book(4, "HP1", "Author 1", "Book Description", 2, 2028),
    Book(5, "HP2", "Author 2", "Book Description", 3, 2027),
    Book(6, "HP3", "Author 3", "Book Description", 1, 2026),
]


def add_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.get("/", status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.get("/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.get("/book_rating/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    keep_books = []
    for book in BOOKS:
        if book.rating <= book_rating:
            keep_books.append(book)
    return keep_books


@app.get("/publish/", status_code=status.HTTP_200_OK)
async def get_books_by_pubish_date(published_date: int = Query(gt=1999, lt=2031)):
    keep_books = []
    for book in BOOKS:
        if book.published_date == published_date:
            keep_books.append(book)
    return keep_books


@app.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(add_book_id(new_book))
    return new_book


@app.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(updated_book: BookRequest):
    for i, book in enumerate(BOOKS):
        if book.id == updated_book.id:
            BOOKS[i] = updated_book
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[i]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
