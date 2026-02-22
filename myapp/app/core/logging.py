import logging


_LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"



def configure_logging(level: str = "INFO") -> None:
    if logging.getLogger().handlers:
        return
    logging.basicConfig(level=level.upper(), format=_LOG_FORMAT)



def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
