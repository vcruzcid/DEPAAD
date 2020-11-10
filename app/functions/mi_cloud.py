import requests
from conf import app_config


def assign_device(userid, deviceid):
    api_endpoint = "/device/updateAccount"
    full_url = app_config.MI_API_URL + api_endpoint
    data = {'accountId': {userid}, 'deviceIds': {deviceid}}
    headers = app_config.AUTH_HEADERS
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    putdevice = requests.put(full_url, data=data, headers=headers)
    return putdevice


def search_device_by_serial(serial, dm_partition_id):
    api_endpoint = f"/device?q={serial}&rows=50&start=0&fq=&dmPartitionId={dm_partition_id}"
    full_url = app_config.MI_API_URL + api_endpoint
    device_search = requests.request(
        "GET", full_url, headers=app_config.AUTH_HEADERS)
    return device_search


# TODO: Add feature to support multiple cloud spaces


def get_mi_cloud_dmpartitionid():
    api_endpoint = "/tenant/partition/device"
    full_url = app_config.MI_API_URL + api_endpoint
    cloud_partition = requests.request(
        "GET", full_url, headers=app_config.AUTH_HEADERS).json()
    return cloud_partition["result"]["searchResults"][0]["id"]


def get_mi_cloud_user(username):
    api_endpoint = f"/account?q={username}"
    full_url = app_config.MI_API_URL + api_endpoint
    cloud_user = requests.request(
        "GET", full_url, headers=app_config.AUTH_HEADERS).json()
    return cloud_user["result"]["searchResults"]
