from pydantic import BaseModel
from datetime import date


# ----- Schemas for User table -----
class BaseUser(BaseModel):
    username: str | None = None


class DetailUser(BaseUser):
    password: str | None = None


class CompleteUser(BaseUser):
    user_id: int

    class Config:
        from_attributes = True


# ----- Schemas for SecurityTarget table -----
class BaseST(BaseModel):
    st_name: str | None = None

    class Config:
        from_attributes = True


class DetailST(BaseST):
    st_id: int
    st_details: dict
    is_valid: bool


class UpdateST(BaseST):
    owner_id: int | None = None
