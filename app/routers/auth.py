from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.auth import TokenResponse, UserLogin
from app.services.auth_service import AuthService
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    auth_service = AuthService(session)

    return auth_service.login(login_data)

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    auth_service = AuthService(session)
    auth_service.logout(token)

    return {"message": "Logged out successfully"}