from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Optional, List
from starlette import status

app = FastAPI()


# ====== MODELS ======
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


# ====== DỮ LIỆU MẪU ======
BOOKS: List[Book] = [
    Book(id=1, title="Clean Code", author="Robert C. Martin", description="Book 1", published_year=2008, rating=5),
    Book(id=2, title="The Pragmatic Programmer", author="Andrew Hunt", description="Book 2", published_year=1999, rating=4),
]


# ====== ENDPOINTS ======
@app.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_books():
    return BOOKS


@app.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(..., gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(book_create: BookCreate):
    new_id = len(BOOKS) + 1
    new_book = Book(id=new_id, **book_create.model_dump())  # dùng model_dump thay vì dict()
    BOOKS.append(new_book)
    return new_book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(..., gt=0)):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            del BOOKS[index]
            return  # 204 không trả về nội dung
    raise HTTPException(status_code=404, detail="Book not found")
