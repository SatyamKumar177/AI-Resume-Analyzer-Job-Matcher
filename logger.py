import logging
import structlog
from backend.utils.config import settings


def configure_logging() -> None:
    """Configure structured logging with structlog."""
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.ENVIRONMENT == "development":
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        shared_processors.append(structlog.processors.JSONRenderer(indent=None))

    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Set logging level
    logging.getLogger().setLevel(getattr(logging, settings.LOG_LEVEL.upper()))


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Get a structured logger instance."""
    return structlog.get_logger(name)
