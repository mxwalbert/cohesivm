import time
import numpy as np
import multiprocessing as mp
from abc import ABC
from typing import Any
from typing import TypeVar, List
from typing import Tuple
from cohesivm.channels import Channel
from cohesivm.channels import CurrentSource, Voltmeter
from cohesivm.devices import Device
from cohesivm.interfaces import InterfaceType, Interface
from cohesivm.database import Dimensions
from cohesivm.measurements import Measurement
from cohesivm.data_stream import FakeQueue
import fpp_connect  # our mimetic API


TChannel = TypeVar('TChannel', bound='FPPChannel')


class FPPChannel(Channel, ABC):
    """Abstract class which implements the properties and methods which all FPP channels have in common."""

    def set_property(self, name: str, value: Any) -> None:
        self.connection.set(self.identifier, name, value)

    def get_property(self, name: str) -> Any:
        return self.connection.get(self.identifier, name)

    def enable(self) -> None:
        self.set_property('ENABLE', True)

    def disable(self) -> None:
        self.set_property('DISABLE', True)


class CurrentSourceChannel(FPPChannel, CurrentSource):
    """A current source channel of the mimetic four point probe.

    :param auto_range: Setting if the current range should be set automatically.
    :param max_voltage: Limit for the voltage which is passed through the measured device.
    :raises TypeError: If the types of the parameters are wrong.
    :raises ValueError: If the ``max_voltage`` is not between 1e-4 and 10 V.
    """

    def __init__(self, auto_range: bool = True, max_voltage: float = 10.) -> None:
        identifier = 'CS'
        settings = {
            'AR': auto_range,
            'MV': max_voltage
        }
        super().__init__(identifier, settings)

    def _check_settings(self) -> None:
        if type(self.settings['AR']) is not bool:
            raise TypeError
        if type(self.settings['MV']) is not float:
            raise TypeError
        if not 1e-4 <= self.settings['MV'] <= 10.:
            raise ValueError

    def enable(self) -> None:
        self.source_current(0.)
        super().enable()

    def source_current(self, current: float) -> None:
        if type(current) is not float:
            raise TypeError
        if abs(current) > 0.2:
            raise ValueError
        self.set_property('SOURCE', current)


class VoltmeterChannel(FPPChannel, Voltmeter):
    """A voltmeter channel of the mimetic four point probe."""

    def __init__(self) -> None:
        identifier = 'VM'
        settings = None
        super().__init__(identifier, settings)

    def _check_settings(self) -> None:
        return None

    def measure_voltage(self) -> float:
        return self.get_property('MEASURE')


class FPPDevice(Device):
    """Implements the mimetic four point probe.

    :param com_port: The COM port where the FPP device is connected.
    :param channels: List of channels which are subclasses of the :class:`FPPChannel`. Could be a single channel or
    both. Duplicates are not allowed.
    :raises TypeError: If a channel is not a :class:`FPPChannel`.
    :raises ValueError: If duplicate channels are provided.
    """

    def __init__(self, com_port: str, channels: List[TChannel] = None) -> None:
        if channels is None:
            channels = [CurrentSourceChannel(), VoltmeterChannel()]
        else:
            channel_identifiers = set()
            for channel in channels:
                if not isinstance(channel, FPPChannel):
                    raise TypeError
                channel_identifiers.add(channel.identifier)
            if len(channels) != len(channel_identifiers):
                raise ValueError
        self.com_port = com_port
        super().__init__(channels)

    def _establish_connection(self) -> fpp_connect.Device:
        return fpp_connect.Device(self.com_port)


class FPPInterfaceType(InterfaceType):
    """Consists of two pairs of terminals which can be connected to two different device channels, e.g., one DC
    current source and one voltmeter."""


class FPP2X2(Interface):
    """This interface is an array of 2x2 measurement points, each of which consists of two contact pairs to act
    as a four-point probe.

    :param com_port: The COM port where the FPP interface is connected.
    """

    _interface_type = FPPInterfaceType
    _contact_ids = ['BL', 'BR', 'TL', 'TR']
    _contact_positions = {
        'BL': (10., 10.),
        'BR': (30., 10.),
        'TL': (10., 30.),
        'TR': (30., 30.)
    }
    _interface_dimensions = Dimensions.Rectangle(40., 40.)

    def __init__(self, com_port: str) -> None:
        super().__init__(Dimensions.Generic([-3., -1., 1., 3.], [0., 0., 0., 0.]))
        self.interface_hw = fpp_connect.Interface(com_port)

    def _select_contact(self, contact_id: str) -> None:
        self.interface_hw.select(contact_id)


class FPPMeasurement(Measurement):
    """A class for performing four point probe measurements at multiple currents.

    :param currents: The currents in A which should be sources to measure the voltage.
    :param temperature: The temperature of the sample during the measurement in K.
    :param film_thickness: The thickness of the measured conductive film in mm.
    """

    _interface_type = FPPInterfaceType
    _required_channels = [(CurrentSource,), (Voltmeter,)]
    _output_type = [('Current (A)', float), ('Voltage (V)', float)]

    def __init__(self, currents: Tuple[float, ...], temperature: float, film_thickness: float = None) -> None:
        self._currents = currents
        settings = {
            'currents': currents,
            'temperature': temperature,
            'film_thickness': film_thickness
        }
        super().__init__(settings=settings, output_shape=(len(currents), 2))

    def run(self, device: Device, data_stream: mp.Queue = None) -> np.ndarray:
        if data_stream is None:
            data_stream = FakeQueue()
        results = []
        with device.connect():
            for current in self._currents:
                device.channels[0].source_current(current)
                result = current, device.channels[1].measure_voltage()
                data_stream.put(result)
                results.append(result)
                time.sleep(1)  # for running the measurement in the GUI
        time.sleep(2)
        return np.array(results, dtype=self.output_type)
