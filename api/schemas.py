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
    st_details: dict | None
    eval_details: dict | None
    is_evaluated: bool
    eval_passed: bool | None
    eval_model: str | None


class UpdateST(BaseModel):
    token: str


class EvaluateST(BaseModel):
    st_details: dict
    eval_details: dict
    eval_passed: bool
    eval_model: str
