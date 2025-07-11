import os
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

ENV: str = "dev"

VALID_FILES: Tuple[str, ...] = (".gpkg", ".xml", ".xlsx")

##### GEOSERVER
#GEOSERVER_URL:str = 'https://gisdev.iocasta.com.br'
GEOSERVER_URL:str = 'http://gisdev.iocasta.com.br'

GEOSERVER_USER:str = 'admin'
GEOSERVER_PASSWORD:str = 'geoserver'
GEOSERVER_WORKSPACE:str = 'gold'

##### GEONETWORK
#GEONETWORK_SERVER:str = 'https://catalogdev.iocasta.com.br'
GEONETWORK_SERVER:str = 'http://catalogdev.iocasta.com.br'
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

