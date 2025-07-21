import logging
import certifi
import requests

import app.src.config as settings

logger = logging.getLogger(__name__)

def delete_record(record_id: str) -> None:
    """
    Deletes a record from Geonetwork by its UUID.
    """
    session = requests.Session()
    response = session.post(settings.GEONETWORK_AUTH_URL)

    xsrf_token = response.cookies.get("XSRF-TOKEN")
    if xsrf_token:
        logger.info("The XSRF Token is: %s", xsrf_token)
    else:
        logger.error("Unable to find the XSRF token")

    headers = {
        "Accept": "application/json",
        "X-XSRF-TOKEN": xsrf_token,
        "Cache-Control": "no-cache",
    }

    response = session.delete(
        f"{settings.GEONETWORK_SERVER}/srv/api/records/{record_id}",
        auth=(settings.GEONETWORK_USERNAME, settings.GEONETWORK_PASSWORD),
        headers=headers,
        verify=certifi.where(),
    )

    if response.status_code != 204:
        logger.error(f"Error deleting record {record_id}: {response.text}")
        raise Exception(f"Error deleting record {record_id}: {response.text}")


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
        verify=certifi.where(),
    )

    if response.status_code != 201:
        logger.error(f"Error uploading XML to Geonetwork: {response.text}")
        raise Exception(f"Error uploading XML to Geonetwork: {response.text}")
    z=dict(response.json()['metadataInfos'])    
    uuid: str = z[[x for x in z][0]][0]['uuid']

    return uuid

