# 📚 Book API with FastAPI

A simple API to manage books with image upload.

---

## ⚡ Features

- Add a book with an image (`POST /books/`)
- Search books by title, author, or publisher (`GET /search/`)
- Title and query length: 3–100 characters
- Images stored in `images/` folder
- Data stored in SQL

---

## 🛠 Installation

1. Clone the repo:

```bash
git clone https://github.com/USERNAME/REPO.git
cd REPO
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate  # Linux / Mac

pip install -r requirements.txt

python -m uvicorn main:app --reload

Swagger UI: http://127.0.0.1:8000/docs
```
