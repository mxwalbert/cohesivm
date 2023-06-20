"""Implements the Ossila X200 Source Measure Unit which relies on the xtralien module:
https://pypi.org/project/xtralien/"""
from __future__ import annotations
import importlib
try:
    importlib.import_module('xtralien')
except ImportError:
    raise ImportError("Package 'xtralien' is not installed.")
import xtralien
import contextlib
import time
from enum import Enum
from decimal import Decimal
import numpy as np
from typing import List, Any, Dict
from ..abcs import DeviceABC
from ..channels import SourceMeasureUnitChannel, VoltmeterChannel


class OssilaX200ChannelState(Enum):
    DISABLED = 1
    ENABLED = 2


class OssilaX200Channel:
    """Implements the properties and methods which all Ossila X200 channels have in common."""

    def __init__(self, identifier, settings):
        self._identifier = identifier
        self._settings = settings
        self._connection = None
        self._state = OssilaX200ChannelState.DISABLED

    @property
    def identifier(self) -> str:
        """String identifier of the channel."""
        return self._identifier

    @property
    def settings(self) -> Dict[str, Any]:
        """Dictionary of channel settings which are keyed by the parameter name of the `__init__` method without the
        leading 's_'."""
        return self._settings

    @property
    def connection(self) -> xtralien.Device | None:
        """Holds the device reference while a connection is established through using the `Device.connect`
        contextmanager."""
        return self._connection

    def _set_property(self, name: str, value: Any):
        if self._connection is None:
            raise RuntimeError('A device connection must be established in order to communicate with the channel!')
        method = getattr(self._connection[self.identifier].set, name)
        method(value, response=0)
        time.sleep(0.01)

    def _get_property(self, name: str) -> Any:
        if self._connection is None:
            raise RuntimeError('A device connection must be established in order to communicate with the channel!')
        if self._state is OssilaX200ChannelState.ENABLED:
            self.disable()
        method = getattr(self._connection[self.identifier].get, name)
        return method()

    def _check_settings(self):
        raise NotImplementedError

    def apply_settings(self):
        """Checks and applies the settings."""
        self._check_settings()
        for name, value in self._settings.items():
            self._set_property(name, value)

    def change_setting(self, setting, value):
        """Modifies the `__settings` property and overwrites the settings on the device.

        :param setting: String key of the setting in the `__settings' property. This is the parameter name in the
            __init__ method without the leading 's_', e.g., 'osr' for the parameter `s_osr`.
        :param value: New value of the setting.
        :raises KeyError: If `setting` is not a valid setting identifier string.
        """
        if setting not in self._settings.keys():
            raise KeyError(f"'{setting}' is not a valid setting identifier string.")
        self._settings[setting] = value
        self.apply_settings()

    def enable(self):
        """Enables the channel."""
        if self._state is OssilaX200ChannelState.ENABLED:
            return
        self._set_property('enabled', True)
        self._state = OssilaX200ChannelState.ENABLED

    def disable(self):
        """Disables the channel."""
        if self._state is OssilaX200ChannelState.DISABLED:
            return
        self._set_property('enabled', False)
        self._state = OssilaX200ChannelState.DISABLED


class OssilaX200SMUChannel(SourceMeasureUnitChannel, OssilaX200Channel):
    """A source measure unit (SMU) channel of the Ossila X200 device which can source a voltage and measure the voltage
    and current. For more details and specifications see the user manual of the Ossila X200."""

    current_ranges = (200e-3, 20e-3, 2e-3, 200e-6, 20e-6, 0.)

    def __init__(self, identifier: str = 'smu1', auto_range: bool = False, s_delay: int = 1000, s_filter: int = 1,
                 s_osr: int = 5, s_range: int = 1):
        """Initializes one of the two source measure unit (SMU) channels of the Ossila X200 device.

        :param identifier: String identifier of the SMU channel: 'smu1' or 'smu2'.
        :param auto_range: If the flag is set True, the `source_and_measure` method will automatically find the ideal
            current range from the available ranges (see `s_range`).
        :param s_delay: Setting for the voltage settling time in µs.
        :param s_filter: Setting for the number of repeated measurements which get averaged.
        :param s_osr: Setting for the sampling rate which is 64*2**n samples/datapoint with n in [0,9] or [10,19] for
            1x or 2x mode of the analog-to-digital converter. E.g., the default setting of 5 corresponds to a sampling
            rate of 2048 samples/datapoint with an RMS noise of 750 nV and a measurement rate of 36 datapoints/s.
        :param s_range: Setting for the current measurement range which takes a value in [1,5] and allows maximum
            absolute currents of 200 mA, 20 mA, 2 mA, 200 µA, and 20 µA, respectively.
        :raises TypeError: If the type of setting values is incorrect.
        :raises ValueError: If the identifier is not available or setting values are out of bounds.
        """
        if identifier not in ['smu1', 'smu2']:
            raise ValueError("Identifier of the SMU channel must be 'smu1' or 'smu2'!")
        self._identifier = identifier
        self._auto_range = auto_range
        self._settings = {
            'delay': Decimal(s_delay),
            'filter': s_filter,
            'osr': s_osr,
            'range': s_range
        }
        self._check_settings()
        OssilaX200Channel.__init__(self, self._identifier, self._settings)

    @property
    def auto_range(self) -> bool:
        return self._auto_range

    @auto_range.setter
    def auto_range(self, new_value: bool):
        """Enable or disable the use of the automatic current range selection."""
        self._auto_range = new_value

    def _check_settings(self):
        if type(self._settings['delay']) is not Decimal:
            raise TypeError('Setting `delay` must be Decimal!')
        if self._settings['delay'] < 0:
            raise ValueError('Setting `delay` must not be negative!')
        if type(self._settings['filter']) is not int:
            raise TypeError('Setting `filter` must be int!')
        if self._settings['filter'] < 0:
            raise ValueError('Setting `filter` must not be negative!')
        if self._settings['osr'] not in range(20):
            raise ValueError('Setting `osr` must be in [0,19]!')
        if self._settings['range'] not in range(1, 6):
            raise ValueError('Setting `range` must be in [1,5]!')

    def disable(self):
        """Sets the source voltage to 0 V and disables the channel."""
        self._set_property('voltage', Decimal(0))
        OssilaX200Channel.disable(self)

    def measure_voltage(self):
        self.enable()
        return self._connection[self.identifier].measurev()[0]

    def measure_current(self):
        self.enable()
        return self._connection[self.identifier].measurei()[0]

    def source_voltage(self, voltage: float):
        """Sets the output voltage to the defined value.

        :param voltage: Output voltage of the power source in V. Must be in [-10, 10].
        :raises ValueError: If voltage is out of bounds.
        """
        self.enable()
        if abs(voltage) > 10:
            raise ValueError('Absolute voltage must not exceed 10 V!')
        self._set_property('voltage', Decimal(voltage))

    def _find_range(self, voltage: float):
        self._set_property('range', 1)
        self.source_voltage(voltage)
        for i in range(len(self.current_ranges)):
            if abs(self.measure_current()) < self.current_ranges[i+1]:
                self._set_property('range', i + 2)
            else:
                break

    def source_and_measure(self, voltage: float) -> np.ndarray[float, float]:
        """Sets the output voltage to the defined value, then measures the actual voltage and current.

        :param voltage: Output voltage of the power source in V. Must be in [-10, 10].
        :returns: Measurement result as tuple: (voltage (V), current (A)).
        :raises ValueError: If voltage is out of bounds.
        """
        self.enable()
        if abs(voltage) > 10:
            raise ValueError('Absolute voltage must not exceed 10 V!')
        if self._auto_range:
            self._find_range(voltage)
        return self._connection[self.identifier].oneshot(Decimal(voltage))[0]


class OssilaX200VsenseChannel(VoltmeterChannel, OssilaX200Channel):
    """A voltmeter channel (Vsense) of the Ossila X200 device which can measure the voltage with high precision. For
    more details and specifications see the user manual of the Ossila X200."""

    def __init__(self, identifier: str = 'vsense1', s_osr: int = 5):
        """Initializes one of the two voltmeter channels (Vsense) of the Ossila X200 device.

        :param identifier: String identifier of the SMU channel: 'vsense1' or 'vsense2'.
        :param s_osr: Setting for the sampling rate which is 64*2**n samples/datapoint with n in [0,9] or [10,19] for
            1x or 2x mode of the analog-to-digital converter. E.g., the default setting of 5 corresponds to a sampling
            rate of 2048 samples/datapoint with an RMS noise of 750 nV and a measurement rate of 55 datapoints/s.
        :raises ValueError: If the identifier or the setting value is not available.
        """
        if identifier not in ['vsense1', 'vsense2']:
            raise ValueError("Identifier of the voltmeter channel must be 'vsense1' or 'vsense2'!")
        self._identifier = identifier
        self._settings = {
            'osr': s_osr
        }
        self._check_settings()
        OssilaX200Channel.__init__(self, self._identifier, self._settings)

    def _check_settings(self):
        if self._settings['osr'] not in range(20):
            raise ValueError('Setting `osr` must be in [0,19]!')

    def measure_voltage(self):
        self.enable()
        return self._connection[self.identifier].measure()[0]


class OssilaX200(DeviceABC):
    """Implements the Ossila X200 Source Measure Unit as a Device class which is a container for the channels and the
    device connection."""

    def __init__(self, channels: List[OssilaX200SMUChannel | OssilaX200VsenseChannel] = None,
                 address: str = '', port: int = 0, serial_timeout: float = 0.1):
        """Initializes the Ossila X200 Source Measure Unit.

        :param channels: List of channels which are subclasses of the OssilaX200Channel class. A maximum of 4 channels,
            i.e., 2xSMU and 2xVsense, are available. Duplicates are not allowed.
        :param address: COM (USB) or IP (Ethernet) address of the Ossila X200.
        :param port: Must be defined for connections over ethernet.
        :param serial_timeout: Timeout for the serial connection over USB in s.
        :raises TypeError: If a channel is not an OssilaX200Channel. If connection arguments `port` and `serial_timeout`
            cannot be cast to their required type.
        :raises ValueError: If too many channels or duplicate channels are provided.
        """
        if channels is None:
            channels = [OssilaX200SMUChannel()]
        if len(channels) > 4:
            raise ValueError('Number of channels must not exceed 4!')
        channel_identifiers = set()
        for channel in channels:
            if not isinstance(channel, OssilaX200Channel):
                raise TypeError(f'Channel {channel} is not an OssilaX200Channel!')
            channel_identifiers.add(channel.identifier)
        if len(channels) != len(channel_identifiers):
            raise ValueError('Duplicate channels are not allowed!')
        try:
            port = int(port)
        except ValueError:
            raise TypeError('Connection argument `port` must be int. Type casting failed.')
        try:
            serial_timeout = float(serial_timeout)
        except ValueError:
            raise TypeError('Connection argument `serial_timeout` must be float. Type casting failed.')
        connection_args = {'addr': address, 'port': port, 'serial_timeout': serial_timeout}
        DeviceABC.__init__(self, channels, connection_args)

    @property
    def channels(self) -> List[OssilaX200SMUChannel | OssilaX200VsenseChannel]:
        return self._channels

    @contextlib.contextmanager
    def connect(self):
        """Establishes the connection to the device and enables its channels. Must be used in form of a resource such
        that the channels are disabled and the connection is closed safely.

        Usage example:

        >>> device = OssilaX200(address='COM1')
        >>> with device.connect():
        >>>     # do something
        """
        connection = xtralien.Device(**self._connection_args)
        for channel in self._channels:
            channel._connection = connection
            channel.apply_settings()
        try:
            yield
        finally:
            for channel in self._channels:
                channel.disable()
                channel._connection = None
            connection.close()
