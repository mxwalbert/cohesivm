import serial


class SerialCommunication:
    """
    A class for establishing and managing serial communication with a device.
    """

    def __init__(self, com_port: str, baudrate: int = 9600, timeout: int = 1):
        """
        Initialize the SerialCommunication instance.

        :param com_port: The COM port of the device.
        :param baudrate: The baudrate for serial communication. Default is 9600.
        :param timeout: The timeout value for serial communication. Default is 1.
        """
        self.com_port = com_port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def __enter__(self):
        self.serial = serial.Serial(self.com_port, baudrate=self.baudrate, timeout=self.timeout)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.serial is not None and self.serial.is_open:
            self.serial.close()

    def send_signal(self, data: str):
        """
        Send a signal or command to the connected device over the serial interface.

        :param data: The data to be sent.
        """
        if self.serial is not None and self.serial.is_open:
            self.serial.write(str(data).encode())

    def receive_signal(self) -> str:
        """
        Receive a signal or response from the connected device over the serial interface.

        :returns: The received signal or response.
        """
        if self.serial is not None and self.serial.is_open:
            return self.serial.readline().decode().strip()
