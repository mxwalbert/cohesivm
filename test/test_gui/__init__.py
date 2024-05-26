import time
import numpy as np
import multiprocessing as mp
from cohesivm.database import Dimensions
from cohesivm.interfaces import InterfaceType, InterfaceABC
from cohesivm.devices import DeviceABC
from cohesivm.measurements import MeasurementABC
from cohesivm.channels import SourceMeasureUnitChannel, VoltmeterChannel


class DemoInterface(InterfaceABC):
    _interface_type = InterfaceType.Demo1
    _sample_dimensions = Dimensions.Point()
    _pixel_ids = ['11', '12', '21', '22']
    _pixel_positions = {pixel: position for pixel, position in zip(_pixel_ids, [(0, 1), (1, 1), (0, 0), (1, 0)])}

    def __init__(self):
        InterfaceABC.__init__(self, Dimensions.Point())

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
