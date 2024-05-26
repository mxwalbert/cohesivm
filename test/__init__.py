import numpy as np
import multiprocessing as mp
from typing import Any, Tuple
from cohesivm.database import Dimensions
from cohesivm.interfaces import InterfaceType, InterfaceABC
from cohesivm.devices import DeviceABC
from cohesivm.measurements import MeasurementABC
from cohesivm.channels import SourceMeasureUnitChannel, VoltmeterChannel
from cohesivm.analysis import AnalysisABC, result_buffer
from cohesivm.plots import XYPlot


class DemoInterface(InterfaceABC):
    _interface_type = InterfaceType.Demo1
    _pixel_ids = ['0']
    _pixel_positions = {'0': (0, 0)}
    _sample_dimensions = Dimensions.Point()

    def __init__(self):
        InterfaceABC.__init__(self, pixel_dimensions=Dimensions.Point())

    def _select_pixel(self, pixel: str):
        pass


class DemoMeasurement(MeasurementABC):
    _name = 'demo'
    _interface_type = InterfaceType.Demo1
    _required_channels = [(SourceMeasureUnitChannel, VoltmeterChannel)]
    _output_type = np.dtype([('x', float), ('y', float)])

    def __init__(self):
        MeasurementABC.__init__(self, {}, (1, 0))

    def run(self, device: DeviceABC, data_stream: mp.Queue):
        return np.array([0])


class DemoSourceMeasureUnitChannel(SourceMeasureUnitChannel):

    def __init__(self):
        SourceMeasureUnitChannel.__init__(self)

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
        pass


class DemoDevice(DeviceABC):
    def __init__(self, channels=None):
        if channels is None:
            channels = [DemoSourceMeasureUnitChannel()]
        DeviceABC.__init__(self, channels)

    def _establish_connection(self) -> bool:
        return True


class DemoAnalysis(AnalysisABC):

    def __init__(self, dataset, pixel_positions=None):
        functions = {
            'Maximum': self.max
        }
        plots = {
            'Semilog': self.semilog
        }
        AnalysisABC.__init__(self, functions, plots, dataset, pixel_positions)

    @result_buffer
    def max(self, pixel):
        if self.dataset[pixel].dtype.names is None:
            return max(self.dataset[pixel])
        return max(self.dataset[pixel][self.dataset[pixel].dtype.names[-1]])

    def semilog(self, pixel):
        plot = XYPlot()
        plot.make_plot()
        data = self.dataset[pixel].copy()
        data[data.dtype.names[1]] = np.log(data[data.dtype.names[1]])
        plot.update_plot(data)
        return plot.figure
