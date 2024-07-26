from fastapi import HTTPException, status

validation_failed = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Username or password incorrect.")

token_expired = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Could not validate credentials.",
                              headers={"WWW-Authenticate": "Bearer"})

bad_request = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Request failed.")

duplicate_data = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail="Data Duplicated.")

no_such_user = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="User not found.")
password_incorrect = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail="Password incorrect.")

no_such_st = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="Security Target not found.")

st_not_belongs = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                               detail="Security Target not belongs to user.")
