import contextlib
import numpy as np
from queue import Queue
from typing import Tuple
from cohesivm import experiment, database, InterfaceType
from cohesivm.abcs import CompatibilityError, DeviceABC, MeasurementABC, InterfaceABC
import pytest
import os
from cohesivm.channels import SourceMeasureUnitChannel, VoltmeterChannel


@pytest.fixture
def db():
    db = database.Database('test.hdf5')
    yield db
    os.remove(db.path)


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
        DeviceABC.__init__(self, [DemoSourceMeasureUnitChannel()], {})

    @contextlib.contextmanager
    def connect(self):
        print('connected')
        yield
        print('disconnected')


class DemoDevice2(DemoDevice):
    def __init__(self):
        DemoDevice.__init__(self)
        self._channels = []


class DemoMeasurement(MeasurementABC):
    _name = 'demo'
    _interface_type = InterfaceType.Demo1
    _required_channels = [(SourceMeasureUnitChannel, VoltmeterChannel)]

    def __init__(self):
        MeasurementABC.__init__(self, {})

    def run(self, device: DeviceABC, data_stream: Queue):
        pass


class DemoMeasurement2(DemoMeasurement):
    _required_channels = [(VoltmeterChannel,)]

    def __init__(self):
        DemoMeasurement.__init__(self)


class DemoInterface(InterfaceABC):
    _interface_type = InterfaceType.Demo1
    _pixels = ['0']
    _sample_layout = {'0': np.array([0, 0])}

    def select_pixel(self, pixel: str):
        pass


class DemoInterface2(DemoInterface):
    _interface_type = InterfaceType.Demo2


cases_compatibility_error = [
    (DemoInterface2(), DemoDevice(), DemoMeasurement(), ['0']),
    (DemoInterface(), DemoDevice2(), DemoMeasurement(), ['0']),
    (DemoInterface(), DemoDevice(), DemoMeasurement2(), ['0']),
    (DemoInterface(), DemoDevice(), DemoMeasurement(), ['0', '1'])
]


@pytest.mark.parametrize("interface,device,measurement,pixels", cases_compatibility_error)
def test_compatibility_error(db, interface, device, measurement, pixels):
    with pytest.raises(CompatibilityError):
        experiment.Experiment(
            database=db,
            device=device,
            measurement=measurement,
            interface=interface,
            sample_id='Test',
            selected_pixels=pixels
        )


class TestExperiment:

    def __init__(self, db):
        self.demo_experiment = experiment.Experiment(
            database=db,
            device=DemoDevice(),
            measurement=DemoMeasurement(),
            interface=DemoInterface(),
            sample_id='Test',
            selected_pixels=['0']
        )

    def test_setup(self):
        self.demo_experiment.setup()
