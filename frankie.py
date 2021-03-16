import json
from enum import Enum

import requests

HOST = "http://192.168.0.1"
# In my experience, the referrer must be set as host in the headers but perhaps there is a use case where they are different
REFERER = HOST

### Below this line are things found in the default http://192.168.0.1/ interface
def get_about():
    """
    Corresponds to: http://192.168.0.1/about/
    """
    return send_request("/cgi-bin/about.index.cgi", "load", "null")


def get_hidden_debug():
    """
    Corresponds to: http://192.168.0.1/about/ (whn you click debug)
    """
    return send_request("/cgi-bin/hidden.debug-lte_engineering.cgi", "load", "null")


def get_apns():
    """
    Corrresponds to: http://192.168.0.1/settings/mobile_network-apn.html
    """
    return send_request("/cgi-bin/settings.mobile_network-apn.cgi", "load", "null")


def connect():
    """
    Corrresponds to: http://192.168.0.1/
    """
    return send_request("/cgi-bin/home.index.cgi", "connect", "null")


def disconnect():
    """
    Corrresponds to: http://192.168.0.1/
    """
    return send_request("/cgi-bin/home.index.cgi", "disconnect", "null")


def set_active_apn(index):
    """
    Corresponds to: http://192.168.0.1/settings/mobile_network-apn.html
    data is zero-indexed
    After running set_active_apn you either need to run the "connect" command or reboot
    """
    apnData = get_apns()
    for apn in apnData["data"]["apns"]:
        apn["active"] = ""
        ## These two must be set to strings
        apn["index"] = str(apn["index"])
        apn["auth"] = str(apn["auth"])

    if index > len(apnData["data"]["apns"]):
        raise IndexError(
            f"Index {index} was passed but available apns length was {len(apnData['data']['apns'])}"
        )
    apnData["data"]["apns"][index]["active"] = "true"

    return send_request(
        "/cgi-bin/settings.mobile_network-apn.cgi", "save", "null", apnData["data"]
    )


def get_wifi_settings_basic():
    """
    Corresponds to: http://192.168.0.1/settings/wifi-basic.html
    """
    return send_request("/cgi-bin/settings.wifi-basic.cgi", "load", "null")


def set_wifi_settings_basic(data):
    """
    Corresponds to: http://192.168.0.1/settings/wifi-basic.html
    TODO:
    I do not have the time/need to make this into a function with parameters.
    A PR to improve this would be very welcome.
    """
    return send_request("/cgi-bin/settings.wifi-basic.cgi", "load", data)


def get_wifi_settings_advanced():
    """
    Corresponds to: http://192.168.0.1/settings/wifi-advanced.html
    """
    return send_request("/cgi-bin/settings.wifi-advanced.cgi", "load", "null")


def set_wifi_settings_advanced(data):
    """
    Corresponds to: http://192.168.0.1/settings/wifi-advanced.html
    TODO:
    I do not have the time/need to make this into a function with parameters.
    A PR to improve this would be very welcome.
    """
    return send_request("/cgi-bin/settings.wifi-advanced.cgi", "load", data)


def get_wifi_connected_devices():
    """
    Corresponds to: http://192.168.0.1/connected_devices/connected.html
    NOTE: This may be obvious, but if you are doing USB tethering the won't show here
    """
    return send_request("/cgi-bin/connected_devices.connected.cgi", "load", "null")


def get_display_preferences():
    """
    Corresponds to: http://192.168.0.1/settings/device-preferences.html
    """
    return send_request("/cgi-bin/settings.device-preferences.cgi", "load", "null")


class DisplayTimeout(Enum):
    _30_SECONDS = "0"
    _1_MINUTE = "1"
    _5_MINUTES = "2"
    _NEVER = "3"


def set_display_preferences(timeout: DisplayTimeout, led_enabled: bool):
    """
    Corresponds to: http://192.168.0.1/settings/device-preferences.html
    """
    led_value = "1" if led_enabled else "0"
    data = {"device_display_timeout": timeout.value, "led": led_value}
    return send_request(
        "/cgi-bin/settings.device-preferences.cgi", "save", "null", data
    )


### Below this line are things found in the http://192.168.0.1/hidden/ interface
def get_LTE_settings():
    """
    Corresponds to: http://192.168.0.1/hidden/data-lte.html
    """
    return send_request("/cgi-bin/hidden.data-lte.cgi", "load")


def set_LTE_band_priorities(band_priorities: [str]):
    """
    Corresponds to: http://192.168.0.1/hidden/data-lte.html
    This can be used to prioritize bands, though I'm not sure if you can "force" any specific band.
    Available bands can be retrived from the corresponding get function
    band_priorities: an array of strings ex: ['4', '66', '12', '71', '2'].
        The bands at the biginning of the array will get the highest priority.
        You can put as few bands as you like
        You must reboot after setting this for changes to apply
    """
    data = {"configured_list": band_priorities}
    return send_request("/cgi-bin/hidden.data-lte.cgi", "apply_band_priorities", data)


### Below this line are things found in the http://192.168.0.1/webpst/ interface
def reboot():
    """
    Sends the reboot request
    Corresponds to: http://192.168.0.1/webpst/reboot.html
    """
    return send_request("/cgi-bin/init_page.cgi", "reboot")


### Below this line are things found in the http://192.168.0.1/engineering/ interface
def get_imei_and_mac():
    """
    Get the IMEI and mac addresses
    Corrersponds to: http://192.168.0.1/engineering/franklin/imei_mac.html
    """
    return send_request("/cgi-bin/webpst.imei_mac.cgi", "load", "null")


def set_imei_and_mac(imei="", mac0="", mac1=""):
    """
    Set the imei and/or mac addresses
    Fields left blank are not changed
    This should only be used to for repairing corrupted data

    Use strings for input
    Corresponds to: http://192.168.0.1/engineering/franklin/imei_mac.html
    """
    data = {"imei": str(imei), "mac_wlan0ap": str(mac0), "mac_wlan1ap": str(mac1)}
    return send_request("/cgi-bin/webpst.imei_mac.cgi", "save", "null", data)


def send_request(path, command, params=None, data=None):
    url = HOST + path
    payload = {"command": command}
    if data is not None:
        payload["data"] = data
    if params is not None:
        payload["params"] = params
    headers = {"Referer": REFERER}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.json()
