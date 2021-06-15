from flask import Flask, request, jsonify
from devices import Devices
from logger import log

app = Flask(__name__)

devices = Devices()
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


@app.route('/api/update')
def update():
    devices.auto_update = True
    devices.update()
    return {'message': 'Automatic update enabled'}, 200


@app.route('/api/noupdate')
def noupdate():
    devices.auto_update = False
    return {'message': 'Automatic update disabled'}, 200


if __name__ == '__main__':
    app.run()
