import sqlalchemy
from sqlalchemy import Column, ForeignKey
from database import metadata

User = sqlalchemy.Table(
    "User",
    metadata,
    Column("user_id", sqlalchemy.INTEGER, primary_key=True, index=True),
    Column("username", sqlalchemy.VARCHAR(50), nullable=False, unique=True),
    Column("password", sqlalchemy.CHAR(64), nullable=False)
)

SecurityTarget = sqlalchemy.Table(
    "SecurityTarget",
    metadata,
    Column("st_id", sqlalchemy.INTEGER, primary_key=True, index=True),
    Column("st_name", sqlalchemy.VARCHAR(50), nullable=False, unique=True),
    Column("st_details", sqlalchemy.JSON, nullable=False),
    Column("st_file", sqlalchemy.TEXT, nullable=False),
    Column("eval_details", sqlalchemy.TEXT, nullable=False),
    Column("eval_file", sqlalchemy.TEXT, nullable=False),
    Column("is_valid", sqlalchemy.BOOLEAN, nullable=False),
    Column("owner_id", sqlalchemy.INTEGER, ForeignKey("User.user_id"), nullable=False)
)
