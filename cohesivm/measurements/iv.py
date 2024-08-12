"""Implements the Measurement class for obtaining the current-voltage characteristic."""
from __future__ import annotations
import numpy as np
import multiprocessing as mp
import time
from cohesivm.interfaces import HighLow
from cohesivm.measurements import Measurement
from cohesivm.devices import Device
from cohesivm.channels import VoltageSMU, SweepVoltageSMU
from cohesivm.data_stream import FakeQueue


class CurrentVoltageCharacteristic(Measurement):
    """A measurement class for obtaining the current-voltage characteristic.

    Performs the measurement by iterating over the voltage range. The results are returned as structured array with
    datapoint tuples: ('Voltage (V)', 'Current (A)').

    :param start_voltage: Begin of the measurement range in V.
    :param end_voltage: End of the measurement range in V.
    :param voltage_step: Voltage change for each datapoint in V. Must be larger than 0.
    :param hysteresis: Flags if the voltage range should be measured a second time in reverse order directly after
        the initial measurement.
    :param illuminated: Flags if the measurement is conducted under illumination.
    :param power_in: The power of the input radiation source which is used for the efficiency calculation in W/mm^2.
    :raises ValueError: If ``voltage_step`` is not larger than 0.
    """

    _interface_type = HighLow
    _required_channels = [(VoltageSMU, SweepVoltageSMU)]
    _output_type = [('Voltage (V)', float), ('Current (A)', float)]

    def __init__(self, start_voltage: float, end_voltage: float, voltage_step: float, hysteresis: bool = False,
                 illuminated: bool = True, power_in: float = 0.001) -> None:
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
        self._round_digit = self._find_least_significant_digit(voltage_step)
        voltage_range = end_voltage - start_voltage if end_voltage > start_voltage else start_voltage - end_voltage
        data_length = int(round(voltage_range / voltage_step, self._round_digit) + 1)
        data_length = data_length * 2 if hysteresis else data_length
        super().__init__(settings=settings, output_shape=(data_length, 2))

    @staticmethod
    def _find_least_significant_digit(number: float) -> int:
        number_str = str(float(number))
        decimal_position = number_str.find('.')
        return len(number_str) - decimal_position - 1

    def run(self, device: Device, data_stream: mp.Queue = None) -> np.ndarray:
        if data_stream is None:
            data_stream = FakeQueue()
        with device.connect():
            if isinstance(device.channels[0], SweepVoltageSMU):
                results = device.channels[0].sweep_voltage_and_measure(
                    self._start_voltage, self._end_voltage, self._voltage_step, self._hysteresis)
                for result in results:
                    data_stream.put(result)
                    time.sleep(0.001)
            else:
                results = self._run(device, data_stream)
        return np.array(results, dtype=self.output_type)

    def _run(self, device: Device, data_stream: mp.Queue = None) -> list[tuple[float, float]]:
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
