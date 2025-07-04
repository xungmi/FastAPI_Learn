from pydantic import BaseModel

class Book(BaseModel):
    id: int
    title: str
    author: str

book = Book(id=1, title="Clean Code", author="Robert C. Martin")
book_data = book.dict()
print(book_data)  # {'id': 1, 'title': 'Clean Code', 'author': 'Robert C. Martin'}

new_book = Book(**book_data)
print(new_book)  # id=1 title='Clean Code' author='Robert C. Martin'