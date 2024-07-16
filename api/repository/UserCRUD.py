from models import User, SecurityTarget
from database import db, execute_stmt_in_tran
from schemas import BaseUser, CompleteUser
from authentication.hashing import hash_password


async def get_user_by_name(username: str) -> BaseUser:
    stmt = User.select().where(User.c.username == username)
    return await db.fetch_one(stmt)


async def create_user(user: BaseUser) -> bool:
    stmt = User.insert().values(username=user.username,
                                password=hash_password(user.password))
    return await execute_stmt_in_tran([stmt])


async def update_user(user: CompleteUser) -> bool:
    stmt = User.update().where(User.c.user_id == user.user_id).values(username=user.username,
                                                                      password=user.password)
    return await execute_stmt_in_tran([stmt])


async def delete_user(user_id: int) -> bool:
    stmt1 = SecurityTarget.delete().where(SecurityTarget.c.owner_id == user_id)
    stmt2 = User.delete().where(User.c.user_id == user_id)
    return await execute_stmt_in_tran([stmt1, stmt2])
