"""Utility functions for logging and debugging."""
import logging
from datetime import datetime
from pathlib import Path


def setup_logging():
    """Configure logging for tests."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


logger = setup_logging()


def log_test_info(message: str, level: str = "info"):
    """Log test information."""
    level_func = getattr(logger, level.lower(), logger.info)
    level_func(message)
