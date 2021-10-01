import json
import time
from src.android_device import AndroidDevice
from src.logger import log
from src.ios_device import IOSDevice
from src.utils import read_config_file, get_connected_ios_devices, get_connected_android_devices
from threading import Thread
from src.hub_manager import enable_all_ports, disable_all_ports
from src.constants import BATTERY_CHECK_INTERVAL


class Devices:
    def __init__(self):
        self.device_list = []
        self.populate_device_list()
        self.cycle_mode = True
        self.hubs = set([device.hub_serial for device in self.device_list])

    def populate_device_list(self):
        device_list = read_config_file()
        for device_params in device_list['devices']:
            if device_params['os'].lower() == "android":
                self.device_list.append(AndroidDevice(device_params))
            else:
                self.device_list.append(IOSDevice(device_params))

    def disconnect(self):
        for hub in self.hubs:
            disable_all_ports(hub)

    def connect(self):
        for hub in self.hubs:
            enable_all_ports(hub)
        time.sleep(0.5)
        self.update_connections()

    def to_dict(self):
        return [device.to_dict() for device in self.device_list]

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

    def connect_device(self, udid):
        device = self.get(udid)
        device.connect()

    def disconnect_device(self, udid):
        device = self.get(udid)
        device.disconnect()

    def update_connections(self):
        android_devices = get_connected_android_devices()
        ios_devices = get_connected_ios_devices()
        for device in self.device_list:
            if type(device) is AndroidDevice:
                device.connected = device.udid in android_devices
            else:
                device.connected = device.udid in ios_devices

    def update_battery_percentages(self):
        for device in self.device_list:
            device.update_battery_percentage()

    def cycle(self):
        while True:
            if self.cycle_mode:
                self.connect()
                log.info("cycle update")
                for device in self.device_list:
                    device.update_charge_status()
                self.update_connections()
            time.sleep(BATTERY_CHECK_INTERVAL)

    def update(self):
        cycles = Thread(name='cycle', target=self.cycle)
        cycles.setDaemon(True)
        cycles.start()
