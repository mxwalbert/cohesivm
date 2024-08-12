import numpy as np
from typing import Tuple
from cohesivm.measurements.iv import CurrentVoltageCharacteristic
from .. import DemoSourceMeasureUnitChannel, DemoDevice


class DemoSourceMeasureUnitChannel2(DemoSourceMeasureUnitChannel):

    def source_voltage_and_measure(self, voltage: float) -> Tuple[float, float]:
        return voltage, 0.5*voltage


def test_iv():
    start_voltage = 0.
    end_voltage = 10.
    voltage_step = 0.1
    test_input = np.arange(start_voltage, end_voltage+voltage_step, voltage_step)
    test_output = np.array([(i, 0.5*i) for i in test_input], dtype=[('Voltage (V)', float), ('Current (A)', float)])
    measurement = CurrentVoltageCharacteristic(start_voltage, end_voltage, voltage_step)
    result = measurement.run(DemoDevice(channels=[DemoSourceMeasureUnitChannel2()]))
    assert len(result) == measurement.output_shape[0]
    assert np.allclose(result['Voltage (V)'], test_output['Voltage (V)'])
    assert np.allclose(result['Current (A)'], test_output['Current (A)'])
