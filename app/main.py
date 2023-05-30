import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from collections import defaultdict



from sqlalchemy.inspection import inspect
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
templates = Jinja2Templates(directory="app/templates")



import pandas as pd
def query_to_dict(rset):
    result = defaultdict(list)
    for obj in rset:
        instance = inspect(obj)
        for key, x in instance.attrs.items():
            result[key].append(x.value)
    return result


# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url='postgresql://postgres:password123@postgres/fastapi')

@app.get("/")
async def root(request: Request,response_class=HTMLResponse):
    return templates.TemplateResponse("base.html", 
            {"request": request})    

@app.post('/book/', response_model=SchemaBook)
async def book(book: SchemaBook):
    db_book = ModelBook(title=book.title, rating=book.rating, author_id = book.author_id)
    db.session.add(db_book)
    db.session.commit()
    return db_book

@app.get('/books/')
async def books(request: Request, response_class=HTMLResponse):
    books = db.session.query(ModelBook).all()
    df = pd.DataFrame(query_to_dict(books))
    return templates.TemplateResponse("table.html", 
            {"request": request, "table": df.to_html()})

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