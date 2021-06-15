from flask import Flask, request, jsonify
from devices import Devices

app = Flask(__name__)


@app.route('/api/status')
def status():
    requested_udid = request.args.get('device')
    devices = Devices()
    if requested_udid is None:
        return jsonify(devices.to_dict()), 200
    else:
        if devices.contains(requested_udid):
            return devices.get(requested_udid).to_dict(), 200
    return {'error': f'Device with udid {requested_udid} not connected.'}, 404


if __name__ == '__main__':
    app.run()
