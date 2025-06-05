
# ETL Silver to Gold

## Informações necessárias

### Criar o pdf com dicinário de dados

- Pegar do .XLSX
- Pegar da tabela do .gpkg
- Fazer o pdfexit
- Colocar o PDF em um www
- Adicionar o link do www no XML

### Publicar o .GPKG

#### SLD

- Publicar o SLD caso já não exista

#### Geoserver

- Feature store:

- Extrair do XML
  - Inicio
  - Termino
  - Theme
  - Abstract
  - Nome

- Criar a datastore
  - Atalizar do featurestore com
    - Informações do XML
    - Informações do SLD

#### Geonetwork

- Enviar XML
- Ajustar o Geoserver com o id do geonetwork

## Instalação GDAL

[referência](https://medium.com/@felipempfreelancer/install-gdal-for-python-on-ubuntu-24-04-9ed65dd39cac)

```sh
sudo apt-get update
sudo apt install python3-pip -y 
sudo apt install python3.12-venv
sudo apt-get install -y libgdal-dev gdal-bin python3-gdal
sudo apt-get install python3.12-dev -y
sudo apt-get install build-essential ##This one solves some bugs sometimes
export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal
```

### Para o poetry

```sh
 poetry add GDAL==`gdal-config --version`
 ```

## JINA2 e gerção do PDF

[referência](https://linlinzhao.com/tech/2021/01/20/jinja-report.html) 

```sh
sudo apt install -y wkhtmltopdf
```