import logging

from venv import logger
import requests
import xml.etree.ElementTree as ET
from app.src import config as settings
import jinja2
import app.src.config as settings

logger = logging.getLogger(__name__)

# Define GEONETWORK_NAMESPACES if not present in settings
GEONETWORK_NAMESPACES = {
    "gmd": "http://www.isotc211.org/2005/gmd",
    "gco": "http://www.isotc211.org/2005/gco",
}


def render_html(values: list[dict], name: str, abstract: str) -> str:

    template_loader = jinja2.FileSystemLoader(searchpath=settings.JINJA_SEARCH_PATH)
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "dictionary.html"
    template = template_env.get_template(template_file)

    context: dict = {
        "titulo": name,
        "headers": values[0].keys(),
        "records": values,
        "caption": abstract,
    }

    output_text = template.render(context=context).replace(r"\n", "")

    return output_text


def proc_key(key: str) -> str:

    response = requests.get(
        f"{settings.GEONETWORK_SERVER}/srv/api/records/{key}/formatters/xml"
    )
    root = ET.fromstring(response.content)

    titulo_path = ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"
    titulo_element = root.find(titulo_path, namespaces=GEONETWORK_NAMESPACES)
    title_str = ""
    if titulo_element is not None:
        title_str = titulo_element.text
    else:
        title_str = "No title found"

    campos = root.findall(".//data_dictionary/field")

    collection = []
    for item in range(0, len(campos)):

        try:
            tipo = campos[item][2].text
        except IndexError:
            tipo = "Falta"

        collection.append(
            {"name": campos[item][0].text, "desc": campos[item][1].text, "type": tipo}
        )
    output_text = render_html(
        values=collection, name=title_str.__str__(), abstract=f"[{key}] {title_str}"
    )

    return output_text
