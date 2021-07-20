import subprocess
from logger import log
from device import Device
from utils import shell

from utils import get_connected_ios_devices


class IOSDevice(Device):
    def __init__(self, device_params):
        super().__init__(device_params)

    def update_battery_percentage(self):
        try:
            charge = shell(f'ideviceinfo -u {self.udid} -q com.apple.mobile.battery -k BatteryCurrentCapacity')
            self.battery_percentage = int(charge)
        except subprocess.CalledProcessError:
            log.info(f"Could not update battery status for {self.name} ({self.udid}). Check connection.")
