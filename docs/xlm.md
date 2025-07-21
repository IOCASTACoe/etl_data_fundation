# Validação


| Field             | xPath                                                                                                                        |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| title             | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation/gmd:title/gco:CharacterString               |
| language          | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:language/gmd:LanguageCode                                            |
| date              | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:citation/gmd:CI_Citation//gmd:date/gmd:CI_Date/gmd:date/gco:DateTime |
| abstract          | .//gmd:identificationInfo/gmd:MD_DataIdentification/gmd:abstract/gco:CharacterString                                         |
| theme             | .//SupplementaryFiles/Theme                                                                                                  |
| category_acronym  | .//SupplementaryFiles/CategoryAcronym                                                                                        |
| Datas inpicio/Fim | .//gmd:extent/gmd:EX_Extent/gmd:temporalElement/gmd:EX_TemporalExtent/gmd:extent                                             |



## Recursos de teste:
https://xpather.com/

## Teste do xML
http://catalogdev.iocasta.com.br/srv/por/catalog.edit#/import
