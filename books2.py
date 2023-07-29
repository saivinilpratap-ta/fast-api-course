from fastapi import  FastAPI, Body
from fastapi import  Path #a way to validate path paramters of an API
from fastapi import  Query #a way to validate Query paramters of an API
from fastapi import HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import  status
app=FastAPI()




class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self,id,title,author,description,rating,published_date):
        self.id=id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
BOOKS = [
    Book(1,"Me pro","Vinil","very nice man",5,2021),
    Book(3,"Me Good","Vinil3","very good man",5,2022),
    Book(2,"Me confident","Vinil2","very confident man",5,2023),
]

class BookRequest(BaseModel):
    """
    These below validations are visibile in swagger API endpoint,
    as we are using BaseModel, Field. This is also visible as a
    Docstring in the swagger UI
    """
    id:Optional[int] = Field(title="id is not needed")
    title: str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating:int = Field(gt= 0, lt = 6)
    published_date:int = Field(gt = 0)

    class Config:
        """
        we will be using this class as a text placeholder in swagger
        documentation, so that user who wants to send an input can
        copy this text, make some changes, then send it body of API.
        """
        json_schema_extra = {
            'example' : {
                "title" : "A new book",
                "author" : "vinil",
                "description": "Wonderful book on the cards",
                "rating" : 5,
                "published_date": 2023
            }
        }
@app.get("/books")
async  def read_all_books():
    return BOOKS

@app.post("/create_book", status_code = status.HTTP_201_CREATED)
async  def create_book(book_request:BookRequest):
    print(type(book_request))
    new_book = Book(**book_request.dict())
    new_book = find_book_id(new_book)
    print(type(new_book))
    BOOKS.append(new_book)

@app.get("/book/{book_id}", status_code = status.HTTP_200_OK)
async def fetch_a_particular_book(book_id: int = Path(gt=0)): #this defines that ID that is being passed as a path parameter should be greater than 0
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="item not found")

@app.get('/book/fetch_by_rating/')
async  def fetch_a_book_by_rating(rating: int = Query(ge=1,le=5)):
    book_list = []
    for book in BOOKS:
        if book.rating == rating:
            book_list.append(book)
    return book_list

@app.put('/book/update_book' , status_code = status.HTTP_204_NO_CONTENT)
async def update_particular_book(updated_book:BookRequest):
    for ind,value in enumerate(BOOKS):
        if value.id == updated_book.id:
            BOOKS[ind] = updated_book
    # return BOOKS

@app.delete('/book/remove_book')
async def remove_particular_book(book:BookRequest):
    for ind,value in enumerate(BOOKS):
        if value.id == book.id:
            BOOKS.remove(BOOKS)
    return BOOKS

@app.get('/book/get_books_by_published_date/{published_date}')
def fetch_books_by_published_date(published_date:int = Path(gt=2019)):
    books_of_published_date=[]
    for book in BOOKS:
        print(book.published_date)
        print(published_date)
        if book.published_date == published_date:
            books_of_published_date.append(book)
    return  books_of_published_date

@app.get('/book/get_books_by_published_dates/')
def fetch_books_by_published_dates(published_date:int):
    books_of_published_date=[]
    for book in BOOKS:
        print(book.published_date)
        print(published_date)
        if book.published_date == published_date:
            books_of_published_date.append(book)
    return  books_of_published_date

def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book

