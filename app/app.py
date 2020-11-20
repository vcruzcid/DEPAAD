import os
import logging
import uuid
from flask import Flask, render_template, session, request, redirect, url_for
from flask_session import Session
from conf import app_config
from functions import ms_auth, ps_common, mi_cloud
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


@app.route("/")
def index():
    try:
        session["deviceSerial"] = request.args["deviceSerial"]
        if ps_common._get_ios_device is False:
            return render_template('error.html', useragent=request.user_agent)
        if session.get("user"):
            return render_template('complete.html', deviceSerial=session.get("deviceSerial"), username=session.get("preferred_username"))
        else:
            return redirect(url_for("login", deviceSerial=session.get("deviceSerial"), username=session.get("preferred_username")))
    except SystemExit:
        app.logger.error('Device serial number not provided')
        return render_template(
            'error.html', error="no serial number provided", useragent=request.user_agent)


@app.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    # Technically we could use empty list [] as scopes to do just sign in,
    # here we choose to also collect end user consent upfront
    auth_url = ms_auth._build_auth_url(
        scopes=app_config.SCOPE, state=session["state"])
    return render_template("login.html", auth_url=auth_url)


# Its absolute URL must match the app's redirect_uri set in AAD.
@app.route("/getAADToken")
def authorized():
    if request.args['state'] != session.get("state"):
        return redirect(url_for("index"))
    cache = ms_auth._load_cache()
    result = ms_auth._build_msal_app(
        cache).acquire_token_by_authorization_code(
            request.args['code'], scopes=app_config.SCOPE,
            redirect_uri=url_for("authorized", _external=True))

    if "error" in result:
        return "Login failure: %s, %s" % (
            result["error"], result.get("error_description"))
    session["user"] = result.get("id_token_claims")
    ms_auth._save_cache(cache)
    return redirect(url_for("complete", username=session["user"]["preferred_username"], deviceSerial=session.get("deviceSerial")))


@app.route("/complete")
def complete():
    username = session["user"]["preferred_username"]
    device_serial = ps_common._get_device_serial_from_args
    try:
        device = mi_cloud.search_device_by_serial(
            device_serial, mi_cloud.get_mi_cloud_dmpartitionid()).json()
        device_id = device["result"]["searchResults"][0]['id']
        if device_id:
            cloud_user = mi_cloud.get_mi_cloud_user(username)
            mi_cloud.assign_device(cloud_user[0]['id'], device_id)
            return render_template(
                "complete.html", deviceSerial=device_serial, username=username)
    except SystemExit:
        app.logger.error('Device serial number not found on MI Cloud')
        return render_template(
            'error.html', error="serial Number:  serial number not found on MI Cloud",
            useragent=request.user_agent, device_serial=device_serial)


@app.route("/logout")
def logout():
    session.clear()  # Wipe out the user and the token cache from the session
    return redirect(  # Also need to log out from the Microsoft Identity platform
        "https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        "?post_logout_redirect_uri=" + url_for("index", _external=True))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.context_processor
def psversion():
    return dict(psver=app_config.VERSION)

# remove comment: app.jinja_env.globals.update(_build_auth_url=_build_auth_url)  # Used in template


if __name__ == "__main__":
    app.run()


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        "logs/depaad.log", maxBytes=1024000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('DEPAAD Started...')
