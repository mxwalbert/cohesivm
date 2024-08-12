import copy
import numpy as np
import multiprocessing as mp
from typing import Any, Tuple
from cohesivm.database import Dimensions, DatabaseDict
from cohesivm.interfaces import InterfaceType, Interface
from cohesivm.devices import Device
from cohesivm.measurements import Measurement
from cohesivm.channels import Channel, Voltmeter, VoltageSMU
from cohesivm.analysis import Analysis, result_buffer
from cohesivm.plots import XYPlot


class DemoInterfaceType(InterfaceType):
    """For testing purposes."""


class DemoInterface(Interface):
    _interface_type = DemoInterfaceType
    _contact_ids = ['0']
    _contact_positions = {'0': (0, 0)}
    _interface_dimensions = Dimensions.Point()

    def __init__(self):
        super().__init__(pixel_dimensions=Dimensions.Point())

    def _select_contact(self, contact_id: str):
        pass


class DemoMeasurement(Measurement):
    _name = 'demo'
    _interface_type = DemoInterfaceType
    _required_channels = [(VoltageSMU,)]
    _output_type = [('x', float), ('y', float)]

    def __init__(self):
        super().__init__({}, (1, 0))

    def run(self, device: Device, data_stream: mp.Queue):
        return np.array([0])


class DemoSourceMeasureUnitChannel(VoltageSMU):

    def __init__(self, identifier: str = None, settings: DatabaseDict = None) -> None:
        Channel.__init__(self, identifier, settings)

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

    def source_voltage_and_measure(self, voltage: float) -> Tuple[float, float]:
        pass


class DemoDevice(Device):
    def __init__(self, channels=None):
        if channels is None:
            channels = [DemoSourceMeasureUnitChannel()]
        super().__init__(channels)

    def _establish_connection(self) -> bool:
        return True


class DemoAnalysis(Analysis):

    def __init__(self, dataset, contact_positions=None):
        functions = {
            'Maximum': self.max,
            'Minimum': self.min,
            'Sum': self.sum,
            'Dot Product': self.dot_product,
            'Average': self.average
        }
        plots = {
            'Measurement': self.measurement,
            'Semilog': self.semilog
        }
        super().__init__(functions, plots, dataset, contact_positions)

    @result_buffer
    def max(self, contact_id):
        if self.data[contact_id].dtype.names is None:
            return max(self.data[contact_id])
        return max(self.data[contact_id][self.data[contact_id].dtype.names[1]])

    @result_buffer
    def min(self, contact_id):
        if self.data[contact_id].dtype.names is None:
            return min(self.data[contact_id])
        return min(self.data[contact_id][self.data[contact_id].dtype.names[1]])

    @result_buffer
    def sum(self, contact_id):
        if self.data[contact_id].dtype.names is None:
            return sum(self.data[contact_id])
        return sum(self.data[contact_id][self.data[contact_id].dtype.names[1]])

    @result_buffer
    def dot_product(self, contact_id):
        if self.data[contact_id].dtype.names is None:
            return sum(self.data[contact_id])
        return sum(self.data[contact_id][self.data[contact_id].dtype.names[0]]
                   * self.data[contact_id][self.data[contact_id].dtype.names[1]])

    @result_buffer
    def average(self, contact_id):
        if self.data[contact_id].dtype.names is None:
            return sum(self.data[contact_id]) / len(self.data[contact_id])
        return sum(self.data[contact_id][self.data[contact_id].dtype.names[-1]]) / len(self.data[contact_id])

    def measurement(self, contact_id):
        plot = XYPlot()
        plot.make_plot()
        data = copy.deepcopy(self.data[contact_id])
        plot.update_plot(data)
        return plot.figure

    def semilog(self, contact_id):
        plot = XYPlot()
        plot.make_plot()
        data = copy.deepcopy(self.data[contact_id])
        data[data.dtype.names[1]] = np.log(data[data.dtype.names[1]])
        plot.update_plot(data)
        return plot.figure
