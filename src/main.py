import uvicorn
from fastapi import APIRouter, FastAPI

from src.app.internal.core.auth.transport.handlers import auth_router
from src.app.internal.users.transport.handlers import users_router
from src.settings import get_settings

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


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
