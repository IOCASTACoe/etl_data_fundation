# import requests
# import json

# def modify_layer(geoserver_endpoint: str, user: str, password: str, workspace: str, layer: str, attributes: dict):
    

#     data = {"layer": attributes}

#     url = f"{geoserver_endpoint}/rest/workspaces/{workspace}/layers/{layer}"

#     headers = {"Content-type": "application/json"}
#     requests.put(url, auth=(user, password), data=json.dumps(data), headers=headers)