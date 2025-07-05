from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi import HTTPException
app = FastAPI()

# Danh sách sách mẫu
books = [
    {"title": "Title 1", "author": "Author 1", "category": "Science"},
    {"title": "Title 2", "author": "Author 2", "category": "Science"},
    {"title": "Title 3", "author": "Author 3", "category": "History"},
    {"title": "Title 4", "author": "Author 4", "category": "Math"},
    {"title": "Title 5", "author": "Author 5", "category": "Math"},
    {"title": "Title 6", "author": "Author 2", "category": "Math"},
]

class Book(BaseModel):
    title: str
    author: str
    category: str

# Endpoint để đọc tất cả sách
@app.get("/books")
async def read_all_books():
    return books

@app.get("/books/my-book")
async def read_my_favorite_book():
    return {"title": "My Favorite Book"}

@app.get("/books/{book_title}")
async def read_book(book_title: str, category: Optional[str] = False):
    for book in books:
        if book["title"] == book_title:
            if category == book["category"]:
                return {"title": book["title"], "category": book["category"]}
            return book
    return {"error": "Book not found"}

@app.post("/books/create-book")
async def create_book(new_book: Book):
    books.append(new_book.dict())
    return new_book

@app.put("/books/update-book/{book_title}")
async def update_book(book_title: str, updated_book: Book):
    for book in books:
        if book["title"].lower() == book_title.lower():
            book.update(updated_book.dict())
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/delete-book/{book_title}")
async def delete_book(book_title: str):
    for book in books:
        if book["title"].lower() == book_title.lower():
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

# 1. Create a new API Endpoint that can 
# fetch all books from a specific author 
# using either Path Parameters or Query Parameters.
@app.get("/books/author/{author_name}")
async def read_books_by_author(author_name: str):
    author_books = [book for book in books if book["author"].lower() == author_name.lower()]
    if not author_books:
        raise HTTPException(status_code=404, detail="No books found for this author")
    return author_books
