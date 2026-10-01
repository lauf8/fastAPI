from sqlmodel import SQLModel


class UserCreate(SQLModel):
    name: str
    email: str


class UserResponse(SQLModel):
    id: int
    name: str
    email: str
    phone: str | None = None
    address: str | None = None

class PaginationMeta(SQLModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedUsersResponse(SQLModel):
    data: list[UserResponse]
    pagination: PaginationMeta