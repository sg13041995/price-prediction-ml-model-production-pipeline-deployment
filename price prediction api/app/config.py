import logging
import sys
from types import FrameType
from typing import List, cast

from loguru import logger

# To create our config class
from pydantic import AnyHttpUrl, BaseSettings

# Any log at info level or above will be captured
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # logging levels are type int


# Settings class to specify things like project name etc.
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"

    # Meta
    logging: LoggingSettings = LoggingSettings()

    # BACKEND_CORS_ORIGINS is a comma-separated list of origins
    # e.g: http://localhost,http://localhost:4200,http://localhost:3000
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # type: ignore
        "http://localhost:8000",  # type: ignore
        "https://localhost:3000",  # type: ignore
        "https://localhost:8000",  # type: ignore
    ]

    PROJECT_NAME: str = "House Price Prediction API"

    # This is specific to pydantic
    # We can specify some options for pydantic classes
    class Config:
        case_sensitive = True


# See: https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging  # noqa
# Recommended by loguru
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def setup_app_logging(config: Settings) -> None:
    """Prepare custom logging for our application."""
    # Intercepting the default log messages from uvicorn logger to loguru
    LOGGERS = ("uvicorn.asgi", "uvicorn.access")
    logging.getLogger().handlers = [InterceptHandler()]
    for logger_name in LOGGERS:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = [InterceptHandler(level=config.logging.LOGGING_LEVEL)]

    # Simplified handler
    logger.configure(
        handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}]
    )

# This settings object is exported
settings = Settings()
