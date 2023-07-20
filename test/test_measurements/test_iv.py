import numpy as np
from typing import Tuple, Any
from cohesivm.channels import ChannelABC, SourceMeasureUnitChannel
from cohesivm.devices import DeviceABC
from cohesivm.measurements.iv import CurrentVoltageCharacteristic


class DemoSourceMeasureUnitChannel(SourceMeasureUnitChannel, ChannelABC):

    def set_property(self, name: str, value: Any):
        pass

    def get_property(self, name: str) -> Any:
        pass

    def _check_settings(self):
        pass

    def enable(self):
        pass

    def disable(self):
        pass

    def measure_voltage(self) -> float:
        pass

    def measure_current(self) -> float:
        pass

    def source_voltage(self, voltage: float):
        pass

    def source_and_measure(self, voltage: float) -> Tuple[float, float]:
        return voltage, 0.5*voltage


class DemoDevice(DeviceABC):

    def __init__(self):
        DeviceABC.__init__(self, [DemoSourceMeasureUnitChannel()])

    def _establish_connection(self) -> bool:
        return True


def test_iv():
    start_voltage = 0.
    end_voltage = 10.
    voltage_step = 0.1
    test_input = np.arange(start_voltage, end_voltage+voltage_step, voltage_step)
    test_output = np.array([(i, 0.5*i) for i in test_input], dtype=[('Voltage (V)', float), ('Current (A)', float)])
    measurement = CurrentVoltageCharacteristic(start_voltage, end_voltage, voltage_step)
    result = measurement.run(DemoDevice())
    assert len(result) == measurement.output_shape[0]
    assert np.allclose(result['Voltage (V)'], test_output['Voltage (V)'])
    assert np.allclose(result['Current (A)'], test_output['Current (A)'])
