from pydantic import BaseModel


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


class ListST(BaseST):
    st_id: int


class DetailST(ListST):
    st_details: dict
    st_file: str
    eval_details: str
    is_valid: bool


class CreateST(BaseST):
    st_details: dict
    st_file: str
    eval_details: str
    eval_file: str
    is_valid: bool


class UpdateST(BaseST):
    owner_id: int | None = None
