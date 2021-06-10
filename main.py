from flask import Flask, request, jsonify
from utils import generate_devices

app = Flask(__name__)


@app.route('/api/status')
def status():
    requested_udid = request.args.get('device')
    devices = generate_devices()
    for device in devices:
        if device.udid == requested_udid:
            device.update_battery_percentage()
            resp = jsonify(device.to_dict())
            resp.status_code = 200
            return resp
    resp = jsonify({'error': f'Device with udid {requested_udid} not connected.'})
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run()
