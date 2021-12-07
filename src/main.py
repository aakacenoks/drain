import atexit
from time import sleep

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

from src.constants import CONNECTION_WAITING_TIME, DISCONNECTION_WAITING_TIME
from src.devices import Devices
from src.logger import log
from src.utils import get_appium_process_count

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

devices = Devices()
devices.start_battery_monitor()

@app.route('/api/status', methods=['GET'])
@cross_origin()
def status():
    requested_udid = request.args.get('device')
    if requested_udid is None:
        return jsonify({'cycle_mode': devices.cycle_mode, 'devices': devices.to_dict()}), 200
    else:
        if devices.contains(requested_udid):
            return jsonify({'cycle_mode': devices.cycle_mode, 'device': devices.get(requested_udid).to_dict()}), 200
    return {'error': f'device with udid {requested_udid} not connected.'}, 404

@app.route('/api/cycle', methods=['POST'])
@cross_origin()
def cycle():
    processes = get_appium_process_count()
    if processes < 1:
        devices.cycle_mode = True
        return {'message': 'cycle mode enabled'}, 200
    message = f'cycle mode requested but not enabled. reason: there are {processes} appium processes running'
    log.info(message)
    return {'message': message}, 405

@app.route('/api/connect', methods=['POST'])
@cross_origin()
def connect():
    if request.data:
        key_value_pair = list(request.json.items())
        if key_value_pair[0][0] == 'device':
            udid = key_value_pair[0][1]
            devices.connect_device(udid)
            sleep(CONNECTION_WAITING_TIME)
            devices.update_connections()
            devices.update_battery_percentages()
            message = f'individual device {udid} connected'
            log.info(message)
            return {'message': message}, 200
        return {'error': 'wrong payload. try: {device: udid}'}, 405
    devices.cycle_mode = False
    devices.connect()
    devices.update_battery_percentages()
    message_success = 'cycle mode disabled. all ports connected. ready for testing.'
    log.info(message_success)
    return {'message': message_success}, 200

@app.route('/api/disconnect', methods=['POST'])
@cross_origin()
def disconnect():
    if request.data:
        key_value_pair = list(request.json.items())
        if key_value_pair[0][0] == 'device':
            udid = key_value_pair[0][1]
            if devices.contains(udid):
                devices.disconnect_device(udid)
                sleep(DISCONNECTION_WAITING_TIME)
                devices.update_connections()
                message = f'individual device {udid} disconnected'
                log.info(message)
                return {'message': message}, 200
            return {'error': f'unknown device udid ({udid})'}, 405
        return {'error': 'wrong payload. try: {device: udid}'}, 405
    error_no_device = 'could not disconnect - no device given in payload'
    log.info(error_no_device)
    return {'error': error_no_device}, 405

if __name__ == '__main__':
    atexit.register(connect)
    app.run()
