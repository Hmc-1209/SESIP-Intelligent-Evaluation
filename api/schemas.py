from pydantic import BaseModel
from datetime import date


# ----- Schemas for User table -----
class BaseUser(BaseModel):
    username: str
    password: str


class CompleteUser(BaseUser):
    user_id: int

    class Config:
        from_attributes = True


class BaseST(BaseModel):
    st_name: str
    is_valid: bool


class CompleteST(BaseST):
    create_date: date
    update_date: date
    sesip_level: int
    owner_id: int

    class Config:
        from_attributes = True
