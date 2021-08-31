from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from devices import Devices
from logger import log
import threading, atexit

from utils import get_appium_process_count

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

devices = Devices()
devices.update()

@app.route("/")
def index():
    return render_template('index.html', devices=devices)

@app.route('/api/status', methods=['GET'])
@cross_origin()
def status():
    log.info(f'active number of threads: {threading.active_count()}')
    requested_udid = request.args.get('device')
    if requested_udid is None:
        return jsonify(devices.to_dict()), 200
    else:
        if devices.contains(requested_udid):
            return devices.get(requested_udid).to_dict(), 200
    return {'error': f'Device with udid {requested_udid} not connected.'}, 404

@app.route('/api/cycle', methods=['POST'])
@cross_origin()
def cycle():
    processes = get_appium_process_count()
    if processes < 1:
        devices.cycle_mode = True
        devices.auto_update = True
        return {'message': 'cycle mode enabled'}, 200
    message = f'cycle mode requested but not enabled. there are {processes} appium processes running'
    log.info(message)
    return {'message': message}, 405

@app.route('/api/connect', methods=['POST'])
@cross_origin()
def connect():
    try:
        devices.cycle_mode = False
        devices.auto_update = False
        devices.connect()
        return {'message': 'cycle mode disabled. all ports connected. ready for testing.'}, 200
    except:
        message = f'could not connect all ports. check hub connection'
        log.info(message)
        return {'message': message}, 500


if __name__ == '__main__':
    atexit.register(connect)
    app.run()
