from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password):
    """Hash the password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_pwd, hashed_pwd):
    """Verify the hashed password against plain password"""
    return pwd_context.verify(plain_pwd, hashed_pwd)
