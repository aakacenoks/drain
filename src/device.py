import json
from hub_manager import enable_port, disable_port
from logger import log

MAX_BATTERY = 80
MIN_BATTERY = 30


class Device:
    def __init__(self, device_params):
        self.name = device_params['name']
        self.os = device_params['os']
        self.udid = device_params['udid']
        self.hub_serial = device_params['hub_serial']
        self.hub_port = device_params['hub_port']
        self.connected = False
        self.battery_percentage = 0
        self.charging = True

    def update_charge_status(self):
        self.update_battery_percentage()
        if self.connected:
            if self.battery_percentage >= MAX_BATTERY and self.charging:
                log.info(f"{self.name} is charged enough ({self.battery_percentage}/{MAX_BATTERY}). turning off charging.")
                self.charging = False
                self.disconnect()
            elif self.battery_percentage <= MIN_BATTERY and not self.charging:
                log.info(f"{self.name} is drained enough ({self.battery_percentage}/{MIN_BATTERY}). turning on charging.")
                self.charging = True
                self.connect()
            elif (self.battery_percentage < MAX_BATTERY) and self.charging:
                log.info(f"{self.name} is charging ({self.battery_percentage}/{MAX_BATTERY}). continuing the charge.")
                return
            elif self.battery_percentage > MIN_BATTERY and not self.charging:
                log.info(f"{self.name} is draining ({self.battery_percentage}/{MIN_BATTERY}). continuing the drain.")
                self.disconnect()
            else:
                self.charging = True

    def disconnect(self):
        disable_port(self.hub_serial, self.hub_port)

    def connect(self):
        enable_port(self.hub_serial, self.hub_port)

    def to_dict(self):
        return {
            'name': self.name,
            'os': self.os,
            'udid': self.udid,
            'hub_serial': self.hub_serial,
            'hub_port': self.hub_port,
            'connected': self.connected,
            'battery_percentage': self.battery_percentage,
        }

    def to_string(self):
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)

    def update_battery_percentage(self):
        pass
