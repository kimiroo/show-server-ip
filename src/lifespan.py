from contextlib import asynccontextmanager
from fastapi import FastAPI
from util.deps import close_ip_querier

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await close_ip_querier()
