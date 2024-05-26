"""Module containing the implemented interfaces which inherit the Interface Abstract Base Class."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from .serial_communication import SerialCommunication
from .database import Dimensions
import time


class InterfaceType:
    """Contains types of interfaces as constants which are assigned to an Interface class. Each interface type is
    implemented as private class which implements the __str__ method."""
    class _Demo:
        def __str__(self):
            return 'For testing purposes.'

    Demo1 = _Demo()
    Demo2 = _Demo()

    class _HiLo:
        def __str__(self):
            return 'Consist of a "HI" terminal which is the positive or high-voltage output used for sourcing voltage' \
                   'or current and a "LO" terminal which serves as the negative or low-voltage reference.'

    HI_LO = _HiLo()


class InterfaceABC(ABC):
    """Implements the properties of the interface and a method which establishes a connection to the available pixels.
    A method for generating a dictionary which holds the corresponding sample layout must be implemented as well."""

    _interface_type = NotImplemented
    _sample_dimensions = NotImplemented
    _pixel_ids = NotImplemented
    _pixel_positions = NotImplemented

    @abstractmethod
    def __init__(self, pixel_dimensions: Dimensions.Shape | Dict[str, Dimensions.Shape]):
        if type(pixel_dimensions) != dict:
            pixel_dimensions = {pixel: pixel_dimensions for pixel in self.pixel_ids}
        self._pixel_dimensions = pixel_dimensions

    @property
    def name(self) -> str:
        """Name of the interface which is the name of the class."""
        return self.__class__.__name__

    @property
    def interface_type(self) -> InterfaceType:
        """Constant interface type object which has a descriptive string representation."""
        if self._interface_type is NotImplemented:
            raise NotImplementedError
        return self._interface_type

    @property
    def sample_dimensions(self) -> Dimensions.Shape:
        """The size and shape of the sample used with this interface represented by a ``Dimensions.Shape`` object."""
        if self._sample_dimensions is NotImplemented:
            raise NotImplementedError
        return self._sample_dimensions

    @property
    def pixel_ids(self) -> List[str]:
        """List of available pixels."""
        if self._pixel_ids is NotImplemented:
            raise NotImplementedError
        return self._pixel_ids

    @property
    def pixel_positions(self) -> Dict[str, Tuple[float, float]]:
        """A dictionary which contains the positions of the pixels on the sample as tuples of floats. The coordinates
        are given in mm and the origin is in the bottom-left corner."""
        if self._pixel_positions is NotImplemented:
            raise NotImplementedError
        return self._pixel_positions

    @property
    def pixel_dimensions(self) -> Dict[str, Dimensions.Shape]:
        """The size and shape of the pixels on the sample represented by a dictionary of ``Dimensions.Shape``
        objects."""
        return self._pixel_dimensions

    def select_pixel(self, pixel: str):
        """Checks if the pixel value is valid and runs the `_select_pixel` method for the actual pixel selection.

        :param pixel: The pixel value.
        :raises ValueError: If the pixel is not available on the interface.
        """
        if pixel not in self._pixel_ids:
            raise ValueError(f"Pixel {pixel} is not available!")
        self._select_pixel(pixel)

    @abstractmethod
    def _select_pixel(self, pixel: str):
        """Method to connect the interface to the specified pixel."""


class TrivialHILO(InterfaceABC):
    """This interface is the conventional, single-point connection to a sample with one positive/high-voltage terminal
    and one negative/low-voltage terminal. It can also be used if the selection of pixels is carried out manually
    (not recommended)."""
    _interface_type = InterfaceType.HI_LO
    _pixel_ids = ['0']
    _pixel_positions = {'0': (0., 0.)}
    _sample_dimensions = Dimensions.Point()

    def __init__(self, pixel_dimensions: Dimensions.Shape | Dict[str, Dimensions.Shape]):
        InterfaceABC.__init__(self, pixel_dimensions)

    def _select_pixel(self, pixel: str):
        pass


class MA8X8(InterfaceABC):
    """The implementation of the Measurement Array 8x8 interface which consist of 64 front contact pixels and a single
    back contact on an area of 25 mm x 25 mm. The interface is controlled by an Arduino Nano Every board which is
    connected through a serial COM port."""
    _interface_type = InterfaceType.HI_LO
    _pixel_ids = [str(i + 1 + 10 * (j + 1)) for j in range(8) for i in range(8)]
    _pixel_positions = {pixel: (2.7 + (int(pixel) % 10 - 1) * 2.8, 25.0 - 2.7 - (int(pixel) // 10 - 1) * 2.8)
                        for pixel in _pixel_ids}
    _sample_dimensions = Dimensions.Rectangle(25., 25.)

    def __init__(self, com_port: str, pixel_dimensions: Dimensions.Shape | Dict[str, Dimensions.Shape]):
        """Initializes the Measurement Array 8x8 interface by defining the serial connection to the Arduino board.

        :param com_port: The COM port of the Arduino Nano Every board.
        :param pixel_dimensions: The size and shape of the pixel_ids on the sample.
        """
        InterfaceABC.__init__(self, pixel_dimensions)
        self.arduino = SerialCommunication(com_port, baudrate=9600, timeout=2)

    def select_pixel(self, pixel: str):
        """Select a pixel on the Measurement Array 8x8 by sending a signal to the Arduino board.

        :param pixel: The pixel value to activate.
        :raises ValueError: If the pixel is not available on the interface.
        :raises RuntimeError: If the pixel selection fails.
        """
        InterfaceABC.select_pixel(self, pixel)

    def _select_pixel(self, pixel: str):
        with self.arduino as serial:
            response = serial.send_and_receive_data(str(self.pixel_ids.index(pixel) + 1))
            if response != '1':
                raise RuntimeError(f"Failed to activate pixel {pixel}")
            time.sleep(0.5)
