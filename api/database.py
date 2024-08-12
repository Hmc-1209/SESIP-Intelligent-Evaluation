from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import MetaData
from sqlalchemy.sql.elements import ClauseElement
import databases
import config

# from sshtunnel import SSHTunnelForwarder

# In case someday the API and the database are in different server
# for ssh usage
# server = SSHTunnelForwarder(
#     ('YOUR_SERVER_IP_HERE', 22),
#     ssh_username=config.ssh_username,
#     ssh_password=config.ssh_password,
#     remote_bind_address=('localhost', 3306)
# )

# server.start()

# Database settings
DATABASE_URL = f"mysql+asyncmy://{config.db_user}:{config.db_pass}@{config.db_host}:{config.db_port}/{config.db_name}"
db = databases.Database(DATABASE_URL)

metadata = MetaData()


async def execute_stmt_in_tran(stmt_list: list[ClauseElement]) -> bool:
    """
    Execute a list of SQL statements within a database transaction.

    This asynchronous function performs the following steps:
    - Starts a new database transaction.
    - Executes each SQL statement in the provided `stmt_list` within the transaction.
    - Commits the transaction if all statements are executed successfully.
    - Rolls back the transaction and returns `False` if any statement fails.

    Args:
        stmt_list (list[ClauseElement]): A list of SQL statements to be executed.

    Returns:
        bool: `True` if all statements were executed and committed successfully, `False` otherwise.
    """

    tran = db.transaction()

    try:
        await tran.start()
        for stmt in stmt_list:
            await db.execute(stmt)
        await tran.commit()
        return True

    except:
        await tran.rollback()
        return False


async def create_with_result(stmt: ClauseElement) -> int:
    """
    Execute a single SQL Create statement within a database transaction and return the ID of the created item.

    This asynchronous function performs the following steps:
    - Starts a new database transaction.
    - Executes the provided SQL statement (`stmt`) within the transaction.
    - Commits the transaction if the statement is executed successfully.
    - Rolls back the transaction and returns `0` if an error occurs.

    Args:
        stmt (ClauseElement): The SQL Create statement to be executed.

    Returns:
        int: The ID of the created item if successful; `0` if an error occurs.
    """

    tran = db.transaction()

    try:
        await tran.start()
        result = await db.execute(stmt)
        await tran.commit()
        return result

    except:
        await tran.rollback()
        return 0
