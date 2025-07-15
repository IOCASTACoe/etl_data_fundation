
import logging

from osgeo import gdal
from osgeo import ogr

logger = logging.getLogger(__name__)

def get_gpkg_attributes(gpk_file_path: str) -> list[dict]:
    ds = ogr.Open(gpk_file_path, gdal.GA_Update)
    layer = ds.GetLayer(0)

    matrix: dict = dict()
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
            "type": fdefn.GetTypeName(),
        }
        schema.append(record)
    
    return schema