import requests
import json
import app.src.config as settings

import ast
import re
from geo.Geoserver import Geoserver
from app.src.publis_catalog import delete_record


def modify_layer(layer: str, 
                attributes: dict,
                is_coverage: bool) -> None:
    

    headers = {"Content-type": "application/json"}

    root_name = "coverage" if is_coverage else  "featureType"
    saida = {root_name: {
        "name": layer,
        "title": attributes.get('title', ''),
        "abstract": attributes.get('abstract', ''),
        'keywords': 
                {"string": attributes['keywords']}
    }}

    if not is_coverage:
        saida[root_name]["pg_tables"] = layer
        
    #Coverage or FeatureType
    if is_coverage:
        url_put = f"{settings.GEOSERVER_URL}/rest/workspaces/{settings.GEOSERVER_WORKSPACE}/coveragestores/{layer}/coverages/{layer}"
    else:
        url_put = f"{settings.GEOSERVER_URL}/rest/workspaces/{settings.GEOSERVER_WORKSPACE}/datastores/{layer}/featuretypes/{layer}"

    
    response_put = requests.put(url_put, auth=(settings.GEOSERVER_USER, settings.GEOSERVER_PASSWORD), data=json.dumps(saida, indent=4), headers=headers)
    if response_put.status_code != 200:
        raise Exception(f"Failed to modify layer: {response_put.text}")
    

def get_layer(layer: str):
    
    headers = {"Content-type": "application/json"}

    payload = ""
    url_get = f"{settings.GEOSERVER_URL}/rest/layers/{layer}.json"
    response_get = requests.get(url_get, auth=(settings.GEOSERVER_USER, settings.GEOSERVER_PASSWORD), data=payload, headers=headers)
    if response_get.status_code != 200:
        raise Exception(f"Failed to get layer: {response_get.text}")
    payload= json.loads(response_get.text)

    sld_name =payload['layer']['defaultStyle']['name'].replace(f"{settings.GEOSERVER_WORKSPACE}:","")

    url_get_2 = payload['layer']['resource']['href']
    
    ## Nome of the store is the fifth part of the URL
    paremter_five_store_name = r"(?:https?:\/\/[^\/]+\/)?(?:[^\/]+\/){5}([^\/]+)"
    match = re.search(paremter_five_store_name, url_get_2)
    if match:
        five_store_name = match.group(1)
    else:
        raise Exception("Failed to extract five store name from URL")
    
    
    response_feature_get = requests.get(url_get_2, auth=(settings.GEOSERVER_USER, settings.GEOSERVER_PASSWORD), headers=headers)
    if response_feature_get.status_code != 200:
            raise Exception(f"Failed to get featurestore: {response_get.text}")
    payload_2 = json.loads(response_feature_get.text)
    
    layer_type = "featureType" if payload['layer']['type'] == 'VECTOR' else "coverage"        
            
    # Converte a string para uma lista de dicionários
    
    dicionario ={}
    collection= payload_2[layer_type]["keywords"]["string"].split("|")
    for item in collection:
        k, v = item.split(":",1)
        dicionario[k] = v.strip()

    dicionario['sld_name'] = sld_name
    dicionario['layer_type'] = payload['layer']['type']
    dicionario['store_name'] = five_store_name
    dicionario['layer'] = payload['layer']['name']
    dicionario['layer_name'] = payload['layer']['name'].replace(f"{settings.GEOSERVER_WORKSPACE}:","")

    return dicionario



def delete_store_layer_style(workspace: str, layer: str):
    data_dict = get_layer(layer)

    try:
        delete_layer(workspace=workspace, layer=layer, data_dict=data_dict)
    except Exception as e:
        raise Exception(f"Failed to delete layer {layer}: {str(e)}")
    
    """
    try:
        delete_data_store(workspace=workspace, data_dict=data_dict)
    except Exception as e:
        raise Exception(f"Failed to delete data store for layer {layer}: {str(e)}")
    """

    try:
        delete_record(data_dict['id'])
    except Exception as e:
        raise Exception(f"Failed to delete record {data_dict['id']}: {str(e)}")

    try:
        delete_style(workspace=workspace, sld_name=data_dict['sld_name'])
    except Exception as e:
        raise Exception(f"Failed to delete style {data_dict['sld_name']}: {str(e)}")


    return f"Layer {layer} deleted successfully from workspace {workspace}."

def delete_data_store(layer: str, 
                      is_coverage: bool) -> None:
    
    headers = {"Content-type": "application/json"}

    #Coverage or FeatureType
    if is_coverage:
        url_delete = f"{settings.GEOSERVER_URL}/rest/workspaces/{settings.GEOSERVER_WORKSPACE}/coveragestores/{layer}"
    else:
        url_delete = f"{settings.GEOSERVER_URL}/rest/workspaces/{settings.GEOSERVER_WORKSPACE}/datastores/{layer}"

    response_delete = requests.delete(url_delete, auth=(settings.GEOSERVER_USER, settings.GEOSERVER_PASSWORD), headers=headers)
    if response_delete.status_code != 200:
        raise Exception(f"Failed to delete datastore: {response_delete.text}")
    


def delete_layer(workspace:str, layer:str, data_dict: dict):
    
    is_coverage = data_dict['layer_type'] == "RASTER"
    
    geo = Geoserver(
            service_url=settings.GEOSERVER_URL,
            username=settings.GEOSERVER_USER,
            password=settings.GEOSERVER_PASSWORD,
        )   
    try: 
        geo.delete_layer(layer_name=data_dict["layer_name"], workspace=workspace)
    except Exception as e:
        raise Exception(f"Failed to delete layer {data_dict['layer_name']}: {str(e)}")

    try:
        delete_data_store(layer=data_dict['store_name'], is_coverage=is_coverage)
    except Exception as e:
        raise Exception(f"Failed to delete data store for layer {data_dict['layer_name']}: {str(e)}")
    
    return f"Layer {layer} deleted successfully from workspace {workspace}."


def delete_style(workspace:str, sld_name:str):

    if sld_name in ["generic","line","point","polygon","raster", ""]:
        return "Style deletion skipped for default styles."

    geo = Geoserver(
            service_url=settings.GEOSERVER_URL,
            username=settings.GEOSERVER_USER,
            password=settings.GEOSERVER_PASSWORD,
        )    

    try:
        geo.delete_style(style_name=sld_name, workspace=workspace)
    except Exception as e:
        raise Exception(f"Failed to delete style {sld_name}: {str(e)}")
            
    return f"Style {sld_name} deleted successfully from workspace {workspace}."