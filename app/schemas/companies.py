from datetime import datetime

from pydantic import EmailStr, Field
from sqlmodel import SQLModel


class CompanyCreate(SQLModel):
    legal_name: str = Field(min_length=2, max_length=255)
    trade_name: str | None = Field(default=None, max_length=255)
    document: str = Field(min_length=11, max_length=14)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=255)


class CompanyUpdate(SQLModel):
    legal_name: str | None = Field(default=None, min_length=2, max_length=255)
    trade_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


class CompanyResponse(SQLModel):
    id: int
    legal_name: str
    trade_name: str | None = None
    document: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None


class PaginationMeta(SQLModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedCompaniesResponse(SQLModel):
    data: list[CompanyResponse]
    pagination: PaginationMeta