import contextlib
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


class TestSourceMeasureUnitChannel(SourceMeasureUnitChannel):

    def measure_voltage(self) -> float:
        pass

    def measure_current(self) -> float:
        pass

    def source_voltage(self, voltage: float):
        pass

    def source_and_measure(self, voltage: float) -> Tuple[float, float]:
        return voltage, 0.5 * voltage


class TestDevice(DeviceABC):
    def __init__(self):
        DeviceABC.__init__(self, [TestSourceMeasureUnitChannel()], {})

    @contextlib.contextmanager
    def connect(self):
        print('connected')
        yield
        print('disconnected')


class TestDevice2(TestDevice):
    def __init__(self):
        TestDevice.__init__(self)
        self._channels = []


class TestMeasurement(MeasurementABC):
    _name = 'test'
    _interface_type = InterfaceType.Test1
    _required_channels = [(SourceMeasureUnitChannel, VoltmeterChannel)]

    def __init__(self):
        MeasurementABC.__init__(self, {})

    def run(self, device: DeviceABC, data_stream: Queue):
        pass


class TestMeasurement2(TestMeasurement):
    _required_channels = [(VoltmeterChannel,)]

    def __init__(self):
        TestMeasurement.__init__(self)


class TestInterface(InterfaceABC):
    _interface_type = InterfaceType.Test1
    _pixels = ['0']

    def select_pixel(self, pixel: str):
        pass


class TestInterface2(TestInterface):
    _interface_type = InterfaceType.Test2


cases_compatibility_error = [
    (TestInterface2(), TestDevice(), TestMeasurement(), ['0']),
    (TestInterface(), TestDevice2(), TestMeasurement(), ['0']),
    (TestInterface(), TestDevice(), TestMeasurement2(), ['0']),
    (TestInterface(), TestDevice(), TestMeasurement(), ['0', '1'])
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
