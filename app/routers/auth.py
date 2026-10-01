from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.schemas.auth import TokenResponse, UserLogin
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    auth_service = AuthService(session)

    return auth_service.login(login_data)