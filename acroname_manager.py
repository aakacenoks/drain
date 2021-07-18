import brainstem
from brainstem.result import Result

from logger import log


def connect_to_hub(serial_number):
    stem = brainstem.stem.USBHub3p()
    result = stem.discoverAndConnect(1, serial_number=serial_number)
    if result == Result.NO_ERROR:
        return stem
    else:
        log.info("Error Connecting to USBHub3p(). Make sure you are using the correct module object")
    pass


def disable_all_ports(serial_number):
    stem = connect_to_hub(serial_number)
    for port in range(0, 8):
        stem.usb.setPortDisable(port)
    stem.disconnect()


def enable_all_ports(serial_number):
    stem = connect_to_hub(serial_number)
    for port in range(0, 8):
        stem.usb.setPortEnable(port)
    stem.disconnect()


def disable_port(serial_number, port_number):
    stem = connect_to_hub(serial_number)
    stem.usb.setPortDisable(port_number)
    stem.disconnect()


def enable_port(serial_number, port_number):
    stem = connect_to_hub(serial_number)
    stem.usb.setPortEnable(port_number)
    stem.disconnect()
