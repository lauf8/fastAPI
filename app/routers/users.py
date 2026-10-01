from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.schemas.users import UserCreate, UserResponse, PaginatedUsersResponse
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session)]



@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate, session: Session = Depends(get_session)):
    user_service = UserService(session)

    return user_service.create_user(user_data)

@router.get("/", response_model=PaginatedUsersResponse)
def list_users(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
):
    repository = UserRepository(session)

    return repository.paginate(
        page=page,
        per_page=per_page,
    )