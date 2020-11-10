import uuid
import requests
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_session import Session  # https://pythonhosted.org/Flask-Session
import msal
import app_config


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


@app.route("/")
def index():
    session["deviceSerial"] = request.args["deviceSerial"]
    if _get_ios_device == False:
        return render_template('error.html', useragent=request.user_agent)
    if session.get("user"):
        return render_template('complete.html', deviceSerial=session.get("deviceSerial"), username=session.get("preferred_username"))
    else:
        return redirect(url_for("login", deviceSerial=session.get("deviceSerial"), username=session.get("preferred_username")))
        

@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = _build_auth_url(scopes=app_config.SCOPE, state=session["state"])
    #return redirect(auth_url)
    return render_template("login.html", auth_url=auth_url, version=msal.__version__)


# Its absolute URL must match the app's redirect_uri set in AAD.
@app.route("/getAADToken")
def authorized():
    if request.args['state'] != session.get("state"):
        return redirect(url_for("index"))
    cache = _load_cache()
    result = _build_msal_app(cache).acquire_token_by_authorization_code(
        request.args['code'],
        # Misspelled scope would cause an HTTP 400 error here.
        scopes=app_config.SCOPE,
        redirect_uri=url_for("authorized", _external=True))
    
    if "error" in result:
        return "Login failure: %s, %s" % (
            result["error"], result.get("error_description"))
    session["user"] = result.get("id_token_claims")
    _save_cache(cache)
    return redirect(url_for("complete", username=session["user"]["preferred_username"], deviceSerial=session.get("deviceSerial")))


@app.route("/complete")
def complete():
    username = session["user"]["preferred_username"]
    deviceSerial = request.args.get('deviceSerial')
    device = search_device_by_serial(
        deviceSerial, get_mi_cloud_dmpartitionid()).json()
    deviceid = device["result"]["searchResults"][0]['id']
    cloud_user = get_mi_cloud_user(username)
    assign_device(cloud_user[0]['id'], deviceid)
    return render_template("complete.html", deviceSerial=deviceSerial, username=username )    

@app.route("/logout")
def logout():
    session.clear()  # Wipe out the user and the token cache from the session
    return redirect(  # Also need to log out from the Microsoft Identity platform
        "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        "?post_logout_redirect_uri=" + url_for("index", _external=True))

#TODO: Add validation if the serial is not found on MI Cloud
def search_device_by_serial(serial, dm_partition_id):
    api_endpoint = f"/device?q={serial}&rows=50&start=0&fq=&dmPartitionId={dm_partition_id}"
    full_url = app_config.MI_API_URL + api_endpoint
    device_search = requests.request(
        "GET", full_url, headers=app_config.AUTH_HEADERS)
    return device_search

#TODO: Add feature to support multiple cloud spaces
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


def assign_device(userid,deviceid):
    api_endpoint = "/device/updateAccount"
    full_url = app_config.MI_API_URL + api_endpoint
    data = {'accountId': {userid}, 'deviceIds': {deviceid}}
    headers = app_config.AUTH_HEADERS
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    putdevice = requests.put(full_url, data=data, headers=headers)
    return putdevice

def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)


def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache)
    accounts = cca.get_accounts()
    if accounts:  # So all accounts belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID, authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET, token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))

def _get_device_serial_from_args():
    #Get the device serial number from the arguments
    deviceSerialNumberFromArgs = request.args['deviceSerial']
    if deviceSerialNumberFromArgs:
        return deviceSerialNumberFromArgs

#TODO: Remove MACOS from the list for prod!
def _get_ios_device():
    if request.user_agent.platform == "iPhone" or request.user_agent.platform == "iPad" or request.user_agent.platform == "macos":
        return True

#TODO: Move error handling


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

#app.jinja_env.globals.update(_build_auth_url=_build_auth_url)  # Used in template

if __name__ == "__main__":
    app.run()
