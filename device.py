from utils import shell, adb_devices


class Device:
    def __init__(self, device_params):
        self.name = device_params['name']
        self.os = device_params['os']
        self.udid = device_params['udid']
        self.hub_serial = device_params['hub_serial']
        self.hub_port = device_params['hub_port']
        self.connected = False
        self.battery_percentage = -1

    def update_connection(self):
        if self.os.lower() == 'android':
            if self.udid in adb_devices():
                self.connected = True
                return
        # elif self.os.lower() == 'ios':
        #     charge = shell(f'idevice_id --list | grep {self.udid}')
        # else:
        #     raise Exception(f'Unknown device OS ({self.os})')
        # self.connected = int(charge)

    def update_battery_percentage(self):
        # Do this after X amount of time forever
        # Safely catch connection errors
        if self.os.lower() == 'android':
            charge = shell(f"adb -s {self.udid} shell dumpsys battery | grep level | sed -n -e 's/^.*level: //p'")
        elif self.os.lower() == 'ios':
            charge = shell(f'ideviceinfo -u {self.udid} -q com.apple.mobile.battery -k BatteryCurrentCapacity')
        else:
            raise Exception(f'Unknown device OS ({self.os})')
        print(self.udid)

        self.battery_percentage = int(charge)

    def to_dict(self):
        self.update_connection()
        return {
            'name': self.name,
            'os': self.os,
            'udid': self.udid,
            'hub_serial': self.hub_serial,
            'hub_port': self.hub_port,
            'connected': self.connected,
            'battery_percentage': self.battery_percentage,
        }