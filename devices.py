from device import Device
from utils import read_devices


class Devices:
    def __init__(self):
        self.device_list = self.generate_devices()

    def generate_devices(self):
        generated_devices = []
        device_list = read_devices()
        for device_params in device_list['devices']:
            new_device = Device(device_params)
            generated_devices.append(new_device)
        return generated_devices
