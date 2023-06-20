"""Module containing the Experiment class which is responsible for packaging the multiple components of an experiment
together and handling the worker process which executes the measurements in the background."""
import multiprocessing as mp
from typing import List
from .abcs import CompatibilityError, StateError, ExperimentState, ExperimentABC
from .abcs import DeviceABC, MeasurementABC, InterfaceABC
from .database import Database, Metadata
from .data_stream import FakeQueue


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
            selected_pixels = interface.pixels
        if data_stream is None:
            data_stream = FakeQueue()
        ExperimentABC.__init__(self, state, database, device, measurement, interface, sample_id, selected_pixels,
                               data_stream)
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
                                         f"index {i} is a {self.device.channels[i].__class__.__name__}.")
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

        self._current_pixel_idx = mp.Value('i', -1)

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
            data = self.measurement.run(self.device, self.data_stream)
            self.database.save(data, self.dataset, pixel)

        self._current_pixel_idx.value = self.current_pixel_idx + 1

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

        self._state = ExperimentState.ABORTED

        self.process.terminate()
