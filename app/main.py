import psycopg
from fastapi import FastAPI, HTTPException
from app.routers import users

app = FastAPI(title="FastAPI PostgreSQL")

app.include_router(users.router)