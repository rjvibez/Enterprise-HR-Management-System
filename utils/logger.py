import os
import logging

# Ensure logs directory exists before configuring log file
os.makedirs("logs", exist_ok=True)
log_filepath = os.path.join("logs", "app.log")

try:
    logging.basicConfig(
        filename=log_filepath,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
except Exception:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

logger = logging.getLogger("HRSystem")