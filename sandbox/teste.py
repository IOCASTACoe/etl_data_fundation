


"""
field_name = ".//data_dictionary/field/name"
field_description = ".//data_dictionary/field/description"
response = requests.get('http://cobalto.iocasta.com.br:8081/srv/api/records/4299abfd-f862-4b87-ad96-4cb38f34a888/formatters/xml')
root = ET.fromstring(response.content)
title_elements = root.findall(".//data_dictionary/field")

for field in title_elements:
    el = ET.Element("type")
    el.text = "char"
    field.append(el)

ET.ElementTree(root).write("teste.xml", encoding="utf-8", xml_declaration=True)

print("Fields:")


logger.info("Generate PDF file")

html_path_final: str = f"{settings.TEMP_FILES}{file_name}"
file_to_remove:str = html2pdf(html_path_final.__str__())
os.remove(file_to_remove)
"""