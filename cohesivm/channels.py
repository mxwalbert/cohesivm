"""Module containing the channel abstract base classes which provide the templates of methods to implement."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Tuple, Any, TypeVar
from .database import database_dict_type


TChannelABC = TypeVar('TChannelABC', bound='ChannelABC')


class ChannelABC(ABC):
    """Contains the properties and methods to operate a physical device channel. The implementation of a child class
    must define the property getter and setter which are used to configure the channel. Further, a channel class
    inherits a traits class which contains the abstract methods that must be implemented."""
    @abstractmethod
    def __init__(self, identifier: str = None, settings: database_dict_type = None):
        self._identifier = identifier
        self._settings = {} if settings is None else settings
        self._connection = None
        self._check_settings()

    @property
    def identifier(self) -> str:
        """String identifier of the channel."""
        return self._identifier

    @property
    def settings(self) -> database_dict_type:
        """Dictionary of channel settings."""
        return self._settings if len(self._settings) > 0 else {'default': 0}

    @property
    def connection(self) -> Any | None:
        """Holds the device reference while a connection is established through using the `Device.connect`
        contextmanager."""
        return self._connection

    @abstractmethod
    def set_property(self, name: str, value: Any):
        """Sets a property/device-setting to the provided value."""

    @abstractmethod
    def get_property(self, name: str) -> Any:
        """Retrieves the current value of a property/device-setting."""

    @abstractmethod
    def _check_settings(self):
        """Validates the values which are stored in the `settings` dictionary before they are transferred to the
        device."""

    def apply_settings(self):
        """Applies the settings."""
        for name, value in self._settings.items():
            self.set_property(name, value)

    def change_setting(self, setting, value):
        """Modifies the `_settings` property and overwrites the settings on the device.

        :param setting: String key of the setting in the `_settings' property.
        :param value: New value of the setting.
        :raises KeyError: If `setting` is not a valid setting identifier string.
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
    def enable(self):
        """Enables the channel. Must be executed before any channel method can be run."""

    @abstractmethod
    def disable(self):
        """Disables the channel."""

    def measure_voltage(self) -> float:
        """Measures the voltage.

        :returns: Measurement result in V.
        """

    def measure_current(self) -> float:
        """Measures the current.

        :returns: Measurement result in A.
        """

    def source_voltage(self, voltage: float):
        """Sets the DC output voltage to the defined value.

        :param voltage: Output voltage of the DC power source in V.
        """

    def source_current(self, current: float):
        """Sets the DC output current to the defined value.

        :param current: Output current of the DC power source in A.
        """

    def source_voltage_and_measure(self, voltage: float) -> Tuple[float, float]:
        """Sets the DC output voltage to the defined value and measures the current.

        :param voltage: Output voltage of the power source in V.
        :returns: Measurement result: (voltage (V), current (A)).
        """

    def source_current_and_measure(self, current: float) -> Tuple[float, float]:
        """Sets the DC output current to the defined value and measures the voltage.

        :param current: Output current of the power source in A.
        :returns: Measurement result: (current (A), voltage (V)).
        """

    def use_hw_sweep(self) -> bool:
        """Flags whether the built-in hardware sweep should be used for the measurement."""

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

    def set_oscillator_frequency(self, frequency: float):
        """Sets the AC frequency of the oscillator to the defined value.

        :param frequency: Oscillator frequency in Hz.
        """

    def set_oscillator_voltage(self, voltage: float):
        """Sets the AC voltage of the oscillator to the defined value.

        :param voltage: Oscillator voltage level in V.
        """

    def set_oscillator_current(self, current: float):
        """Sets the AC current of the oscillator to the defined value.

        :param current: Oscillator current level in A.
        """

    def measure_impedance(self) -> Tuple[float, float]:
        """Performs an impedance measurement and returns the magnitude and phase angle of the complex impedance vector.

        :returns: Measurement result as tuple: (magnitude (1), phase (deg))
        """


class LCRMeter(ChannelABC):
    """Enables the measurement of the inductance (L), capacitance (C), and resistance (R) of an electronic component."""

    @abstractmethod
    def source_voltage(self, voltage: float):
        pass

    @abstractmethod
    def source_current(self, current: float):
        pass

    @abstractmethod
    def set_oscillator_frequency(self, frequency: float):
        pass

    @abstractmethod
    def set_oscillator_voltage(self, voltage: float):
        pass

    @abstractmethod
    def set_oscillator_current(self, current: float):
        pass

    @abstractmethod
    def measure_impedance(self) -> Tuple[float, float]:
        pass


class Voltmeter(ChannelABC):
    """Measures the electric potential difference between two points in a circuit."""

    @abstractmethod
    def measure_voltage(self) -> float:
        pass


class Amperemeter(ChannelABC):
    """Measures the current flowing through a circuit."""

    @abstractmethod
    def measure_current(self) -> float:
        pass


class VoltageSource(ChannelABC):
    """Supplies a constant DC voltage."""

    @abstractmethod
    def source_voltage(self, voltage: float):
        pass


class VoltageSMU(ChannelABC):
    """Combines the functions of a voltage source and current measurement device."""

    @abstractmethod
    def source_voltage_and_measure(self, voltage: float) -> Tuple[float, float]:
        pass


class SweepVoltageSMU(ChannelABC):
    """Implements hardware sweep capabilities of a voltage SMU channel."""

    @property
    @abstractmethod
    def use_hw_sweep(self) -> bool:
        pass

    @abstractmethod
    def sweep_voltage_and_measure(self, start_voltage: float, end_voltage: float, voltage_step: float, hysteresis: bool
                                  ) -> list[tuple[float, float]]:
        pass
