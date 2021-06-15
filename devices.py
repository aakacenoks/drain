from device import Device
from utils import read_devices
import threading
import time
from logger import log


class Devices:
    def __init__(self):
        self.device_list = self.generate_devices()
        self.auto_update = False

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

    def update_connection(self):
        while True:
            if self.auto_update:
                log.info("Start connection update")
                time.sleep(1)
                log.info("End connection update")
            else:
                log.info("Auto-update disabled. Connection will not be updated.")
                raise SystemExit()

    def update_battery_percentage(self):
        while True:
            if self.auto_update:
                log.info("Start battery update")
                time.sleep(1)
                log.info("End battery update")
            else:
                log.info("Auto-update disabled. Battery stats will not be updated.")
                raise SystemExit()

    def update(self):
        connection_updates = threading.Thread(name='connection', target=self.update_connection)
        battery_updates = threading.Thread(name='battery', target=self.update_battery_percentage)
        connection_updates.setDaemon(True)
        battery_updates.setDaemon(True)
        connection_updates.start()
        battery_updates.start()
