from fastapi import HTTPException, status

# Bad Request (400) Exceptions
bad_request = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Request failed.")

duplicate_data = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail="Data Duplicated.")

st_not_belongs = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                               detail="Security Target not belongs to user.")

invalid_model = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Invalid model.")

invalid_level = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Invalid level.")

invalid_token = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="Invalid token.")

eval_has_performed = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail="Evaluation has been performed.")

eval_not_performed = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                   detail="Evaluation has not been performed.")

evaluation_failed = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail="Evaluation failed.")

validation_failed = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                  detail="Username or password incorrect.")

# Unauthorized (401) Exceptions
token_expired = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="Could not validate credentials.",
                              headers={"WWW-Authenticate": "Bearer"})

password_incorrect = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail="Password incorrect.")

# Not Found (404) Exceptions
no_such_st = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                           detail="Security Target not found.")

no_such_file = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="File not found.")
