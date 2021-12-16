import subprocess
from src.logger import log
from src.device import Device
from src.utils import shell


class IOSDevice(Device):
    def __init__(self, device_params):
        super().__init__(device_params)

    def update_battery_percentage(self):
        try:
            charge = shell(f'ideviceinfo -u {self.udid} -q com.apple.mobile.battery -k BatteryCurrentCapacity')
            self.battery_percentage = int(charge)
        except (subprocess.CalledProcessError, ValueError):
            log.warning(f"Could not update battery status for {self.name} ({self.udid}). Check connection.")
            self.connected = None
