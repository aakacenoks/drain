import json


class Device:
    def __init__(self, device_params):
        self.name = device_params['name']
        self.os = device_params['os']
        self.udid = device_params['udid']
        self.hub_serial = device_params['hub_serial']
        self.hub_port = device_params['hub_port']
        self.connected = False
        self.battery_percentage = None

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
