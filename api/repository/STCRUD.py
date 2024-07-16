from models import SecurityTarget
from database import db, execute_stmt_in_tran
from schemas import DetailST


async def get_st_by_user_id(user_id: int) -> list[DetailST]:
    stmt = SecurityTarget.select().where(SecurityTarget.c.owner_id == user_id)
    return await db.fetch_all(stmt)
