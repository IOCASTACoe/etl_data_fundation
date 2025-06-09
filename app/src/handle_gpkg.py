
import logging

from osgeo import gdal
from osgeo import ogr

logger = logging.getLogger(__name__)

def build_final_attributes(file_path: str, comments: dict) -> list[dict]:
    ds = ogr.Open(file_path, gdal.GA_Update)
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
            "type": matrix[fdefn.type],
             # "width": fdefn.width,
            "comment": comments[fdefn.name],
        }
        schema.append(record)
    
    record = {"name": layer.GetGeometryColumn(), "type":ogr.GeometryTypeToName(layer.GetGeomType()), "comment": str(layer.GetSpatialRef())}
    schema.append(record)
    return schema