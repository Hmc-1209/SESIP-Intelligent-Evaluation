from database import db, execute_stmt_in_tran, create_with_result
from models import SecurityTarget
from schemas import BaseST, DetailST, UpdateST, EvaluateST


async def get_st_by_id(st_id: int) -> DetailST:
    """
    Retrieve a security target by its ID.

    Args:
        st_id (int): The ID of the security target to retrieve.

    Returns:
        DetailST: The detailed information of the security target with the specified ID.
    """

    stmt = SecurityTarget.select().where(SecurityTarget.c.st_id == st_id)
    return await db.fetch_one(stmt)


async def get_st_by_name(st_name: str) -> BaseST:
    """
    Retrieve a security target by its name.

    Args:
        st_name (str): The name of the security target to retrieve.

    Returns:
        BaseST: The basic information of the security target with the specified name.
    """

    stmt = SecurityTarget.select().where(SecurityTarget.c.st_name == st_name)
    return await db.fetch_one(stmt)


async def get_st_by_user_id(user_id: int) -> list[DetailST]:
    """
    Retrieve all security targets associated with a specific user.

    Args:
        user_id (int): The ID of the user whose security targets are to be retrieved.

    Returns:
        list[DetailST]: A list of detailed information for all security targets owned by the specified user.
    """

    stmt = SecurityTarget.select().where(SecurityTarget.c.owner_id == user_id)
    return await db.fetch_all(stmt)


async def create_st(st_name: str, owner_id: int) -> int:
    """
    Create a new security target.

    Args:
        st_name (str): The name of the new security target.
        owner_id (int): The ID of the user who owns the security target.

    Returns:
        int: The ID of the newly created security target.
    """

    stmt = SecurityTarget.insert().values(st_name=st_name,
                                          is_evaluated=False,
                                          owner_id=owner_id)
    return await create_with_result(stmt)


async def update_st_by_id(st_id: int, owner_id: int) -> bool:
    """
    Update the owner of a security target.

    Args:
        st_id (int): The ID of the security target to update.
        owner_id (int): The new owner ID to set for the security target.

    Returns:
        bool: True if the update was successful; otherwise, False.
    """

    stmt = SecurityTarget.update().where(SecurityTarget.c.st_id == st_id).values(owner_id=owner_id)
    return await execute_stmt_in_tran([stmt])


async def update_st_after_eval(st_id: int, update_st: EvaluateST) -> bool:
    """
    Update a security target with evaluation results.

    Args:
        st_id (int): The ID of the security target to update.
        update_st (EvaluateST): An instance of `EvaluateST` containing the evaluation results.

    Returns:
        bool: True if the update was successful; otherwise, False.
    """

    stmt = SecurityTarget.update().where(SecurityTarget.c.st_id == st_id).values(st_details=update_st.st_details,
                                                                                 is_evaluated=True,
                                                                                 eval_passed=update_st.eval_passed,
                                                                                 eval_model=update_st.eval_model)
    return await execute_stmt_in_tran([stmt])


async def delete_st_by_id(st_id: int) -> bool:
    """
    Delete a security target by its ID.

    Args:
        st_id (int): The ID of the security target to delete.

    Returns:
        bool: True if the deletion was successful; otherwise, False.
    """

    stmt = SecurityTarget.delete().where(SecurityTarget.c.st_id == st_id)
    return await execute_stmt_in_tran([stmt])
