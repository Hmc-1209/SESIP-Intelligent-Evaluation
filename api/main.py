from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import db
import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to database
    await db.connect()
    yield
    # Disconnect to database
    await db.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(router.token)
app.include_router(router.user)
app.include_router(router.st)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
