from fastapi import APIRouter, Query
from sqlmodel import Session, select, func

from app.database import engine
from app.models.user import User
class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def paginate(
        self,
        page: int,
        per_page: int,
    ):
        offset = (page - 1) * per_page
        total_statement = select(func.count()).select_from(User)
        total = self.session.exec(total_statement).one()
        users_statement = (
            select(User)
            .order_by(User.id)
            .offset(offset)
            .limit(per_page)
        )
        users = self.session.exec(users_statement).all()
        return {
            "data": users,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page,
                "has_next": page * per_page < total,
                "has_previous": page > 1,
            },
        }