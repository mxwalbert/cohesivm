"""Module contains the implemented devices which inherit the Device Abstract Base Class and consist of device channels
which implement the measurement methods."""
from __future__ import annotations
import contextlib
from abc import ABC, abstractmethod
from typing import List, Any
from ..channels import ChannelABC, TChannelABC
from ..database import database_dict_type


def requires_connection(method):
    def wrapper(self, *args, **kwargs):
        if self.connection is None:
            raise RuntimeError('A device connection must be established in order to communicate with the channel!')
        result = method(self, *args, **kwargs)
        return result
    return wrapper


class DeviceABC(ABC):
    """Implements the connection and the channels of a measurement device."""

    def __init__(self, channels: List[TChannelABC]):
        self._channels = channels

    @property
    def name(self) -> str:
        """Name of the device which is the name of the class."""
        return self.__class__.__name__

    @property
    def channels(self) -> List[ChannelABC]:
        """A list of ``Channel`` instances."""
        return self._channels

    @property
    def channels_names(self) -> List[str]:
        """List of class names of the channels."""
        return [channel.__class__.__name__ for channel in self._channels]

    @property
    def channels_settings(self) -> List[database_dict_type]:
        """List of settings dictionaries of the channels."""
        return [channel.settings for channel in self._channels]

    @abstractmethod
    def _establish_connection(self) -> Any:
        """Opens the device connection and returns the resource."""

    @contextlib.contextmanager
    def connect(self):
        """Establishes the connection to the device and enables its channels. Must be used in form of a resource such
        that the channels are disabled and the connection is closed safely."""
        connection = self._establish_connection()
        for channel in self._channels:
            channel._connection = connection
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
