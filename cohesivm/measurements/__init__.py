"""This Module contains the :class:`Measurement` Abstract Base Class and the implemented measurements
(standalone modules) which follow this ABC. The main responsibility is to perform the measurement procedure by calling
the corresponding :class:`~cohesivm.channels.Channel` methods and to return the acquired data. Therefore, the
:class:`Measurement` issues a list of channels which are required to run the measurement procedure."""
from __future__ import annotations
import numpy as np
import multiprocessing as mp
from abc import ABC, abstractmethod
from typing import List, Tuple, Type
from cohesivm.database import DatabaseDict
from cohesivm.interfaces import InterfaceType
from cohesivm.devices import Device


class Measurement(ABC):
    """The implementation of a child class should hold the properties which are needed for correct database integration
    and interface/device compatibility. A method for running the measurement procedure must be implemented as well.

    :param settings: A dictionary which holds the settings of the measurement which may be provided by the child class.
    :param output_shape: The expected Numpy shape of the measurement result.

    **Required properties**

    :_interface_type: The :class:`~cohesivm.interfaces.InterfaceType` which needs to correspond to the
        :class:`~cohesivm.interfaces.Interface`.
    :_required_channels: A list of :class:`~cohesivm.channels.Channel` classes (not objects) which are required to
        run the measurement procedure.
    :_output_type: The expected data type of the measurement result.
    """

    _interface_type = NotImplemented
    _required_channels = NotImplemented
    _output_type = NotImplemented

    def __init__(self, settings: DatabaseDict, output_shape: tuple) -> None:
        if len(settings) == 0:
            settings = {'default': 0}
        self._settings = dict(sorted(settings.items()))
        self._output_shape = output_shape

    @property
    def name(self) -> str:
        """The Name of the measurement procedure which is the name of the class."""
        return self.__class__.__name__

    @property
    def interface_type(self) -> InterfaceType:
        """The type of interface which is used to check the compatibility with the
        :class:`~cohesivm.interfaces.Interface`."""
        if self._interface_type is NotImplemented:
            raise NotImplementedError
        return self._interface_type

    @property
    def required_channels(self) -> List[Tuple]:
        """A list of required channels given as tuple of possible channel classes which will be checked against the
        :attr:`~cohesivm.devices.Device.channels` of the :class:`~cohesivm.devices.Device`."""
        if self._required_channels is NotImplemented:
            raise NotImplementedError
        return self._required_channels

    @property
    def output_type(self) -> List[Tuple[str, Type]]:
        """The expected data type of the measurement result."""
        if self._output_type is NotImplemented:
            raise NotImplementedError
        return self._output_type

    @property
    def output_shape(self) -> np.ndarray.shape:
        """The expected shape of the measurement result."""
        if self._output_shape is NotImplemented:
            raise NotImplementedError
        return self._output_shape

    @property
    def settings(self) -> DatabaseDict:
        """A dictionary which holds the settings of the measurement and is generated at object initialization."""
        return self._settings

    @abstractmethod
    def run(self, device: Device, data_stream: mp.Queue) -> np.ndarray:
        """Actual implementation of the measurement procedure which returns the measurement results and optionally
        sends them to the ``data_stream``.

        :param device: An instance of a class which inherits the :class:`~cohesivm.devices.Device` and complies with
            the :attr:`~cohesivm.measurements.Measurement.required_channels`.
        :param data_stream: A queue-like object where the measurement results can be sent to, e.g., for real-time
            plotting of the measurement.
        :returns: A Numpy structured array with tuples of datapoints according to the
            :attr:`~cohesivm.measurements.Measurement.output_shape`.
        """
        pass


from . import iv, cv
