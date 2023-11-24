import time
from typing import Callable

import uvicorn
from fastapi import APIRouter, FastAPI, Request

from src.app.internal.core.auth.transport.handlers import auth_router
from src.app.internal.users.transport.handlers import users_router
from src.config.settings import get_settings

settings = get_settings()

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(auth_router)
api_router.include_router(users_router)

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)

app.include_router(api_router)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
