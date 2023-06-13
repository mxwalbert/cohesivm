"""Implements the Measurement class for obtaining the current-voltage characteristic."""
from __future__ import annotations
import numpy as np
import multiprocessing as mp
from .. import InterfaceType
from ..abcs import MeasurementABC, DeviceABC
from ..channels import SourceMeasureUnitChannel
from ..data_stream import FakeQueue


class CurrentVoltageCharacteristic(MeasurementABC):
    """A Measurement class for obtaining the current-voltage characteristic of a device."""

    _name = 'CurrentVoltageCharacteristic'
    _interface_type = InterfaceType.HI_LO
    _required_channels = [(SourceMeasureUnitChannel,)]

    def __init__(self, start_voltage: float, end_voltage: float, voltage_step: float, hysteresis: bool = False):
        """Initializes the class for current-voltage characteristic measurements and stores the settings in the property
        `settings` which can be used to create a Metadata object.

        :param start_voltage: Begin of the measurement range in V.
        :param end_voltage: End of the measurement range in V.
        :param voltage_step: Voltage change for each datapoint in V. Must be larger than 0.
        :param hysteresis: Flags if the voltage range should be measured a second time in reverse order directly after
            the initial measurement.
        :raises ValueError: If `voltage_step` is not larger than 0.
        """
        if voltage_step <= 0:
            raise ValueError('Voltage step must be larger than 0!')
        self.__start_voltage = start_voltage
        self.__end_voltage = end_voltage
        self.__voltage_step = voltage_step
        self.__hysteresis = hysteresis
        settings = {
            'sv': np.array(start_voltage),
            'ev': np.array(end_voltage),
            'vs': np.array(voltage_step),
            'h': np.array(hysteresis)
        }
        MeasurementABC.__init__(self, settings)

    def run(self, device: DeviceABC, data_stream: mp.Queue = None) -> np.ndarray:
        """Performs the measurement by iterating over the voltage range and returns the results as structured array.
        If a `data_stream` queue is provided, the results will also be sent there.

        :param device: An instance of a class which inherits the DeviceABC and complies with the `required_channels`.
        :param data_stream: A queue-like object where the measurement results can be sent to, e.g., for real-time
            plotting of the measurement.
        :returns: A Numpy structured array with tuples of datapoints: ('Voltage (V)', 'Current (A)').
        """
        if data_stream is None:
            data_stream = FakeQueue()
        results = []
        set_voltage = self.__start_voltage
        inverse = 1 if self.__start_voltage > self.__end_voltage else 0
        with device.connect():
            while (set_voltage < self.__end_voltage) ^ inverse or set_voltage == self.__end_voltage:
                result = device.channels[0].source_and_measure(set_voltage)
                results.append(result)
                data_stream.put(result)
                set_voltage += self.__voltage_step * (-1) ** inverse
            if self.__hysteresis:
                set_voltage -= self.__voltage_step * (-1) ** inverse
                while (set_voltage > self.__start_voltage) ^ inverse or set_voltage == self.__start_voltage:
                    result = device.channels[0].source_and_measure(set_voltage)
                    results.append(result)
                    data_stream.put(result)
                    set_voltage -= self.__voltage_step * (-1) ** inverse
        return np.array(results, dtype=[('Voltage (V)', float), ('Current (A)', float)])
