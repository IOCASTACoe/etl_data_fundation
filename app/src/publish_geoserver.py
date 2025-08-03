import json
import logging
import pathlib

import app.src.config as settings
from geo.Geoserver import Geoserver
from app.src.coverages import modify_layer
import xml.etree.ElementTree as ET


logger = logging.getLogger(__name__)


def publiblish_geoserver(file_path:str,
                         sld_file_full_path:pathlib.Path,
                         title:str,
                         theme:str,
                         abstract:str,
                         cat_acronym:str,
                         sta_date:str,
                         end_date:str,
                         id:str,
                         id_layer:str,
                         sufixo:str) -> None:

    geo = Geoserver(
        service_url=settings.GEOSERVER_URL,
        username=settings.GEOSERVER_USER,
        password=settings.GEOSERVER_PASSWORD,
    )    

    path = file_path

    keys = ["start_date","end_date","cat_acronym","id"]
    values = [sta_date,end_date,cat_acronym,id]
    dict_keywords = "|".join([f"{k}:{v}" for k,v in zip(keys, values)])

    


    attributes = {"abstract": abstract
                  ,"title": title
                 ,"keywords": dict_keywords
                 ,"theme": theme
                 ,"defaultStyle": {"name": "raster"}
                 ,"sld_name": sld_file_full_path.stem
                 }

    
    is_coverage = sufixo == ".tif"

    if is_coverage:
        geo.create_coveragestore(path=path,
                                workspace=settings.GEOSERVER_WORKSPACE,
                                layer_name=id_layer)
        
    else:
    
        geo.create_gpkg_datastore(path=path,                                  
                                 store_name=id_layer, 
                                 workspace=settings.GEOSERVER_WORKSPACE)
        
                                 
        geo.edit_featuretype(recalculate="nativebbox,latlonbbox", 
                        store_name=id_layer,
                        workspace=settings.GEOSERVER_WORKSPACE,  # type: ignore
                        pg_table= id_layer,  # type: ignore
                        name=id_layer,
                        title=title,                          
                        abstract=abstract)
        


    # TODO: Check if the SLD file for raster




    sld_name = sld_file_full_path.stem

    sld_xpath = "//StyledLayerDescriptor/@version"
    tree = ET.parse(file_path)
    root = tree.getroot()
    sld_version = root.find(sld_xpath)    


    geo.upload_style(path=sld_file_full_path.as_posix().__str__(),
                    name=sld_name, 
                    workspace=settings.GEOSERVER_WORKSPACE,
                    sld_version=sld_version)

    geo.publish_style(layer_name=id_layer, 
                    style_name=sld_name,
                    workspace=settings.GEOSERVER_WORKSPACE, 
                    sld_version=sld_version)

    


    modify_layer(layer=id_layer, attributes=attributes, is_coverage=is_coverage)


    


    
    """
    geo.edit_featuretype(recalculate="nativebbox,latlonbbox", 
                         store_name=id, # type: ignore'
                         workspace=settings.GEOSERVER_WORKSPACE,  # type: ignore
                         pg_table= name,  # type: ignore
                         name=name,
                         title=theme,                          
                         abstract=abstract,
                         keywords=dict_keywords) # type: ignore
    """

    
