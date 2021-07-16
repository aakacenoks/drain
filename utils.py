import subprocess
import yaml


def shell(command):
    byte_output = subprocess.check_output(command, shell=True)
    return byte_output.decode('UTF-8').rstrip()


def get_connected_devices(shell_output):
    connected_devices = []
    lines = shell_output.split('\n')[1:]
    for line in lines:
        el = line.split()
        if len(el) > 0:
            adb_id = line.split()[0]
            connected_devices.append(adb_id)
    return connected_devices


def get_connected_android_devices():
    output = shell('adb devices')
    return get_connected_devices(output)


def get_connected_ios_devices():
    output = shell('idevice_id --list')
    return get_connected_devices(output)


def read_devices():
    with open("config/devices.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise Exception(f'Could not read config file: {exc}')


def represents_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False