from flask import request


# TODO: Add validation if the serial is not found on MI Cloud
def _get_device_serial_from_args():
    # Get the device serial number from the arguments
    deviceSerialNumberFromArgs = request.args['deviceSerial']
    if deviceSerialNumberFromArgs:
        return deviceSerialNumberFromArgs


# TODO: Remove MACOS from the list for prod!
def _get_ios_device():
    if request.user_agent.platform == "iPhone" or request.user_agent.platform == "iPad" or request.user_agent.platform == "macos":
        return True
