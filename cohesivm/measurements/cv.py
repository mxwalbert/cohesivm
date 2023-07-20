"""Implements the Measurement class for obtaining the capacitance-voltage characteristic."""
from __future__ import annotations
import numpy as np
import multiprocessing as mp
from ..interfaces import InterfaceType
from ..measurements import MeasurementABC
from ..devices import DeviceABC
from ..channels import LCRMeterChannel
from ..data_stream import FakeQueue


class CapacitanceVoltageProfiling(MeasurementABC):
    """A Measurement class for obtaining the capacitance-voltage characteristic of a device."""

    _interface_type = InterfaceType.HI_LO
    _required_channels = [(LCRMeterChannel,)]
    _output_type = [('Magnitude (1)', float), ('Phase (deg)', float)]

    def __init__(self, frequency: float, start_voltage: float, end_voltage: float, voltage_step: float,
                 oscillator_voltage: float | False, oscillator_current: float | False = False):
        """Initializes the measurement for capacitance-voltage profiling and stores the settings in the property
        `settings` which can be used to create a Metadata object.

        :param frequency: The oscillator frequency of the applied AC field.
        :param start_voltage: Begin of the measurement range in V.
        :param end_voltage: End of the measurement range in V.
        :param voltage_step: Voltage change for each datapoint in V. Must be larger than 0.
        :param oscillator_voltage: Oscillating voltage level of the applied AC field. If set to None, the
            `oscillator_current` will be used.
        :param oscillator_current: Oscillating current level of the applied AC field. Only used if `oscillator_voltage`
            is set to None.
        :raises ValueError: If `voltage_step` is not larger than 0.
        """
        if voltage_step <= 0:
            raise ValueError('Voltage step must be larger than 0!')
        if oscillator_voltage is False and oscillator_current is False:
            raise ValueError('One of `oscillator_voltage` or `oscillator_current` must be set!')
        self.__frequency = frequency
        self.__start_voltage = start_voltage
        self.__end_voltage = end_voltage
        self.__voltage_step = voltage_step
        self.__oscillator_voltage = oscillator_voltage
        self.__oscillator_current = oscillator_current
        settings = {
            'frequency': frequency,
            'start_voltage': start_voltage,
            'end_voltage': end_voltage,
            'voltage_step': voltage_step,
            'oscillator_voltage': oscillator_voltage,
            'oscillator_current': oscillator_current
        }
        self.__round_digit = self.find_least_significant_digit(voltage_step)
        voltage_range = end_voltage - start_voltage if end_voltage > start_voltage else start_voltage - end_voltage
        data_length = int(np.floor(voltage_range / voltage_step) + 1)
        MeasurementABC.__init__(self, settings=settings, output_shape=(data_length, 2))

    @staticmethod
    def find_least_significant_digit(number):
        number_str = str(float(number))
        decimal_position = number_str.find('.')
        return len(number_str) - decimal_position - 1

    def run(self, device: DeviceABC, data_stream: mp.Queue = None) -> np.ndarray:
        """Performs the measurement by iterating over the voltage range and returns the results as structured array.
        If a `data_stream` queue is provided, the results will also be sent there.

        :param device: An instance of a class which inherits the DeviceABC and complies with the `required_channels`.
        :param data_stream: A queue-like object where the measurement results can be sent to, e.g., for real-time
            plotting of the measurement.
        :returns: A Numpy structured array with tuples of datapoints: ('Magnitude (1)', 'Phase (deg)').
        """
        if data_stream is None:
            data_stream = FakeQueue()
        results = []
        set_voltage = self.__start_voltage
        inverse = 1 if self.__start_voltage > self.__end_voltage else 0
        with device.connect():
            device.channels[0].enable()
            if self.__oscillator_voltage is False:
                device.channels[0].set_oscillator_current(self.__oscillator_current)
            else:
                device.channels[0].set_oscillator_voltage(self.__oscillator_voltage)
            device.channels[0].set_oscillator_frequency(self.__frequency)
            while (set_voltage < self.__end_voltage) ^ inverse or set_voltage == self.__end_voltage:
                result = device.channels[0].measure_impedance()
                results.append(result)
                data_stream.put(result)
                set_voltage = round(set_voltage + self.__voltage_step * (-1) ** inverse, self.__round_digit)
        return np.array(results, dtype=self.output_type)
