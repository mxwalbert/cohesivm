from __future__ import annotations
import pytest
import configparser
from cohesivm import config
from cohesivm.devices.agilent.Agilent4284A import Agilent4284A, Agilent4284ALCRChannel
from cohesivm.devices.ossila import OssilaX200SMUChannel


class TestConfiguration:

    cases_lcr_channel_exceptions = [
        (-1, 'MEDIUM', 64, ValueError),
        (1, 'TEST', 64, ValueError),
        (1, 'MEDIUM', 3, ValueError)
    ]

    @pytest.mark.parametrize("s_trigger_delay, s_integration_time, s_averaging_rate, expected",
                             cases_lcr_channel_exceptions)
    def test_smu_channel_exceptions(self, s_trigger_delay, s_integration_time, s_averaging_rate, expected):
        with pytest.raises(expected):
            Agilent4284ALCRChannel(
                s_trigger_delay=s_trigger_delay,
                s_integration_time=s_integration_time,
                s_averaging_rate=s_averaging_rate
            )

    cases_device_exceptions = [
        # too many channels
        ([Agilent4284ALCRChannel(), Agilent4284ALCRChannel()], ValueError),
        # not Agilent4284ALCRChannel
        ([OssilaX200SMUChannel()], TypeError)
    ]

    @pytest.mark.parametrize("channels, expected", cases_device_exceptions)
    def test_device_exceptions(self, channels, expected):
        with pytest.raises(expected):
            Agilent4284A(channels=channels)

    cases_change_setting_exceptions = [
        # wrong type of trigger delay
        ('TRIGGER:DELAY', 'test', TypeError),
        # aperture format not correct
        ('APERTURE', 1, TypeError),
        ('APERTURE', 'SHORT,64,1', TypeError),
        ('APERTURE', 'SHORT', TypeError),
        # setting not available on channel
        ('s_trigger_delay', '1', KeyError),
        # no device connection established
        ('TRIGGER:DELAY', '1', RuntimeError)
    ]

    @pytest.mark.parametrize("setting_key, setting_value, expected", cases_change_setting_exceptions)
    def test_change_setting_exceptions(self, setting_key, setting_value, expected):
        lcr = Agilent4284ALCRChannel()
        with pytest.raises(expected):
            lcr.change_setting(setting_key, setting_value)


@pytest.mark.incremental
class TestAgilent4284ADeviceAndChannels:
    """The tests within this class require a connected device."""

    try:
        resource_name = config.get_option('Agilent4284A', 'resource_name')
    except configparser.NoSectionError:
        resource_name = ''
    device = Agilent4284A(channels=[Agilent4284ALCRChannel()], resource_name=resource_name)

    def test_connection(self):
        try:
            with self.device.connect():
                pass
        except Exception as exc:
            assert False, f"Establishing the connection failed: '{exc}'. The following tests which rely on the " \
                          f"connection will be skipped."

    def test_initialization(self):
        with self.device.connect():
            assert self.device.channels[0].get_property('TRIGGER:DELAY') == \
                   str(int(float(self.device.channels[0].settings['TRIGGER:DELAY'])))
            integration_times = {'SHOR': 'SHORT', 'MED': 'MEDIUM', 'LONG': 'LONG'}
            integration_time, averaging_rate = self.device.channels[0].get_property('APERTURE').split(',')
            assert f'{integration_times[integration_time]},{averaging_rate}' == \
                   self.device.channels[0].settings['APERTURE']
            assert ['OFF', 'ON'][int(self.device.channels[0].get_property('AMPLITUDE:ALC'))] == \
                   self.device.channels[0].settings['AMPLITUDE:ALC']

    def test_change_setting(self):
        with self.device.connect():
            new_trigger_delay = 2
            self.device.channels[0].change_setting('TRIGGER:DELAY', new_trigger_delay)
            assert self.device.channels[0].get_property('TRIGGER:DELAY') == str(new_trigger_delay)

    def test_source_voltage(self):
        with self.device.connect():
            try:
                self.device.channels[0].source_voltage(0.)
            except Exception as exc:
                assert False, f"Setting a voltage failed: '{exc}'"

    def test_source_current(self):
        with self.device.connect():
            try:
                self.device.channels[0].source_current(0.)
            except Exception as exc:
                assert False, f"Setting a current failed: '{exc}'"

    def test_set_oscillator_frequency(self):
        with self.device.connect():
            try:
                self.device.channels[0].set_oscillator_frequency(1000)
            except Exception as exc:
                assert False, f"Setting an oscillator frequency failed: '{exc}'"

    def test_set_oscillator_voltage(self):
        with self.device.connect():
            try:
                self.device.channels[0].set_oscillator_voltage(0)
            except Exception as exc:
                assert False, f"Setting an oscillator voltage failed: '{exc}'"

    def test_set_oscillator_current(self):
        with self.device.connect():
            try:
                self.device.channels[0].set_oscillator_current(0)
            except Exception as exc:
                assert False, f"Setting an oscillator current failed: '{exc}'"

    def test_measure_impedance(self):
        with self.device.connect():
            result = self.device.channels[0].measure_impedance()
            assert type(result) == tuple
            assert len(result) == 2
