import requests
import xml.etree.ElementTree as ET

URL_GEOSERVER = "http://cobalto.iocasta.com.br:8080/geoserver/gold/"

url = f"{URL_GEOSERVER}ows"


xml_template = """<?xml version="1.0" encoding="UTF-8"?><wps:Execute version="1.0.0" service="WPS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.opengis.net/wps/1.0.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wcs="http://www.opengis.net/wcs/1.1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
  <ows:Identifier>gs:Bounds</ows:Identifier>
  <wps:DataInputs>
    <wps:Input>
      <ows:Identifier>features</ows:Identifier>
      <wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wfs" method="POST">
        <wps:Body>
          <wfs:GetFeature service="WFS" version="1.0.0" outputFormat="GML2" xmlns:gold="gold.iocasta.com.br">
            <wfs:Query typeName="{type_name_tag}"/>
          </wfs:GetFeature>
        </wps:Body>
      </wps:Reference>
    </wps:Input>
  </wps:DataInputs>
  <wps:ResponseForm>
    <wps:RawDataOutput>
      <ows:Identifier>bounds</ows:Identifier>
    </wps:RawDataOutput>
  </wps:ResponseForm>
</wps:Execute>
"""

xml_data = xml_template.replace("{type_name_tag}", "gold:pol_bio_imp_bio_20181218")

request_headers = {
    'Content-Type': 'application/xml',
    'Accept': 'application/xml'
}

response = requests.post(url, data=xml_data, headers=request_headers)

root = ET.fromstring(response.text)

namespaces = {'ows': 'http://www.opengis.net/ows/1.1'}
first = root.findall(".//ows:UpperCorner", namespaces)[0].text
second = root.findall(".//ows:LowerCorner", namespaces)[0].text

bound_box = f"{first} {second}".replace(" ", ",")

return bound_box