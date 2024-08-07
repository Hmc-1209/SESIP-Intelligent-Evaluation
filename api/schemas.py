from pydantic import BaseModel, ConfigDict
# from fastapi.responses import FileResponse


# ----- Schemas for User table -----
class BaseUser(BaseModel):
    username: str


class DetailUser(BaseUser):
    password: str


class UpdateUser(BaseModel):
    old_password: str
    new_password: str


class CompleteUser(BaseUser):
    user_id: int

    model_config = ConfigDict(
        from_attributes=True
    )


# ----- Schemas for SecurityTarget table -----
class BaseST(BaseModel):
    st_name: str | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class ListST(BaseST):
    st_id: int


class DetailST(ListST):
    st_details: dict
    eval_details: dict | None
    is_evaluated: bool
    is_valid: bool | None


class UpdateST(BaseST):
    owner_id: int | None = None
