import json
import time
from src.android_device import AndroidDevice
from src.logger import log
from src.ios_device import IOSDevice
from src.utils import get_data_from_yaml, get_connected_ios_devices, get_connected_android_devices
from threading import Thread
from src.hub_manager import enable_all_ports, disable_all_ports
from src.constants import BATTERY_CHECK_INTERVAL, CONNECTION_WAITING_TIME, DISCONNECTION_WAITING_TIME


class Devices:
    def __init__(self):
        self.device_list = []
        self.populate_device_list()
        self.cycle_mode = True
        self.hubs = set([device.hub_serial for device in self.device_list])

    def populate_device_list(self):
        device_list = get_data_from_yaml('devices.yaml')
        for device_params in device_list['devices']:
            if device_params['os'].lower() == "android":
                self.device_list.append(AndroidDevice(device_params))
            elif device_params['os'].lower() == "ios":
                self.device_list.append(IOSDevice(device_params))

    def disconnect(self):
        for hub in self.hubs:
            disable_all_ports(hub)
        time.sleep(DISCONNECTION_WAITING_TIME)
        self.update_connections()

    def connect(self):
        for hub in self.hubs:
            enable_all_ports(hub)
        time.sleep(CONNECTION_WAITING_TIME)
        self.update_connections()

    def to_dict(self):
        return [device.to_dict() for device in self.device_list]

    def to_string(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def contains(self, udid):
        return any(device.udid == udid for device in self.device_list)

    def get(self, udid):
        return next((device for device in self.device_list if device.udid == udid), None)

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
                self.update_connection_status(device, android_devices)
            else:
                self.update_connection_status(device, ios_devices)

    def update_connection_status(self, device, devices):
        if device.udid in devices:
            device.connected = True
        elif device.udid not in devices and device.connected is not None:
            device.connected = False
        else:
            device.connected = None  # error - port is on, but device not in list of connected devices

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

    def start_battery_monitor(self):
        cycles = Thread(name='cycle', target=self.cycle)
        cycles.setDaemon(True)
        cycles.start()
