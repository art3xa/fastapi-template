import uvicorn
from fastapi import FastAPI

from src.config.settings import get_settings

settings = get_settings()

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)


@app.get("/")
def root():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
