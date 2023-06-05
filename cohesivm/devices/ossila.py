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
from decimal import Decimal
from typing import Tuple, List, Any
from ..abcs import DeviceABC
from ..channels import SourceMeasureUnitChannel, VoltmeterChannel


class OssilaX200Channel:
    """Implements the properties and methods which all Ossila X200 channels have in common."""

    _identifier = None
    __connection = None
    __settings = None

    @property
    def identifier(self) -> str:
        """String identifier of the channel."""
        return self._identifier

    def __set_property(self, name: str, value: Any):
        method = getattr(self.__connection[self.identifier].set, name)
        method(value, response=0)
        time.sleep(0.01)

    def __check_settings(self):
        raise NotImplementedError

    def __apply_settings(self):
        self.__check_settings()
        for name, value in self.__settings.items():
            self.__set_property(name, value)

    def change_setting(self, setting, value):
        """Modifies the `__settings` property and overwrites the settings on the device.

        :param setting: String key of the setting in the `__settings' property. This is the parameter name in the
            __init__ method without the leading 's_', e.g., 'osr' for the parameter `s_osr`.
        :param value: New value of the setting.
        """
        self.__settings[setting] = value
        self.__apply_settings()

    def enable(self):
        """Applies the settings and enables the channel."""
        self.__apply_settings()
        self.__set_property('enable', True)

    def disable(self):
        """Disables the channel."""
        self.__set_property('enable', False)


class OssilaX200SMUChannel(SourceMeasureUnitChannel, OssilaX200Channel):
    """A source measure unit (SMU) channel of the Ossila X200 device which can source a voltage and measure the voltage
    and current. For more details and specifications see the user manual of the Ossila X200."""

    current_ranges = (200e-3, 20e-3, 2e-3, 200e-6, 20e-6, 0.)

    def __init__(self, identifier: str = 'smu1', auto_range: bool = False,
                 s_delay: int = 1000, s_filter: int = 1, s_osr: int = 5, s_range: int = 1):
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
        self.__settings = {
            'delay': Decimal(s_delay),
            'filter': s_filter,
            'osr': s_osr,
            'range': s_range
        }
        self.__check_settings()

    @property
    def auto_range(self) -> bool:
        return self._auto_range

    @auto_range.setter
    def auto_range(self, new_value: bool):
        """Enable or disable the use of the automatic current range selection."""
        self._auto_range = new_value

    def __check_settings(self):
        if type(self.__settings['delay']) is not Decimal:
            raise TypeError('Setting `delay` must be Decimal!')
        if self.__settings['delay'] < 0:
            raise ValueError('Setting `delay` must not be negative!')
        if type(self.__settings['filter']) is not int:
            raise TypeError('Setting `filter` must be int!')
        if self.__settings['filter'] < 0:
            raise ValueError('Setting `filter` must not be negative!')
        if self.__settings['osr'] not in range(20):
            raise ValueError('Setting `osr` must be in [0,19]!')
        if self.__settings['range'] not in range(1, 6):
            raise ValueError('Setting `range` must be in [1,5]!')

    def disable(self):
        """Sets the source voltage to 0 V and disables the channel."""
        self.__set_property('voltage', Decimal(0))
        self.__set_property('enable', False)

    def measure_voltage(self):
        return self.__connection[self.identifier].measurev()[0]

    def measure_current(self):
        return self.__connection[self.identifier].measurei()[0]

    def source_voltage(self, voltage: float):
        """Sets the output voltage to the defined value.

        :param voltage: Output voltage of the power source in V. Must be in [-10, 10].
        :raises ValueError: If voltage is out of bounds.
        """
        if abs(voltage) > 10:
            raise ValueError('Absolute voltage must not exceed 10 V!')
        self.__set_property('voltage', Decimal(voltage))

    def _find_range(self, voltage: float):
        self.__set_property('range', 1)
        self.__set_property('voltage', Decimal(voltage))
        for i in range(len(self.current_ranges)):
            if abs(self.measure_current()) < self.current_ranges[i+1]:
                self.__set_property('range', i + 2)
            else:
                break

    def source_and_measure(self, voltage: float) -> Tuple[float, float]:
        """Sets the output voltage to the defined value, then measures the actual voltage and current.

        :param voltage: Output voltage of the power source in V. Must be in [-10, 10].
        :returns: Measurement result as tuple: (voltage (V), current (A)).
        :raises ValueError: If voltage is out of bounds.
        """
        if abs(voltage) > 10:
            raise ValueError('Absolute voltage must not exceed 10 V!')
        if self._auto_range:
            self._find_range(voltage)
        return self.__connection[self.identifier].oneshot(Decimal(voltage))[0]


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
        self.__settings = {
            'osr': s_osr
        }

    def __check_settings(self):
        if self.__settings['osr'] not in range(20):
            raise ValueError('Setting `osr` must be in [0,19]!')

    def measure_voltage(self):
        return self.__connection[self.identifier].measure()[0]


class OssilaX200(DeviceABC):
    """Implements the Ossila X200 Source Measure Unit as a Device class which is a container for the channels and the
    device connection."""

    def __init__(self, channels: List[OssilaX200SMUChannel | OssilaX200VsenseChannel] = None,
                 address: str = '', port: int = 8888, serial_timeout: float = 0.1):
        """Initializes the Ossila X200 Source Measure Unit.

        :param channels: List of channels which are subclasses of the OssilaX200Channel class. A maximum of 4 channels,
            i.e., 2xSMU and 2xVsense, are available. Duplicates are not allowed.
        :param address: COM (USB) or IP (Ethernet) address of the Ossila X200.
        :param port: Must be defined for connections over ethernet.
        :param serial_timeout: Timeout for the serial connection over USB in s.
        :raises ValueError: If too many channels or duplicate channels are provided.
        """
        if channels is None:
            channels = [OssilaX200SMUChannel()]
        if len(channels) > 4:
            raise ValueError('Number of channels must not exceed 4!')
        channel_identifiers = set()
        for channel in channels:
            channel_identifiers.add(channel.identifier)
        if len(channels) != len(channel_identifiers):
            raise ValueError('Duplicate channels are not allowed!')
        self._channels = channels
        self._connection_args = {'address': address, 'port': port, 'serial_timeout': serial_timeout}

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
            channel.__connection = connection
            channel.enable()
        try:
            yield
        finally:
            for channel in self._channels:
                channel.disable()
                channel.__connection = None
            connection.close()
