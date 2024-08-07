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

DATABASE_URL = f"mysql+asyncmy://{config.db_user}:{config.db_pass}@{config.db_host}:{config.db_port}/{config.db_name}"

db = databases.Database(DATABASE_URL)

metadata = MetaData()


async def execute_stmt_in_tran(stmt_list: list[ClauseElement]) -> bool:
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
    tran = db.transaction()

    try:
        await tran.start()
        result = await db.execute(stmt)
        await tran.commit()
        return result

    except:
        await tran.rollback()
        return 0
