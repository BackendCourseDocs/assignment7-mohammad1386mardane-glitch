from fastapi import FastAPI, Query, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List
import shutil

app = FastAPI()


app.mount("/images", StaticFiles(directory="images"), name="images")


class Book(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    author: str
    publisher: str
    image_url: str


books: List[Book] = [
    
]

@app.post("/books/", response_model=Book)
def add_book(
    id: int = Form(...),
    title: str = Form(..., min_length=3, max_length=100),
    author: str = Form(...),
    publisher: str = Form(...),
    image: UploadFile = File(...)
):

    if any(b.id == id for b in books):
        raise HTTPException(status_code=400, detail="Book with this ID already exists")

    file_path = f"images/{image.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    new_book = Book(
        id=id,
        title=title,
        author=author,
        publisher=publisher,
        image_url=f"/images/{image.filename}"
    )

    books.append(new_book)
    return new_book

@app.get("/search/", response_model=List[Book])
def search_books(
    q: str = Query(..., min_length=3, max_length=100)
):
    return [
        book for book in books
        if q.lower() in book.title.lower()
        or q.lower() in book.author.lower()
        or q.lower() in book.publisher.lower()
    ]