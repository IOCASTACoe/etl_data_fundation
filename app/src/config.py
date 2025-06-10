import os
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

ENV: str = "dev"

VALID_FILES: Tuple[str, ...] = (".gpkg", ".xml", ".xlsx")

##### GEOSERVER
GEOSERVER_URL:str = 'https://gis.iocasta.com.br/geoserver'
GEOSERVER_USER:str = 'admin'
GEOSERVER_PASSWORD:str = 'geoserver'
GEOSERVER_WORKSPACE:str = 'gold'

##### GEONETWORK
GEONETWORK_SERVER:str = 'https://catalog.iocasta.com.br'
GEONETWORK_USERNAME:str = 'admin'
GEONETWORK_PASSWORD:str = 'admin'
GEONETWORK_AUTH_URL = GEONETWORK_SERVER + "/srv/eng/info?type=me"

LOG_DIR:str = "logs/"
JINJA_SEARCH_PATH: str = "templates/"
TEMP_FILES:str = "temp_files/"

def init_dir():
  for dir_name in [LOG_DIR, TEMP_FILES]:
    if not os.path.isdir(dir_name):
        logging.info(f"Creating directory {dir_name}")
        os.mkdir(dir_name)


"""
/home/vscode/data/new/file/BIO/especies_ameacadas/20240101/00/md_bio_sp_end_20240101.xml
<gmd:dataQualityInfo>
    <gmd:DQ_DataQuality>
      <gmd:lineage>
        <gmd:LI_Lineage>
          <gmd:processStep>
            <gmd:LI_ProcessStep>
              <gmd:description>
.//gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gco:description

"""
