from flask import Flask, request, jsonify

from config.device.devices import Devices
from logger import log

app = Flask(__name__)

devices = Devices()

print(devices.to_dict())
devices.auto_update = True
devices.update()

log.debug("test log")


@app.route('/api/status')
def status():
    requested_udid = request.args.get('device')
    if requested_udid is None:
        return jsonify(devices.to_dict()), 200
    else:
        if devices.contains(requested_udid):
            return devices.get(requested_udid).to_dict(), 200
    return {'error': f'Device with udid {requested_udid} not connected.'}, 404


if __name__ == '__main__':
    app.run()
