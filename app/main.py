import psycopg
from fastapi import FastAPI, HTTPException
from app.routers import auth, companies, users

app = FastAPI(title="FastAPI PostgreSQL")

app.include_router(users.router, prefix="/v1")
app.include_router(auth.router, prefix="/v1")
app.include_router(companies.router, prefix="/v1")