from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field
from pydantic import model_validator
from api.security import HashedPassword
from api.utils.models import TimestamppedModel


class User(TimestamppedModel, table=True):
    id: Optional[UUID] = Field(
        primary_key=True, nullable=False, default_factory=uuid4
    )
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    password: HashedPassword
    is_admin: bool = Field(default=False)

    @model_validator(mode="before")
    def format_unique_fields(self):
        self.email = self.email.lower().replace(" ", "")
        self.username = self.username.lower().replace(" ", "")

        return self
