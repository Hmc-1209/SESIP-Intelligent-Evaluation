from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from repository.TokenCRUD import generate_access_token, validate_access_token
from authentication.JWTtoken import get_current_user
from utils.transfer_token_process import generate_transfer_token
from exception import validation_failed
from schemas import CompleteUser

router = APIRouter(prefix="/token", tags=["Token"])


@router.post("/")
async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    """
    Generate a new access token for the user.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password for authentication.

    Returns:
        dict[str, str]: A dictionary containing the generated access token.

    Raises:
        validation_failed: If the username or password is incorrect or token generation fails.
    """

    data = {
        "username": form_data.username,
        "password": form_data.password
    }

    token = await generate_access_token(data)

    if not token:
        raise validation_failed

    return {"access_token": token}


@router.post("/validate_access_token")
async def validate_the_access_token(token: str) -> CompleteUser:
    """
    Validate the provided access token and return the associated user information.

    Args:
        token (str): The access token to validate.

    Returns:
        CompleteUser: The user information associated with the valid access token.
    """

    return await validate_access_token(token)


@router.post("/transfer_token")
async def create_transfer_token(current_user=Depends(get_current_user)) -> str:
    return generate_transfer_token(current_user.user_id)
