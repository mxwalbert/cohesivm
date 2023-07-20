from __future__ import annotations

import time
import numpy as np
import multiprocessing as mp
from typing import Tuple, Dict

from cohesivm.database import Dimensions
from cohesivm.interfaces import InterfaceType, InterfaceABC
from cohesivm.devices import DeviceABC
from cohesivm.measurements import MeasurementABC
from cohesivm.channels import SourceMeasureUnitChannel, VoltmeterChannel


class DemoInterface(InterfaceABC):
    _interface_type = InterfaceType.Demo1
    _pixels = ['11', '12', '21', '22']
    _sample_layout = {
        '11': np.array([0, 0]),
        '12': np.array([1, 0]),
        '21': np.array([0, -1]),
        '22': np.array([1, -1])
    }
    _sample_dimensions = Dimensions.Point()

    def __init__(self, pixel_dimensions: Dimensions.Shape | Dict[str, Dimensions.Shape]):
        InterfaceABC.__init__(self, pixel_dimensions)

    def _select_pixel(self, pixel: str):
        pass


class DemoMeasurement(MeasurementABC):
    _name = 'demo'
    _interface_type = InterfaceType.Demo1
    _required_channels = [(SourceMeasureUnitChannel, VoltmeterChannel)]
    _output_type = np.dtype([('x', float), ('y', float)])

    def __init__(self):
        MeasurementABC.__init__(self, {}, (10, 2))

    def run(self, device: DeviceABC, data_stream: mp.Queue):
        results = []
        for i in range(10):
            result = (i, i*i)
            data_stream.put(result)
            results.append(result)
            time.sleep(1)
        return np.array(results)


class DemoSourceMeasureUnitChannel(SourceMeasureUnitChannel):

    def measure_voltage(self) -> float:
        pass

    def measure_current(self) -> float:
        pass

    def source_voltage(self, voltage: float):
        pass

    def source_and_measure(self, voltage: float) -> Tuple[float, float]:
        pass


class DemoDevice(DeviceABC):
    def __init__(self):
        DeviceABC.__init__(self, [DemoSourceMeasureUnitChannel()])

    def _establish_connection(self) -> bool:
        return True


