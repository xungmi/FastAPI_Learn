from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from starlette import status


app = FastAPI()


# Models
class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_year: int
    rating: Optional[int] = None


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=10, max_length=300)
    published_year: int = Field(..., ge=0, le=2100)
    rating: Optional[int] = Field(default=None, ge=0, le=5)
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "description": "A handbook of agile software craftsmanship.",
                "published_year": 2008,
                "rating": 5
            }
        }

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=300)
    published_year: Optional[int] = Field(None, ge=0, le=2100)
    rating: Optional[int] = Field(None, ge=0, le=5)

# ====== Sample data ======
BOOKS: List[Book] = [
    Book(
        id=1,
        title="Clean Code",
        author="Robert C. Martin",
        description="A handbook of agile software craftsmanship.",
        published_year=2008,
        rating=5
    ),
    Book(
        id=2,
        title="The Pragmatic Programmer",
        author="Andrew Hunt",
        description="Your journey to mastery in software development.",
        published_year=1999,
        rating=4
    ),
    Book(
        id=3,
        title="Atomic Habits",
        author="James Clear",
        description="An easy & proven way to build good habits & break bad ones.",
        published_year=2018,
        rating=5
    ),
]


# ====== ENDPOINTS ======
@app.get("/books", status_code=status.HTTP_200_OK, response_model=List[Book])
async def get_books(
    id : Optional[int] = Query(None, gt=0, description="Filter by book ID (must be > 0)"),
    title: Optional[str] = Query(None, min_length=1, max_length=100, description="Filter by book title"),
    author: Optional[str] = Query(None, min_length=1, max_length=100, description="Filter by book author"),
    published_year: Optional[int] = Query(None, gt=0, le=2100, description="Filter by published year"),
    rating: Optional[int] = Query(None, ge=0, le=5, description="Filter by book rating")
):
    result = BOOKS
    if id:
        result = [book for book in result if book.id == id]
    if title:
        result = [book for book in result if book.title.lower() == title.lower()]
    if author:
        result = [book for book in result if book.author.lower() == author.lower()]
    if published_year:
        result = [book for book in result if book.published_year == published_year]
    if rating:
        result = [book for book in result if book.rating == rating]
    return result


@app.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_create: BookCreate):
    new_id = len(BOOKS) + 1
    new_book = Book(id=new_id, **book_create.dict())
    BOOKS.append(new_book)
    return new_book


@app.put("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(
    book_id: int = Path(..., gt=0, description="The ID of the book to update (must be > 0)"),
    book_update: BookUpdate = ...
):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            if not book_update.dict(exclude_unset=True):
                raise HTTPException(status_code=400, detail="No data provided for update")
            
            updated_book = book.copy(update=book_update.dict(exclude_unset=True))
            BOOKS[index] = updated_book
            return
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(..., gt=0, description="The ID of the book to delete (must be > 0)")):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[index]
            return
    raise HTTPException(status_code=404, detail="Book not found")
