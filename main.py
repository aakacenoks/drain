from flask import Flask, request, jsonify
import subprocess
import yaml

app = Flask(__name__)


def shell(command):
    byte_output = subprocess.check_output(command, shell=True)
    return byte_output.decode('UTF-8').rstrip()


class Device:
    def __init__(self, device_params):
        self.name = device_params['name']
        self.os = device_params['os']
        self.udid = device_params['udid']
        self.hub_serial = device_params['hub_serial']
        self.port = device_params['hub_port']
        self.params = device_params

    def get_battery_percentage(self):
        if self.os == 'Android':
            return shell(f"adb -s {self.udid} shell dumpsys battery | grep level | sed -n -e 's/^.*level: //p'")
        else:
            return shell(f'ideviceinfo -u {self.udid} -q com.apple.mobile.battery -k BatteryCurrentCapacity')


def read_devices():
    with open("devices.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def create_devices(device_list):
    devices = []
    for device_params in device_list['devices']:
        new_device = Device(device_params)
        devices.append(new_device)
    return devices


@app.route('/api/status')
def status():
    requested_udid = request.args.get('device')
    devices = create_devices(read_devices())
    for device in devices:
        if device.udid == requested_udid:
            params = device.params
            params['battery'] = device.get_battery_percentage()
            resp = jsonify(params)
            resp.status_code = 200
            return resp
    resp = jsonify({'error': f'Device with udid {requested_udid} not connected.'})
    resp.status_code = 404
    return resp


if __name__ == '__main__':
    app.run()
