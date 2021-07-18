from flask import Flask, request, jsonify
from config.device.devices import Devices
from logger import log

app = Flask(__name__)

devices = Devices()
print(devices.to_string())
devices.update()


@app.route('/api/status')
def status():
    requested_udid = request.args.get('device')
    if requested_udid is None:
        return jsonify(devices.to_dict()), 200
    else:
        if devices.contains(requested_udid):
            return devices.get(requested_udid).to_dict(), 200
    return {'error': f'Device with udid {requested_udid} not connected.'}, 404


@app.route('/api/cycle')
def cycle():
    devices.cycle_mode = True
    return {'message': 'Automatic update disabled'}, 200


@app.route('/api/connect')
def connect():
    devices.cycle_mode = False
    return {'message': 'Automatic update disabled'}, 200


@app.route('/api/noupdate')
def no_update():
    devices.auto_update = False
    return {'message': 'Automatic update disabled'}, 200


@app.route('/api/update')
def update():
    devices.auto_update = True
    return {'message': 'Automatic update enabled'}, 200


if __name__ == '__main__':
    app.run()
