# 📚 Book API

A **simple API for managing books** built with FastAPI and PostgreSQL.

This project allows you to:
- Add new books with images
- Search books by title, author, or publisher
- Get a list of authors and the number of books they have

---

## ⚡ Features

- Add new books with `POST /books/`
- Search books with `GET /search/?q=keyword`
- Get authors and book counts with `GET /authors/`
- Uses **SQLAlchemy Core** with PostgreSQL
- Stores book images in the `/images/` folder

---

## 🛠️ Installation & Setup

### Install environment and dependencies

```bash
python -m venv venv # Windows
venv\Scripts\activate # Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```
swagger UI : http://127.0.0.1:5432/docs