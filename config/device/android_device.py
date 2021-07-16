import subprocess

from config.device.device import Device
from utils import shell


class AndroidDevice(Device):
    def __init__(self, device_params):
        super().__init__(device_params)

    def update_battery_percentage(self):
        try:
            charge = shell(f"adb -s {self.udid} shell dumpsys battery | grep level | sed -n -e 's/^.*level: //p'")
            self.battery_percentage = int(charge)
        except (subprocess.CalledProcessError, ValueError) as error:
            print('Handling run-time error:', error)
