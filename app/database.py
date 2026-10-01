import os

from sqlalchemy.engine import URL
from sqlmodel import Session, create_engine


database_url = URL.create(
    "postgresql+psycopg",
    username=os.environ["PGUSER"],
    password=os.environ["PGPASSWORD"],
    host=os.environ["PGHOST"],
    port=int(os.environ["PGPORT"]),
    database=os.environ["PGDATABASE"],
)

engine = create_engine(database_url)


def get_session():
    with Session(engine) as session:
        yield session