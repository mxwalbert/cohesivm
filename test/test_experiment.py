import pytest
import os
import time
import multiprocessing as mp
from cohesivm import experiment, database, CompatibilityError
from cohesivm.interfaces import InterfaceType
from cohesivm.experiment import StateError, ExperimentState
from cohesivm.devices import DeviceABC
from cohesivm.channels import VoltmeterChannel
from cohesivm.database import Metadata, Dimensions
from . import DemoDevice, DemoMeasurement, DemoInterface


@pytest.fixture
def db():
    db = database.Database('test.hdf5')
    yield db
    os.remove(db.path)


class DemoDevice2(DemoDevice):
    def __init__(self):
        DemoDevice.__init__(self)
        self._channels = []


class DemoMeasurement2(DemoMeasurement):
    _required_channels = [(VoltmeterChannel,)]

    def __init__(self):
        DemoMeasurement.__init__(self)


class DemoMeasurement3(DemoMeasurement):

    def __init__(self):
        DemoMeasurement.__init__(self)

    def run(self, device: DeviceABC, data_stream: mp.Queue):
        while True:
            pass


class DemoInterface2(DemoInterface):
    _interface_type = InterfaceType.Demo2


cases_compatibility_error = [
    (DemoInterface2(), DemoDevice(), DemoMeasurement(), ['0']),
    (DemoInterface(), DemoDevice2(), DemoMeasurement(), ['0']),
    (DemoInterface(), DemoDevice(), DemoMeasurement2(), ['0']),
    (DemoInterface(), DemoDevice(), DemoMeasurement(), ['0', '1'])
]


@pytest.mark.parametrize("interface,device,measurement,pixel_ids", cases_compatibility_error)
def test_compatibility_error(db, interface, device, measurement, pixel_ids):
    with pytest.raises(CompatibilityError):
        experiment.Experiment(
            database=db,
            device=device,
            measurement=measurement,
            interface=interface,
            sample_id='Test',
            selected_pixels=pixel_ids
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
    def test_setup(self, db, demo_experiment):
        metadata = Metadata(
            measurement=demo_experiment.measurement.name,
            measurement_settings=demo_experiment.measurement.settings,
            sample_id=demo_experiment.sample_id,
            device=demo_experiment.device.name,
            channels=demo_experiment.device.channels_names,
            channels_settings=demo_experiment.device.channels_settings,
            interface=demo_experiment.interface.name,
            sample_dimensions=str(Dimensions.Point()),
            pixel_ids=demo_experiment.interface.pixel_ids,
            pixel_positions=list(demo_experiment.interface.pixel_positions.values()),
            pixel_dimensions=[str(Dimensions.Point()) for _ in demo_experiment.interface.pixel_ids]
        )

        for state in [ExperimentState.READY, ExperimentState.RUNNING]:
            with pytest.raises(StateError):
                demo_experiment._state = state
                demo_experiment.setup()

        demo_experiment._state = ExperimentState.INITIAL
        demo_experiment.setup()
        assert demo_experiment.dataset == f'/{demo_experiment.measurement.name}/{metadata.settings_hash}/{db._timestamp}-{demo_experiment.sample_id}'
        assert demo_experiment.state == ExperimentState.READY

    def test_preview_and_execute(self, demo_experiment):
        with pytest.raises(StateError):
            demo_experiment._state = ExperimentState.RUNNING
            demo_experiment.preview('0')
        demo_experiment._state = ExperimentState.INITIAL

        with pytest.raises(CompatibilityError):
            demo_experiment.preview('1')

        demo_experiment.preview('0')
        try:
            demo_experiment.process.join()
        except AssertionError:
            pass
        assert demo_experiment.state == ExperimentState.INITIAL

        demo_experiment.setup()
        demo_experiment.preview('0')
        try:
            demo_experiment.process.join()
        except AssertionError:
            pass
        assert demo_experiment.state == ExperimentState.READY

    def test_start_and_execute(self, demo_experiment):
        with pytest.raises(StateError):
            demo_experiment.start()

        for state in [ExperimentState.RUNNING, ExperimentState.FINISHED, ExperimentState.ABORTED]:
            with pytest.raises(StateError):
                demo_experiment._state = state
                demo_experiment.start()

        demo_experiment._state = ExperimentState.INITIAL
        demo_experiment.setup()
        demo_experiment.start()
        try:
            demo_experiment.process.join()
        except AssertionError:
            pass
        assert demo_experiment.state == ExperimentState.FINISHED

    def test_running_abort(self, demo_experiment2):
        with pytest.raises(StateError):
            demo_experiment2.abort()

        for state in [ExperimentState.FINISHED, ExperimentState.ABORTED]:
            with pytest.raises(StateError):
                demo_experiment2._state = state
                demo_experiment2.abort()

        demo_experiment2._state = ExperimentState.INITIAL
        demo_experiment2.setup()
        demo_experiment2.start()
        time.sleep(1)
        demo_experiment2.abort()
        assert demo_experiment2.state == ExperimentState.ABORTED

        demo_experiment2.preview('0')
        time.sleep(1)
        demo_experiment2.abort()
        assert demo_experiment2.state == ExperimentState.ABORTED

    def test_ready_abort(self, demo_experiment):
        demo_experiment.setup()
        demo_experiment.abort()
        assert demo_experiment.state == ExperimentState.INITIAL

        demo_experiment._state = ExperimentState.READY
        demo_experiment.abort()
        assert demo_experiment.state == ExperimentState.INITIAL
