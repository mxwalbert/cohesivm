"""This Module contains the :class:`Device` Abstract Base Class and the implemented devices (standalone modules) which
follow this ABC. The main responsibilities are to establish the communication with the physical device and to contain
the measurement channels (:class:`~cohesivm.channels.Channel`). For simplicity, the source code of the channel
implementations may also be put into the modules of the devices."""
from __future__ import annotations
import contextlib
from abc import ABC, abstractmethod
from typing import List, Any, Generator
from cohesivm.channels import TChannel
from cohesivm.database import DatabaseDict


class Device(ABC):
    """Implements the connection and the channels of a measurement device.

    :param channels: A list of implemented :class:`~cohesivm.channels.Channel` instances.
    """

    def __init__(self, channels: List[TChannel]) -> None:
        self._channels = channels

    @property
    def name(self) -> str:
        """Name of the device which is the name of the class."""
        return self.__class__.__name__

    @property
    def channels(self) -> List[TChannel]:
        """A list of implemented :class:`~cohesivm.channels.Channel` instances."""
        return self._channels

    @property
    def channels_names(self) -> List[str]:
        """A list of class names of the channels."""
        return [channel.__class__.__name__ for channel in self._channels]

    @property
    def channels_settings(self) -> List[DatabaseDict]:
        """A list of settings dictionaries of the channels."""
        return [channel.settings for channel in self._channels]

    @abstractmethod
    def _establish_connection(self) -> Any:
        """Opens the device connection and returns the resource.

        :meta public:
        """

    @contextlib.contextmanager
    def connect(self) -> Generator[None, None, None]:
        """Establishes the connection to the device and enables its channels. Must be used in form of a resource such
        that the channels are disabled and the connection is closed safely.

        Example
        -------

        .. code-block:: python

            with device.connect():
                device.channel[0].measure()
        """
        connection = self._establish_connection()
        for channel in self._channels:
            channel._connection = connection
            channel.enable()
            channel.apply_settings()
        try:
            yield
        finally:
            for channel in self._channels:
                channel.disable()
                channel._connection = None
            try:
                connection.close()
            except AttributeError:
                pass


from . import ossila, agilent
