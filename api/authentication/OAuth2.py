from fastapi.security import OAuth2PasswordBearer

# Create an instance of OAuth2PasswordBearer to handle OAuth2 password flow.
# This is used to extract the access token from the request's Authorization header.
oauth2_token_scheme = OAuth2PasswordBearer(tokenUrl='/token')
