"""Module containing the implemented interfaces which inherit the Interface Abstract Base Class."""
from . import InterfaceType
from .abcs import InterfaceABC
from .serial_communication import SerialCommunication
import numpy as np


class TrivialHILO(InterfaceABC):
    """This interface is the conventional, single-point connection to a sample with one positive/high-voltage terminal
    and one negative/low-voltage terminal. It can also be used if the selection of pixels is carried out manually
    (not recommended)."""
    _interface_type = InterfaceType.HI_LO
    _pixels = ['0']
    _sample_layout = {'0': np.array([0, 0])}

    def select_pixel(self, pixel: str):
        """Only checks if the pixel value is valid.

        :param pixel: The pixel value.
        :raises ValueError: If the pixel is not available on the interface.
        """
        if pixel not in self._pixels:
            raise ValueError(f"Pixel {pixel} is not available!")


class MA8X8(InterfaceABC):
    """The implementation of the Measurement Array 8x8 interface which consist of 64 front contact pixels and a single
    back contact on an area of 25 mm x 25 mm. The interface is controlled by an Arduino Nano Every board which is
    connected through a serial COM port."""
    _interface_type = InterfaceType.HI_LO
    _pixels = [str(i+1 + 10*(j+1)) for j in range(8) for i in range(8)]
    _sample_layout = {pixel: np.array(
        (2.7 + (int(pixel) % 10 - 1) * 2.8, 25.0 - 2.7 - (int(pixel) // 10 - 1) * 2.8)
    ) for pixel in _pixels}

    def __init__(self, com_port: str):
        """Initializes the Measurement Array 8x8 interface by defining the serial connection to the Arduino board.

        :param com_port: The COM port of the Arduino Nano Every board.
        """
        self._arduino = SerialCommunication(com_port, baudrate=9600, timeout=2)

    def select_pixel(self, pixel: str):
        """Select a pixel on the Measurement Array 8x8 by sending a signal to the Arduino board.

        :param pixel: The pixel value to activate.
        :raises ValueError: If the pixel is not available on the interface.
        :raises RuntimeError: If the pixel selection fails.
        """
        if pixel not in self._pixels:
            raise ValueError(f"Pixel {pixel} is not available!")
        with self._arduino as serial:
            serial.send_signal(pixel)
            response = serial.receive_signal()
            if response != "1":
                raise RuntimeError(f"Failed to activate pixel {pixel}")
