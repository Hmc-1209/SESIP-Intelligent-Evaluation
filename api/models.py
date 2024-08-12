import sqlalchemy
from sqlalchemy import Column, ForeignKey
from database import metadata

# Define the User table schema
User = sqlalchemy.Table(
    "User",
    metadata,
    Column("user_id", sqlalchemy.INTEGER, primary_key=True, index=True),
    Column("username", sqlalchemy.VARCHAR(50), nullable=False, unique=True),
    Column("password", sqlalchemy.CHAR(64), nullable=False)
)

# Define the SecurityTarget table schema
SecurityTarget = sqlalchemy.Table(
    "SecurityTarget",
    metadata,
    Column("st_id", sqlalchemy.INTEGER, primary_key=True, index=True),
    Column("st_name", sqlalchemy.VARCHAR(50), nullable=False),
    Column("st_details", sqlalchemy.JSON, nullable=True),
    Column("is_evaluated", sqlalchemy.BOOLEAN, nullable=False),
    Column("eval_passed", sqlalchemy.BOOLEAN, nullable=True),
    Column("eval_model", sqlalchemy.VARCHAR(15), nullable=True),
    Column("owner_id", sqlalchemy.INTEGER, ForeignKey("User.user_id"), nullable=False)
)
