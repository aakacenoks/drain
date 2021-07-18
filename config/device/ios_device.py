import subprocess
from config.device.device import Device
from utils import shell


class IOSDevice(Device):
    def __init__(self, device_params):
        super().__init__(device_params)

    def update_battery_percentage(self):
        try:
            charge = shell(f'ideviceinfo -u {self.udid} -q com.apple.mobile.battery -k BatteryCurrentCapacity')
            self.battery_percentage = int(charge)
        except subprocess.CalledProcessError as error:
            print('Handling run-time error:', error)

