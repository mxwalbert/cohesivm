"""Implements the Ossila X200 Source Measure Unit.
Requires the xtralien module: https://pypi.org/project/xtralien/"""
from __future__ import annotations
import importlib
try:
    importlib.import_module('xtralien')
except ImportError:
    raise ImportError("Package 'xtralien' is not installed.")
import xtralien
import time
import numpy as np
from decimal import Decimal
from typing import List, Any, Tuple, TypeVar
from abc import ABC
from . import DeviceABC, requires_connection
from ..channels import ChannelABC, Voltmeter, Amperemeter, VoltageSource, VoltageSMU
from ..database import database_dict_type


TOssilaX200Channel = TypeVar('TOssilaX200Channel', bound='OssilaX200Channel')


class OssilaX200Channel(ChannelABC, ABC):
    """Abstract class which implements the properties and methods which all Ossila X200 channels have in common."""

    @requires_connection
    def set_property(self, name: str, value: Any):
        method = getattr(self.connection[self.identifier].set, name)
        method(value, response=0)
        time.sleep(0.01)

    @requires_connection
    def get_property(self, name: str) -> Any:
        method = getattr(self.connection[self.identifier].get, name)
        result = method()
        if type(result) == str:
            result = result.replace('\x00', '')
        return result

    def enable(self):
        self.set_property('enabled', True)

    def disable(self):
        self.set_property('enabled', False)


class OssilaX200SMUChannel(OssilaX200Channel, Voltmeter, Amperemeter, VoltageSource, VoltageSMU):
    """A source measure unit (SMU) channel of the Ossila X200 device which can source a voltage and measure the voltage
    and current. For more details and specifications see the user manual of the Ossila X200."""

    def __init__(self, identifier: str = 'smu1', auto_range: bool = False, delay: float = 0.001, s_filter: int = 1,
                 s_osr: int = 5, s_range: int = 1):
        """Initializes one of the two source measure unit (SMU) channels of the Ossila X200.

        :param identifier: String identifier of the SMU channel: 'smu1' or 'smu2'.
        :param auto_range: Flags if the current measurement range should be determined automatically by the
            `source_and_measure` method.
        :param delay: Setting for the voltage settling time in s.
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
        self._delay = delay
        self._settings = {
            'filter': s_filter,
            'osr': s_osr,
            'range': s_range
        }
        OssilaX200Channel.__init__(self, self._identifier, self._settings)

    @property
    def auto_range(self) -> bool:
        return self._auto_range

    @auto_range.setter
    def auto_range(self, new_value: bool):
        """If True, the `source_and_measure` method will automatically set the current measurement range."""
        self._auto_range = new_value

    @property
    def delay(self) -> float:
        return self._delay

    @delay.setter
    def delay(self, new_value: float):
        """Set the voltage settling time between applying the voltage and measuring the voltage-current pair."""
        self._delay = new_value

    @property
    def settings(self) -> database_dict_type:
        whole_settings_dict = {'auto_range': self.auto_range, 'delay': self.delay}
        for k, v in self._settings.items():
            whole_settings_dict[k] = v
        return whole_settings_dict

    def _check_settings(self):
        if type(self._settings['filter']) is not int:
            raise TypeError('Setting `filter` must be int!')
        if self._settings['filter'] < 0:
            raise ValueError('Setting `filter` must not be negative!')
        if self._settings['osr'] not in range(20):
            raise ValueError('Setting `osr` must be in [0,19]!')
        if self._settings['range'] not in range(1, 6):
            raise ValueError('Setting `range` must be in [1,5]!')

    def enable(self):
        """Sets the source voltage to 0 V and enables the channel."""
        self.set_property('voltage', Decimal('0'))
        OssilaX200Channel.enable(self)

    def disable(self):
        """Sets the source voltage to 0 V and disables the channel."""
        self.set_property('voltage', Decimal('0'))
        OssilaX200Channel.disable(self)

    @requires_connection
    def measure_voltage(self):
        return self.connection[self.identifier].measurev()[0]

    @requires_connection
    def measure_current(self):
        return self.connection[self.identifier].measurei()[0]

    def source_voltage(self, voltage: float):
        """Sets the DC output voltage to the defined value.

        :param voltage: Output voltage of the DC power source in V. Must be in [-10, 10].
        :raises ValueError: If voltage is out of bounds.
        """
        if abs(voltage) > 10:
            raise ValueError('Absolute voltage must not exceed 10 V!')
        self.set_property('voltage', Decimal(str(voltage)))

    current_limits = (0.1, 0.01, 0.001, 0.0001, 0.00001, 0.)

    @requires_connection
    def _find_range(self) -> np.ndarray[float, float]:
        while True:
            result = self.connection[self.identifier].measure()[0]
            i = 0
            for i in range(6):
                if float(abs(result[1])) >= self.current_limits[i]:
                    break
            if i == 0:
                return result
            current_range = self.get_property('range')
            if i > current_range:
                if (i - current_range) > 2:
                    i = int(current_range + 2)
            elif i == current_range:
                return result
            self.set_property('range', i)

    @requires_connection
    def source_voltage_and_measure(self, voltage: float) -> Tuple[float, float]:
        """Sets the output voltage to the defined value, then measures the actual voltage and current.

        :param voltage: Output voltage of the power source in V. Must be in [-10, 10].
        :returns: Measurement result as a tuple: (voltage (V), current (A)).
        :raises ValueError: If voltage is out of bounds.
        """
        if abs(voltage) > 10:
            raise ValueError('Absolute voltage must not exceed 10 V!')
        self.source_voltage(voltage)
        if self.auto_range:
            if self.get_property('error') == 'true':
                self.set_property('range', 1)
                self.source_voltage(voltage)
            time.sleep(self.delay)
            result = self._find_range()
        else:
            time.sleep(self.delay)
            result = self.connection[self.identifier].measure()[0]
        return result[0], result[1]


class OssilaX200VsenseChannel(OssilaX200Channel, Voltmeter):
    """A voltmeter channel (Vsense) of the Ossila X200 device which can measure the voltage with high precision. For
    more details and specifications see the user manual of the Ossila X200."""

    def __init__(self, identifier: str = 'vsense1', s_osr: int = 5):
        """Initializes one of the two voltmeter channels (Vsense) of the Ossila X200.

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
        OssilaX200Channel.__init__(self, self._identifier, self._settings)

    def _check_settings(self):
        if self._settings['osr'] not in range(20):
            raise ValueError('Setting `osr` must be in [0,19]!')

    @requires_connection
    def measure_voltage(self):
        return self.connection[self.identifier].measure()[0]


class OssilaX200(DeviceABC):
    """Implements the Ossila X200 Source Measure Unit as a Device class which is a container for the channels and the
    device connection. For more details and specifications see the user manual of the Ossila X200."""

    def __init__(self, channels: List[TOssilaX200Channel] = None,
                 address: str = '', port: int = 0, serial_timeout: float = 0.1):
        """Initializes the Ossila X200 Source Measure Unit.

        :param channels: List of channels which are subclasses of the OssilaX200Channel class. A maximum of 4 channels,
            i.e., 2xSMU and 2xVsense, are available. Duplicates are not allowed.
        :param address: COM (USB) or IP (Ethernet) address of the Ossila X200.
        :param port: Must be defined for connections over ethernet.
        :param serial_timeout: Timeout for the serial connection over USB in s.
        :raises TypeError: If a channel is not an OssilaX200Channel. If connection arguments `port` and `serial_timeout`
            cannot be cast to their required type.
        :raises ValueError: If duplicate channels are provided.
        """
        if channels is None:
            channels = [OssilaX200SMUChannel()]
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
        self._connection_args = {'addr': address, 'port': port, 'serial_timeout': serial_timeout}
        DeviceABC.__init__(self, channels)

    @property
    def channels(self) -> List[TOssilaX200Channel]:
        return self._channels

    def _establish_connection(self) -> xtralien.Device:
        dev = xtralien.Device(**self._connection_args)
        if len(dev.connections) == 0:
            del dev
            raise RuntimeError('There are no connected xtralien devices.')
        return dev
