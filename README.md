# NOVA E‑Commerce

A futuristic e‑commerce store with FastAPI backend and PostgreSQL.

## Run locally

1. Create a PostgreSQL database `nova`.
2. Run `database/schema.sql` to create tables and insert sample data.
3. Copy `.env.example` to `.env` and set your `DATABASE_URL`.
4. Install dependencies: `pip install -r requirements.txt`
5. Run: `uvicorn backend.main:app --reload`
6. Open `frontend/index.html` in your browser (or serve via the backend).

## Deploy with Docker

`docker-compose up -d`
