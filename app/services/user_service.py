from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.core.security import hash_password
from app.models.user import User
from app.schemas.users import UserCreate


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserCreate) -> User:
        self.ensure_email_is_unique(user_data.email)
        self.ensure_phone_is_unique(user_data.phone)
        user = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
            address=user_data.address,
            phone=user_data.phone,
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user
    def ensure_email_is_unique(self, email: str) -> None:
        statement = select(User).where(User.email == email)
        user = self.session.exec(statement).first()

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists",
            )

    def ensure_phone_is_unique(self, phone: str | None) -> None:
        if phone is None:
            return

        statement = select(User).where(User.phone == phone)
        user = self.session.exec(statement).first()

        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Phone already exists",
            )