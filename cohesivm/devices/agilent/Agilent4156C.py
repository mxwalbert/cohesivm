"""Implements the Agilent 4156C Precision Semiconductor Parameter Analyzer.

Requires the PyVISA package: https://pypi.org/project/PyVISA/"""
from __future__ import annotations
import pyvisa
from abc import ABC
from typing import List, Any, TypeVar
from cohesivm.devices import Device
from cohesivm.channels import Channel, SweepVoltageSMU

TChannel = TypeVar('TChannel', bound='Agilent4156CChannel')


class Agilent4156CChannel(Channel, ABC):
    """Abstract base class which implements the properties and methods which all Agilent 4156C channels have in
    common."""

    @property
    def identifier_list(self) -> list[str]:
        return self.identifier.split(',')

    def _write(self, command: str) -> None:
        """Sends an ASCII command to the device.

        :param command: ASCII command string which is sent to the device.
        """
        self.connection.write(command)

    def _query(self, command: str) -> str:
        """Sends an ASCII command to the device and returns the response.

        :param command: ASCII command string which is sent to the device.
        :returns: The response string, which should be in ASCII format if the device is set up correctly.
        """
        return self.connection.query(command)

    def wait_for_completion(self) -> None:
        """Sends an ASCII query to check if the operation on the device is finished. Waits for the response with an
        increased timeout."""
        old_timeout = self.connection.timeout
        self.connection.timeout = 1000000
        self.connection.query('*OPC?')
        self.connection.timeout = old_timeout

    def set_property(self, name: str, value: Any = None) -> None:
        if value is None:
            self._write(name)
        else:
            self._write(f'{name} {value}')

    def get_property(self, name: str) -> Any:
        return self._query(f'{name}?')

    def get_key_property(self, name: str, key: str) -> Any:
        """Retrieves the value of a property which is further specified by the `key` argument."""
        return self._query(f'{name}? {key}')

    def disable(self) -> None:
        for identifier in self.identifier_list:
            self.set_property(f':PAGE:CHAN:{identifier}:DIS')


class SweepVoltageSMUChannel(Agilent4156CChannel, SweepVoltageSMU):
    """Two source monitor units of the Agilent 4156C configured to work as one Sweep Voltage SMU channel. For more
    details and specifications see the user manual of the Agilent 4156C.

    :param force_smu: String identifier of the SMU channel which is used as voltage source: 'SMU1', 'SMU2', 'SMU3'
        or 'SMU4'.
    :param com_smu: String identifier of the SMU channel which is used as common connection: 'SMU1', 'SMU2', 'SMU3'
        or 'SMU4'.
    :param s_compliance: Float value for the current compliance in A, i.e., the maximum allowed current. Determines
        the voltage output range: maximum voltage is 20, 40, 100 V for 0.1, 0.05, 0.02 A compliance, respectively.
        The minimum value is 0.1 pA.
    :param s_int_time: String value for the integration time which can be one of 'SHORT', 'MEDIUM', 'LONG'.
    :param s_delay: Float value for the time in s between setting a voltage step and running a current measurement.
    :param s_hold_time: Float value for the time in s before the sweep is started.
    :raises ValueError: If the identifier is not available or if a setting value is not valid.
    :raises TypeError: If a setting type is not supported.
    """

    def __init__(self, force_smu: str = 'SMU1', com_smu: str = 'SMU2', s_compliance: float = 0.05,
                 s_int_time: str = 'MEDIUM', s_delay: float = 0.0, s_hold_time: float = 0.0) -> None:
        if force_smu == com_smu:
            raise ValueError("The `force_smu` must not be the same as the `com_smu`!")
        if not {force_smu, com_smu} <= {'SMU1', 'SMU2', 'SMU3', 'SMU4'}:
            raise ValueError("Identifier of the SMU channels must be one of 'SMU1', 'SMU2', 'SMU3' or 'SMU4'!")
        self._force_smu = force_smu
        self._com_smu = com_smu
        self._identifier = f'{force_smu},{com_smu}'
        self._commands = {
            'int_time': ':PAGE:MEAS:MSET:ITIM:MODE',
            'compliance': ':PAGE:MEAS:SWE:VAR1:COMP',
            'delay': ':PAGE:MEAS:SWE:DEL',
            'hold_time': ':PAGE:MEAS:SWE:HTIM'
        }
        self._settings = {
            self._commands['int_time']: s_int_time,
            self._commands['compliance']: s_compliance,
            self._commands['delay']: s_delay,
            self._commands['hold_time']: s_hold_time
        }
        self._max_voltage = 100
        Agilent4156CChannel.__init__(self, self._identifier, self._settings)

    def _check_settings(self) -> None:
        if self._settings[self._commands['int_time']] not in ['SHORT', 'MEDIUM', 'LONG']:
            raise ValueError("Integration time (`int_time`) must be either 'SHORT', 'MEDIUM' or 'LONG'!")
        try:
            compliance = float(self._settings[self._commands['compliance']])
        except ValueError:
            raise TypeError('Compliance setting cannot be cast to float!')
        if compliance < 0.1e-12 or compliance > 0.1:
            raise ValueError('Current compliance must be between 0.1 pA and 0.1 A!')
        if compliance > 0.02:
            if compliance > 0.05:
                self._max_voltage = 20
            else:
                self._max_voltage = 40
        else:
            self._max_voltage = 100
        try:
            delay = float(self._settings[self._commands['delay']])
        except ValueError:
            raise TypeError('Delay setting cannot be cast to float!')
        if delay < 0 or delay > 60:
            raise ValueError('Delay must be between 0 and 60 s!')
        try:
            hold_time = float(self._settings[self._commands['hold_time']])
        except ValueError:
            raise TypeError('Hold time setting cannot be cast to float!')
        if hold_time < 0 or hold_time > 600:
            raise ValueError('Hold time must be between 0 and 600 s!')

    def enable(self) -> None:
        self.set_property(':PAGE:CHAN:MODE', 'SWE')
        self.set_property(f':PAGE:CHAN:{self._force_smu}:FUNC', 'VAR1')
        self.set_property(f':PAGE:CHAN:{self._force_smu}:MODE', 'V')
        self.set_property(f':PAGE:CHAN:{self._force_smu}:INAM', f"'I{self._force_smu}'")
        self.set_property(f':PAGE:CHAN:{self._force_smu}:VNAM', f"'V{self._force_smu}'")
        self.set_property(f':PAGE:CHAN:{self._com_smu}:FUNC', 'CONS')
        self.set_property(f':PAGE:CHAN:{self._com_smu}:MODE', 'COMM')
        self.set_property(f':PAGE:CHAN:{self._com_smu}:INAM', f"'I{self._com_smu}'")
        self.set_property(f':PAGE:CHAN:{self._com_smu}:VNAM', f"'V{self._com_smu}'")
        self.set_property(f':PAGE:MEAS:MSET:{self._force_smu}:RANG:MODE', 'AUTO')
        self.set_property(':PAGE:MEAS:SWE:VAR1:SPAC', 'LIN')
        self.set_property(':FORM:DATA', 'ASC')

    def sweep_voltage_and_measure(self, start_voltage: float, end_voltage: float, voltage_step: float, hysteresis: bool
                                  ) -> list[tuple[float, float]]:
        if abs(start_voltage) > self._max_voltage or abs(end_voltage) > self._max_voltage:
            raise ValueError(f'Voltage must not exceed maximum value of {self._max_voltage} V!')
        self.set_property(f':PAGE:MEAS:SWE:VAR1:MODE', 'DOUBLE' if hysteresis else 'SINGLE')
        self.set_property(':PAGE:MEAS:SWE:VAR1:STAR', f'{start_voltage:.6f}')
        self.set_property(':PAGE:MEAS:SWE:VAR1:STOP', f'{end_voltage:.6f}')
        self.set_property(':PAGE:MEAS:SWE:VAR1:STEP', f'{voltage_step:.6f}')
        self.set_property(':PAGE:SCON:SING')
        self.wait_for_completion()
        self.set_property(':DISP', f'ON')
        self.set_property(':PAGE:GLIS:GRAP')
        self.set_property(':PAGE:GLIS:SCAL:AUTO', 'ONCE')
        self.set_property(':DISP', f'OFF')
        voltage_list = self.get_key_property(':DATA', f"'V{self._force_smu}'").split(',')
        current_list = self.get_key_property(':DATA', f"'I{self._force_smu}'").split(',')
        return [(float(voltage), float(current)) for voltage, current in zip(voltage_list, current_list)]


class Agilent4156C(Device):
    """Implements the Agilent 4156C Precision Semiconductor Parameter Analyzer as a Device class which is a container
    for the channels and the device connection. For more details and specifications see the user manual of the
    Agilent 4156C.

    :param channels: List of channels which are subclasses of the :class:`Agilent4156CChannel`. The device consists of
        4xSMU, 2xVSU, and 2xVMU channels.
    :param resource_name: The VISA string identifier of the device.
    :raises TypeError: If a channel is not a subclass of the Agilent4156CChannel class.
    :raises ValueError: If duplicate channels are provided.
    """

    def __init__(self, channels: List[TChannel] = None, resource_name: str = '') -> None:
        if channels is None:
            channels = [SweepVoltageSMUChannel()]
        channel_identifiers = []
        for channel in channels:
            if not isinstance(channel, Agilent4156CChannel):
                raise TypeError(f'Channel {channel} is not an Agilent4156CChannel!')
            channel_identifiers += channel.identifier_list
        if len(channel_identifiers) != len(set(channel_identifiers)):
            raise ValueError('Duplicate channels are not allowed!')
        self._resource_name = resource_name
        super().__init__(channels)

    @property
    def channels(self) -> List[TChannel]:
        return self._channels

    def _establish_connection(self) -> pyvisa.resources.GPIBInstrument:
        rm = pyvisa.ResourceManager()
        res: pyvisa.resources.GPIBInstrument = rm.open_resource(self._resource_name)
        res.write('*RST;*CLS')
        res.write(':DISP OFF')
        res.write(':PAGE:CHAN:ALL:DIS')
        return res
