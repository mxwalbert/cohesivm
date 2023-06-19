import contextlib
import numpy as np
from queue import Queue
from typing import Tuple
from cohesivm import experiment, database, InterfaceType
from cohesivm.abcs import CompatibilityError, DeviceABC, MeasurementABC, InterfaceABC, StateError, ExperimentState
import pytest
import os
from cohesivm.channels import SourceMeasureUnitChannel, VoltmeterChannel
from cohesivm.database import Metadata
import time


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
        return np.array([0])


class DemoMeasurement2(DemoMeasurement):
    _required_channels = [(VoltmeterChannel,)]

    def __init__(self):
        DemoMeasurement.__init__(self)


class DemoMeasurement3(DemoMeasurement):

    def __init__(self):
        DemoMeasurement.__init__(self)

    def run(self, device: DeviceABC, data_stream: Queue):
        while True:
            pass


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


@pytest.fixture
def demo_experiment(db):
    return experiment.Experiment(
        database=db,
        device=DemoDevice(),
        measurement=DemoMeasurement(),
        interface=DemoInterface(),
        sample_id='Test',
        selected_pixels=['0']
    )


@pytest.fixture
def demo_experiment2(db):
    return experiment.Experiment(
        database=db,
        device=DemoDevice(),
        measurement=DemoMeasurement3(),
        interface=DemoInterface(),
        sample_id='Test',
        selected_pixels=['0']
    )


class TestExperiment:
    cases_state_error = [
        ExperimentState.READY,
        ExperimentState.RUNNING,
        ExperimentState.FINISHED,
        ExperimentState.ABORTED
    ]

    @pytest.mark.parametrize("state", cases_state_error)
    def test_setup(self, db, demo_experiment, state):
        metadata = Metadata(
            measurement=demo_experiment.measurement.name,
            settings=demo_experiment.measurement.settings,
            sample_id=demo_experiment.sample_id,
            sample_layout=demo_experiment.interface.sample_layout,
        )

        with pytest.raises(StateError):
            demo_experiment._state = state
            demo_experiment.setup()

        demo_experiment._state = ExperimentState.INITIAL
        demo_experiment.setup()
        assert demo_experiment.dataset == f'/{demo_experiment.measurement.name}/{metadata.settings_string}/{db._timestamp}-{demo_experiment.sample_id}'
        assert demo_experiment.state == ExperimentState.READY

    def test_start_and_execute(self, demo_experiment):
        with pytest.raises(StateError):
            demo_experiment.start()

        demo_experiment.setup()
        demo_experiment.start()
        try:
            demo_experiment.process.join()
        except AssertionError:
            pass
        assert demo_experiment.state == ExperimentState.FINISHED

    def test_abort(self, demo_experiment2):
        demo_experiment2.setup()
        demo_experiment2.start()
        time.sleep(1)
        demo_experiment2.abort()
        assert demo_experiment2.state == ExperimentState.ABORTED
