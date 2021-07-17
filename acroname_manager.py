import brainstem
from brainstem.result import Result

from logger import log


class AcronameManager:
    def __init__(self):
        self.stem = None

    def connect_to_hub(self, serial_number):
        stem = brainstem.stem.USBHub3p()
        result = stem.discoverAndConnect(1, serial_number=serial_number)
        if result == Result.NO_ERROR:
            self.stem = stem
        else:
            log.info("Error Connecting to USBHub3p(). Make sure you are using the correct module object")
        pass

    def disable_all_ports(self, serial_number):
        self.connect_to_hub(serial_number)
        for port in range(0, 8):
            self.stem.usb.setPortDisable(port)
        self.stem.disconnect()

    def enable_all_ports(self, serial_number):
        self.connect_to_hub(serial_number)
        for port in range(0, 8):
            self.stem.usb.setPortEnable(port)
        self.stem.disconnect()

    def disable_port(self, serial_number, port_number):
        self.connect_to_hub(serial_number)
        self.stem.usb.setPortDisable(port_number)
        self.stem.disconnect()

    def enable_port(self, serial_number, port_number):
        self.connect_to_hub(serial_number)
        self.stem.usb.setPortEnable(port_number)
        self.stem.disconnect()
