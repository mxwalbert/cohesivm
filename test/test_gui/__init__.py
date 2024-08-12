import time
import numpy as np
import multiprocessing as mp
from .. import DemoInterfaceType
from cohesivm.database import Dimensions
from cohesivm.interfaces import Interface
from cohesivm.devices import Device
from cohesivm.measurements import Measurement


class DemoInterface(Interface):
    _interface_type = DemoInterfaceType
    _interface_dimensions = Dimensions.Point()
    _contact_ids = ['11', '12', '21', '22']
    _contact_positions = {c: p for c, p in zip(_contact_ids, [(0, 1), (1, 1), (0, 0), (1, 0)])}

    def __init__(self):
        Interface.__init__(self, Dimensions.Point())

    def _select_contact(self, contact_id: str):
        pass


class DemoMeasurement(Measurement):
    _name = 'demo'
    _interface_type = DemoInterfaceType
    _required_channels = []
    _output_type = np.dtype([('x', float), ('y', float)])

    def __init__(self):
        Measurement.__init__(self, {}, (10, 2))

    def run(self, device: Device, data_stream: mp.Queue):
        results = []
        for i in range(10):
            result = (i, i*i)
            data_stream.put(result)
            results.append(result)
            time.sleep(1)
        return np.array(results)
