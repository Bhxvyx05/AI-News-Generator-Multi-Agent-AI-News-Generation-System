import logging
import sys

# Configure root logger
logger = logging.getLogger("AI-News-Generator")
logger.setLevel(logging.DEBUG)  # capture all levels

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # default console level

# File handler (optional: logs saved to file)
file_handler = logging.FileHandler("logs/search_agent.log", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Log format
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Attach handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Convenience functions
def info(msg): logger.info(msg)
def debug(msg): logger.debug(msg)
def warning(msg): logger.warning(msg)
def error(msg): logger.error(msg)
def critical(msg): logger.critical(msg)
