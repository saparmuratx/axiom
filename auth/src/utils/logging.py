import os
from logging.config import dictConfig

from datetime import datetime

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
            "format": "%(asctime)s %(levelprefix)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S %z",
            "use_colors": True,
        },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,  # Keep logs for 30 days
            "filename": f"logs/log_{datetime.now().strftime('%d_%m_%Y')}.log",
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
            "propagate": True,
        },
    },
}


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    dictConfig(LOGGING_CONFIG)
