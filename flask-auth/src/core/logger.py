from core.config import settings


def get_logging_config_dict(log_level):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": settings.log_format},
        },
        "handlers": {
            "console": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "standard",
            },
        },
        "loggers": {
            "": {
                "handlers": settings.log_default_handlers,
                "level": log_level,
                "propagate": True,
            },
        },
    }
