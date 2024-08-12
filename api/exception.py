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

no_such_file = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail="File not found.")

eval_has_performed = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                   detail="Evaluation has been performed.")

eval_not_performed = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                   detail="Evaluation has not been performed.")

evaluation_failed = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail="Evaluation failed.")

invalid_model = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                              detail="Invalid model.")

invalid_level = HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                              detail="Invalid level.")
