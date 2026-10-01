from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: int | None = Field(default=None, primary_key=True)
    legal_name: str
    trade_name: str | None = None
    document: str = Field(index=True, unique=True)
    email: str | None = Field(default=None, index=True)
    phone: str | None = None
    address: str | None = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None