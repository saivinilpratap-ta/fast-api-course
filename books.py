from fastapi import FastAPI,Body

apps = FastAPI() #to use FastAPI here


BOOKS = [
    {"title":"1", "author":'Author One', 'category':'fiction'},
{"title":"2", "author":'Author Two', 'category':'fiction'},
{"title":"3", "author":'Author Three', 'category':'science'},
{"title":"4", "author":'Author Four', 'category':'science'},
{"title":"5", "author":'Author Five', 'category':'Political'},
{"title":"6", "author":'Author Six', 'category':'Political'},
]


@apps.get("/books") #books here is the endpoint.
async def read_all_books(): #by default all functions are async, as it is the framework starlette that fastapi uses.
    return  BOOKS

@apps.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param:str):
    return  {"dynamic_param":dynamic_param}

@apps.get("/books/")
def get_books_by_category(category:str):
    books_list=[]

    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_list.append(book)
    return books_list

@apps.post('/books/new_book')
def add_new_book(new_book = Body()):
    BOOKS.append(new_book)
    return BOOKS

@apps.put('/books/update_book')
async def update_particular_book(update_book=Body()):
    """here using title, we will update the genre"""
    for book in BOOKS:
        if book.get("title").casefold() == update_book.get("title").casefold():
            book["category"] = update_book.get("category")


@apps.delete('/books/delete_book/{book_title}')
def remove_book(book_title:str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            BOOKS.pop(book)

@apps.get('/books/get_author_specific_books/{author}')
def fetch_author_related_books(author:str):
    author_specific_books = []
    for book in BOOKS:
        if book.get("author").casefold() == author.casefold():
            author_specific_books.append(book)
    return author_specific_books
