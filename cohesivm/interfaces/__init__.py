"""This module contains the :class:`Interface` Abstract Base Class and the implemented interfaces. The main
responsibility is to establish a physical connection to the available contacts which are defined within the class."""
from __future__ import annotations
import importlib
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Union
from cohesivm.database import Dimensions


class InterfaceType(ABC):
    """This class is used to check if the :class:`~cohesivm.measurements.Measurement` and
    :class:`~cohesivm.interfaces.Interface` are compatible."""


class HighLow(InterfaceType):
    """Consist of a "High" terminal which is the positive or high-voltage output used for sourcing voltage or current
    and a "Low" terminal which serves as the negative or low-voltage reference."""


class Interface(ABC):
    """A child class implements the properties of the interface and a method which establishes a connection to the
    available contacts.

    :param pixel_dimensions: The sizes and shapes of the pixels on the sample.

    **Required properties**

    :_interface_type: The :class:`InterfaceType` of the interface which needs to correspond to the
        :class:`~cohesivm.measurements.Measurement`.
    :_interface_dimensions: The :class:`~cohesivm.database.Dimensions.Shape` of the interface.
    :_contact_ids: A list of strings which corresponds to the identifiers of the contacts.
    :_contact_positions: A mapping of the ``_contact_ids`` and the positions of the contacts on the interface.
    """

    _interface_type = NotImplemented
    _interface_dimensions = NotImplemented
    _contact_ids = NotImplemented
    _contact_positions = NotImplemented

    @abstractmethod
    def __init__(self, pixel_dimensions: Union[Dimensions.Shape, Dict[str, Dimensions.Shape]]) -> None:
        if type(pixel_dimensions) != dict:
            pixel_dimensions = {contact_id: pixel_dimensions for contact_id in self.contact_ids}
        self._pixel_dimensions = pixel_dimensions

    @property
    def name(self) -> str:
        """Name of the interface which is the name of the class."""
        return self.__class__.__name__

    @property
    def interface_type(self) -> InterfaceType:
        """Constant interface type object."""
        if self._interface_type is NotImplemented:
            raise NotImplementedError
        return self._interface_type

    @property
    def interface_dimensions(self) -> Dimensions.Shape:
        """The size and shape of this interface."""
        if self._interface_dimensions is NotImplemented:
            raise NotImplementedError
        return self._interface_dimensions

    @property
    def contact_ids(self) -> List[str]:
        """List of available contacts."""
        if self._contact_ids is NotImplemented:
            raise NotImplementedError
        return self._contact_ids

    @property
    def contact_positions(self) -> Dict[str, Tuple[float, float]]:
        """A dictionary which contains the positions of the contacts on the interface as tuples of floats. The
        coordinates are given in mm and the origin is in the bottom-left corner."""
        if self._contact_positions is NotImplemented:
            raise NotImplementedError
        return self._contact_positions

    @property
    def pixel_dimensions(self) -> Dict[str, Dimensions.Shape]:
        """The size and shape of the pixels on the sample."""
        return self._pixel_dimensions

    def select_contact(self, contact_id: str) -> None:
        """Checks if the contact value is valid and runs the `_select_contact` method for the actual contact selection.

        :param contact_id: The ID of the contact.
        :raises ValueError: If the contact is not available on the interface.
        """
        if contact_id not in self._contact_ids:
            raise ValueError(f"Contact {contact_id} is not available!")
        self._select_contact(contact_id)

    @abstractmethod
    def _select_contact(self, contact_id: str) -> None:
        """Method to connect the interface to the specified contact.

        :param contact_id: The ID of the contact.
        :meta public:
        """


from cohesivm.interfaces.trivial import TrivialHighLow


try:
    importlib.import_module('serial')
    import serial
    serial_available = True
except ImportError:
    serial_available = False

if serial_available:
    from cohesivm.interfaces.ma8x8 import MA8X8
