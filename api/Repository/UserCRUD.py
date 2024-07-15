from models import User
from database import db, execute_stmt_in_tran
from schemas import BaseUser, CompleteUser
from Authentication.hashing import hash_password


async def get_user_by_name(username: str) -> BaseUser:
    stmt = User.select().where(User.c.username == username)
    return await db.fetch_one(stmt)


async def create_user(user: BaseUser) -> bool:
    stmt = User.insert().values(username=user.username,
                                password=hash_password(user.password))
    return await execute_stmt_in_tran([stmt])
