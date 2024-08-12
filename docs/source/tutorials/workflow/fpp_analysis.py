import math
import copy
import numpy as np
import matplotlib.pyplot as plt
from typing import Union, Dict, Tuple, List
from cohesivm.analysis import Analysis, result_buffer
from cohesivm.database import Dataset, Dimensions
from cohesivm.plots import XYPlot


class FPPAnalysis(Analysis):
    """Implements the functions and plots to analyse the data of a four-point-probe measurement
    (``FPPMeasurement``).

    :param dataset: A tuple of (i) data arrays which are mapped to contact IDs and (ii) the corresponding metadata
        of the dataset. Or, optionally, just (i).
    :param interface_dimensions: The :class:`~cohesivm.database.Dimensions.Shape` of the interface. Required if the
        ``dataset`` contains no :class:`~cohesivm.database.Metadata`.
    :param contact_position_dict: A dictionary of contact IDs and the corresponding coordinates on the sample.
        Required if the ``dataset`` contains no :class:`~cohesivm.database.Metadata`.
    :param pixel_dimension_dict: A dictionary of contact IDs and the corresponding
        :class:`~cohesivm.database.Dimensions.Generic` shape of the pixels. Required if the ``dataset`` contains no
        :class:`~cohesivm.database.Metadata`.
    :param temperature: The temperature of the sample during the measurement in K. Required if the ``dataset``
        contains no :class:`~cohesivm.database.Metadata`.
    :param film_thickness: The thickness of the conductive film in mm. Required if the ``dataset`` contains no
        :class:`~cohesivm.database.Metadata`.
    """

    def __init__(self, dataset: Union[Dataset, Dict[str, np.ndarray]],
                 interface_dimensions: Dimensions.Shape = None,
                 contact_position_dict: Dict[str, Tuple[float, float]] = None,
                 pixel_dimension_dict: Dict[str, Dimensions.Generic] = None,
                 temperature: float = None,
                 film_thickness: float = None,
                 ) -> None:

        functions = {
            'Temperature (K)': self.temperature,
            'Film Thickness (mm)': self.film_thickness,
            'Linear Fit Resistance (Ohm)': self.linear,
            'Sheet Resistance (Ohm)': self.sheet,
            'Film Resistivity (Ohm mm)': self.rho_film,
            'Bulk Resistivity (Ohm mm)': self.rho_bulk,
            'Edge Distance i0 (mm)': self.edge_dist_i0,
            'Edge Distance i3 (mm)': self.edge_dist_i3,
            'Edge Sheet Resistance (Ohm)': self.edge_sheet,
            'Edge Film Resistivity (Ohm mm)': self.edge_rho_film,
            'Edge Bulk Resistivity (Ohm mm)': self.edge_rho_bulk,
        }

        plots = {
            'Measurement': self.measurement,
            'Film Resistivity': self.resistance_plot
        }

        super().__init__(functions, plots, dataset, contact_position_dict)

        if self.metadata is not None:
            self._interface_dimensions = Dimensions.object_from_string(self.metadata.interface_dimensions)
            self._contact_position_dict = self.metadata.contact_position_dict
            self._pixel_dimension_dict = {
                k: Dimensions.object_from_string(v) for k, v in self.metadata.pixel_dimension_dict.items()}
            self._temperature = self.metadata.measurement_settings['temperature']
            self._film_thickness = self.metadata.measurement_settings['film_thickness']
        else:
            self._interface_dimensions = interface_dimensions
            self._contact_position_dict = contact_position_dict
            self._pixel_dimension_dict = pixel_dimension_dict
            self._temperature = temperature
            self._film_thickness = film_thickness

        self.il = 'Current (A)'
        self.vl = 'Voltage (V)'

    def temperature(self, contact_id: str = '') -> float:
        """Retrieves the sample temperature from the measurement settings.

        :param contact_id: Does nothing.
        :returns: The temperature of the sample during the measurement in K.
        """
        return self._temperature

    def film_thickness(self, contact_id: str = '') -> float:
        """Retrieves the sample film thickness from the measurement settings.

        :param contact_id: Does nothing.
        :returns: The thickness of the measured conductive film in mm.
        """
        return self._film_thickness

    @result_buffer
    def probe_coordinates(self, contact_id: str) -> List[Tuple[float, float]]:
        """Calculates the absolute coordinates of the four point probe with respect to the interface.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: A list of coordinate tuples for the four contacts of the probe.
        """
        d = self._pixel_dimension_dict[contact_id]
        x_offset, y_offset = self._contact_position_dict[contact_id]
        x_abs = [x_offset + x for x in d.x_coords]
        y_abs = [y_offset + y for y in d.y_coords]
        return list(zip(x_abs, y_abs))

    @staticmethod
    def line_distance(x1y1: Tuple[float, float], x2y2: Tuple[float, float], xpyp: Tuple[float, float]
                      ) -> Tuple[float, float, float]:
        """Calculates the 2D distance between a line (given by two points) and another point.

        :param x1y1: The coordinates of the first point on the line.
        :param x2y2: The coordinates of the second point on the line.
        :param xpyp: The coordinates of the point for which the distance should be calculated.
        :returns: A tuple of the signed distance and the x- and y-component of the normal unit vector.
        """
        x1, y1 = x1y1
        x2, y2 = x2y2
        xp, yp = xpyp
        a = y2 - y1
        b = - (x2 - x1)
        c = -a * x1 - b * y1
        m = math.sqrt(a * a + b * b)
        a_prim, b_prim, c_prim = a/m, b/m, c/m
        dist = a_prim * xp + b_prim * yp + c_prim
        return dist, a_prim, b_prim

    @result_buffer
    def edge_distances(self, contact_id: str) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
        """Calculates the line distances of the closest edge to a four point probe.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: A tuple of line distance tuples (see :meth:`line_distance`).
        """
        xy = self.probe_coordinates(contact_id)
        if_d = self._interface_dimensions
        best_dist = (0., 0., 0.), (0., 0., 0.)
        # only works with a rectangular interface
        if not isinstance(if_d, Dimensions.Rectangle):
            return best_dist
        edge_vectors = [(0., 0.), (if_d.width, 0.), (if_d.width, if_d.height), (0., if_d.height), (0., 0.)]
        min_dist = float('inf')
        for x1y1, x2y2 in zip(edge_vectors[:4], edge_vectors[1:]):
            dist = self.line_distance(x1y1, x2y2, xy[0]), self.line_distance(x1y1, x2y2, xy[3])
            dist_avg = (abs(dist[0][0]) + abs(dist[1][0])) / 2
            if dist_avg < min_dist:
                min_dist = dist_avg
                best_dist = dist
        return best_dist

    @result_buffer
    def mirrored_coordinates(self, contact_id: str) -> List[Tuple[float, float]]:
        """Calculates coordinates for the current source contacts of a four point probe mirrored along the closest
        edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: A list of coordinate tuples for the two mirrored contacts of the probe.
        """
        xy_m = self.probe_coordinates(contact_id)[0], self.probe_coordinates(contact_id)[3]
        dist = self.edge_distances(contact_id)
        return [(xy_m[i][0] - 2 * dist[i][1] * dist[i][0], xy_m[i][1] - 2 * dist[i][2] * dist[i][0])
                for i in range(2)]

    @staticmethod
    def l_mn(xy: List[Tuple[float, float]], m: int, n: int) -> float:
        return math.log((xy[m][0] - xy[n][0])**2 + (xy[m][1] - xy[n][1])**2)

    @staticmethod
    def s_mn(xy: List[Tuple[float, float]], m: int, n: int) -> float:
        return math.sqrt((xy[m][0] - xy[n][0])**2 + (xy[m][1] - xy[n][1])**2)

    @result_buffer
    def l0(self, contact_id: str) -> float:
        xy = self.probe_coordinates(contact_id)
        return self.l_mn(xy, 1, 0) + self.l_mn(xy, 2, 3) - self.l_mn(xy, 1, 3) - self.l_mn(xy, 2, 0)

    @result_buffer
    def s0(self, contact_id: str) -> float:
        xy = self.probe_coordinates(contact_id)
        return -1/self.s_mn(xy, 1, 0) - 1/self.s_mn(xy, 2, 3) + 1/self.s_mn(xy, 1, 3) + 1/self.s_mn(xy, 2, 0)

    @result_buffer
    def lm(self, contact_id: str) -> float:
        xy = self.probe_coordinates(contact_id) + self.mirrored_coordinates(contact_id)
        return (self.l0(contact_id)
                + self.l_mn(xy, 1, 4) + self.l_mn(xy, 2, 5) - self.l_mn(xy, 1, 5) - self.l_mn(xy, 2, 4))

    @result_buffer
    def sm(self, contact_id: str) -> float:
        xy = self.probe_coordinates(contact_id) + self.mirrored_coordinates(contact_id)
        return (self.s0(contact_id) -
                1/self.s_mn(xy, 1, 4) - 1/self.s_mn(xy, 2, 5) + 1/self.s_mn(xy, 1, 5) + 1/self.s_mn(xy, 2, 4))

    @result_buffer
    def linear(self, contact_id: str) -> float:
        """Performs a linear regression between the measured current and voltage values to obtain the slope, i.e.,
        the fitted resistance after Ohm's Law.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The fraction between the measured voltage and sourced current fitted over all data points in Ohm.
        """
        return float(np.polyfit(self.data[contact_id][self.il], self.data[contact_id][self.vl], deg=1)[0])

    @result_buffer
    def sheet(self, contact_id: str) -> float:
        """Calculates the sheet resistance for a probe far from the edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The sheet resistance in Ohm.
        """
        return abs(4 * math.pi * self.linear(contact_id) * 1 / self.l0(contact_id))

    @result_buffer
    def rho_film(self, contact_id: str) -> float:
        """Calculates the resistivity of a film for a probe far from the edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The film resistivity in Ohm mm.
        """
        t = self.film_thickness()
        return abs(self.sheet(contact_id) * t) if t is not None else None

    @result_buffer
    def rho_bulk(self, contact_id: str) -> float:
        """Calculates the resistivity of a bulk material for a probe far from the edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The bulk resistivity in Ohm mm.
        """
        return abs(2 * math.pi * self.linear(contact_id) * 1 / self.s0(contact_id))

    @result_buffer
    def edge_dist_i0(self, contact_id: str) -> float:
        """Retrieves the distance of the i0 contact of the four point probe to the closest edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The edge distance of the i0 contact in mm.
        """
        return self.edge_distances(contact_id)[0][0]

    @result_buffer
    def edge_dist_i3(self, contact_id: str) -> float:
        """Retrieves the distance of the i3 contact of the four point probe to the closest edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The edge distance of the i3 contact in mm.
        """
        return self.edge_distances(contact_id)[1][0]

    @result_buffer
    def edge_sheet(self, contact_id: str) -> float:
        """Calculates the sheet resistance for a probe close to an edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The edge sheet resistance in Ohm.
        """
        return abs(4 * math.pi * self.linear(contact_id) * 1 / self.lm(contact_id))

    @result_buffer
    def edge_rho_film(self, contact_id: str) -> float:
        """Calculates the resistivity of a film for a probe close to an edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The edge film resistivity in Ohm mm.
        """
        t = self.film_thickness()
        return abs(self.edge_sheet(contact_id) * t) if t is not None else None

    @result_buffer
    def edge_rho_bulk(self, contact_id: str) -> float:
        """Calculates the resistivity of a bulk material for a probe close to an edge.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: The edge bulk resistivity in Ohm mm.
        """
        return abs(2 * math.pi * self.linear(contact_id) * 1 / self.sm(contact_id))

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

    def resistance_plot(self, contact_id: str) -> plt.Figure:
        """Creates a plot of the resistance calculated after Ohm's Law. Should be a horizontal line for the ideal
        case.

        :param contact_id: The ID of the contact from the :class:`~cohesivm.interfaces.Interface`.
        :returns: A figure object which may be displayed by the :class:`~cohesivm.gui.AnalysisGUI`.
        """
        plot = XYPlot(origin=False)
        plot.make_plot()
        data = copy.deepcopy(self.data[contact_id])
        data[self.vl] = data[self.vl] / data[self.il]
        data.dtype = copy.deepcopy(data.dtype)
        data.dtype.names = (self.il, 'Resistance (Ohm)')
        plot.update_plot(data)
        plot.ax.axhline(y=self.linear(contact_id), color='r', ls='--')
        return plot.figure
