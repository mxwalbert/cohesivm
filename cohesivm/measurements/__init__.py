"""Module contains the implemented measurements which inherit the Measurement Abstract Base Class ."""
from __future__ import annotations
import numpy as np
import multiprocessing as mp
from abc import ABC, abstractmethod
from typing import List, Tuple, Type
from ..database import database_dict_type
from ..interfaces import InterfaceType
from ..devices import DeviceABC


class MeasurementABC(ABC):
    """The implementation of a child class should hold the properties which are needed for correct database integration
    and interface/device compatibility. A method for running the measurement procedure must be implemented as well."""

    _interface_type = NotImplemented
    _required_channels = NotImplemented
    _output_type = NotImplemented

    def __init__(self, settings: database_dict_type, output_shape: tuple):
        if len(settings) == 0:
            settings = {'default': 0}
        self._settings = settings
        self._output_shape = output_shape

    @property
    def name(self) -> str:
        """Name of the measurement procedure which is the name of the class."""
        return self.__class__.__name__

    @property
    def interface_type(self) -> InterfaceType:
        """Constant interface type object which has a descriptive string representation."""
        if self._interface_type is NotImplemented:
            raise NotImplementedError
        return self._interface_type

    @property
    def required_channels(self) -> List[Tuple]:
        """A list of required channels given as tuple of possible channel classes which will be checked against the
        `channels` list of the ``Device``."""
        if self._required_channels is NotImplemented:
            raise NotImplementedError
        return self._required_channels

    @property
    def output_type(self) -> np.dtype | List[Tuple[str, Type]]:
        """The Numpy data type of the measurement result."""
        if self._output_type is NotImplemented:
            raise NotImplementedError
        return self._output_type

    @property
    def output_shape(self) -> np.shape:
        """The Numpy shape of the measurement result."""
        if self._output_shape is NotImplemented:
            raise NotImplementedError
        return self._output_shape

    @property
    def settings(self) -> database_dict_type:
        """A dictionary which holds the settings of the measurement and is generated at object initialization."""
        return self._settings

    @abstractmethod
    def run(self, device: DeviceABC, data_stream: mp.Queue):
        """Actual implementation of the measurement procedure which returns the measurement results and optionally sends
        them to the ``data_stream``."""
        pass
