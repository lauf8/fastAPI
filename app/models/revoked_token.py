from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class RevokedToken(SQLModel, table=True):
    __tablename__ = "revoked_tokens"

    id: int | None = Field(default=None, primary_key=True)
    jti: str = Field(index=True, unique=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))