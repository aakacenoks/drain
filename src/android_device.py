import subprocess
from src.device import Device
from src.utils import shell
from src.logger import log


class AndroidDevice(Device):
    def __init__(self, device_params):
        super().__init__(device_params)

    def update_battery_percentage(self):
        try:
            charge = shell(f"adb -s {self.udid} shell dumpsys battery | grep level | sed -n -e 's/^.*level: //p'")
            self.battery_percentage = int(charge)
        except (subprocess.CalledProcessError, ValueError):
            log.warning(f"Could not update battery status for {self.name} ({self.udid}). Check connection.")
