import logging
import xml.etree.ElementTree as ET
import app.src.config as settings

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

        self.erros = []

        if root is not None:

            try:
                title_xpath: str = (
                    ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString"
                )
                title_elements = self._extract_gmd_data(root, title_xpath, self._namespaces)
                self.record["title"] = (title_elements[0].text)
            except IndexError:
                logger.error("Title element not found in XML.")
                self.erros.append("No title found")

            try:
                language_xpath: str = (
                    ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode"
                )
                language_elements = self._extract_gmd_data(root, language_xpath, self._namespaces)
                self.record["language"] = language_elements[0].text
            except IndexError:
                logger.error("Language element not found in XML.")
                self.erros.append("No language found")

            try:
                date_xpath: str = (
                    ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation//gmd:date/gmd:CI_Date/gmd:date/gco:DateTime"
                )
                date_elements = self._extract_gmd_data(root, date_xpath, self._namespaces)
                self.record["date"] = date_elements[0].text
            except IndexError:
                logger.error("Date element not found in XML.")
                self.erros.append("No date found")

            try:
                abstract_xpath: str = (
                    ".//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString"
                )
                abstract_elements = self._extract_gmd_data(root, abstract_xpath, self._namespaces)
                self.record["abstract"] = abstract_elements[0].text
            except IndexError:
                logger.error("Abstract element not found in XML.")
                self.erros.append("No abstract found")

            try:
                quality_xpath: str = (
                    ".//gmd:dataQualityInfo/gmd:DQ_DataQuality/gmd:lineage/gmd:LI_Lineage/gmd:processStep/gmd:LI_ProcessStep/gmd:description/gco:CharacterString"
                )
                quality_elements = self._extract_gmd_data(root, quality_xpath, self._namespaces)
                self.record["quality"] = quality_elements[0].text
            except IndexError:
                logger.error("Quality element not found in XML.")
                self.erros.append("No quality found")

            try:
                theme_elements = root.findall(".//SupplementaryFiles/Theme")
                self.record["theme"] = theme_elements[0].text
            except IndexError:
                logger.error("Theme element not found in XML.")
                self.erros.append("No theme found")

            try:
                category_acronym_elements = root.findall(".//SupplementaryFiles/CategoryAcronym")
                self.record["category_acronym"] = category_acronym_elements[0].text
            except IndexError:
                logger.error("Category acronym element not found in XML.")
                self.erros.append("No category acronym found")

            try:
                extent_xpath: str = (".//gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent")
                self.record["sta_date"] = self._extract_gmd_data(root, extent_xpath, self._namespaces)[0][0][0].text
                self.record["end_date"] = self._extract_gmd_data(root, extent_xpath, self._namespaces)[0][0][1].text
            except IndexError:
                logger.error("Start date element not found in XML.")
                self.erros.append("No start date found")
        else:
            logger.error("Failed to read XML file or no root element found.")
            self.erros.append("Failed to read XML file or no root element found.")
            self.record = {}

    def get_erros(self) -> str:
        if len(self.erros) > 0:
            result = (f"Errors found: {', '.join(self.erros)}")
        return result
                



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

    def complete_dictionary(self, file_path: str, attibutes:list[dict]):


        tree = ET.parse(file_path)
        root = tree.getroot()
        root = self._read_gmd_xml(file_path)
        

        # Extract namespaces from the file
        # namespaces = {node[0]: node[1] for _, node in ET.iterparse(file_path, events=['start-ns'])}

        namespaces: dict = {
            "gmd": "http://www.isotc211.org/2005/gmd",
            "gco": "http://www.isotc211.org/2005/gco",
            # Add other namespaces as needed
        }

        # Register namespaces to ensure they are preserved
        for prefix, uri in namespaces.items():
            ET.register_namespace(prefix, uri)

        title_elements = self._extract_gmd_data(root, ".//data_dictionary/field", namespaces=namespaces)

        for field in title_elements:

            attr_type = "None"
            col = [x for x in attibutes if x['name'] == field.find('name').text]
            if col:
                 attr_type = col[0]['type']

            el = ET.Element("type")
            el.text = attr_type
            field.append(el)


        str_uuid:str = ".//gmd:fileIdentifier/gco:CharacterString"
        uuid_element = self._extract_gmd_data(root, str_uuid, namespaces=namespaces)
        uuid = uuid_element[0].text

        str_xpath: str = ".//gmd:transferOptions/gmd:MD_DigitalTransferOptions/gmd:onLine[1]/gmd:CI_OnlineResource/gmd:linkage/gmd:URL"
        url_element = self._extract_gmd_data(root, str_xpath, namespaces=namespaces)
        url_element[0].text = f"{settings.ETLAPI_URL}/get_geonetwork_data_dict/key={uuid}"        

        ET.ElementTree(root).write(file_path, encoding="utf-8", xml_declaration=True)
        

    
    def complete_links(self, file_path: str, lst_links: list[dict]):
        # Parse the XML file
        
        root = self._read_gmd_xml(file_path)
        

        # Extract namespaces from the file
        # namespaces = {node[0]: node[1] for _, node in ET.iterparse(file_path, events=['start-ns'])}

        namespaces: dict = {
            "gmd": "http://www.isotc211.org/2005/gmd",
            "gco": "http://www.isotc211.org/2005/gco",
            # Add other namespaces as needed
        }

        # Register namespaces to ensure they are preserved
        for prefix, uri in namespaces.items():
            ET.register_namespace(prefix, uri)


        # Define the XPath for the link elements
        link_path = ".//gmd:distributionInfo/gmd:MD_Distribution/gmd:transferOptions//gmd:MD_DigitalTransferOptions"
        link_elements = self._extract_gmd_data(root, link_path, namespaces=namespaces)
        

        # Add new links
        for item in lst_links:
            ns2_CharacterString = ET.Element("gco:CharacterString")
            ns2_CharacterString.attrib["xmlns:gco"] = "http://www.isotc211.org/2005/gco"
            ns2_CharacterString.text = item["protocol"]
            ns0_protocol = ET.Element("gmd:protocol")
            
            ns0_protocol.append(ns2_CharacterString)

            ns0_URL = ET.Element("gmd:URL")
            ns0_URL.text = item["url"]
            ns0_linkage = ET.Element("gmd:linkage")
            ns0_linkage.append(ns0_URL)

            description_CharacterString = ET.Element("gco:CharacterString")
            description_CharacterString.attrib["xmlns:gco"] = "http://www.isotc211.org/2005/gco"
            description_CharacterString.text = item["label"]
            ns0_description = ET.Element("gmd:description")
            ns0_description.append(description_CharacterString)


            ns0_CI_OnlineResource = ET.Element("gmd:CI_OnlineResource")
            ns0_CI_OnlineResource.append(ns0_linkage)
            ns0_CI_OnlineResource.append(ns0_protocol)
            ns0_CI_OnlineResource.append(ns0_description)

            element = ET.Element("gmd:onLine")
            element.append(ns0_CI_OnlineResource)
            ET.SubElement(link_elements[0], "gmd:onLine").append(element)

        # Write the updated XML back to the file
        ET.ElementTree(root).write(file_path, encoding="utf-8", xml_declaration=True)
