from owslib.wfs import WebFeatureService

from urllib.parse import quote


def format_url(data: str):
    data = data.replace("\n", "")
    data = quote(data, safe=":/?&=,")
    return data


def url_wms(url: str, layer_name: str, bbox: str) -> str:

    return f"""{url}wms
?service=WMS
&version=1.1.0
&request=GetMap
&layers={layer_name}
&styles=
&bbox={bbox}
&width=177
&height=245
&tiled=true
&srs=EPSG:4326
&format=image/png
&transparent=true"""


### GeoJson


def url_geo_json(url: str, layer_name: str) -> str:

    return f"""{url}ows
?service=WFS
&version=1.0.0
&request=GetFeature
&typeName={layer_name}
&outputFormat=application/json"""


##### KMZ


def url_kms(url: str, layer_name: str, bbox: str) -> str:

    return f"""{url}ows
?service=WMS
&version=1.1.0
&request=GetMap
&layers={layer_name}
&width=1024
&height=768
&bbox={bbox}
&format=application/vnd.google-earth.kmz+xml"""


#### Shapefile


def url_shape(url: str, layer_name: str) -> str:

    return f"""{url}ows
?service=WFS
&version=1.0.0
&request=GetFeature
&typeName={layer_name}
&outputFormat=SHAPE-ZIP"""


def url_thumbnail(url: str, layer_name: str, bbox: str) -> str:
    return f"""{url}wms
?service=WMS
&version=1.1.0
&request=GetMap
&layers={layer_name}
&bbox={bbox}
&width=100
&height=100
&srs=EPSG-4326
&styles=
&format=image/png"""


def get_bounds(url: str, type_name: str) -> tuple[int, int, int, int]:

    wfs20 = WebFeatureService(url=f"{url}/wfs", version="2.0.0")
    layer = wfs20.contents[type_name]
    return layer.boundingBox


def get_urls(url: str, layer_name: str) -> list[dict]:

    bounds = get_bounds(url, layer_name)
    str_bounds: str = ",".join(map(str, bounds))

    wms_url = url_wms(url, layer_name, str_bounds)
    geo_json_url = url_geo_json(url, layer_name)
    kmz_url = url_kms(url, layer_name, str_bounds)
    shape_url = url_shape(url, layer_name)
    thumbnail_url = url_thumbnail(url, layer_name, str_bounds)

    result = []
    result.append({"wms_url": format_url(wms_url)})
    result.append({"geo_json_url": format_url(geo_json_url)})
    result.append({"kmz_url": format_url(kmz_url)})
    result.append({"shape_url": format_url(shape_url)})
    result.append({"thumbnail_url": format_url(thumbnail_url)})

    return result


if __name__ == "__main__":

    from handle_xml import HandleXML

    # Example usage
    url: str = "http://cobalto.iocasta.com.br:8080/geoserver/gold/"
    layer_name: str = "gold:pol_soc _ils_20240410"

    urls = get_urls(url, layer_name)

    file = "/home/wilson/workspace/etl_data_fundation/temp_files/79c1f828-7c2b-40c6-a450-f2d67e2d096b/md_soc_com_qlb_20250605.xml"
            
    teste = HandleXML(file)
    saida = teste.complete_links(file, urls)


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
