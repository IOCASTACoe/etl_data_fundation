import os
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

ENV: str = "dev"

VALID_FILES: Tuple[str, ...] = (".gpkg", ".xml", ".xlsx")

if ENV == "dev":
    GEOSERVER_URL:str = 'https://gisdev.iocasta.com.br/geoserver'
    GEONETWORK_SERVER:str = 'https://catalogdev.iocasta.com.br'
    ETLAPI_URL:str = 'https://etlapidev.iocasta.com.br'
else:
    GEOSERVER_URL:str = 'https://gisqas.iocasta.com.br/geoserver'
    GEONETWORK_SERVER:str = 'https://catalogqas.iocasta.com.br'
    ETLAPI_URL:str = 'https://etlapiqas.iocasta.com.br'


GEOSERVER_USER:str = 'admin'
GEOSERVER_PASSWORD:str = 'geoserver'
GEOSERVER_WORKSPACE:str = 'gold'

GEONETWORK_USERNAME:str = 'admin'
GEONETWORK_PASSWORD:str = 'admin'
GEONETWORK_AUTH_URL = GEONETWORK_SERVER + "/srv/eng/info?type=me"

LOG_DIR:str = "logs/"
JINJA_SEARCH_PATH: str = "app/templates/"
TEMP_FILES:str = "temp_files/"

def init_dir():
  for dir_name in [LOG_DIR, TEMP_FILES]:
    if not os.path.isdir(dir_name):
        logging.info(f"Creating directory {dir_name}")
        os.mkdir(dir_name)
