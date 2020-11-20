from flask import request


def _get_device_serial_from_args():
    # Get the device serial number from the arguments
    deviceSerialNumberFromArgs = request.args['deviceSerial']
    if deviceSerialNumberFromArgs:
        return deviceSerialNumberFromArgs


def _get_ios_device():
    if (request.user_agent.platform == "iPhone" or
            request.user_agent.platform == "iPad"):
        return True
