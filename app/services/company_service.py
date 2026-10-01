from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlmodel import Session

from app.models.company import Company
from app.repositories.company_repository import CompanyRepository
from app.schemas.companies import CompanyCreate, CompanyUpdate


class CompanyService:
    def __init__(self, session: Session):
        self.repository = CompanyRepository(session)
        self.session = session

    def list_companies(self, page: int, per_page: int):
        return self.repository.paginate(page, per_page)

    def get_company(self, company_id: int) -> Company:
        company = self.repository.find_by_id(company_id)

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company not found",
            )

        return company

    def create_company(self, company_data: CompanyCreate) -> Company:
        existing_company = self.repository.find_by_document(company_data.document)

        if existing_company:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Document already exists",
            )

        company = Company(
            legal_name=company_data.legal_name,
            trade_name=company_data.trade_name,
            document=company_data.document,
            email=company_data.email,
            phone=company_data.phone,
            address=company_data.address,
        )

        return self.repository.create(company)

    def update_company(
        self,
        company_id: int,
        company_data: CompanyUpdate,
    ) -> Company:
        company = self.get_company(company_id)

        update_data = company_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(company, field, value)

        company.updated_at = datetime.now(timezone.utc)

        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)

        return company

    def delete_company(self, company_id: int) -> None:
        company = self.get_company(company_id)

        self.repository.delete(company)