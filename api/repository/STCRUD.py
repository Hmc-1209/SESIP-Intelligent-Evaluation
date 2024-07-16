from models import SecurityTarget
from database import db, execute_stmt_in_tran
from schemas import BaseST, DetailST, UpdateST


async def get_st_by_id(st_id: int) -> BaseST:
    stmt = SecurityTarget.select().where(SecurityTarget.c.st_id == st_id)
    return await db.fetch_one(stmt)


async def get_st_by_name(st_name: str) -> BaseST:
    stmt = SecurityTarget.select().where(SecurityTarget.c.st_name == st_name)
    return await db.fetch_one(stmt)


async def get_st_by_user_id(user_id: int) -> list[DetailST]:
    stmt = SecurityTarget.select().where(SecurityTarget.c.owner_id == user_id)
    return await db.fetch_all(stmt)


async def update_st_by_id(st_id: int, new_st: UpdateST) -> bool:
    stmt = SecurityTarget.update().where(SecurityTarget.c.st_id == st_id).values(st_name=new_st.st_name,
                                                                                 owner_id=new_st.owner_id)
    return await execute_stmt_in_tran([stmt])
