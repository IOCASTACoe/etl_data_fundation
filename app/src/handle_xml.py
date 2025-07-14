import logging
import xml.etree.ElementTree as ET 

logger = logging.getLogger(__name__)

class HandleXML:

    record: dict = dict()

    _namespaces: dict = {
        "gmd": "http://www.isotc211.org/2005/gmd",
        "gco": "http://www.isotc211.org/2005/gco",
        # Add other namespaces as needed
    }

    def __init__(self, file_path: str):


        logger.info(f"Processing XML file: {file_path}")

        root = self._read_gmd_xml(file_path)

        if root is not None:
            # Define namespaces (if present in your GMD file)



            title_xpath: str = (
                ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"
            )
            date_xpath: str = (
                ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation//gmd:date/gmd:CI_Date/gmd:date/gco:DateTime"
            )
            abstract_xpath: str = (
                ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString"
            )
            quality_xpath: str = (
                ".//gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep/gmd:description/gco:CharacterString"
            )

            # Example: Extracting title and abstract
            title_elements = self._extract_gmd_data(root, title_xpath, self._namespaces)
            date_elements = self._extract_gmd_data(root, date_xpath, self._namespaces)
            abstract_elements = self._extract_gmd_data(
                root, abstract_xpath, self._namespaces
            )
            quality_elements = self._extract_gmd_data(
                root, quality_xpath, self._namespaces
            )
            theme_elements = root.findall("./SupplementaryFiles/Theme")
            category_acronym_elements = root.findall(
                "./SupplementaryFiles/CategoryAcronym"
            )

            self.record["title"] = (
                title_elements[0].text if category_acronym_elements else ""
            )
            self.record["date"] = date_elements[0].text if theme_elements else ""
            self.record["abstract"] = abstract_elements[0].text if quality_elements else ""
            self.record["quality"] = quality_elements[0].text if abstract_elements else ""
            if theme_elements:
                self.record["theme"] = theme_elements[0].text if date_elements else ""
            else:
                self.record["theme"] = "No theme found"
                logger.error("No theme found in XML file.") 
            self.record["category_acronym"] = (
                category_acronym_elements[0].text if title_elements else ""
            )
            # TODO Ajustar
            self.record["sta_date"] = "error"
            self.record["end_date"] = "error"

    def _read_gmd_xml(self, file_path):

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            logging.error(f"Error parsing XML file: {e}")
            return None
        except FileNotFoundError:
            logging.error(f"Error: File not found: {file_path}")
            return None

    def _extract_gmd_data(self, root, xpath, namespaces=None):
        if namespaces is None:
            namespaces = {}
        return root.findall(xpath, namespaces)
