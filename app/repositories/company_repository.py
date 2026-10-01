from sqlmodel import Session, func, select

from app.models.company import Company


class CompanyRepository:
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, company_id: int) -> Company | None:
        return self.session.get(Company, company_id)

    def find_by_document(self, document: str) -> Company | None:
        statement = select(Company).where(Company.document == document)

        return self.session.exec(statement).first()

    def paginate(self, page: int, per_page: int):
        offset = (page - 1) * per_page

        total_statement = select(func.count()).select_from(Company)
        total = self.session.exec(total_statement).one()

        companies_statement = (
            select(Company)
            .order_by(Company.id)
            .offset(offset)
            .limit(per_page)
        )

        companies = self.session.exec(companies_statement).all()

        return {
            "data": companies,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page,
                "has_next": page * per_page < total,
                "has_previous": page > 1,
            },
        }

    def create(self, company: Company) -> Company:
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)

        return company

    def delete(self, company: Company) -> None:
        self.session.delete(company)
        self.session.commit()