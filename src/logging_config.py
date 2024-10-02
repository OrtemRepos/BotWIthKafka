import sys
import structlog

try:
    from rich.traceback import install

    install()
except ImportError:
    ...

shared_processors = (
    structlog.processors.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.dev.set_exc_info,
    structlog.processors.TimeStamper(fmt="iso"),
)

if sys.stderr.isatty():
    processors = [
        *shared_processors,
        structlog.dev.ConsoleRenderer(),
    ]
else:
    processors = [
        *shared_processors,
        structlog.processors.dict_tracebacks,
        structlog.processors.JSONRenderer(),
    ]

structlog.configure(
    processors=processors,  # type: ignore
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)


logger = structlog.get_logger()
