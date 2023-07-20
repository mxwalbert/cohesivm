import pytest
import os
import time
import numpy as np
import multiprocessing as mp
from typing import Tuple, Any
from cohesivm import experiment, database
from cohesivm.interfaces import InterfaceType, InterfaceABC
from cohesivm.experiment import StateError, ExperimentState, CompatibilityError
from cohesivm.measurements import MeasurementABC
from cohesivm.devices import DeviceABC
from cohesivm.channels import ChannelABC, SourceMeasureUnitChannel, VoltmeterChannel
from cohesivm.database import Metadata, Dimensions


@pytest.fixture
def db():
    db = database.Database('test.hdf5')
    yield db
    os.remove(db.path)


class DemoSourceMeasureUnitChannel(ChannelABC, SourceMeasureUnitChannel):

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
    def __init__(self):
        DeviceABC.__init__(self, [DemoSourceMeasureUnitChannel()])

    def _establish_connection(self) -> bool:
        return True


class DemoDevice2(DemoDevice):
    def __init__(self):
        DemoDevice.__init__(self)
        self._channels = []


class DemoMeasurement(MeasurementABC):
    _name = 'demo'
    _interface_type = InterfaceType.Demo1
    _required_channels = [(SourceMeasureUnitChannel, VoltmeterChannel)]
    _output_type = np.dtype([('x', float), ('y', float)])

    def __init__(self):
        MeasurementABC.__init__(self, {}, (1, 0))

    def run(self, device: DeviceABC, data_stream: mp.Queue):
        return np.array([0])


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


class DemoInterface(InterfaceABC):
    _interface_type = InterfaceType.Demo1
    _pixels = ['0']
    _sample_layout = {'0': np.array([0, 0])}
    _sample_dimensions = Dimensions.Point()

    def __init__(self):
        InterfaceABC.__init__(self, pixel_dimensions=Dimensions.Point())

    def _select_pixel(self, pixel: str):
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
    def test_setup(self, db, demo_experiment):
        metadata = Metadata(
            measurement=demo_experiment.measurement.name,
            measurement_settings=demo_experiment.measurement.settings,
            sample_id=demo_experiment.sample_id,
            device=demo_experiment.device.name,
            channels=demo_experiment.device.channels_names,
            channels_settings=demo_experiment.device.channels_settings,
            interface=demo_experiment.interface.name,
            sample_dimensions=Dimensions.Point(),
            sample_layout=demo_experiment.interface.sample_layout,
            pixel_dimensions=Dimensions.Point()
        )

        for state in [ExperimentState.READY, ExperimentState.RUNNING]:
            with pytest.raises(StateError):
                demo_experiment._state = state
                demo_experiment.setup()

        demo_experiment._state = ExperimentState.INITIAL
        demo_experiment.setup()
        assert demo_experiment.dataset == f'/{demo_experiment.measurement.name}/{metadata.settings_string}/{db._timestamp}-{demo_experiment.sample_id}'
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
