from fastapi import HTTPException, status
from sqlmodel import Session, select
from datetime import datetime, timezone

from app.core.security import create_access_token, verify_password, decode_access_token
from app.models.user import User
from app.models.revoked_token import RevokedToken
from app.schemas.auth import UserLogin, TokenResponse
from jose import JWTError


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
    
    def logout(self, token: str) -> None:
        try:
            payload = decode_access_token(token)
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        jti = payload.get("jti")
        expires_at = payload.get("exp")

        if not jti or not expires_at:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        statement = select(RevokedToken).where(RevokedToken.jti == jti)
        revoked_token = self.session.exec(statement).first()

        if revoked_token:
            return

        revoked_token = RevokedToken(
            jti=jti,
            expires_at=datetime.fromtimestamp(expires_at, timezone.utc),
        )

        self.session.add(revoked_token)
        self.session.commit()