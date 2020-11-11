import requests
from conf import app_config
import app


def assign_device(userid, deviceid):
    api_endpoint = "/device/updateAccount"
    full_url = app_config.MI_API_URL + api_endpoint
    data = {'accountId': {userid}, 'deviceIds': {deviceid}}
    headers = app_config.AUTH_HEADERS
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    try:
        putdevice = requests.put(full_url, data=data, headers=headers)
        app.logger.info('Assigned Deviceid: {deviceid} to user: {userid}')
        return putdevice
    except:
        app.logger.error(
            'Error while assigning Deviceid: {deviceid} to user: {userid}')


def search_device_by_serial(serial, dm_partition_id):
    api_endpoint = f"/device?q={serial}&rows=50&start=0&fq=&dmPartitionId={dm_partition_id}"
    full_url = app_config.MI_API_URL + api_endpoint
    try:
        device_search = requests.request(
            "GET", full_url, headers=app_config.AUTH_HEADERS)
        return device_search
    except:
        app.logger.error('Error while getting info in MI Cloud for device serial: {serial}')

# TODO: Add feature to support multiple cloud spaces


def get_mi_cloud_dmpartitionid():
    api_endpoint = "/tenant/partition/device"
    full_url = app_config.MI_API_URL + api_endpoint
    try:
        cloud_partition = requests.request(
            "GET", full_url, headers=app_config.AUTH_HEADERS).json()
        return cloud_partition["result"]["searchResults"][0]["id"]
    except:
        app.logger.error('Error while getting MI Cloud partitionID')


def get_mi_cloud_user(username):
    api_endpoint = f"/account?q={username}"
    full_url = app_config.MI_API_URL + api_endpoint
    try:
        cloud_user = requests.request(
            "GET", full_url, headers=app_config.AUTH_HEADERS).json()
        return cloud_user["result"]["searchResults"]
    except:
        app.logger.error('Error while getting MI Cloud info for: {username}')
