import atexit
from time import sleep

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

from src.constants import CONNECTION_WAITING_TIME, DISCONNECTION_WAITING_TIME
from src.devices import Devices
from src.hub_manager import enable_all_ports, disable_port
from src.logger import log
from src.utils import get_appium_process_count, get_all_connected_devices

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

devices = Devices()
devices.start_battery_monitor()

@app.route('/api/status', defaults={'udid': None}, methods=['GET'])
@app.route('/api/status/<string:udid>', methods=['GET'])
@cross_origin()
def status(udid):
    if not udid:
        return jsonify({'cycle_mode': devices.cycle_mode, 'devices': devices.to_dict()}), 200
    if devices.contains(udid):
        return jsonify({'cycle_mode': devices.cycle_mode, 'device': devices.get(udid).to_dict()}), 200
    return {'error': f'device with udid {udid} in unknown.'}, 404

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

@app.route('/api/connect', defaults={'udid': None}, methods=['POST'])
@app.route('/api/connect/<string:udid>', methods=['POST'])
@cross_origin()
def connect(udid):
    if udid:
        if devices.contains(udid):
            devices.get(udid).connect()
            sleep(CONNECTION_WAITING_TIME)
            devices.update_connections()
            devices.get(udid).update_battery_percentage()
            message = f'individual device {udid} connected'
            log.info(message)
            return {'message': message}, 200
        return {'error': f'unknown device ({udid})'}, 404
    devices.cycle_mode = False
    devices.connect()
    devices.update_battery_percentages()
    message_success = 'cycle mode disabled. all ports connected. ready for testing.'
    log.info(message_success)
    return {'message': message_success}, 200

@app.route('/api/disconnect/<string:udid>', methods=['POST'])
@cross_origin()
def disconnect(udid):
    if udid and devices.contains(udid):
        devices.get(udid).disconnect()
        sleep(DISCONNECTION_WAITING_TIME)
        devices.update_connections()
        message = f'individual device {udid} disconnected'
        log.info(message)
        return {'message': message}, 200
    return {'error': f'unknown device udid ({udid})'}, 404

@app.route('/api/search/<string:udid>', methods=['GET'])
@cross_origin()
def search(udid):
    if devices.cycle_mode:
        log.info(f'searching for device with udid ({udid})...')
        for hub in devices.hubs:
            enable_all_ports(hub)
        sleep(CONNECTION_WAITING_TIME)
        connected_devices = get_all_connected_devices()
        if udid in connected_devices:
            for hub in devices.hubs:
                for port in range(0, 8):
                    disable_port(hub, port)
                    sleep(DISCONNECTION_WAITING_TIME)
                    updated_list = get_all_connected_devices()
                    missing_devices = [device for device in connected_devices if device not in updated_list]
                    if udid in missing_devices:
                        device_info = {'udid': udid, 'hub': hub, 'port': port}
                        log.info(f'device found. info: {device_info}')
                        return device_info, 200
                    log.info(f'searched device did not disconnect. the last disconnected device was {missing_devices[0]}')
            return {'message': f'device ({udid}) is connected, but could not be disconnected'}, 404
        return {'message': f'device ({udid}) is not connected to any of the hubs ({devices.hubs})'}, 404
    return {'message': 'search is only allowed during cycle mode'}, 405

if __name__ == '__main__':
    atexit.register(connect)
    app.run()
