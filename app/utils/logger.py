# app/utils/logger.py

import logging
import sys

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger instance.

    Args:
        name (str): Name for the logger, usually __name__.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid duplicate logs in environments like notebooks or tests
    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] - %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
