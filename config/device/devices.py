import json
import time
from config.device.android_device import AndroidDevice
from config.device.ios_device import IOSDevice
from utils import read_devices, get_connected_ios_devices, get_connected_android_devices
from threading import Thread
from logger import log
from acroname_manager import enable_all_ports, disable_all_ports


class Devices:
    def __init__(self):
        self.device_list = self.generate_devices()
        self.auto_update = True
        self.cycle_mode = True
        self.hubs = set([device.hub_serial for device in self.device_list])

    def generate_devices(self):
        generated_devices = []
        device_list = read_devices()
        for device_params in device_list['devices']:
            if device_params['os'].lower() == "android":
                generated_devices.append(AndroidDevice(device_params))
            else:
                generated_devices.append(IOSDevice(device_params))
        return generated_devices

    def disconnect(self):
        for hub in self.hubs:
            disable_all_ports(hub)

    def connect(self):
        for hub in self.hubs:
            enable_all_ports(hub)

    def to_dict(self):
        return [d.to_dict() for d in self.device_list]

    def to_string(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

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
                log.info("conection update")
                android_devices = get_connected_android_devices()
                ios_devices = get_connected_ios_devices()
                for device in self.device_list:
                    if type(device) is AndroidDevice:
                        device.connected = device.udid in android_devices
                    else:
                        device.connected = device.udid in ios_devices
                time.sleep(10)
            else:
                time.sleep(30)

    def update_battery_percentage(self):
        while True:
            if self.auto_update:
                log.info("battery update")
                for device in self.device_list:
                    device.update_battery_percentage()
                time.sleep(15)
            else:
                time.sleep(30)

    def cycle(self):
        while True:
            if self.cycle_mode:
                pass

    def update(self):
        connection_updates = Thread(name='connection', target=self.update_connection)
        connection_updates.setDaemon(True)
        connection_updates.start()
        battery_updates = Thread(name='battery', target=self.update_battery_percentage)
        battery_updates.setDaemon(True)
        battery_updates.start()
        cycles = Thread(name='cycle', target=self.cycle)
        cycles.setDaemon(True)
        cycles.start()
