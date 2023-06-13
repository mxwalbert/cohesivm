"""Module containing the channel abstract base classes which provide the templates of methods to implement."""
from abc import abstractmethod
from typing import Tuple
from .abcs import ChannelABC


class SourceMeasureUnitChannel(ChannelABC):
    """Combines the functions of a current source and a voltage measurement device."""

    @abstractmethod
    def measure_voltage(self) -> float:
        """Measures the voltage.

        :returns: Measurement result in V.
        """

    @abstractmethod
    def measure_current(self) -> float:
        """Measures the current.

        :returns: Measurement result in A.
        """

    @abstractmethod
    def source_voltage(self, voltage: float):
        """Sets the output voltage to the defined value.

        :returns: Output voltage of the power source in V.
        """

    @abstractmethod
    def source_and_measure(self, voltage: float) -> Tuple[float, float]:
        """Sets the output voltage to the defined value, then measures the actual voltage and current.

        :param voltage: Output voltage of the power source in V.
        :returns: Measurement result as tuple: (voltage (V), current (A)).
        """


class VoltmeterChannel(ChannelABC):
    """Measures the electric potential difference between two points in a circuit."""

    @abstractmethod
    def measure_voltage(self) -> float:
        """Measures the voltage.

        :returns: Measurement result in V.
        """
