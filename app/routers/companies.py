from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.database import get_session
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.companies import (
    CompanyCreate,
    CompanyResponse,
    CompanyUpdate,
    PaginatedCompaniesResponse,
)
from app.services.company_service import CompanyService


router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(
    company_data: CompanyCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    company_service = CompanyService(session)

    return company_service.create_company(company_data)


@router.get("/", response_model=PaginatedCompaniesResponse)
def list_companies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    company_service = CompanyService(session)

    return company_service.list_companies(page, per_page)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    company_service = CompanyService(session)

    return company_service.get_company(company_id)


@router.patch("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    company_service = CompanyService(session)

    return company_service.update_company(company_id, company_data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    company_service = CompanyService(session)
    company_service.delete_company(company_id)