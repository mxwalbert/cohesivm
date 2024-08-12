"""This module contains the :class:`Channel` Abstract Base Class which should be inherited by device channels. The main
responsibility is to execute actions on the physical device channels for which the device
:attr:`~cohesivm.channels.Channel.connection` is stored.

Furthermore, all possible channel methods are defined in the :class:`Channel` in order for a
:class:`~cohesivm.measurements.Measurement` to recognize them. Trait classes, e.g., :class:`Voltmeter`, will inherit
these methods and set the ones that must be implemented abstract. Then they can be used to be implemented in a device
module and for the compatibility check of the :class:`~cohesivm.experiment.Experiment`."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Any, TypeVar, Union
from cohesivm.database import DatabaseDict


TChannel = TypeVar('TChannel', bound='Channel')


class Channel(ABC):
    """Contains the properties and methods to operate a physical device channel. The implementation of a child class
    must define the :meth:`get_property` and :meth:`set_property` methods which are used to configure the channel.
    Practically, the child class will inherit a trait class (child class of this class) which additionally defines the
    specific methods which must be implemented.

    :param identifier: String identifier of the channel.
    :param settings: Dictionary of channel settings."""
    @abstractmethod
    def __init__(self, identifier: str = None, settings: DatabaseDict = None) -> None:
        self._identifier = identifier
        if settings is None or len(settings) == 0:
            settings = {'default': 0}
        self._settings = dict(sorted(settings.items()))
        self._connection = None
        self._check_settings()

    @property
    def identifier(self) -> str:
        """String identifier of the channel."""
        return self._identifier

    @property
    def settings(self) -> DatabaseDict:
        """Dictionary of channel settings."""
        return self._settings

    @property
    def connection(self) -> Union[Any, None]:
        """Holds the resource of the device connection while a connection is established through using
        the :meth:`~cohesivm.devices.Device.connect` contextmanager."""
        if self._connection is None:
            raise RuntimeError('A device connection must be established in order to communicate with the channel!')
        return self._connection

    @abstractmethod
    def set_property(self, name: str, value: Any) -> None:
        """Sets a property/device-setting to the provided value.

        :param name: The name of the property/device-setting to be set.
        :param value: The value to which the property/device-setting should be set.
        """

    @abstractmethod
    def get_property(self, name: str) -> Any:
        """Retrieves the current value of a property/device-setting.

        :param name: The name of the property/device-setting to get.
        :returns: The value of the property/device-setting.
        """

    @abstractmethod
    def _check_settings(self) -> None:
        """Validates the values in the `settings` dictionary before they are applied on the device."""

    def apply_settings(self) -> None:
        """Applies the settings."""
        for name, value in self._settings.items():
            self.set_property(name, value)

    def change_setting(self, setting, value) -> None:
        """Modifies the :attr:`settings` and overwrites the settings on the device.

        :param setting: String key of the setting in the :attr:`settings`.
        :param value: New value of the setting.
        :raises KeyError: If ``setting`` is not a valid setting identifier string.
        """
        if setting not in self._settings.keys():
            raise KeyError(f"'{setting}' is not a valid setting identifier string. "
                           f"Valid keys are: {list(self._settings.keys())}")
        old_value = self._settings[setting]
        self._settings[setting] = value
        try:
            self._check_settings()
        except Exception as exc:
            self._settings[setting] = old_value
            raise exc
        self.apply_settings()

    @abstractmethod
    def enable(self) -> None:
        """Enables the channel. Must be executed before any channel method can be run."""

    @abstractmethod
    def disable(self) -> None:
        """Disables the channel."""

    def measure_voltage(self) -> float:
        """Measures the voltage.

        :returns: Measurement result in V.
        """
        raise NotImplementedError

    def measure_current(self) -> float:
        """Measures the current.

        :returns: Measurement result in A.
        """
        raise NotImplementedError

    def source_voltage(self, voltage: float) -> None:
        """Sets the DC output voltage to the defined value.

        :param voltage: Output voltage of the DC power source in V.
        """
        raise NotImplementedError

    def source_current(self, current: float) -> None:
        """Sets the DC output current to the defined value.

        :param current: Output current of the DC power source in A.
        """
        raise NotImplementedError

    def source_voltage_and_measure(self, voltage: float) -> Tuple[float, float]:
        """Sets the DC output voltage to the defined value and measures the current.

        :param voltage: Output voltage of the power source in V.
        :returns: Measurement result: (voltage (V), current (A)).
        """
        raise NotImplementedError

    def source_current_and_measure(self, current: float) -> Tuple[float, float]:
        """Sets the DC output current to the defined value and measures the voltage.

        :param current: Output current of the current source in A.
        :returns: Measurement result: (current (A), voltage (V)).
        """
        raise NotImplementedError

    def sweep_voltage_and_measure(self, start_voltage: float, end_voltage: float, voltage_step: float, hysteresis: bool
                                  ) -> list[tuple[float, float]]:
        """Sweeps over the specified voltage range and measures the current for each voltage step.

        :param start_voltage: Begin of the measurement range in V.
        :param end_voltage: End of the measurement range in V.
        :param voltage_step: Voltage change for each datapoint in V. Must be larger than 0.
        :param hysteresis: Flags if the voltage range should be measured a second time in reverse order directly after
            the initial measurement.
        :returns: Measurement results: [(voltage1 (V), current1 (A)), (voltage2 (V), current2 (A)), ...]
        """
        raise NotImplementedError

    def set_oscillator_frequency(self, frequency: float) -> None:
        """Sets the AC frequency of the oscillator to the defined value.

        :param frequency: Oscillator frequency in Hz.
        """
        raise NotImplementedError

    def set_oscillator_voltage(self, voltage: float) -> None:
        """Sets the AC voltage of the oscillator to the defined value.

        :param voltage: Oscillator voltage level in V.
        """
        raise NotImplementedError

    def set_oscillator_current(self, current: float) -> None:
        """Sets the AC current of the oscillator to the defined value.

        :param current: Oscillator current level in A.
        """
        raise NotImplementedError

    def measure_impedance(self) -> Tuple[float, float]:
        """Performs an impedance measurement and returns the magnitude and phase angle of the complex impedance vector.

        :returns: Measurement result as tuple: (magnitude (1), phase (deg))
        """
        raise NotImplementedError


class Voltmeter(Channel):
    """Measures the electric potential difference between two points in a circuit."""

    @abstractmethod
    def measure_voltage(self) -> float:
        pass


class Amperemeter(Channel):
    """Measures the current flowing through a circuit."""

    @abstractmethod
    def measure_current(self) -> float:
        pass


class VoltageSource(Channel):
    """Supplies a constant DC voltage."""

    @abstractmethod
    def source_voltage(self, voltage: float) -> None:
        pass


class CurrentSource(Channel):
    """Supplies a constant DC current."""

    @abstractmethod
    def source_current(self, current: float) -> None:
        pass


class VoltageSMU(Channel):
    """Combines the functions of a voltage source and current measurement device."""

    @abstractmethod
    def source_voltage_and_measure(self, voltage: float) -> Tuple[float, float]:
        pass


class CurrentSMU(Channel):
    """Combines the functions of a current source and voltage measurement device."""

    @abstractmethod
    def source_current_and_measure(self, current: float) -> Tuple[float, float]:
        pass


class SweepVoltageSMU(Channel):
    """Implements hardware sweep capabilities of a voltage SMU channel."""

    @abstractmethod
    def sweep_voltage_and_measure(self, start_voltage: float, end_voltage: float, voltage_step: float, hysteresis: bool
                                  ) -> list[tuple[float, float]]:
        pass


class LCRMeter(Channel):
    """Enables the measurement of the inductance (L), capacitance (C), and resistance (R) of an electronic component."""

    @abstractmethod
    def source_voltage(self, voltage: float) -> None:
        pass

    @abstractmethod
    def source_current(self, current: float) -> None:
        pass

    @abstractmethod
    def set_oscillator_frequency(self, frequency: float):
        pass

    @abstractmethod
    def set_oscillator_voltage(self, voltage: float) -> None:
        pass

    @abstractmethod
    def set_oscillator_current(self, current: float) -> None:
        pass

    @abstractmethod
    def measure_impedance(self) -> Tuple[float, float]:
        pass
