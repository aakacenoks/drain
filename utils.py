import subprocess
import yaml
from device import Device


def shell(command):
    byte_output = subprocess.check_output(command, shell=True)
    return byte_output.decode('UTF-8').rstrip()


def read_devices():
    with open("config/devices.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(f'Could not read config file: {exc}')


def generate_devices():
    generated_devices = []
    device_list = read_devices()
    for device_params in device_list['devices']:
        new_device = Device(device_params)
        generated_devices.append(new_device)
    return generated_devices
