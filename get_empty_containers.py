# Get containers without attachments and without urls/domains in it

import requests
from datetime import datetime, timedelta
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://192.168.5.128/rest"
USER_NAME = "admin"
PASSWORD = "password"
DATEFORMAT = "%Y-%m-%d"
NO_OF_DAYS = 7
CEF_KEY_LIST = ["destinationDnsDomain", "requestURL", "sourceDnsDomain"]


def rest_call(endpoint, include_expensive=True, page_size=0, **params):
    url = f"{BASE_URL}/{endpoint}"

    if include_expensive:
        url += f"?include_expensive"

    if page_size is 0 or page_size:
        params["page_size"] = page_size

    r = requests.get(url, auth=(USER_NAME, PASSWORD), verify=False, params=params)
    r_json = r.json()

    return r_json


def get_containers(age, params=dict()):
    date_week_ago = (datetime.today() - timedelta(days=age)).date().strftime(DATEFORMAT)

    params["_filter_create_time__gte"] = f'"{date_week_ago}"'

    r_json = rest_call("container", **params)

    all_containers = r_json.get("data")
    containers_without_artifacts = [container for container in all_containers if container.get("artifact_count") is 0]
    containers_with_artifacts = [container for container in all_containers if container.get("artifact_count") is not 0]

    return containers_with_artifacts, all_containers


def get_containers_without_attachments(container_id_list, params=dict()):
    params["_filter_container_id__in"] = str(container_id_list)

    r_json = rest_call("container_attachment", **params)
    # rest_call(f'container?_filter_create_time__gte="2022-08-01"')

    containers_with_attachments = r_json.get("data")
    containers_with_attachments_id_list = [container.get("container") for container in containers_with_attachments]
    print(f"containers_with_attachments_id_list: {containers_with_attachments_id_list}")

    containers_without_attachments_id_list = [id for id in container_id_list if
                                              id not in containers_with_attachments_id_list]

    return containers_without_attachments_id_list


def get_containers_without_artifacts(container_id_list, cef_key_list, params=dict()):
    container_list = []
    for cef in cef_key_list:
        params_copy = params.copy()
        params_copy[f"_filter_artifact__cef__{cef}__isnull"] = False
        params_copy["_filter_id__in"] = str(container_id_list)
        r_json = rest_call("container", **params_copy)
        if r_json.get("data"):
            container_list.extend(r_json.get("data"))

    containers_with_artifacts_id_list = [container.get("id") for container in container_list]
    print(f"containers_with_artifacts_id_list: {containers_with_artifacts_id_list}")
    containers_without_artifacts_id_list = [id for id in container_id_list if
                                            id not in containers_with_artifacts_id_list]

    return containers_without_artifacts_id_list


containers_with_artifacts, all_containers = get_containers(NO_OF_DAYS)
container_id_list = [x.get("id") for x in all_containers]
print(f"container_id_list: {container_id_list}")
containers_without_attachments_id_list = get_containers_without_attachments(container_id_list)
print(f"containers_without_attachments_id_list: {containers_without_attachments_id_list}")

containers_without_artifacts_id_list = get_containers_without_artifacts(container_id_list, CEF_KEY_LIST)
print(f"containers_without_artifacts_id_list: {containers_without_artifacts_id_list}")
empty_container_list = list(
    set(containers_without_attachments_id_list).intersection(set(containers_without_artifacts_id_list)))

print(f"Count: {len(empty_container_list)} Final empty container list: {empty_container_list}")
