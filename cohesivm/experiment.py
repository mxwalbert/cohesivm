"""Module containing the Experiment class which is responsible for packaging the multiple components of an experiment
together and handling the worker process which executes the measurements in the background."""
from __future__ import annotations
import time
import multiprocessing as mp
from enum import Enum
from typing import List
from abc import ABC, abstractmethod
from . import CompatibilityError
from .interfaces import InterfaceABC
from .measurements import MeasurementABC
from .devices import DeviceABC
from .database import Database, Metadata
from .data_stream import FakeQueue


class ExperimentState(Enum):
    INITIAL = 1
    READY = 2
    RUNNING = 3
    FINISHED = 4
    ABORTED = 5


class StateError(Exception):
    """Raised by an ``ExperimentABC`` class if a method is not available in the current ``ExperimentState``."""
    pass


class ExperimentABC(ABC):
    """Main class which packages all parts that must be defined for running an experiment using the Statemachine design
    pattern. A child class should implement a compatibility check, the data management and worker handling."""

    def __init__(self, state: mp.Value, database: Database, device: DeviceABC, measurement: MeasurementABC,
                 interface: InterfaceABC, sample_id: str, selected_pixels: List[str], data_stream: mp.Queue):
        self.__state = state
        self._database = database
        self._device = device
        self._measurement = measurement
        self._interface = interface
        self._sample_id = sample_id
        self._selected_pixels = selected_pixels
        self._current_pixel_idx = None
        self._data_stream = data_stream
        self._dataset = None
        self._process = None

    @property
    def state(self) -> ExperimentState:
        """The current state of the experiment stored in a ``multiprocessing.Value``."""
        return ExperimentState(self._state.value)

    @property
    def _state(self) -> mp.Value:
        return self.__state

    @_state.setter
    def _state(self, new_value: ExperimentState):
        self._state.value = new_value.value

    @property
    def database(self) -> Database:
        """An instance of the ``Database`` class."""
        return self._database

    @property
    def device(self) -> DeviceABC:
        """An instance of a class which inherits the ``DeviceABC``."""
        return self._device

    @property
    def measurement(self) -> MeasurementABC:
        """An instance of a class which inherits the ``MeasurementABC``."""
        return self._measurement

    @property
    def interface(self) -> InterfaceABC:
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
    def current_pixel_idx(self) -> int | None:
        """List index of the currently measured pixel from the `selected_pixels` property. Stored as
        ``multiprocessing.Value`` while the `state` property is ``ExperimentState.RUNNING``."""
        return None if self._current_pixel_idx is None else self._current_pixel_idx.value

    @property
    def data_stream(self) -> mp.Queue:
        """A queue-like object where the measurement results can be sent to, e.g., for real-time plotting of the
        measurement."""
        return self._data_stream

    @data_stream.setter
    def data_stream(self, new_value: mp.Queue):
        self._data_stream = new_value

    @property
    def dataset(self) -> str:
        """The dataset of the dataset path in the database which should be obtained from the dataset initialization."""
        return self._dataset

    @property
    def process(self) -> mp.Process:
        """The process which runs the measurements in the background."""
        return self._process

    @abstractmethod
    def _check_compatibility(self):
        """This method should be run during initialization of the object and check if the `measurement`, `device` and
        `interface` are compatible."""
        pass

    @abstractmethod
    def preview(self, pixel: str):
        """Starts a preview measurement on the specified pixel which is executed by a separate worker process running
        the `_execute_preview` method. Changes the `state` property to ``ExperimentState.RUNNING``."""
        pass

    @abstractmethod
    def _execute_preview(self, pixel: str, previous_state: ExperimentState):
        """Runs a preview measurement on the specified pixel and sends the data to the `data_stream` but does not store
        it in the database. Resets the state to the previous one if completed."""
        pass

    @abstractmethod
    def setup(self):
        """Generates the ``Metadata`` object and initializes the dataset in the database. Populates the `dataset`
        property. Changes the `state` property to ``ExperimentState.READY``."""
        pass

    @abstractmethod
    def start(self):
        """Starts the experiment which is executed by a separate worker process running the `_execute` method. Changes
        the `state` property to ``ExperimentState.RUNNING``."""
        pass

    @abstractmethod
    def _execute(self):
        """Selects the pixel on the interface, generates/updates the `current_pixel` property  which is a
        ``multiprocessing.Value``, runs the measurement and stores the result in the database. Changes the `state`
        property to ``ExperimentState.FINISHED`` after completion."""

    @abstractmethod
    def abort(self):
        """If the experiment is not running but setup, the dataset is deleted from the database and the `state`
        property is changed to ``ExperimentState.INITIAL``. Otherwise, terminates the ``multiprocessing.Process`` and
        changes the `state` property to ``ExperimentState.ABORTED``."""
        pass


class Experiment(ExperimentABC):
    """A statemachine which packages the components of an experiment (device, measurement and interface), checks
    their compatibility, executes the measurements in a separate process and keeps track of the progress."""

    def __init__(self, database: Database, device: DeviceABC, measurement: MeasurementABC, interface: InterfaceABC,
                 sample_id: str, selected_pixels: List[str] = None, data_stream: mp.Queue = None):
        """Initializes the experiment and creates a new multiprocessing.Value which holds the current state.

        :param database: An instance of the Database class.
        :param device: An instance of a class which inherits the DeviceABC.
        :param measurement: An instance of a class which inherits the MeasurementABC.
        :param interface: An instance of a class which inherits the InterfaceABC.
        :param sample_id: The string identifier of the sample which should be unique in the database.
        :param selected_pixels: List of selected pixel ids which should be measured. The default are all available
            pixels on the `interface`.
        :param data_stream: A queue-like object where the measurement results can be sent to, e.g., for real-time
            plotting of the measurement.
        :raises CompatibilityError: If the provided components (device, measurement and interface) are not compatible
            with each other.
        """
        state = mp.Value('i', ExperimentState.INITIAL.value)
        if selected_pixels is None:
            selected_pixels = interface.pixel_ids
        if data_stream is None:
            data_stream = FakeQueue()
        ExperimentABC.__init__(self, state, database, device, measurement, interface, sample_id, selected_pixels,
                               data_stream)
        self._check_compatibility()
        self._current_pixel_idx = mp.Value('i', -2)

    def _check_pixel_compatibility(self, pixel: str):
        if pixel not in self.interface.pixel_ids:
            raise CompatibilityError(f"The selected pixel {pixel} is not available on the interface!")

    def _check_compatibility(self):
        if self.interface.interface_type is not self.measurement.interface_type:
            raise CompatibilityError(f"The interface (InterfaceType: {self.interface.interface_type}) and the "
                                     f"measurement (InterfaceType: {self.measurement.interface_type}) are not "
                                     f"compatible with each other!")
        if len(self.measurement.required_channels) > len(self.device.channels):
            raise CompatibilityError(f"The measurement requires {len(self.measurement.required_channels)} channels but"
                                     f" the device has only {len(self.device.channels)} channels configured!")
        for i in range(len(self.measurement.required_channels)):
            if not any([isinstance(self.device.channels[i], parent_class)
                        for parent_class in self.measurement.required_channels[i]]):
                raise CompatibilityError(f"The measurement requires one of these channels on index {i}: "
                                         f"{self.measurement.required_channels[i]} but on the device the channel on "
                                         f"index {i} is a {self.device.channels[i].__class__.__name__}.")
        for pixel in self.selected_pixels:
            self._check_pixel_compatibility(pixel)

    def preview(self, pixel: str):
        state_messages = {
            ExperimentState.RUNNING: "The experiment is already running!"
        }
        if self.state is ExperimentState.RUNNING:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")
        self._check_pixel_compatibility(pixel)
        previous_state = self.state
        self._current_pixel_idx.value = -2
        self._state = ExperimentState.RUNNING
        self._process = mp.Process(target=self._execute_preview,
                                   kwargs={'pixel': pixel, 'previous_state': previous_state})
        self.process.start()

    def _execute_preview(self, pixel: str, previous_state: ExperimentState):
        if self.state is not ExperimentState.RUNNING:
            raise StateError(f"The preview must be started before it can be executed! Current state: {self.state}.")
        self.interface.select_pixel(pixel)
        self.measurement.run(self.device, self.data_stream)
        if previous_state is ExperimentState.READY:
            self._current_pixel_idx.value = -1
            self._state = ExperimentState.READY
        else:
            self._current_pixel_idx.value = -2
            self._state = ExperimentState.INITIAL

    def setup(self):
        state_messages = {
            ExperimentState.READY: "The experiment is already set up!",
            ExperimentState.RUNNING: "The experiment is already running!"
        }
        if self.state not in [ExperimentState.INITIAL, ExperimentState.FINISHED, ExperimentState.ABORTED]:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")
        metadata = Metadata(
            measurement=self.measurement.name,
            measurement_settings=self.measurement.settings,
            sample_id=self.sample_id,
            device=self.device.name,
            channels=self.device.channels_names,
            channels_settings=self.device.channels_settings,
            interface=self.interface.name,
            sample_dimensions=str(self.interface.sample_dimensions),
            pixel_ids=self.interface.pixel_ids,
            pixel_positions=list(self.interface.pixel_positions.values()),
            pixel_dimensions=[str(pixel_dimension) for pixel_dimension in self.interface.pixel_dimensions.values()]
        )
        self._current_pixel_idx.value = -1
        self._dataset = self.database.initialize_dataset(metadata)
        self._state = ExperimentState.READY

    def start(self):
        state_messages = {
            ExperimentState.INITIAL: "The experiment must be setup before it can be started!",
            ExperimentState.RUNNING: "The experiment is already running!",
            ExperimentState.FINISHED: "The experiment is already finished!",
            ExperimentState.ABORTED: "The experiment was aborted!",
        }
        if self.state is not ExperimentState.READY:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")
        self._state = ExperimentState.RUNNING
        self._process = mp.Process(target=self._execute)
        self.process.start()

    def _execute(self):
        state_messages = {
            ExperimentState.INITIAL: "The experiment must be setup before it can be stared!",
            ExperimentState.READY: "The experiment must be started before it can be executed!",
            ExperimentState.FINISHED: "The experiment is already finished!",
            ExperimentState.ABORTED: "The experiment was aborted!",
        }
        if self.state is not ExperimentState.RUNNING:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")

        for pixel in self.selected_pixels:
            self._current_pixel_idx.value = self.current_pixel_idx + 1
            self.interface.select_pixel(pixel)
            time.sleep(0.5)
            data = self.measurement.run(self.device, self.data_stream)
            self.database.save_data(data, self.dataset, pixel)
        self._current_pixel_idx.value = self.current_pixel_idx + 1
        self._state = ExperimentState.FINISHED

    def abort(self):
        state_messages = {
            ExperimentState.INITIAL: "The experiment is not setup or running!",
            ExperimentState.FINISHED: "The experiment is already finished!",
            ExperimentState.ABORTED: "The experiment is already aborted!",
        }
        if self.state not in [ExperimentState.READY, ExperimentState.RUNNING]:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")
        if self.state == ExperimentState.READY:
            self._current_pixel_idx.value = -2
            if self._dataset is not None:
                self.database.delete_dataset(self._dataset)
                self._dataset = None
            self._state = ExperimentState.INITIAL
            return
        self._state = ExperimentState.ABORTED
        self.process.terminate()
