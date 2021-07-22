import subprocess
import yaml


def shell(command):
    byte_output = subprocess.check_output(command, shell=True)
    return byte_output.decode('UTF-8').rstrip()

def get_connected_devices(output_lines):
    connected_devices = []
    for line in output_lines:
        el = line.split()
        if len(el) > 0:
            adb_id = line.split()[0]
            connected_devices.append(adb_id)
    return connected_devices

def get_connected_android_devices():
    output = shell('adb devices')
    return get_connected_devices(output.split('\n')[1:])

def get_connected_ios_devices():
    output = shell('idevice_id --list')
    return get_connected_devices(output.split('\n'))

def get_appium_process_count():
    try:
        output = shell('ps -ax | grep appium | grep -v grep')
        return len(output.split('\n'))
    except subprocess.CalledProcessError:
        return 0

def read_devices():
    with open("config/devices.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(f'Could not read config file: {exc}')
