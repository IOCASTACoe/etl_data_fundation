


from geo.Geoserver import Geoserver

GEOSERVER_URL:str = "http://cobalto.iocasta.com.br:8080/geoserver"

GEOSERVER_USER:str = 'admin'
GEOSERVER_PASSWORD:str = 'geoserver'
GEOSERVER_WORKSPACE:str = 'gold'

geo = Geoserver(
    service_url=GEOSERVER_URL,
    username=GEOSERVER_USER,
    password=GEOSERVER_PASSWORD,
)  

colecao = geo.get_layers()
links = []
for detail in colecao['layers']['layer']:
    link = detail['href']
    response = geo._requests(method='GET', url=link)
    url = response.json()['layer']['resource']['href']
    response = geo._requests(method='GET', url=url)
    if response.status_code != 200:
        continue

    a = response.json()
    try:
        rec = {
            "title": a['featureType']['title'],
            "name": a['featureType']['name'],
            "keywords": a['featureType']['keywords']['string'],
            #"abstract": a['featureType']['abstract']
            } 
    except:
        rec = {"title": a['coverage']['title'],
            "keywords": a['coverage']['keywords']['string'],
            "name": a['coverage']['name'],
            #"abstract": a['layer']['abstract']
            }
    links.append(rec)


    for keyword in links:
        print(keyword['name'], keyword["title"], keyword['keywords'])
print(links)