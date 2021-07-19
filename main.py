from flask import Flask, request, jsonify
from config.device.devices import Devices
from logger import log

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

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
    devices.auto_update = True
    return {'message': 'Cycle mode enabled'}, 200


@app.route('/api/connect')
def connect():
    try:
        devices.cycle_mode = False
        devices.auto_update = False
        devices.connect()
        return {'message': 'Cycle mode disabled. All ports connected.'}, 200
    except:
        return {'error': 'Could not connect all ports. Check hub connection.'}, 500



if __name__ == '__main__':
    app.run()
