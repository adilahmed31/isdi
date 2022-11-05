from flask import request, render_template
from web import app
from web.view import get_device
from privacy_scan_android import do_privacy_check
from web.view.scan import first_element_or_none
import config

social_apps = ['com.whatsapp','com.snapchat.android','com.facebook.orca','org.telegram.messenger']

@app.route("/privacy", methods=['GET'])
def privacy():
    """
    TODO: Privacy scan. Think how should it flow.
    Privacy is a seperate page.
    """
    return render_template(
        'main.html', task="privacy",
        device_primary_user=config.DEVICE_PRIMARY_USER,
        title=config.TITLE
    )

@app.route("/privacy/<device>", methods=['GET'])
def privacy_scope(device):
    sc = get_device(device)
    if not sc:
        return "Please choose one device to scan."
    ser = sc.devices()

    print("Device detected: {}".format(ser))
    if not ser:
        # FIXME: add pkexec scripts/ios_mount_linux.sh workflow for iOS if
        # needed.
        error = "<b>A device wasn't detected. Please follow the "\
            "<a href='/instruction' target='_blank' rel='noopener'>"\
            "setup instructions here.</a></b>"
        return error

    ser = first_element_or_none(ser)
    # clientid = new_client_id()
    print(">>>Privacy Checkup for ", device, ser, "<<<<<")
    installed_apps = sc.get_apps(ser)
    res = ",".join([app for app in social_apps if app in installed_apps])
    return res

@app.route("/privacy/<device>/<cmd>", methods=['GET'])
def privacy_scan(device, cmd):
    sc = get_device(device)
    res = do_privacy_check(sc.serialno, cmd)
    return res
