import logging
import os
import pathlib
import shutil

import app.src.config as settings
from app.src.library.loggin import setup_logging
from app.src.handle_gpkg import get_gpkg_attributes
from app.src.handle_xml import HandleXML
from app.src.publish_geoserver import publiblish_geoserver
from app.src.publis_catalog import upload_xml_geonetwork
from app.src.handle_files import get_path, valid_files

logger = logging.getLogger(__name__)

def main(path:str):

    setup_logging()

    logger.info(f"Starting ETL process for path: {path}")
    dir_path: str = get_path(path)
    arquivo: pathlib.Path = valid_files(dir_path=dir_path, extension=".gpkg")
    file_name: str = arquivo.name.replace(".gpkg", "")
    logger.info(f"Filename to be processed [{file_name}]")


    logger.info("Geopackage Attributes")
    excel_file_full_path: pathlib.Path = valid_files(dir_path=dir_path, extension=".gpkg")
    attibutes:list[dict] = get_gpkg_attributes(excel_file_full_path.__str__())

        
    logger.info("Get XML data")
    xml_file_full_path: pathlib.Path = valid_files(dir_path=dir_path, extension=".xml")
    obj_xml = HandleXML(xml_file_full_path.__str__())
    obj_xml.complete_dictionary(xml_file_full_path.__str__(), attibutes)
    if len(obj_xml.erros) >0:
        logger.error(f"Errors found in XML: {obj_xml.get_erros()}")
        raise Exception(f"Errors found in XML: {obj_xml.get_erros()}")  
    record:dict = obj_xml.record
    logger.info("Get XML passed.")

    logger.info("Publish Geonetwork")
    uuid:str = upload_xml_geonetwork(xml_file_full_path.__str__())

    logger.info("Get sld data")
    sld_path:pathlib.Path = valid_files(dir_path=dir_path, extension=".sld")

    logger.info("Publish Geoserver")
    geo_package_file_full_path: pathlib.Path = valid_files(dir_path=dir_path, extension=".gpkg")
    publiblish_geoserver(file_path=geo_package_file_full_path.__str__(),
                         sld_file_full_path=sld_path,
                         title=record["title"],
                         theme=record["theme"],
                         abstract=record["abstract"],
                         cat_acronym=record["category_acronym"],
                         sta_date=record["sta_date"],
                         end_date=record["end_date"],
                         id=uuid)
    

    logger.info(f"Remove dir: {dir_path}.")
    shutil.rmtree(dir_path)    

    logger.info(f"Finish: {file_name}.")

