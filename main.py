from fastapi import FastAPI, Query, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List
import shutil

from databases import Database
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    select,
    or_,
)

DATABASE_URL = "postgresql+asyncpg://postgres:13861386@localhost:5432/bookdb"
database = Database(DATABASE_URL)
metadata = MetaData()


books_table = Table(
    "books",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(100)),
    Column("author", String(100)),
    Column("publisher", String(100)),
    Column("image_url", String(255)),
)


sync_engine = create_engine("postgresql://postgres:13861386@localhost:5432/bookdb")
metadata.create_all(sync_engine)


app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")


class Book(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    author: str
    publisher: str
    image_url: str


@app.on_event("startup")
async def startup():
    await database.connect()

    query = books_table.select().where(books_table.c.id == 1)
    existing = await database.fetch_one(query)
    if not existing:
        await database.execute(
            books_table.insert().values(
                id=1,
                title="Python Crash Course",
                author="Eric Matthes",
                publisher="No Starch Press",
                image_url="/images/1.jpg",
            )
        )


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/books/", response_model=Book)
async def add_book(
    id: int = Form(...),
    title: str = Form(..., min_length=3, max_length=100),
    author: str = Form(...),
    publisher: str = Form(...),
    image: UploadFile = File(...),
):

    query = books_table.select().where(books_table.c.id == id)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Book with this ID already exists")

    file_path = f"images/{image.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    await database.execute(
        books_table.insert().values(
            id=id,
            title=title,
            author=author,
            publisher=publisher,
            image_url=f"/images/{image.filename}",
        )
    )

    return Book(
        id=id,
        title=title,
        author=author,
        publisher=publisher,
        image_url=f"/images/{image.filename}",
    )


@app.get("/search/", response_model=List[Book])
async def search_books(q: str = Query(..., min_length=3, max_length=100)):
    query = select(books_table).where(
        or_(
            books_table.c.title.ilike(f"%{q}%"),
            books_table.c.author.ilike(f"%{q}%"),
            books_table.c.publisher.ilike(f"%{q}%"),
        )
    )
    results = await database.fetch_all(query)
    return [Book(**r) for r in results]
