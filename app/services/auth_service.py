from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.schemas.auth import UserLogin, TokenResponse


class AuthService:
    def __init__(self, session: Session):
        self.session = session

    def login(self, login_data: UserLogin) -> TokenResponse:
        statement = select(User).where(User.email == login_data.email)
        user = self.session.exec(statement).first()

        if not user or not verify_password(
            login_data.password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = create_access_token(str(user.id))

        return TokenResponse(access_token=access_token)