from __future__ import annotations
import copy
import matplotlib.pyplot as plt
import numpy as np
from numpy.lib import recfunctions as rfn
from typing import Dict, Tuple, Union
from cohesivm.analysis import Analysis
from cohesivm.database import Dataset, Dimensions
from cohesivm.plots import XYPlot


class CapacitanceVoltageProfiling(Analysis):
    """Implements the functions and plots to analyse the data of a capacitance-voltage-profiling measurement
    (:class:`~cohesivm.measurements.cv.CapacitanceVoltageProfiling`).

    :param dataset: A tuple of (i) data arrays which are mapped to contact IDs and (ii) the corresponding metadata of
        the dataset. Or, optionally, just (i).
    :param contact_position_dict: A dictionary of contact IDs and the corresponding positions/coordinates on the sample.
        Required if the ``dataset`` contains no :class:`~cohesivm.database.Metadata`.
    :param areas: A mapping of the contact IDs with the pixel area. Required if the ``dataset`` contains no
        :class:`~cohesivm.database.Metadata`.
    :param frequency: he power of the input radiation source in W/mm^2. Required if the ``dataset`` contains no
        :class:`~cohesivm.database.Metadata`.
    """

    def __init__(self, dataset: Union[Dataset, Dict[str, np.ndarray]],
                 contact_position_dict: Dict[str, Tuple[float, float]] = None,
                 areas: Dict[str, float] = None, frequency: int = None) -> None:

        functions = {
        }

        plots = {
            'Magnitude-Voltage': self.magnitude,
            'Phase-Voltage': self.phase,
            'Mott-Schottky': self.mott_schottky
        }

        super().__init__(functions, plots, dataset, contact_position_dict)

        if self.metadata is not None:
            self._areas = {contact: Dimensions.object_from_string(dimension).area() for contact, dimension
                           in self.metadata.pixel_dimension_dict.items()} if areas is None else areas
            self._frequency = self.metadata.measurement_settings['frequency'] if frequency is None else frequency
        else:
            self._areas = {contact_id: 1. for contact_id in self.data.keys()} if areas is None else areas
            self._frequency = 1 if frequency is None else frequency

        self.vl = 'Voltage (V)'
        self.zl = 'Magnitude (1)'
        self.pl = 'Phase (deg)'

    @property
    def areas(self) -> Dict[str, float]:
        """A mapping of the contact IDs with the pixel area."""
        return self._areas

    @property
    def frequency(self) -> int:
        """The oscillator frequency of the applied AC field in Hz."""
        return self._frequency

    def magnitude(self, contact_id: str) -> plt.Figure:
        """Creates a basic x-y plot of the magnitude's voltage-dependence.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The figure object which may be displayed by the :class:`~cohesivm.gui.AnalysisGUI`.
        """
        plot = XYPlot()
        plot.make_plot()
        data = rfn.drop_fields(copy.deepcopy(self.data[contact_id]), self.pl)
        plot.update_plot(data)
        return plot.figure

    def phase(self, contact_id: str) -> plt.Figure:
        """Creates a basic x-y plot of the phase's voltage-dependence.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The figure object which may be displayed by the :class:`~cohesivm.gui.AnalysisGUI`.
        """
        plot = XYPlot()
        plot.make_plot()
        data = rfn.drop_fields(copy.deepcopy(self.data[contact_id]), self.zl)
        plot.update_plot(data)
        return plot.figure

    def mott_schottky(self, contact_id: str) -> plt.Figure:
        """Creates a basic x-y plot of the 1/C^2 vs. voltage.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The figure object which may be displayed by the :class:`~cohesivm.gui.AnalysisGUI`.
        """
        plot = XYPlot()
        plot.make_plot()
        data = rfn.drop_fields(copy.deepcopy(self.data[contact_id]), self.pl)
        data[self.zl] = (2 * np.pi * self.frequency * data[self.zl])**2
        data = rfn.rename_fields(data, {self.zl: 'Inverse Capacitance Squared (F^-2)'})
        plot.update_plot(data)
        return plot.figure
