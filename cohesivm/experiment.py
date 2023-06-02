"""Module containing the Experiment class which is responsible for packaging the multiple components of an experiment
together and handling the worker process which executes the measurements in the background."""
from multiprocessing import Process
from typing import List
from queue import Queue
from .abcs import CompatibilityError, StateError, ExperimentState, ExperimentABC
from .abcs import DeviceABC, MeasurementABC, InterfaceABC
from .database import Database, Metadata
from .data_stream import FakeQueue


class Experiment(ExperimentABC):
    def __init__(self, database: Database, device: DeviceABC, measurement: MeasurementABC, interface: InterfaceABC,
                 sample_id: str, selected_pixels: List[str] = None,
                 progress_stream: Queue = None, data_stream: Queue = None):
        self._state = ExperimentState.INITIAL
        self._database = database
        self._device = device
        self._measurement = measurement
        self._interface = interface
        self._sample_id = sample_id
        if selected_pixels is None:
            selected_pixels = interface.pixels
        self._selected_pixels = selected_pixels
        if progress_stream is None:
            progress_stream = FakeQueue()
        self._progress_stream = progress_stream
        if data_stream is None:
            data_stream = FakeQueue()
        self._data_stream = data_stream
        self._check_compatibility()

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
                                         f"index {i} is a {self.device.channels[i].__name__}.")
        for pixel in self.selected_pixels:
            if pixel not in self.interface.pixels:
                raise CompatibilityError(f"The selected pixel {pixel} is not available on the interface!")

    def setup(self):
        state_messages = {
            ExperimentState.READY: "The experiment is already set up!",
            ExperimentState.RUNNING: "The experiment is already running!",
            ExperimentState.FINISHED: "The experiment is already finished!",
            ExperimentState.ABORTED: "The experiment was aborted!",
        }
        if self.state is not ExperimentState.INITIAL:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")

        metadata = Metadata(
            measurement=self.measurement.name,
            settings=self.measurement.settings,
            sample_id=self.sample_id,
            sample_layout=self.interface.sample_layout,
        )

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

        self._process = Process(target=self._execute)

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
            self.progress_stream.put(pixel)
            self.interface.select_pixel(pixel)
            data = self.measurement.run(self.device, self.data_stream)
            self.database.save(data, self.dataset, pixel)

        self._state = ExperimentState.FINISHED

    def abort(self):
        state_messages = {
            ExperimentState.INITIAL: "The experiment is not running!",
            ExperimentState.READY: "The experiment is not running!",
            ExperimentState.FINISHED: "The experiment is already finished!",
            ExperimentState.ABORTED: "The experiment is already aborted!",
        }
        if self.state is not ExperimentState.RUNNING:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")

        self.process.terminate()

        self._state = ExperimentState.ABORTED
