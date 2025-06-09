import logging
import requests

import app.src.config as settings

logger = logging.getLogger(__name__)

def upload_xml_geonetwork(file_path:str) -> str:

    session = requests.Session()
    response = session.post(settings.GEONETWORK_AUTH_URL)

    xsrf_token = response.cookies.get("XSRF-TOKEN")
    if xsrf_token:
        print("The XSRF Token is:", xsrf_token)
    else:
        print("Unable to find the XSRF token")

    headers = {"Accept": "application/json", "X-XSRF-TOKEN": xsrf_token}

    headers = {
        "Accept": "application/json",
        "X-XSRF-TOKEN": xsrf_token,
        "Cache-Control": "no-cache",
        "boundary": "7617295b-9851-4b35-963e-cb0488cda4a7",
    }

    params = {
        "metadataType": "METADATA",
        "uuidProcessing": "GENERATEUUID",
        "group": "",
        "category": "",
        "rejectIfInvalid": False,
        "publishToAll": True,
        "assignToCatalog": True,
        "transformWith": "_none_",
        "allowEditGroupM": True,
    }


    response = session.post(
        settings.GEONETWORK_SERVER + "/srv/api/records",
        params=params,
        files={
            "file": open(
                file=file_path, mode="r", encoding="utf-8"
            )
        },
        auth=(settings.GEONETWORK_USERNAME, settings.GEONETWORK_PASSWORD),
        headers=headers,
    )

    z=dict(response.json()['metadataInfos'])    
    uuid: str = z[[x for x in z][0]][0]['uuid']

    return uuid

