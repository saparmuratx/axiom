import os
from logging.config import dictConfig
from fastapi_cli.utils.cli import get_uvicorn_log_config


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
        },
        "rich": {
            "()": "uvicorn.logging.DefaultFormatter",
            "format": "%(levelprefix)s %(message)s",
            "use_colors": True,
        },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,  # Keep logs for 30 days
            "filename": "logs/app.log",
            "formatter": "standard",
            "level": "DEBUG",
            "encoding": "utf-8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
            "formatter": "rich",
            "level": "DEBUG",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
        "uvicorn": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "fastapi_cli": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}


FASTAPI_ROOT_LOGGER = {"handlers": ["default", "file"], "level": "INFO"}

FASTAPI_STANDARD_FORMATTER = {
    "format": "%(asctime)s %(levelname)s %(name)s: %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S %z",
}


FASTAPI_FILE_HANDLER = {
    "class": "logging.handlers.TimedRotatingFileHandler",
    "when": "midnight",
    "interval": 1,
    "backupCount": 30,
    "filename": "logs/app.log",
    "formatter": "standard",
    "level": "DEBUG",
    "encoding": "utf-8",
}


def setup_logging(config_type: str = "uvicorn"):
    os.makedirs("logs", exist_ok=True)
    if config_type == "fastapi":
        config = get_uvicorn_log_config()

        config["loggers"][""] = FASTAPI_ROOT_LOGGER
        config["formatters"]["standard"] = FASTAPI_STANDARD_FORMATTER
        config["handlers"]["file"] = FASTAPI_FILE_HANDLER

        config["loggers"]["uvicorn"]["handlers"].append("file")
        config["loggers"]["uvicorn.access"]["handlers"].append("file")

        dictConfig(config)
    else:
        dictConfig(LOGGING_CONFIG)
