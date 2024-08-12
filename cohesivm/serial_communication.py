"""This module implements a class for serial communication with a physical device."""
from __future__ import annotations
import serial
import time


class SerialCommunication:
    """A class for establishing and managing serial communication with a physical device.

    :param com_port: The COM port of the device.
    :param baudrate: The baudrate for serial communication. Default is 9600.
    :param timeout: The timeout value for serial communication. Default is 1.
    """

    def __init__(self, com_port: str, baudrate: int = 9600, timeout: int = 1) -> None:
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def __enter__(self) -> SerialCommunication:
        self.serial = serial.Serial(self.com_port, baudrate=self.baudrate, timeout=self.timeout)
        time.sleep(0.1)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.serial is not None and self.serial.is_open:
            self.serial.close()

    def send_data(self, data: str) -> None:
        """Send data to the connected device over the serial interface.

        :param data: The data to be sent.
        """
        if self.serial is not None and self.serial.is_open:
            self.serial.write(data.encode())

    def receive_data(self) -> str:
        """Receive a signal or response from the connected device over the serial interface.

        :returns: The received response.
        """
        if self.serial is not None and self.serial.is_open:
            return self.serial.readline().decode().strip()

    def send_and_receive_data(self, data: str, delay: float = 0.5) -> str:
        """Send data to the connected device over the serial interface and receive its response after a specified delay.

        :param data: The data to be sent.
        :param delay: The waiting time in s before receiving the response.
        :returns: The received response.
        """
        self.send_data(data)
        time.sleep(delay)
        return self.receive_data()
