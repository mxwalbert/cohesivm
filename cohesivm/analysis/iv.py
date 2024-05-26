from __future__ import annotations
import copy
import numpy as np
from typing import Dict, Tuple
from . import AnalysisABC, result_buffer
from ..database import dataset_type, Dimensions
from ..plots import XYPlot


def handle_hysteresis(func):
    def wrapper(self, iv_array, *args, **kwargs):
        if self.hysteresis:
            midpoint = len(iv_array) // 2
            args0 = [arg[0] for arg in args]
            args1 = [arg[1] for arg in args]
            return np.array([
                func(self, iv_array[:midpoint], *args0, **kwargs),
                func(self, iv_array[midpoint:], *args1, **kwargs)
            ])
        return func(self, iv_array, *args, **kwargs)
    return wrapper


def current_density(func):
    def wrapper(self, pixel_id):
        if self.hysteresis:
            return (
                func(self, pixel_id)[0] / self.areas[pixel_id],
                func(self, pixel_id)[1] / self.areas[pixel_id]
            )
        return func(self, pixel_id) / self.areas[pixel_id]
    return wrapper


class CurrentVoltageCharacteristic(AnalysisABC):

    def __init__(self, dataset: Dict[str, np.ndarray] | dataset_type,
                 pixel_positions: Dict[str, Tuple[float, float]] = None,
                 areas: Dict[str, float] = None, hysteresis: bool = None,
                 illuminated: bool = None, power_in: float = None):

        functions = {
            'Open Circuit Voltage (V)': self.voc,
            'Short Circuit Current (A)': self.isc,
            'Short Circuit Current (mA)': self.isc_ma,
            'Short Circuit Current Density (A/mm^2)': self.jsc,
            'Short Circuit Current Density (mA/cm^2)': self.jsc_ma,
            'MPP Voltage (V)': self.mpp_v,
            'MPP Current (A)': self.mpp_i,
            'MPP Current (mA)': self.mpp_i_ma,
            'MPP Current Density (A/mm^2)': self.mpp_j,
            'MPP Current Density (mA/cm^2)': self.mpp_j_ma,
            'Fill Factor': self.ff,
            'Efficiency': self.eff,
            'Series Resistance (Ohm)': self.rs,
            'Shunt Resistance (Ohm)': self.rsh
        }

        plots = {
            'Semi-Log': self.semilog
        }

        AnalysisABC.__init__(self, functions, plots, dataset, pixel_positions)

        if self.metadata is not None:
            self.areas = {pixel: Dimensions.object_from_string(
                self.metadata.pixel_dimensions[self.metadata.pixel_ids.index(pixel)]
            ).area() for pixel in self.dataset.keys()} if areas is None else areas
            self.hysteresis = self.metadata.measurement_settings['hysteresis'] if hysteresis is None else hysteresis
            self.illuminated = self.metadata.measurement_settings['illuminated'] if illuminated is None else illuminated
            self.power_in = self.metadata.measurement_settings['power_in'] if power_in is None else power_in
        else:
            self.areas = {pixel: 1. for pixel in self.dataset.keys()} if areas is None else areas
            self.hysteresis = False if hysteresis is None else hysteresis
            self.illuminated = True if illuminated is None else illuminated
            self.power_in = 1. if power_in is None else power_in

        self.vl = 'Voltage (V)'
        self.il = 'Current (A)'

    @handle_hysteresis
    def find_intercept(self, iv_array: np.ndarray, transpose: bool):
        x = iv_array[self.vl]
        y = iv_array[self.il]
        if transpose:
            x, y = y, x
        (x_low, x_high), (y_low, y_high) = [[v[x <= 0], v[x >= 0]] for v in [x, y]]
        lower_bound, upper_bound = x_low.argmax(), x_high.argmin()
        return np.interp(0, [x_low[lower_bound], x_high[upper_bound]], [y_low[lower_bound], y_high[upper_bound]])

    @result_buffer
    def voc(self, pixel_id: str):
        return CurrentVoltageCharacteristic.find_intercept(self, self.dataset[pixel_id], transpose=True)

    @result_buffer
    def isc(self, pixel_id: str):
        return CurrentVoltageCharacteristic.find_intercept(self, self.dataset[pixel_id], transpose=False)

    def isc_ma(self, pixel_id: str):
        return self.isc(pixel_id) * 1000

    @result_buffer
    @current_density
    def jsc(self, pixel_id: str):
        return CurrentVoltageCharacteristic.isc(self, pixel_id)

    def jsc_ma(self, pixel_id: str):
        return self.jsc(pixel_id) * 100000

    @handle_hysteresis
    def _mpp_v(self, iv_array: np.ndarray):
        voltage = iv_array[self.vl]
        current = iv_array[self.il]
        valid_range = (voltage >= 0) & (current <= 0)
        power = voltage[valid_range] * current[valid_range]
        return voltage[valid_range][power.argmin()]

    @result_buffer
    def mpp_v(self, pixel_id: str):
        return CurrentVoltageCharacteristic._mpp_v(self, self.dataset[pixel_id])

    @handle_hysteresis
    def _mpp_i(self, iv_array: np.ndarray, mpp: float):
        voltage = iv_array[self.vl]
        current = iv_array[self.il]
        return current[voltage == mpp][0]

    @result_buffer
    def mpp_i(self, pixel_id: str):
        return CurrentVoltageCharacteristic._mpp_i(self, self.dataset[pixel_id], self.mpp_v(pixel_id))

    def mpp_i_ma(self, pixel_id: str):
        return self.mpp_i(pixel_id) * 1000

    @result_buffer
    @current_density
    def mpp_j(self, pixel_id: str):
        return CurrentVoltageCharacteristic.mpp_i(self, pixel_id)

    def mpp_j_ma(self, pixel_id: str):
        return self.mpp_j(pixel_id) * 100000

    @handle_hysteresis
    def _ff(self, iv_array: np.ndarray, mpp: float, mpp_i: float, voc: float, isc: float):
        return (mpp * mpp_i) / (voc * isc)

    @result_buffer
    def ff(self, pixel_id: str):
        return CurrentVoltageCharacteristic._ff(self, self.dataset[pixel_id], self.mpp_i(pixel_id),
                                                self.mpp_v(pixel_id), self.voc(pixel_id), self.isc(pixel_id))

    @result_buffer
    def eff(self, pixel_id: str):
        return self.voc(pixel_id) * self.jsc(pixel_id) * self.ff(pixel_id) / self.power_in

    @handle_hysteresis
    def find_slope_of_intercept(self, iv_array: np.ndarray, transpose: bool):
        if not transpose:
            x = iv_array[self.vl].round(6)
        else:
            x = iv_array[self.il].round(6)
        regression_points = np.hstack([iv_array[x < 0][-1], iv_array[x == 0], iv_array[x > 0][0]])
        return 1 / np.polyfit(regression_points[self.vl], regression_points[self.il], deg=1)[0]

    @result_buffer
    def rs(self, pixel_id: str):
        return CurrentVoltageCharacteristic.find_slope_of_intercept(self, self.dataset[pixel_id], transpose=True)

    @result_buffer
    def rsh(self, pixel_id: str):
        return CurrentVoltageCharacteristic.find_slope_of_intercept(self, self.dataset[pixel_id], transpose=False)

    def semilog(self, pixel):
        plot = XYPlot()
        plot.make_plot()
        data = copy.deepcopy(self.dataset[pixel])
        y_label = data.dtype.names[1]
        data[y_label] = np.abs(data[y_label])
        plot.update_plot(data)
        plot.ax.set_yscale('log')
        return plot.figure
