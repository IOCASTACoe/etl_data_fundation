

BASE_PATH:str = "/home/vscode/data/new/file"
# BASE_PATH:str = "/home/vscode/data/input"

VALID_FILES:tuple = [".gpkg",".xml",".xlsx"]
CONFIG_DIR = "./config"
LOG_DIR = "./logs"

JINJA_SEARCH_PATH: str = "./config/templates/"

TEMP_FILES:str = "./temp_files/"

GEOSERVER_URL:str = 'https://gis.iocasta.com.br/geoserver'
GEOSERVER_USER:str = 'admin'
GEOSERVER_PASSWORD:str = 'geoserver'
GEOSERVER_WORKSPACE:str = 'gold'

GEONETWORK_SERVER:str = 'https://catalog.iocasta.com.br'
GEONETWORK_USERNAME:str = 'admin'
GEONETWORK_PASSWORD:str = 'admin'
GEONETWORK_AUTH_URL = GEONETWORK_SERVER + "/srv/eng/info?type=me"


# TODO colocar pathlib

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
