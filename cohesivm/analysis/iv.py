from __future__ import annotations
import functools
import copy
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Tuple, Union, Callable
from cohesivm.analysis import Analysis, result_buffer
from cohesivm.database import Dataset, Dimensions
from cohesivm.plots import XYPlot


def handle_hysteresis(func: Callable) -> Callable:
    """Decorator for functions which directly evaluate the measurement data and need to separate it into two individual
    curves (``hysteresis`` of the :attr:`~cohesivm.measurements.iv.CurrentVoltageCharacteristic` is set
    ``True``). The function result will then be a tuple of two floats.

    :param func: The function to be decorated.
    :returns: The decorated function.
    """

    @functools.wraps(func)
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


def current_density(func: Callable) -> Callable:
    """Decorator for functions which should return the result normalized by the
    :attr:`~cohesivm.analysis.iv.CurrentVoltageCharacteristic.areas`.

    :param func: The function to be decorated.
    :returns: The decorated function.
    """

    @functools.wraps(func)
    def wrapper(self, contact_id):
        if self.hysteresis:
            return (
                func(self, contact_id)[0] / self.areas[contact_id],
                func(self, contact_id)[1] / self.areas[contact_id]
            )
        return func(self, contact_id) / self.areas[contact_id]
    return wrapper


class CurrentVoltageCharacteristic(Analysis):
    """Implements the functions and plots to analyse the data of a current-voltage-characteristic measurement
    (:class:`~cohesivm.measurements.iv.CurrentVoltageCharacteristic`).

    :param dataset: A tuple of (i) data arrays which are mapped to contact IDs and (ii) the corresponding metadata of
        the dataset. Or, optionally, just (i).
    :param contact_position_dict: A dictionary of contact IDs and the corresponding positions/coordinates on the sample.
        Required if the ``dataset`` contains no :class:`~cohesivm.database.Metadata`.
    :param areas: A mapping of the contact IDs with the pixel area. Required if the ``dataset`` contains no
        :class:`~cohesivm.database.Metadata`.
    :param hysteresis: Flags if the voltage range of the measurement was swept a second time in reverse order. Required
        if the ``dataset`` contains no :class:`~cohesivm.database.Metadata`.
    :param illuminated: Flags if the sample was illuminated during measurement. Required if the ``dataset`` contains no
        :class:`~cohesivm.database.Metadata`.
    :param power_in: The power of the input radiation source in W/mm^2. Required if the ``dataset`` contains no
        :class:`~cohesivm.database.Metadata`.
    """

    def __init__(self, dataset: Union[Dataset, Dict[str, np.ndarray]],
                 contact_position_dict: Dict[str, Tuple[float, float]] = None,
                 areas: Dict[str, float] = None, hysteresis: bool = None,
                 illuminated: bool = None, power_in: float = None
                 ) -> None:

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
            'Measurement': self.measurement,
            'Semi-Log': self.semilog
        }

        super().__init__(functions, plots, dataset, contact_position_dict)

        if self.metadata is not None:
            self._areas = {contact: Dimensions.object_from_string(dimension).area() for contact, dimension
                           in self.metadata.pixel_dimension_dict.items()} if areas is None else areas
            ms = self.metadata.measurement_settings
            self._hysteresis = ms['hysteresis'] if hysteresis is None else hysteresis
            self._illuminated = ms['illuminated'] if illuminated is None else illuminated
            self._power_in = ms['power_in'] if power_in is None else power_in
        else:
            self._areas = {contact_id: 1. for contact_id in self.data.keys()} if areas is None else areas
            self._hysteresis = False if hysteresis is None else hysteresis
            self._illuminated = True if illuminated is None else illuminated
            self._power_in = 1. if power_in is None else power_in

        self.vl = 'Voltage (V)'
        self.il = 'Current (A)'

    @property
    def areas(self) -> Dict[str, float]:
        """A mapping of the contact IDs with the pixel area."""
        return self._areas

    @property
    def hysteresis(self) -> bool:
        """Flags if the voltage range of the measurement was swept a second time in reverse order."""
        return self._hysteresis

    @property
    def illuminated(self) -> bool:
        """Flags if the sample was illuminated during measurement."""
        return self._illuminated

    @property
    def power_in(self) -> float:
        """The power of the input radiation source in W/mm^2."""
        return self._illuminated

    @handle_hysteresis
    def _find_intercept(self, iv_array: np.ndarray, transpose: bool) -> Union[float, Tuple[float, float]]:
        """Finds the y-intercept of the provided data, i.e., the y-value at x=0.

        :param iv_array: The data curve.
        :param transpose: Flags if the x- and y-axis should be swapped.
        :returns: The y-intercept(s).
        """
        x = iv_array[self.vl]
        y = iv_array[self.il]
        if transpose:
            x, y = y, x
        (x_low, x_high), (y_low, y_high) = [[v[x <= 0], v[x >= 0]] for v in [x, y]]
        lower_bound, upper_bound = x_low.argmax(), x_high.argmin()
        return np.interp(0, [x_low[lower_bound], x_high[upper_bound]], [y_low[lower_bound], y_high[upper_bound]])

    @result_buffer
    def voc(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the x-intercept of the data curve.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Open Circuit Voltage in V.
        """
        return CurrentVoltageCharacteristic._find_intercept(self, self.data[contact_id], transpose=True)

    @result_buffer
    def isc(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the y-intercept of the data curve.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Short Circuit Current in A.
        """
        return CurrentVoltageCharacteristic._find_intercept(self, self.data[contact_id], transpose=False)

    def isc_ma(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the y-intercept of the data curve and multiplies by 1000.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Short Circuit Current in mA.
        """
        return self.isc(contact_id) * 1000

    @result_buffer
    @current_density
    def jsc(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the y-intercept of the data curve and normalizes by the pixel area.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Short Circuit Current Density in A/mm^2.
        """
        return CurrentVoltageCharacteristic.isc(self, contact_id)

    def jsc_ma(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the y-intercept of the data curve, normalizes by the pixel area and multiplies by 100000.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Short Circuit Current Density in mA/cm^2.
        """
        return self.jsc(contact_id) * 100000

    @handle_hysteresis
    def _mpp_v(self, iv_array: np.ndarray) -> Union[float, Tuple[float, float]]:
        voltage = iv_array[self.vl]
        current = iv_array[self.il]
        valid_range = (voltage >= 0) & (current <= 0)
        power = voltage[valid_range] * current[valid_range]
        return voltage[valid_range][power.argmin()]

    @result_buffer
    def mpp_v(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the voltage where the product of the voltage and the current is maximal.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The MPP Voltage in V.
        """
        return CurrentVoltageCharacteristic._mpp_v(self, self.data[contact_id])

    @handle_hysteresis
    def _mpp_i(self, iv_array: np.ndarray, mpp: float) -> Union[float, Tuple[float, float]]:
        voltage = iv_array[self.vl]
        current = iv_array[self.il]
        return current[voltage == mpp][0]

    @result_buffer
    def mpp_i(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the current where the product of the voltage and the current is maximal.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The MPP Current in A.
        """
        return CurrentVoltageCharacteristic._mpp_i(self, self.data[contact_id], self.mpp_v(contact_id))

    def mpp_i_ma(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the current where the product of the voltage and the current is maximal, multiplied by 1000.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The MPP Current in mA.
        """
        return self.mpp_i(contact_id) * 1000

    @result_buffer
    @current_density
    def mpp_j(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the current where the product of the voltage and the current is maximal, normalized by the pixel area.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The MPP Current Density in A/mm^2.
        """
        return CurrentVoltageCharacteristic.mpp_i(self, contact_id)

    def mpp_j_ma(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the current where the product of the voltage and the current is maximal, normalizes by the pixel area,
        and multiplies by 100000.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The MPP Current Density in mA/cm^2.
        """
        return self.mpp_j(contact_id) * 100000

    @handle_hysteresis
    def _ff(self, iv_array: np.ndarray, mpp: float, mpp_i: float, voc: float, isc: float
            ) -> Union[float, Tuple[float, float]]:
        return (mpp * mpp_i) / (voc * isc)

    @result_buffer
    def ff(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the ratio between the area which is span by the MPP voltage and current and the area which is span by
        the Voc and Isc.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Fill Factor as a unit-less fraction.
        """
        return CurrentVoltageCharacteristic._ff(self, self.data[contact_id], self.mpp_i(contact_id),
                                                self.mpp_v(contact_id), self.voc(contact_id), self.isc(contact_id))

    @result_buffer
    def eff(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the ratio between the product of Voc, Jsc and FF and the power of the input radiation source.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Efficiency as a unit-less fraction.
        """
        return abs(self.voc(contact_id) * self.jsc(contact_id) * self.ff(contact_id) / self.power_in)

    @handle_hysteresis
    def _find_slope_of_intercept(self, iv_array: np.ndarray, transpose: bool) -> Union[float, Tuple[float, float]]:
        if not transpose:
            x = iv_array[self.vl].round(6)
        else:
            x = iv_array[self.il].round(6)
        regression_points = np.hstack([iv_array[x < 0][-1], iv_array[x == 0], iv_array[x > 0][0]])
        return 1 / np.polyfit(regression_points[self.vl], regression_points[self.il], deg=1)[0]

    @result_buffer
    def rs(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the slope of the curve at the x-intercept.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Series Resistance in Ohm.
        """
        return CurrentVoltageCharacteristic._find_slope_of_intercept(self, self.data[contact_id], transpose=True)

    @result_buffer
    def rsh(self, contact_id: str) -> Union[float, Tuple[float, float]]:
        """Finds the slope of the curve at the y-intercept.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The Shunt (Parallel) Resistance in Ohm.
        """
        return CurrentVoltageCharacteristic._find_slope_of_intercept(self, self.data[contact_id], transpose=False)

    def measurement(self, contact_id: str) -> plt.Figure:
        """Creates a basic x-y plot of the data.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The figure object which may be displayed by the :class:`~cohesivm.gui.AnalysisGUI`.
        """
        plot = XYPlot()
        plot.make_plot()
        data = copy.deepcopy(self.data[contact_id])
        plot.update_plot(data)
        return plot.figure

    def semilog(self, contact_id: str) -> plt.Figure:
        """Creates a semilog plot of the data curve where the scale of the y-axis is logarithmic.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: A figure object which may be displayed by the :class:`~cohesivm.gui.AnalysisGUI`.
        """
        plot = XYPlot()
        plot.make_plot()
        data = copy.deepcopy(self.data[contact_id])
        data[self.il] = np.abs(data[self.il])
        plot.update_plot(data)
        plot.ax.set_yscale('log')
        return plot.figure
