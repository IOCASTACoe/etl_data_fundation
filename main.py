import logging
from src.lib.loggin import setup_logging
import config.config as settings
import jinja2
import pandas as pd
from pandas import read_excel
import pdfkit

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


def get_geopackage(dir_path: str) -> str:
    pass


def get_path(midle_path: str) -> str:
    return pathlib.Path(settings.BASE_PATH, midle_path).__str__()


def find_files_with_extension_glob(directory, extension):
    pattern = os.path.join(directory, f"*{extension}")
    return glob.glob(pattern)


def valid_files(dir_path: str, extension: str) -> pathlib:
    for ext in settings.VALID_FILES:
        result = find_files_with_extension_glob(directory=dir_path, extension=extension)
        if len(result) > 1:
            raise Exception(
                f"Existem {len(result)} arquivos no diretório {dir_path} com a extensão {extension}."
            )
        elif len(result) == 0:
            raise Exception(
                f"Não existe arquivos no diretório {dir_path} com a extensão {extension}."
            )
        file_path: pathlib = pathlib.Path(result[0])

    return file_path


from osgeo import ogr
from osgeo import gdal


def build_final_attributes(file_path: str, comments: dict) -> list[dict]:
    ds = ogr.Open(file_path, gdal.GA_Update)
    layer = ds.GetLayer(0)

    matrix: dict[str] = dict(str())
    matrix[ogr.OFTBinary] = "Binary"
    matrix[ogr.OFTDate] = "Date"
    matrix[ogr.OFTDateTime] = "DateTime"
    matrix[ogr.OFTInteger] = "Integer"
    matrix[ogr.OFTInteger64] = "Integer 64"
    matrix[ogr.OFTReal] = "Real"
    matrix[ogr.OFTString] = "String"
    matrix[ogr.OFTTime] = "Time"

    schema = []
    ldefn = layer.GetLayerDefn()
    for n in range(ldefn.GetFieldCount()):
        fdefn = ldefn.GetFieldDefn(n)
        record = {
            "name": fdefn.name,
            "type": matrix[fdefn.type],
             # "width": fdefn.width,
            "comment": data_dict[fdefn.name],
        }
        schema.append(record)
    
    record = {"name": layer.GetGeometryColumn(), "type":ogr.GeometryTypeToName(layer.GetGeomType()), "comment": str(layer.GetSpatialRef())}
    schema.append(record)
    return schema


def get_xlsx_rows(file_path: str) -> dict:
    logger.info(f"Processing Excel file: {file_path}")

    lst: dict = {}
    excel_lst = read_excel(file_path)
    for item in excel_lst.to_dict(orient="records"):
        if item.keys() != {"Name", "Description"}:
            logging.info(f"Invalid keys found in the Excel file: {file_path}")
            raise ValueError(f"Invalid keys in the Excel file: {file_path}")
        lst[item["Name"]] = item["Description"]
    return lst


def render_html(values:list[dict], name:str, abstract:str) -> str: 

    template_loader = jinja2.FileSystemLoader(searchpath=settings.JINJA_SEARCH_PATH)
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "dictionary.html"
    template = template_env.get_template(template_file)

    context:dict = {
                        "headers": values[0].keys(),
                        "records": values,
                        "tittle": name,
                        "caption": abstract
                    }
                  


    output_text = template.render(context=context)

    html_path = pathlib.Path(settings.TEMP_FILES, f'{name}.html')
    html_file = open(html_path, 'w')
    html_file.write(output_text)
    html_file.close()

    return html_path


def html2pdf(html_path:str):
    options = {
        'page-size': 'Letter',
        'margin-top': '0.35in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }

    pdf_path:str = f"{html_path}.pdf"
    html_path:str = f"{html_path}.html"
    with open(html_path) as f:
        pdfkit.from_file(f, pdf_path, options=options)


if __name__ == "__main__":
    setup_logging()
    dir_path: str = get_path("BIO/especies_ameacadas/20240101/00/")
    get_file_name = find_files_with_extension_glob(directory=dir_path, extension=".shp")
    arquivo: pathlib = valid_files(dir_path=dir_path, extension=".shp")
    file_name: str = arquivo.name.replace(".shp", "")

    """ Excel data dictctonary """
    excel_file_full_path: pathlib = valid_files(dir_path=dir_path, extension=".xlsx")
    data_dict: dict = get_xlsx_rows(excel_file_full_path.__str__())

    """ Geopackage Attributes"""
    excel_file_full_path: pathlib = valid_files(dir_path=dir_path, extension=".gpkg")
    attibutes:list[dict] = build_final_attributes(excel_file_full_path.__str__(), 
                                       data_dict)

    html_path:str = render_html(values=attibutes, name=file_name, abstract="fdslsdfsdçfdsfsd")
    
    html_path: str = f"{settings.TEMP_FILES}{file_name}"
    html2pdf(html_path)







    paths: list[str] = [
        "CMA/frequencia_queimadas/MapBiomas/20240618/",
        "BIO/especies_ameacadas/20240101/00/",
        "BIO/zona_costeira/IBGE/20240730/00/",
        "BIO/importancia_biologica/MMA/20181218/00/",
        "BIO/biomas/IBGE/2004010100/00/",
    ]
