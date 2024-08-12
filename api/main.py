from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db
import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manages the lifespan of the FastAPI application, including connecting and disconnecting from the database.

    This context manager handles the following tasks:
    - Connects to the database when the application starts.
    - Yields control to the application, allowing it to run.
    - Disconnects from the database when the application is shutting down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None
    """

    # Connect to database
    await db.connect()
    yield
    # Disconnect to database
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

# Include the routers
app.include_router(router.token)
app.include_router(router.user)
app.include_router(router.st)
app.include_router(router.evaluate)

# Add CORS middleware with specific settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)
