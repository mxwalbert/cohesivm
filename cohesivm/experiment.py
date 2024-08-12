"""This module contains the :class:`Experiment` class which is responsible for packaging the multiple components of an
experiment together. Further, it handles the worker process which executes the measurements in the background."""
from __future__ import annotations
import time
import multiprocessing as mp
from enum import Enum
from typing import List, Union
from cohesivm import CompatibilityError
from cohesivm.interfaces import Interface
from cohesivm.measurements import Measurement
from cohesivm.devices import Device
from cohesivm.database import Database, Metadata
from cohesivm.data_stream import FakeQueue


class ExperimentState(Enum):
    """An Enumeration of the different states an :class:`Experiment` can be in."""
    INITIAL = 1
    READY = 2
    RUNNING = 3
    FINISHED = 4
    ABORTED = 5


class StateError(Exception):
    """Raised by an :class:`Experiment` if a method is not valid in the current :class:`ExperimentState`."""


class Experiment:
    """A statemachine which packages the components of an experiment (:class:`~cohesivm.devices.Device`,
    :class:`~cohesivm.interfaces.Interface` and :class:`~cohesivm.measurements.Measurement`), checks their
    compatibility, executes the measurements in a separate process and keeps track of the progress. Creates during
    initialization a new :obj:`multiprocessing.Value` which holds the current state of the experiment.

    :param database: The database where the data is stored.
    :param device: The measurement device which is used to run the experiment.
    :param interface: The contacting hardware which establishes the electronic connection on the sample.
    :param measurement: The routine which is run for each contact on the interface.
    :param sample_id: The string identifier of the sample which should be unique in the database.
    :param selected_contacts: List of selected contact ids which should be measured. The default are all available
        contacts on the :attr:`interface`.
    :param data_stream: A :class:`multiprocessing.Queue`-like object where the measurement results can be sent to,
        e.g., for real-time plotting of the measurement.
    :raises ~cohesivm.CompatibilityError: If the provided components are not compatible with each other.
    """

    def __init__(self, database: Database, device: Device, measurement: Measurement, interface: Interface,
                 sample_id: str, selected_contacts: List[str] = None, data_stream: mp.Queue = None) -> None:
        state = mp.Value('i', ExperimentState.INITIAL.value)
        if selected_contacts is None:
            selected_contacts = interface.contact_ids
        if data_stream is None:
            data_stream = FakeQueue()
        self.__state = state
        self._database = database
        self._device = device
        self._measurement = measurement
        self._interface = interface
        self._sample_id = sample_id
        self._selected_contacts = selected_contacts
        self._current_contact_idx = None
        self._data_stream = data_stream
        self._dataset = None
        self._process = None
        self._check_compatibility()
        self._current_contact_idx = mp.Value('i', -2)

    @property
    def state(self) -> ExperimentState:
        """The current state of the experiment stored in a :obj:`multiprocessing.Value`."""
        return ExperimentState(self._state.value)

    @property
    def _state(self) -> mp.Value:
        return self.__state

    @_state.setter
    def _state(self, new_value: ExperimentState) -> None:
        self._state.value = new_value.value

    @property
    def database(self) -> Database:
        """The database where the data is stored."""
        return self._database

    @property
    def device(self) -> Device:
        """The measurement device which is used to run the experiment."""
        return self._device

    @property
    def measurement(self) -> Measurement:
        """The routine which is run for each contact on the interface."""
        return self._measurement

    @property
    def interface(self) -> Interface:
        """The contacting hardware which establishes the electronic connection on the sample."""
        return self._interface

    @property
    def sample_id(self) -> str:
        """The string identifier of the sample which should be unique in the database."""
        return self._sample_id

    @property
    def selected_contacts(self) -> List[str]:
        """List of selected contact ids which should be measured. The default is all available contacts on the
        :attr:`interface`."""
        return self._selected_contacts

    @property
    def current_contact_idx(self) -> Union[int, None]:
        """List index of the currently measured contact from the :attr:`selected_contacts`. Stored as
        :obj:`multiprocessing.Value` while the :attr:`state` is :attr:`~ExperimentState.RUNNING`."""
        return None if self._current_contact_idx is None else self._current_contact_idx.value

    @property
    def data_stream(self) -> mp.Queue:
        """A :class:`multiprocessing.Queue`-like object where the measurement results can be sent to,
        e.g., for real-time plotting of the measurement."""
        return self._data_stream

    @data_stream.setter
    def data_stream(self, new_value: mp.Queue) -> None:
        """A :class:`multiprocessing.Queue`-like object where the measurement results can be sent to, e.g., for
        real-time plotting of the measurement."""
        self._data_stream = new_value

    @property
    def dataset(self) -> str:
        """The dataset path in the database which should be obtained from the dataset initialization."""
        return self._dataset

    @property
    def process(self) -> mp.Process:
        """The process which runs the measurements in the background."""
        return self._process

    def _check_contact_compatibility(self, contact_id: str) -> None:
        if contact_id not in self.interface.contact_ids:
            raise CompatibilityError(f"The selected contact {contact_id} is not available on the interface!")

    def _check_compatibility(self) -> None:
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
        for contact_id in self.selected_contacts:
            self._check_contact_compatibility(contact_id)

    def preview(self, contact_id: str) -> None:
        """Starts a preview measurement on the specified contact which is executed by a separate worker process. Sends
        the data to the :attr:`data_stream` but does not store it in the database.

        Changes the :attr:`state` property to :attr:`~ExperimentState.RUNNING`. Resets the :attr:`state` to the
        previous one if completed.

        :param contact_id: The id of the contact for which the preview measurement should be run.
        :raises StateError: If the :attr:`state` is :attr:`~ExperimentState.RUNNING`.
        """
        state_messages = {
            ExperimentState.RUNNING: "The experiment is already running!"
        }
        if self.state is ExperimentState.RUNNING:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")
        self._check_contact_compatibility(contact_id)
        previous_state = self.state
        self._current_contact_idx.value = -2
        self._state = ExperimentState.RUNNING
        self._process = mp.Process(target=self._execute_preview,
                                   kwargs={'contact_id': contact_id, 'previous_state': previous_state})
        self.process.start()

    def _execute_preview(self, contact_id: str, previous_state: ExperimentState) -> None:
        if self.state is not ExperimentState.RUNNING:
            raise StateError(f"The preview must be started before it can be executed! Current state: {self.state}.")
        self.interface.select_contact(contact_id)
        self.measurement.run(self.device, self.data_stream)
        if previous_state is ExperimentState.READY:
            self._current_contact_idx.value = -1
            self._state = ExperimentState.READY
        else:
            self._current_contact_idx.value = -2
            self._state = ExperimentState.INITIAL

    def setup(self) -> None:
        """Generates the :class:`~cohesivm.database.Metadata` object and initializes the dataset in the database.
        Populates the :attr:`dataset`.

        Changes the :attr:`state` to :attr:`~ExperimentState.READY`.

        :raises StateError: If the :attr:`state` is none of :attr:`~ExperimentState.INITIAL`,
            :attr:`~ExperimentState.FINISHED` or :attr:`~ExperimentState.ABORTED`.
        """
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
            interface_dimensions=str(self.interface.interface_dimensions),
            contact_ids=self.interface.contact_ids,
            contact_positions=list(self.interface.contact_positions.values()),
            pixel_dimensions=[str(contact_dimension) for contact_dimension in self.interface.pixel_dimensions.values()]
        )
        self._current_contact_idx.value = -1
        self._dataset = self.database.initialize_dataset(metadata)
        self._state = ExperimentState.READY

    def start(self) -> None:
        """Starts the experiment which is executed by a separate worker process. Selects the contact on the interface,
        generates/updates the :attr:`current_contact_idx` which is a :obj:`multiprocessing.Value`, runs the measurement
        and stores the result in the database.

        Changes the :attr:`state` to :attr:`~ExperimentState.RUNNING` while running. Changes the :attr:`state` to
        :attr:`~ExperimentState.FINISHED` after completion.

        :raises StateError: If the :attr:`state` is not :attr:`~ExperimentState.READY`.
        """
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

    def _execute(self) -> None:
        state_messages = {
            ExperimentState.INITIAL: "The experiment must be setup before it can be stared!",
            ExperimentState.READY: "The experiment must be started before it can be executed!",
            ExperimentState.FINISHED: "The experiment is already finished!",
            ExperimentState.ABORTED: "The experiment was aborted!",
        }
        if self.state is not ExperimentState.RUNNING:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")

        for contact_id in self.selected_contacts:
            self._current_contact_idx.value = self.current_contact_idx + 1
            self.interface.select_contact(contact_id)
            time.sleep(0.5)
            data = self.measurement.run(self.device, self.data_stream)
            self.database.save_data(data, self.dataset, contact_id)
        self._current_contact_idx.value = self.current_contact_idx + 1
        self._state = ExperimentState.FINISHED

    def quickstart(self) -> None:
        """Executes the :meth:`setup` and :meth:`start` to directly run the experiment.

        :raises StateError: If the :attr:`state` is none of :attr:`~ExperimentState.INITIAL`,
            :attr:`~ExperimentState.FINISHED` or :attr:`~ExperimentState.ABORTED`.
        """
        self.setup()
        self.start()

    def abort(self) -> None:
        """If the experiment is not running but setup, the dataset is deleted from the database and the :attr:`state`
        is changed to :attr:`~ExperimentState.INITIAL`. Otherwise, terminates the :class:`multiprocessing.Process`
        and changes the :attr:`state` to :attr:`~ExperimentState.ABORTED`.

        :raises StateError: If the :attr:`state` is neither of :attr:`~ExperimentState.READY` nor
            :attr:`~ExperimentState.RUNNING`.
        """
        state_messages = {
            ExperimentState.INITIAL: "The experiment is not setup or running!",
            ExperimentState.FINISHED: "The experiment is already finished!",
            ExperimentState.ABORTED: "The experiment is already aborted!",
        }
        if self.state not in [ExperimentState.READY, ExperimentState.RUNNING]:
            raise StateError(f"{state_messages[self.state]} Current state: {self.state}.")
        if self.state == ExperimentState.READY:
            self._current_contact_idx.value = -2
            if self._dataset is not None:
                self.database.delete_dataset(self._dataset)
                self._dataset = None
            self._state = ExperimentState.INITIAL
            return
        self._state = ExperimentState.ABORTED
        self.process.terminate()
