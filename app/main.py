import psycopg
from fastapi import FastAPI, HTTPException
from app.routers import users,auth

app = FastAPI(title="FastAPI PostgreSQL")

app.include_router(users.router, prefix="/v1")
app.include_router(auth.router, prefix="/v1")