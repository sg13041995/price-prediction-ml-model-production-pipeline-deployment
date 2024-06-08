from typing import Any

from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger

# This is another router from api module
# This is for more complex APIs
from app.api import api_router

# Our config
from app.config import settings, setup_app_logging

# setup logging as early as possible
setup_app_logging(config=settings)

# Our main Fast API app
# FAST API makes use of OpenAPI standard and we get out of the box documentation when specifying openapi_url, some response schemas and configs  
app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# We have a couple of routers

# This is a router
root_router = APIRouter()

# Home endpoint
@root_router.get("/")
def index(request: Request) -> Any:
    """Basic HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)

# We are including the routers in our app
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")
    
    # We are importing the uvicorn here only in the case of developemnt while involking the file directly   
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
