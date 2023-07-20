from __future__ import annotations
import pytest
import numpy as np
from decimal import Decimal
from typing import List
from cohesivm import config
from cohesivm.devices.agilent import Agilent4284ALCRChannel
from cohesivm.devices.ossila import OssilaX200, OssilaX200SMUChannel, OssilaX200VsenseChannel


smu1 = OssilaX200SMUChannel()
smu2 = OssilaX200SMUChannel('smu2')
smu3 = OssilaX200SMUChannel()
smu3._identifier = 'smu3'
vsense1 = OssilaX200VsenseChannel()
vsense2 = OssilaX200VsenseChannel('vsense2')


class TestConfiguration:

    cases_smu_channel_exceptions = [
        ('test', 1, 5, 1, ValueError),
        ('smu1', 1., 5, 1, TypeError),
        ('smu1', -1, 5, 1, ValueError),
        ('smu1', 1, 20, 1, ValueError),
        ('smu1', 1, 5, 0, ValueError)
    ]

    @pytest.mark.parametrize("identifier, s_filter, s_osr, s_range, expected", cases_smu_channel_exceptions)
    def test_smu_channel_exceptions(self, identifier, s_filter, s_osr, s_range, expected):
        with pytest.raises(expected):
            OssilaX200SMUChannel(
                identifier=identifier,
                s_filter=s_filter,
                s_osr=s_osr,
                s_range=s_range
            )

    cases_vsense_channel_exceptions = [
        ('test', 5, ValueError),
        ('vsense1', 20, ValueError)
    ]

    @pytest.mark.parametrize("identifier, s_osr, expected", cases_vsense_channel_exceptions)
    def test_vsense_channel_exceptions(self, identifier, s_osr, expected):
        with pytest.raises(expected):
            OssilaX200VsenseChannel(
                identifier=identifier,
                s_osr=s_osr
            )

    cases_device_exceptions = [
        # duplicate channels
        ([smu1, smu1], ValueError),
        # duplicate channels
        ([vsense1, vsense1], ValueError),
        # too many channels
        ([smu1, smu2, vsense1, vsense2, smu3], ValueError),
        # not OssilaX200Channel
        ([Agilent4284ALCRChannel()], TypeError)
    ]

    @pytest.mark.parametrize("channels, expected", cases_device_exceptions)
    def test_device_exceptions(self, channels, expected):
        with pytest.raises(expected):
            OssilaX200(channels=channels)

    cases_change_setting_exceptions = [
        # wrong type of filter
        (smu1, 'filter', 1., TypeError),
        # delay out of range
        (smu1, 'filter', -1, ValueError),
        # setting not available on channel
        (vsense1, 'filter', 1, KeyError),
        # no device connection established
        (smu1, 'filter', 1, RuntimeError)
    ]

    @pytest.mark.parametrize("channel, setting_key, setting_value, expected", cases_change_setting_exceptions)
    def test_change_setting_exceptions(self, channel, setting_key, setting_value, expected):
        with pytest.raises(expected):
            channel.change_setting(setting_key, setting_value)


class DemoConnection:
    class Setter:
        pass

    def __init__(self):
        self.get = self
        self.set = DemoConnection.Setter()
        self._enabled = False
        self.set.enabled = self.set_enabled
        self._filter = 1
        self.set.filter = self.set_filter
        self._osr = 5
        self.set.osr = self.set_osr
        self._range = 1
        self.set.range = self.set_range
        self._voltage = 0.
        self.set.voltage = self.set_voltage
        self._resistance = 100
        self.set.resistance = self.set_resistance
        self.measure = self.measure

    def enabled(self):
        return self._enabled

    def set_enabled(self, value: bool, response):
        self._enabled = value

    def filter(self):
        return self._filter

    def set_filter(self, value: int, response):
        self._filter = value

    def osr(self):
        return self._osr

    def set_osr(self, value: int, response):
        self._osr = value

    def range(self):
        return self._range

    def set_range(self, value: int, response):
        self._range = value

    def voltage(self):
        return self._voltage

    def set_voltage(self, value: Decimal, response):
        self._voltage = float(value)

    def resistance(self):
        return self._resistance

    def set_resistance(self, value: float, response):
        self._resistance = value

    def measure(self) -> List[np.ndarray[float, float]]:
        return [np.array([self._voltage, self._voltage / self._resistance])]


class DemoOssilaX200(OssilaX200):

    def __init__(self, channels):
        OssilaX200.__init__(self, channels=channels)

    def _establish_connection(self) -> dict:
        return {
            'smu1': DemoConnection(),
            'smu2': DemoConnection(),
            'vsense1': DemoConnection(),
            'vsense2': DemoConnection()
        }


@pytest.mark.incremental
class TestOssilaDeviceAndChannels:
    """The tests within this class require a connected device."""

    try:
        connection_kwargs = config.get_section('OssilaX200')
    except KeyError:
        connection_kwargs = {}
    device = OssilaX200(channels=[smu1, vsense1], **connection_kwargs)

    def test_connection(self):
        try:
            with self.device.connect():
                pass
        except Exception as exc:
            assert False, f"Establishing the connection failed: '{exc}'. The following tests which rely on the " \
                          f"connection will be skipped."

    def test_initialization(self):
        with self.device.connect():
            assert self.device.channels[0].get_property('filter') == self.device.channels[0].settings['filter']
            assert self.device.channels[0].get_property('osr') == self.device.channels[0].settings['osr']
            assert self.device.channels[0].get_property('range') == self.device.channels[0].settings['range']
            assert self.device.channels[1].get_property('osr') == self.device.channels[1].settings['osr']

    def test_change_setting(self):
        with self.device.connect():
            new_filter = 2
            self.device.channels[0].change_setting('filter', new_filter)
            assert self.device.channels[0].get_property('filter') == new_filter
            new_osr = 4
            self.device.channels[1].change_setting('osr', new_osr)
            assert self.device.channels[1].get_property('osr') == new_osr

    def test_smu_measure_voltage(self):
        with self.device.connect():
            result = self.device.channels[0].measure_voltage()
            assert isinstance(result, float)

    def test_smu_measure_current(self):
        with self.device.connect():
            result = self.device.channels[0].measure_current()
            assert isinstance(result, float)

    def test_smu_source_voltage(self):
        with self.device.connect():
            try:
                self.device.channels[0].source_voltage(0.)
            except Exception as exc:
                assert False, f"Setting a voltage failed: '{exc}'"

    def test_smu_source_and_measure(self):
        with self.device.connect():
            result = self.device.channels[0].source_and_measure(0.)
            assert type(result) == tuple
            assert len(result) == 2
            assert all([isinstance(value, float) for value in result])

    def test_vsense_measure_voltage(self):
        with self.device.connect():
            result = self.device.channels[1].measure_voltage()
            assert isinstance(result, float)
