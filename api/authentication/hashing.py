from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password) -> str:
    """
    Hash the given password using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def verify_password(plain_pwd, hashed_pwd) -> bool:
    """
    Verify that the plain text password matches the hashed password.

    Args:
        plain_pwd (str): The plain text password to check.
        hashed_pwd (str): The hashed password to compare against.

    Returns:
        bool: True if the plain text password matches the hashed password, otherwise False.
    """
    return pwd_context.verify(plain_pwd, hashed_pwd)
