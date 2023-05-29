import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from app.schema import Book as SchemaBook
from app.schema import Author as SchemaAuthor

from app.schema import Book
from app.schema import Author

from app.models import Book as ModelBook
from app.models import Author as ModelAuthor

import os
from dotenv import load_dotenv

load_dotenv('.env')


app = FastAPI()

# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url='postgresql://postgres:password123@postgres/fastapi')

@app.get("/")
async def root():
    return {"message": "Welcome to book world"}


@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id = book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.get('/books/')
async def books():
    books = db.session.query(ModelBook).all()
    return books

@app.get('/books/{book_id}')
async def books(book_id: int):
    # books = db.session.query(ModelBook).all()
    return {"book": f"Description for book id {book_id}"}
  
@app.post('/author/', response_model=SchemaAuthor)
async def author(author:SchemaAuthor):
    db_author = ModelAuthor(name=author.name, age=author.age)
    db.session.add(db_author)
    db.session.commit()
    return db_author

@app.get('/authors/')
async def authors():
    authors = db.session.query(ModelAuthor).all()
    return authors

@app.get('/authors/{author_id}')
async def authors(author_id: int):
    author = db.session.query(ModelAuthor).get(author_id)
    return author

# To run locally
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)