import logging

import app.src.config as settings
from geo.Geoserver import Geoserver

logger = logging.getLogger(__name__)

def publiblish_geoserver(file_path:str,
                         title:str,
                         theme:str,
                         abstract:str,
                         cat_acronym:str,
                         sta_date:str,
                         end_date:str,
                         id:str) -> None:

    geo = Geoserver(
        service_url=settings.GEOSERVER_URL,
        username=settings.GEOSERVER_USER,
        password=settings.GEOSERVER_PASSWORD
    )

    geo.create_gpkg_datastore(path=file_path,
                                store_name=title, 
                                workspace=settings.GEOSERVER_WORKSPACE)
    
    col = geo.get_featuretypes(workspace=settings.GEOSERVER_WORKSPACE,
                         store_name=title
                         )
    name = col[0]

    dict_keywords = [{"start_date":sta_date}, 
                    {"end_date":end_date},
                    {"cat_acronym":cat_acronym},
                    {'id':id}]

    geo.edit_featuretype(recalculate="nativebbox,latlonbbox", 
                         store_name=title, # type: ignore
                         workspace=settings.GEOSERVER_WORKSPACE,  # type: ignore
                         pg_table= name,  # type: ignore
                         name=name,
                         title=theme, 
                         abstract=abstract,
                         keywords=dict_keywords) # type: ignore