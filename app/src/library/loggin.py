import logging
import logging.config
import os
from datetime import datetime
import app.src.config as settings

from dotenv import dotenv_values, load_dotenv
import app.src.config as settings
def setup_logging():

    load_dotenv()
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(settings.ENV, "logging.dev.ini")
    config_path = f"app/config/{config}"

    timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{settings.LOG_DIR}/{timestamp}.log"},
    )