from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import app.src.config as settings

import urllib.parse


def wms_format(layer_name: str, bbox: str) -> dict:

    return {
        "service": "WMS",
        "version": "1.1.0",
        "request": "GetMap",
        "layers": layer_name,
        "bbox": bbox,
        "width": "177",
        "height": "245",
        "srs": "EPSG:4326",
        "styles": "",
    }


def get_bounds(type_name: str) -> tuple[int, int, int, int]:

    url: str = settings.GEOSERVER_URL
    wms_service = WebMapService(url=f"{url}/wms", version="1.3.0")
    layer = wms_service.contents[type_name]
    return layer.boundingBox


def get_urls(url: str, layer_name: str) -> list[dict]:

    bounds = get_bounds(layer_name)
    str_bounds: str = ",".join(map(str, bounds[:-1]))

    wms_link = f"{url}wms?"
    wfs_link = f"{url}ows?"

    wfs_url = {
        "service": "WFS",
        "version": "1.0.0",
        "request": "GetFeature",
        "typeName": layer_name,
    }
    wms_url = wms_format(layer_name, str_bounds)

    result = []

    record_datadict = {
        "url": f"https://cobalto.iocasta.com.br:8080/geoserver/gold/datadict/{layer_name}",
        "protocol": "WWW:LINK-1.0-http--link",
        "label": "Link para dicionário de dados ou documentação complementar)",
    }
    result.append(record_datadict)

    url_openlayers = wms_url.copy()
    url_openlayers["width"] = "768"
    url_openlayers["height"] = "768"
    record_open_layers = {
        "url": f"{wms_link}{urllib.parse.urlencode(url_openlayers)}&format=application/openlayers",
        "protocol": "WWW:LINK-1.0-http--link",
        "label": "Link para visualização de camada geográfica (OpenLayers)",
    }
    result.append(record_open_layers)

    url_wms2 = wms_url.copy()
    record_wms2 = {
        "url": f"{wms_link}{urllib.parse.urlencode(url_wms2)}&format=image/png",
        "protocol": "OGC:WMS",
        "label": "Serviço OGC para visualização de camada geográfica (WMS)",
    }
    result.append(record_wms2)

    if layer_name.find(":rst") > -1:
        url_shape = wfs_url.copy()
        record_shape = {
            "url": f"{wfs_link}{urllib.parse.urlencode(url_shape)}&format=Shapefile",
            "protocol": "WWW:DOWNLOAD-1.0-http--download",
            "label": "Download de arquivo vetorial Shape File",
        }
        result.append(record_shape)
    else:
        url_geotiff = wms_url.copy()
        record_geotiff = {
        "url": f"{wms_link}{urllib.parse.urlencode(url_geotiff)}&format=image/geotiff",
        "protocol": "WWW:DOWNLOAD-1.0-http--download",
        "label": "Download de arquivo Geotif",
        }
        result.append(record_geotiff)

    return result


if __name__ == "__main__":

    from handle_xml import HandleXML

    # Example usage
    url: str = "http://cobalto.iocasta.com.br:8080/geoserver/gold/"
    # layer_name: str = "gold:pl_iwt_rvr_20121217"
    layer_name = "gold:pl_iwt_rvr_20121217"

    urls = get_urls(url, layer_name)

    file = "/home/wilson/workspace/etl_data_fundation/docs/teste.xml"

    teste = HandleXML(file)
    saida = teste.complete_links(file, urls)
    print(saida)

"""
from owslib.wps import WebProcessingService
from owslib.wps import printInputOutput
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService

url = "http://cobalto.iocasta.com.br:8080/geoserver/gold"


def get_layer_image(url:str)
wms = WebMapService('http://cobalto.iocasta.com.br:8080/geoserver/gold/wms', version='1.3.0')
img = wms.getmap(   layers=['pol_bio_imp_bio_20181218'],
                    styles=[],
                    srs='EPSG:4326',
                    bbox=z,
                    size=(765, 768),
                    format='image/jpeg',
                    transparent=True
                    )
out = open('jpl_mosaic_visb.jpg', 'wb')
out.write(img.read())
out.close()
"""
