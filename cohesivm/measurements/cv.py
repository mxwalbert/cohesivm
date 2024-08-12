"""Implements the Measurement class for obtaining the capacitance-voltage profile."""
from __future__ import annotations
import numpy as np
import multiprocessing as mp
from typing import Union
from cohesivm.interfaces import HighLow
from cohesivm.measurements import Measurement
from cohesivm.devices import Device
from cohesivm.channels import LCRMeter
from cohesivm.data_stream import FakeQueue


class CapacitanceVoltageProfiling(Measurement):
    """A Measurement class for obtaining the capacitance-voltage characteristic of a device.

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

    _interface_type = HighLow
    _required_channels = [(LCRMeter,)]
    _output_type = [('Magnitude (1)', float), ('Phase (deg)', float)]

    def __init__(self, frequency: float, start_voltage: float, end_voltage: float, voltage_step: float,
                 oscillator_voltage: Union[float, False], oscillator_current: Union[float, False] = False) -> None:
        if voltage_step <= 0:
            raise ValueError('Voltage step must be larger than 0!')
        if oscillator_voltage is False and oscillator_current is False:
            raise ValueError('One of `oscillator_voltage` or `oscillator_current` must be set!')
        self._frequency = frequency
        self._start_voltage = start_voltage
        self._end_voltage = end_voltage
        self._voltage_step = voltage_step
        self._oscillator_voltage = oscillator_voltage
        self._oscillator_current = oscillator_current
        settings = {
            'frequency': frequency,
            'start_voltage': start_voltage,
            'end_voltage': end_voltage,
            'voltage_step': voltage_step,
            'oscillator_voltage': oscillator_voltage,
            'oscillator_current': oscillator_current
        }
        self._round_digit = self._find_least_significant_digit(voltage_step)
        voltage_range = end_voltage - start_voltage if end_voltage > start_voltage else start_voltage - end_voltage
        data_length = int(np.floor(voltage_range / voltage_step) + 1)
        super().__init__(settings=settings, output_shape=(data_length, 2))

    @staticmethod
    def _find_least_significant_digit(number: float) -> int:
        number_str = str(float(number))
        decimal_position = number_str.find('.')
        return len(number_str) - decimal_position - 1

    def run(self, device: Device, data_stream: mp.Queue = None) -> np.ndarray:
        """Performs the measurement by iterating over the voltage range and returns the results as structured array.
        If a ``data_stream`` queue is provided, the results will also be sent there.

        :param device: An instance of a class which inherits the :class:`~cohesivm.devices.Device` and complies with
            the :attr:`~cohesivm.measurements.Measurement.required_channels`.
        :param data_stream: A queue-like object where the measurement results can be sent to, e.g., for real-time
            plotting of the measurement.
        :returns: A Numpy structured array with tuples of datapoints: ('Magnitude (1)', 'Phase (deg)').
        """
        if data_stream is None:
            data_stream = FakeQueue()
        results = []
        set_voltage = self._start_voltage
        inverse = 1 if self._start_voltage > self._end_voltage else 0
        with device.connect():
            if self._oscillator_voltage is False:
                device.channels[0].set_oscillator_current(self._oscillator_current)
            else:
                device.channels[0].set_oscillator_voltage(self._oscillator_voltage)
            device.channels[0].set_oscillator_frequency(self._frequency)
            while (set_voltage < self._end_voltage) ^ inverse or set_voltage == self._end_voltage:
                result = device.channels[0].measure_impedance()
                results.append(result)
                data_stream.put(result)
                set_voltage = round(set_voltage + self._voltage_step * (-1) ** inverse, self._round_digit)
        return np.array(results, dtype=self.output_type)
