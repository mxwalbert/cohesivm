"""Implements the Agilent 4284A Precision LCR Meter.
Requires the PyVISA package for controlling devices over the Virtual Instrument Software Architecture protocol."""
from __future__ import annotations
import importlib
try:
    importlib.import_module('pyvisa')
except ImportError:
    raise ImportError("Package 'pyvisa' is not installed.")
import pyvisa
import time
import math
import warnings
from typing import List, Any, Tuple
from .. import DeviceABC, requires_connection
from ...channels import LCRMeter


class Agilent4284ALCRChannel(LCRMeter):
    """LCR meter channel of the Agilent 4284A device which can measure the inductance (L), capacitance (C), and
    resistance (R) of an electronic component. For more details and specifications see the user manual of the
    Agilent 4284A."""

    def __init__(self, s_trigger_delay: int = 1, s_integration_time: str = 'MEDIUM', s_averaging_rate: int = 64,
                 s_automatic_level_control: bool = False):
        """Initializes the LCR meter channel of the Agilent 4284A.

        :param s_trigger_delay: Setting for the delay of the trigger execution after the command was sent. The value is
            the time in ms and must be between 0 and 60 s.
        :param s_integration_time: Sets the time required to perform an A/D conversion. The value can be one of 'SHORT',
            'MEDIUM', 'LONG'.
        :param s_averaging_rate: Sets the number of individual measurements which are averaged to yield the final
            result. Can be one of 1, 2, 4, 8, 16, 32, 64, 128, 256.
        :param s_automatic_level_control: Flags if the ALC should be used which regulates the actual test level to the
            desired level.
        :raises TypeError: If the type of setting values is incorrect.
        :raises ValueError: If setting values are out of bounds.
        """
        self._identifier = 'lcr'
        self._settings = {
            'TRIGGER:DELAY': f'{s_trigger_delay}',
            'APERTURE': f'{s_integration_time},{s_averaging_rate}',
            'AMPLITUDE:ALC': 'ON' if s_automatic_level_control else 'OFF'
        }
        LCRMeter.__init__(self, self._identifier, self._settings)
        self._trigger_delay = s_trigger_delay

    @requires_connection
    def _write(self, command: str):
        """Sends an ASCII command to the device.

        :param command: ASCII command string which is sent to the device.
        """
        self.connection.write(command)

    @requires_connection
    def _query(self, command: str) -> str:
        """Sends an ASCII command to the device and returns the response.

        :param command: ASCII command string which is sent to the device.
        :returns: The response string, which should be in ASCII format if the device is set up correctly.
        """
        return self.connection.query(command)

    def set_property(self, name: str, value: Any = None):
        if value is None:
            self._write(name)
        else:
            self._write(f'{name} {value}')

    def get_property(self, name: str) -> Any:
        return self._query(f'{name}?')

    def _check_settings(self):
        try:
            trigger_delay = int(self._settings['TRIGGER:DELAY'])
        except ValueError:
            raise TypeError('Setting `TRIGGER:DELAY` cannot be cast to int!')
        if trigger_delay < 0 or trigger_delay > 60000:
            raise ValueError('Setting `TRIGGER:DELAY` must be between 0 and 60000!')
        self._trigger_delay = trigger_delay
        self._settings['TRIGGER:DELAY'] = f'{trigger_delay}'
        try:
            aperture = str(self._settings['APERTURE']).split(',')
            assert len(aperture) == 2
            integration_time = aperture[0]
            averaging_rate = int(aperture[1])
        except AssertionError or ValueError:
            raise TypeError('Setting `APERTURE` must have the format "integration_time,averaging_rate", where '
                            '"averaging_rate" is an int value.')
        if integration_time not in ['SHORT', 'MEDIUM', 'LONG']:
            raise ValueError('Setting `integration_time` (part of setting `APERTURE`) must be one of "SHORT", '
                             '"MEDIUM", "LONG"!')
        if averaging_rate not in [2**p for p in range(9)]:
            raise ValueError('Setting `averaging_rate` (part of setting `APERTURE`) must be one of 1, 2, 4, 8, 16, 32, '
                             '64, 128, 256!')
        self._settings['APERTURE'] = f'{integration_time},{averaging_rate}'
        if self._settings['AMPLITUDE:ALC'] not in ['ON', 'OFF']:
            raise ValueError('Setting `AMPLITUDE:ALC` must be "ON" or "OFF!')

    def enable(self):
        self.disable()
        self.set_property('FUNCTION:IMPEDANCE', 'ZTD')
        self.set_property('FUNCTION:IMPEDANCE:RANGE:AUTO', 'ON')
        self.set_property('TRIGGER:SOURCE', 'BUS')
        self.set_property('INITIATE:CONTINUOUS', 'ON')
        self.set_property('OUTPUT:HPOWER', 'ON')
        self.set_property('BIAS:STATE', 'ON')

    def disable(self):
        self.set_property('*RST;*CLS')
        self.set_property('ABORT')
        self.source_voltage(0)
        self.source_current(0)
        self.set_property('BIAS:STATE', 'OFF')

    def source_voltage(self, voltage: float):
        """Resets the bias current and sets the bias voltage to the defined value.

        :param voltage: Output voltage of the DC power source in V. Must be in [-40, 40].
        :raises ValueError: If voltage is out of bounds.
        """
        if abs(voltage) > 40:
            raise ValueError('Absolute voltage must not exceed 40 V!')
        if abs(voltage) > 20.:
            voltage = round(voltage, 2)
        elif abs(voltage) > 8.:
            if voltage > 0:
                voltage = math.floor(voltage / 0.005) * 0.005
            else:
                voltage = math.ceil(voltage / 0.005) * 0.005
        elif abs(voltage) > 4.:
            if voltage > 0:
                voltage = math.floor(voltage / 0.002) * 0.002
            else:
                voltage = math.ceil(voltage / 0.002) * 0.002
        else:
            voltage = round(voltage, 3)
        self.set_property('BIAS:VOLTAGE', f'{voltage:.3f}')

    def source_current(self, current: float):
        """Resets the bias voltage and sets the bias current to the defined value.

        :param current: Output current of the DC power source in A. Must be in [-0.1, 0.1].
        :raises ValueError: If current is out of bounds.
        """
        if abs(current) > 0.1:
            raise ValueError('Absolute current must not exceed 0.1 A!')
        if abs(current) > 0.08:
            if current > 0:
                current = math.floor(current / 0.00005) * 0.00005
            else:
                current = math.ceil(current / 0.00005) * 0.00005
        elif abs(current) > 0.04:
            if current > 0:
                current = math.floor(current / 0.00002) * 0.00002
            else:
                current = math.ceil(current / 0.00002) * 0.00002
        else:
            current = round(current, 5)
        self.set_property('BIAS:CURRENT', f'{current:.5f}')

    def set_oscillator_frequency(self, frequency: float):
        """Sets the AC frequency of the oscillator to the defined value.

        :param frequency: Oscillator frequency in Hz. Must be in [20, 1000000].
        :raises ValueError: If frequency is out of bounds.
        """
        if frequency < 20 or frequency > 1000000:
            raise ValueError('Oscillator frequency must be between 20 and 1000000 Hz!')
        frequency = round(frequency, 12)
        self.set_property('FREQUENCY', f'{frequency:.12f}')

    def set_oscillator_voltage(self, voltage: float):
        """Resets the AC current and sets the AC voltage of the oscillator to the defined value.

        :param voltage: Oscillator voltage level in V. Must be in [0, 40].
        :raises ValueError: If voltage is out of bounds.
        """
        if voltage < 0 or voltage > 20:
            raise ValueError('Oscillator voltage must be between 0 and 20 V!')
        if 0 < voltage < 0.005:
            voltage = 0
        if voltage > 2.:
            voltage = round(voltage, 1)
        elif voltage > 0.2:
            voltage = round(voltage, 2)
        else:
            voltage = round(voltage, 3)
        self.set_property('VOLTAGE', f'{voltage:.3f}')

    def set_oscillator_current(self, current: float):
        """Resets the AC voltage and sets the AC current of the oscillator to the defined value.

        :param current: Oscillator current level in A. Must be in [0, 0.2].
        :raises ValueError: If current is out of bounds.
        """
        if current < 0 or current > 0.2:
            raise ValueError('Oscillator current must be between 0 and 0.2 A!')
        if 0 < current < 0.00005:
            current = 0
        if current > 0.02:
            current = round(current, 3)
        elif current > 0.002:
            current = round(current, 4)
        else:
            current = round(current, 5)
        self.set_property('CURRENT', f'{current:.5f}')

    def measure_impedance(self) -> Tuple[float, float]:
        self.set_property('TRIGGER:IMMEDIATE')
        time.sleep(self._trigger_delay / 1000)
        result = self.get_property('FETCH').split(',')
        if result[2] != '0':
            warnings.warn(f'Fetching the data resulted in the following unusual status code: {result[2]}')
        return float(result[0]), float(result[1])


class Agilent4284A(DeviceABC):
    """Implements the Agilent 4284A Precision LCR Meter as a Device class which is a container for the channels and the
    device connection. For more details and specifications see the user manual of the Agilent 4284A."""

    def __init__(self, channels: List[Agilent4284ALCRChannel] = None, resource_name: str = ''):
        """Initializes the Agilent 4284A Precision LCR Meter.

        :param channels: A list with a single Agilent4284ALCRChannel instance.
        :param resource_name: The VISA string identifier of the device.
        :raises TypeError: If a channel is not an Agilent4284ALCRChannel.
        :raises ValueError: If too many channels or duplicate channels are provided.
        """
        if channels is None:
            channels = [Agilent4284ALCRChannel()]
        if len(channels) > 1:
            raise ValueError('This device can only hold a single channel!')
        if not isinstance(channels[0], Agilent4284ALCRChannel):
            raise TypeError(f'Channel {channels[0]} is not an Agilent4284ALCRChannel!')
        self._resource_name = resource_name
        DeviceABC.__init__(self, channels)

    @property
    def channels(self) -> List[Agilent4284ALCRChannel]:
        return self._channels

    def _establish_connection(self) -> pyvisa.Resource:
        rm = pyvisa.ResourceManager()
        return rm.open_resource(self._resource_name)
