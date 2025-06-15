

# ETL Silver to Gold

```sh

docker build .
docker run -d -it -p 7500:80 --name etl_instance  etl_fundation


cd /home/vscode/data/new/file/BIO/especies_ameacadas/20240101/00

C:\Temp\dados_silver\silver_data\RESTRICTED\BIO\especies_ameacadas\20240101\00

curl -X 'POST' \
  'http://127.0.0.1:8000/uploadfiles/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data'   \
  -F 'files=@dd_bio_sp_end_20240101.xlsx' \
  -F 'files=@pnt_bio_sp_end_20240101.gpkg'\
  -F 'files=@sld_bio_sp_end_20240101.sld' \
  -F 'files=@md_bio_sp_end_20240101.xml'
```

```sh
 curl -X 'POST'   'http://127.0.0.1:8000/uploadfiles/' 
 -H 'accept: application/json' 
 -H 'Content-Type: multipart/form-data' 
 -F 'files=@dd_bio_sp_end_20240101.xlsx' 
 -F 'files=@pnt_bio_sp_end_20240101.gpkg'   
 -F 'files=@sld_bio_sp_end_20240101.sld' 
 -F 'files=@md_bio_sp_end_20240101.xml' 
```

```python
def upload_sld_to_geoserver(file:str) -> str:

    geo = Geoserver(
        service_url=settings.GEOSERVER_URL,
        username=settings.GEOSERVER_USER,
        password=settings.GEOSERVER_PASSWORD
    )
    styles = geo.get_styles()
    geo.upload_style(path=r'path\to\sld\file.sld', workspace='demo')
    geo.publish_style(layer_name='geoserver_layer_name', style_name='sld_file_name', workspace='demo')
    geo.publish_style(layer_name='geoserver_layer_name', style_name='raster_file_name', workspace='demo')
    

    try:
        geo.get_style(style_name="pointa", workspace=settings.GEOSERVER_WORKSPACE)
    except:
        geo.upload_style(path=r'path\to\sld\file.sld', workspace=settings.GEOSERVER_WORKSPACE)

    print()

    return ""
```

## Informações necessárias

### Criar o pdf com dicinário de dados :rocket:

- Pegar do .XLSX :white_check_mark:
- Pegar da tabela do .gpkg  :white_check_mark:
- Fazer o pdfexit :white_check_mark:
- Colocar o PDF em um www
- Adicionar o link do www no XML

### Publicar o .GPKG

#### SLD

- Publicar o SLD caso já não exista

#### Geoserver

- Feature store: :white_check_mark:

- Extrair do XML  :white_check_mark: :white_check_mark:
  - Inicio
  - Termino
  - Termino
  - Theme
  - Abstract
  - Quality
  - category_aconym

- Criar a datastore
  - Atalizar do featurestore com  :white_check_mark:
    - Informações do XML :white_check_mark:
    - Informações do SLD :white_check_mark:

- REST API
  - Endpoint envio arquivos
  - Endpoint visualização formulário


#### Geonetwork

[exemplo python](https://docs.geonetwork-opensource.org/3.12/api/the-geonetwork-api/#connecting-to-the-api-with-python)

[api](https://www.geocat.ch/geonetwork/doc/api/index.html)


- [api deonetwork](https://catalog.iocasta.com.br/doc/api/index.html)

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
poetry add pdfkit
sudo apt install -y wkhtmltopdf

```

## Markdown

[ícones](https://gist.github.com/rxaviers/7360908)