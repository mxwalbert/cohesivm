"""Implements the Measurement class for obtaining the current-voltage characteristic."""
from __future__ import annotations
import numpy as np
import multiprocessing as mp
import time
from ..interfaces import InterfaceType
from ..measurements import MeasurementABC
from ..devices import DeviceABC
from ..channels import VoltageSMU, SweepVoltageSMU
from ..data_stream import FakeQueue


class CurrentVoltageCharacteristic(MeasurementABC):
    """A Measurement class for obtaining the current-voltage characteristic of a device."""

    _interface_type = InterfaceType.HI_LO
    _required_channels = [(VoltageSMU, SweepVoltageSMU)]
    _output_type = [('Voltage (V)', float), ('Current (A)', float)]

    def __init__(self, start_voltage: float, end_voltage: float, voltage_step: float, hysteresis: bool = False,
                 illuminated: bool = True, power_in: float = 0.001):
        """Initializes the measurement for current-voltage characteristic measurements and stores the settings in the
        property `settings` which can be used to create a Metadata object.

        :param start_voltage: Begin of the measurement range in V.
        :param end_voltage: End of the measurement range in V.
        :param voltage_step: Voltage change for each datapoint in V. Must be larger than 0.
        :param hysteresis: Flags if the voltage range should be measured a second time in reverse order directly after
            the initial measurement.
        :param illuminated: Flags if the measurement is conducted under illumination.
        :param power_in: The power of the input radiation source which is used for the efficiency calculation in W/mm^2.
        :raises ValueError: If `voltage_step` is not larger than 0.
        """
        if voltage_step <= 0:
            raise ValueError('Voltage step must be larger than 0!')
        self._start_voltage = start_voltage
        self._end_voltage = end_voltage
        self._voltage_step = voltage_step
        self._hysteresis = hysteresis
        settings = {
            'start_voltage': start_voltage,
            'end_voltage': end_voltage,
            'voltage_step': voltage_step,
            'hysteresis': hysteresis,
            'illuminated': illuminated,
            'power_in': power_in
        }
        self._round_digit = self.find_least_significant_digit(voltage_step)
        voltage_range = end_voltage - start_voltage if end_voltage > start_voltage else start_voltage - end_voltage
        data_length = int(round(voltage_range / voltage_step, self._round_digit) + 1)
        data_length = data_length * 2 if hysteresis else data_length
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
        :returns: A Numpy structured array with tuples of datapoints: ('Voltage (V)', 'Current (A)').
        """
        if data_stream is None:
            data_stream = FakeQueue()
        with device.connect():
            device.channels[0].enable()
            if isinstance(device.channels[0], SweepVoltageSMU) and device.channels[0].use_hw_sweep:
                results = device.channels[0].sweep_voltage_and_measure(
                    self._start_voltage, self._end_voltage, self._voltage_step, self._hysteresis)
                for result in results:
                    data_stream.put(result)
                    time.sleep(0.001)
            else:
                results = self._run(device, data_stream)
        return np.array(results, dtype=self.output_type)

    def _run(self, device: DeviceABC, data_stream: mp.Queue = None) -> list[tuple[float, float]]:
        results = []
        set_voltage = self._start_voltage
        inverse = 1 if self._start_voltage > self._end_voltage else 0
        while (set_voltage < self._end_voltage) ^ inverse or set_voltage == self._end_voltage:
            result = device.channels[0].source_voltage_and_measure(set_voltage)
            results.append(result)
            data_stream.put(result)
            set_voltage = round(set_voltage + self._voltage_step * (-1) ** inverse, self._round_digit)
        if self._hysteresis:
            set_voltage = round(set_voltage - self._voltage_step * (-1) ** inverse, self._round_digit)
            while (set_voltage > self._start_voltage) ^ inverse or set_voltage == self._start_voltage:
                result = device.channels[0].source_voltage_and_measure(set_voltage)
                results.append(result)
                data_stream.put(result)
                set_voltage = round(set_voltage - self._voltage_step * (-1) ** inverse, self._round_digit)
        return results
