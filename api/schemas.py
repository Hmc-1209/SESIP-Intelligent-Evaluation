from pydantic import BaseModel
from datetime import date


# ----- Schemas for User table -----
class BaseUser(BaseModel):
    username: str | None = None
    password: str | None = None


class CompleteUser(BaseUser):
    user_id: int

    class Config:
        from_attributes = True


# ----- Schemas for SecurityTarget table -----
class BaseST(BaseModel):
    st_name: str


class CompleteST(BaseST):
    create_date: date
    update_date: date
    sesip_level: int
    is_valid: bool
    owner_id: int

    class Config:
        from_attributes = True
