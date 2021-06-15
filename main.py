from flask import Flask, request, jsonify
from devices import Devices

app = Flask(__name__)


@app.route('/api/status')
def status():
    requested_udid = request.args.get('device')
    devices = Devices()
    if requested_udid is None:
        response = jsonify(devices.to_dict())
        response.status_code = 200
        return response
    else:
        if devices.contains(requested_udid):
            response = jsonify(devices.get(requested_udid).to_dict())
            response.status_code = 200
            return response
    resp = jsonify({'error': f'Device with udid {requested_udid} not connected.'})
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run()
