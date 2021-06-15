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
    
    def to_dict(self):
        devices_dict = []
        for device in self.device_list:
            devices_dict.append(device.to_dict())
        return devices_dict

    def contains(self, udid):
        for device in self.device_list:
            if device.udid == udid:
                return True
        return False

    def get(self, udid):
        for device in self.device_list:
            if device.udid == udid:
                return device
        return None