import logging
from src.lib.loggin import setup_logging
import config.config as settings

import pandas as pd
from pandas import read_excel

logger = logging.getLogger(__name__)

def read_excel_file(file_path: str) -> list[dict]:
    lst = [dict]
    excel_lst = read_excel(file_path)
    for item in excel_lst.to_dict(orient="records"):
        if item.keys() != {"Name", "Description"}:
            logging.error(f"Invalid keys found in the Excel file: {file_path}")
            raise ValueError(f"Invalid keys in the Excel file: {file_path}")
        record: dict = {"desc": item["Description"], "name": item["Name"]}
        lst.append(record)


import glob
import pathlib
import os

def get_geopackage(dir_path:str) -> str:
    pass

def get_path(midle_path:str) -> str:
    return pathlib.Path(settings.BASE_PATH, midle_path).__str__()

def find_files_with_extension_glob(directory, extension):
    pattern = os.path.join(directory, f"*{extension}")
    return glob.glob(pattern)


def valid_files(dir_path:str, extension:str) -> pathlib:
    for ext in settings.VALID_FILES:
        result = find_files_with_extension_glob(directory=dir_path, extension=extension)
        if len(result) > 1:
            raise Exception(f"Existem {len(result)} arquivos no diretório {dir_path} com a extensão {extension}.")
        elif len(result) == 0:
            raise Exception(f"Não existe arquivos no diretório {dir_path} com a extensão {extension}.")
        file_path: pathlib = pathlib.Path(result[0])
        
    return file_path





if __name__ == "__main__":
    setup_logging()

    dir_path: str = get_path("BIO/especies_ameacadas/20240101/00/") 
    get_file_name = find_files_with_extension_glob(directory=dir_path, extension=".shp")
    arquivo:pathlib = valid_files(dir_path=dir_path, extension=".shp")
    file_name:str = arquivo.name.replace(".shp", "")
    print()


    paths: list[str] = [
        "CMA/frequencia_queimadas/MapBiomas/20240618/",
        "BIO/especies_ameacadas/20240101/00/",
        "BIO/zona_costeira/IBGE/20240730/00/",
        "BIO/importancia_biologica/MMA/20181218/00/",
        "BIO/biomas/IBGE/2004010100/00/",
    ]
