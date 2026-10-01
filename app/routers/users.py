from typing import Annotated

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.schemas.users import UserCreate, UserRead


router = APIRouter(prefix="/users", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/", response_model=UserRead)
def create_user(data: UserCreate, session: SessionDep):
    user = User.model_validate(data)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get("/", response_model=list[UserRead])
def list_users(session: SessionDep):
    return session.exec(select(User)).all()