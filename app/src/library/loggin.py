import logging
import logging.config
import os
from datetime import datetime

from dotenv import dotenv_values, load_dotenv
import app.src.config as settings
def setup_logging():

    load_dotenv()
    """Load logging configuration"""
    log_configs = {"dev": "logging.dev.ini", "prod": "logging.prod.ini"}
    config = log_configs.get(os.environ["ENV"], "logging.dev.ini")
    config_path = "/".join([settings.CONFIG_DIR, config])

    timestamp = datetime.now().strftime("%Y%m%d-%H:%M:%S")

    logging.config.fileConfig(
        config_path,
        disable_existing_loggers=False,
        defaults={"logfilename": f"{settings.LOG_DIR}/{timestamp}.log"},
    )
