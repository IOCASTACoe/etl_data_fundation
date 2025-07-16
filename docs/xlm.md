# Validação

| Field            | xPath                                                                                                                                          |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| title            | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString                                 |
| identifier       | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:identifier/gmd:MD_Identifier/gmd:code/gco:CharacterString |
| language         | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode                                                              |
| date             | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation//gmd:date/gmd:CI_Date/gmd:date/gco:DateTime                   |
| abstract         | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString                                                           |
| theme            | .//SupplementaryFiles/Theme                                                                                                                    |
| category_acronym | .//SupplementaryFiles/CategoryAcronym                                                                                                          |


## Recursos de teste:
https://xpather.com/

## Teste do xML
http://catalogdev.iocasta.com.br/srv/por/catalog.edit#/import
