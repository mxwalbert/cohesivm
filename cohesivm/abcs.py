"""Module containing the abstract base classes."""
import multiprocessing as mp
from enum import Enum
from abc import ABC, abstractmethod
from queue import Queue
from typing import List, Dict, Any, Tuple
import numpy as np
from . import InterfaceType
from .database import Database


class CompatibilityError(Exception):
    pass


class StateError(Exception):
    pass


class ExperimentState(Enum):
    INITIAL = 1
    READY = 2
    RUNNING = 3
    FINISHED = 4
    ABORTED = 5


class ExperimentABC(ABC):
    """Main class which packages all parts that must be defined for running an experiment using the Statemachine design
    pattern. A child class should implement a compatibility check, the data management and worker handling."""

    _state = None
    _database = None
    _device = None
    _measurement = None
    _interface = None
    _sample_id = None
    _selected_pixels = None
    _data_stream = None
    _dataset = None
    _process = None

    @property
    def state(self) -> ExperimentState:
        """The current state of the experiment stored in a ``multiprocessing.Value``."""
        return ExperimentState(self._state.value)

    @state.setter
    def state(self, new_value: ExperimentState):
        self._state.value = new_value.value

    @property
    def database(self) -> Database:
        """An instance of the ``Database`` class."""
        return self._database

    @property
    def device(self) -> 'DeviceABC':
        """An instance of a class which inherits the ``DeviceABC``."""
        return self._device

    @property
    def measurement(self) -> 'MeasurementABC':
        """An instance of a class which inherits the ``MeasurementABC``."""
        return self._measurement

    @property
    def interface(self) -> 'InterfaceABC':
        """An instance of a class which inherits the ``InterfaceABC``."""
        return self._interface

    @property
    def sample_id(self) -> str:
        """The string identifier of the sample which should be unique in the database."""
        return self._sample_id

    @property
    def selected_pixels(self) -> List[str]:
        """List of selected pixel ids which should be measured. The default are all available pixels on the
        `interface`."""
        return self._selected_pixels

    @property
    def data_stream(self) -> Queue:
        """A queue-like object where the measurement results can be sent to, e.g., for real-time plotting of the
        measurement."""
        return self._data_stream

    @property
    def dataset(self) -> str:
        """The stem of the dataset path in the database which should be obtained from the dataset initialization."""
        return self._dataset

    @property
    def process(self) -> mp.Process:
        """The process which runs the measurements in the background."""
        return self._process

    @abstractmethod
    def __check_compatibility(self):
        """This method should be run during initialization of the object and check if the `measurement`, `device` and
        `interface` are compatible."""
        pass

    @abstractmethod
    def setup(self):
        """Generates the ``Metadata`` object and initializes the dataset in the database. Populates the `dataset`
        property. Changes the `state` to ``ExperimentState.READY``."""
        pass

    @abstractmethod
    def start(self):
        """Starts the experiment which is executed by a separate worker process. Changes the `state` to
        ``ExperimentState.RUNNING``."""
        pass

    @abstractmethod
    def __execute(self):
        """Runs the actual measurements in a separate ``multiprocessing.Process`` and generates/updates the `progress`
        property which is a ``multiprocessing.Array``. Changes the `state` to ``ExperimentState.FINISHED`` after
        completion."""

    @abstractmethod
    def abort(self):
        """Aborting the experiment by terminating the ``multiprocessing.Process``. Changes the `state` to
        ``ExperimentState.ABORTED``."""
        pass


class InterfaceABC(ABC):
    """Implements the properties of the interface and a method which establishes a connection to the available pixels.
    A method for generating a dictionary which holds the corresponding sample layout must be implemented as well."""

    _interface_type = None
    _pixels = None
    _sample_layout = None

    @property
    def interface_type(self) -> InterfaceType:
        """Constant interface type object which has a descriptive string representation."""
        return self._interface_type

    @property
    def pixels(self) -> List[str]:
        """List of available pixels."""
        return self._pixels

    @property
    def sample_layout(self) -> Dict[str, np.ndarray]:
        """A dictionary which contains the pixel ids as string values and their location on the sample as Numpy
        arrays."""
        return self._sample_layout

    @abstractmethod
    def select_pixel(self, pixel: str):
        """Method to connect the interface to the specified pixel."""
        pass


class MeasurementABC(ABC):
    """The implementation of a child class should hold the properties which are needed for correct database integration
    and interface/device compatibility. A method for running the measurement procedure must be implemented as well."""

    _name = None
    _interface_type = None
    _required_channels = None
    _settings = None

    @property
    def name(self) -> str:
        """Name of the measurement procedure for how it will appear in the database."""
        return self._name

    @property
    def interface_type(self) -> InterfaceType:
        """Constant interface type object which has a descriptive string representation."""
        return self._interface_type

    @property
    def required_channels(self) -> List[Tuple]:
        """A list of required channels given as tuple of possible channel classes which will be checked against the
        `channels` list of the ``Device``."""
        return self._required_channels

    @property
    def settings(self) -> Dict[str, np.ndarray]:
        """A dictionary which holds the settings of the measurement and is generated at object initialization. Each
        setting should have unique initials, e.g., ``start_voltage`` <=> 'sv'."""
        return self._settings

    @abstractmethod
    def run(self, device: 'DeviceABC', data_stream: Queue):
        """Actual implementation of the measurement procedure which returns the measurement results and optionally sends
        them to the ``data_stream``."""
        pass


class DeviceABC(ABC):
    """Implements the connection and the channels of a measurement device."""

    _connection_args = None
    _connection = None
    _channels = None

    @property
    def connection_args(self) -> Dict[str, Any]:
        """A dictionary of connection arguments which are used in the ``connect`` method."""
        return self._connection_args

    @property
    def channels(self) -> List[Any]:
        """A list of ``Channel`` instances."""
        return self._channels

    @abstractmethod
    def connect(self):
        """This method must be implemented as a context manager which stores the resource in the property
        `__connection`."""
        pass
