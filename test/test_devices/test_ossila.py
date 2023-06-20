from __future__ import annotations

import contextlib
import pytest
import numpy as np
from decimal import Decimal
from typing import List, Tuple
from cohesivm import config
from cohesivm.channels import VoltmeterChannel
from cohesivm.devices.ossila import OssilaX200, OssilaX200SMUChannel, OssilaX200VsenseChannel


class DemoVoltmeterChannel(VoltmeterChannel):
    def measure_voltage(self) -> float:
        pass


smu1 = OssilaX200SMUChannel()
smu2 = OssilaX200SMUChannel('smu2', auto_range=True)
smu3 = OssilaX200SMUChannel()
smu3._identifier = 'smu3'
vsense1 = OssilaX200VsenseChannel()
vsense2 = OssilaX200VsenseChannel('vsense2')


class TestConfiguration:

    cases_smu_channel_exceptions = [
        ('test', 1000, 1, 5, 1, ValueError),
        ('smu1', -1, 1, 5, 1, ValueError),
        ('smu1', 1000, 1., 5, 1, TypeError),
        ('smu1', 1000, -1, 5, 1, ValueError),
        ('smu1', 1000, 1, 20, 1, ValueError),
        ('smu1', 1000, 1, 5, 0, ValueError)
    ]

    @pytest.mark.parametrize("identifier, s_delay, s_filter, s_osr, s_range, expected", cases_smu_channel_exceptions)
    def test_smu_channel_exceptions(self, identifier, s_delay, s_filter, s_osr, s_range, expected):
        with pytest.raises(expected):
            OssilaX200SMUChannel(
                identifier=identifier,
                s_delay=s_delay,
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
        ([DemoVoltmeterChannel()], TypeError)
    ]

    @pytest.mark.parametrize("channels, expected", cases_device_exceptions)
    def test_device_exceptions(self, channels, expected):
        with pytest.raises(expected):
            OssilaX200(channels=channels)

    cases_change_setting_exceptions = [
        # wrong type of delay
        (smu1, 'delay', 1000, TypeError),
        # delay out of range
        (smu1, 'delay', Decimal(-1), ValueError),
        # setting not available on channel
        (vsense1, 'delay', Decimal(1000), KeyError),
        # no device connection established
        (smu1, 'delay', Decimal(1000), RuntimeError)
    ]

    @pytest.mark.parametrize("channel, setting_key, setting_value, expected", cases_change_setting_exceptions)
    def test_change_setting_exceptions(self, channel, setting_key, setting_value, expected):
        with pytest.raises(expected):
            channel.change_setting(setting_key, setting_value)


class DemoOssilaX200SMUChannel(OssilaX200SMUChannel):
    # current_ranges = (200e-3, 20e-3, 2e-3, 200e-6, 20e-6, 0.)

    voltage_current_pairs = {
        Decimal(0.): 100e-3,
        Decimal(1.): 10e-3,
        Decimal(2.): 1e-3,
        Decimal(3.): 100e-6,
        Decimal(4.): 10e-6,
        Decimal(5.): 1e-6
    }

    class Connection:

        class Set:
            pass

        set = Set()

    def __init__(self):
        OssilaX200SMUChannel.__init__(self, auto_range=True)
        self.range = 1
        self.voltage = Decimal(0)
        self._connection = {self.identifier: DemoOssilaX200SMUChannel.Connection()}
        self._connection[self.identifier].set.enabled = self.set_enabled
        self._connection[self.identifier].set.range = self.set_range
        self._connection[self.identifier].set.voltage = self.set_voltage
        self._connection[self.identifier].measurei = self.measurei
        self._connection[self.identifier].oneshot = self.oneshot

    def set_enabled(self, value: bool, response):
        pass

    def set_range(self, value: int, response):
        self.range = value

    def set_voltage(self, value: Decimal, response):
        self.voltage = value

    def measurei(self) -> List[float]:
        return [self.voltage_current_pairs[self.voltage]]

    def oneshot(self, value: Decimal) -> List[Tuple[float, float]]:
        return [(float(value), self.voltage_current_pairs[value])]


class DemoOssilaX200(OssilaX200):
    def __init__(self, channels):
        OssilaX200.__init__(self, channels=channels)

    @contextlib.contextmanager
    def connect(self):
        yield


def test_smu_auto_range():
    channel = DemoOssilaX200SMUChannel()
    device = DemoOssilaX200([channel])
    with device.connect():
        for i in range(6):
            assert device.channels[0].source_and_measure(float(i)) == \
                   (float(Decimal(i)), channel.voltage_current_pairs[Decimal(i)])
            if i < 5:
                assert channel.range == i + 1
            else:
                assert channel.range == i


@pytest.mark.incremental
class TestOssilaDeviceAndChannels:
    """The tests within this class require a connected device."""

    device = OssilaX200(channels=[smu1, vsense1], **config.get_section('OssilaX200'))

    def test_connection(self):
        try:
            with self.device.connect():
                pass
        except Exception as exc:
            assert False, f"Establishing the connection failed: '{exc}'. The following tests which rely on the " \
                          f"connection will be skipped."

    def test_initialization(self):
        with self.device.connect():
            assert Decimal(self.device.channels[0]._get_property('delay')) == self.device.channels[0].settings['delay']
            assert self.device.channels[0]._get_property('filter') == self.device.channels[0].settings['filter']
            assert self.device.channels[0]._get_property('osr') == self.device.channels[0].settings['osr']
            assert self.device.channels[0]._get_property('range') == self.device.channels[0].settings['range']
            assert self.device.channels[1]._get_property('osr') == self.device.channels[1].settings['osr']

    def test_change_setting(self):
        with self.device.connect():
            new_delay = Decimal(2000)
            self.device.channels[0].change_setting('delay', new_delay)
            assert self.device.channels[0]._get_property('delay') == new_delay
            new_osr = 4
            self.device.channels[1].change_setting('osr', new_osr)
            assert self.device.channels[1]._get_property('osr') == new_osr

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
            assert type(result) == np.ndarray
            assert len(result) == 2

    def test_vsense_measure_voltage(self):
        with self.device.connect():
            result = self.device.channels[1].measure_voltage()
            assert isinstance(result, float)
