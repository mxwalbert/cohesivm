"""This module contains plot classes which are used to interactively display the measurement results."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import bqplot
from abc import ABC, abstractmethod
from typing import Tuple, List, Type
from . import CompatibilityError
from .data_stream import DataStreamABC


class PlotABC(ABC):

    _data_types = NotImplemented

    def __init__(self):
        self._figure = None

    @property
    def figure(self) -> plt.Figure | bqplot.Figure | None:
        """The ``matplotlib.pyplot.Figure`` or ``bqplot.Figure`` object which is populated with the data."""
        return self._figure

    @abstractmethod
    def make_plot(self):
        """Generates the canvas of the plot and populates the static elements."""
        pass

    @abstractmethod
    def update_plot(self, *args, **kwargs):
        """Populates the figure with the data."""
        pass

    @abstractmethod
    def clear_plot(self):
        """Restores the plot to its initial state and removes all displayed data."""
        pass

    @property
    def data_types(self) -> Tuple[type]:
        """A tuple of Numpy data types which corresponds to the expected shape of data points."""
        if self._data_types is NotImplemented:
            raise NotImplementedError
        return self._data_types

    def check_compatibility(self, data_dtype: np.dtype | List[Tuple[str, Type]]):
        """Checks if the types of the data are compatible with the plot."""
        if len(data_dtype) != len(self.data_types):
            raise CompatibilityError(
                "The dtype of the data and the data_types of the plot must have the same lengths!")
        for mtype_name, ptype in zip(data_dtype.names, self.data_types):
            if not np.issubdtype(data_dtype[mtype_name], ptype):
                raise CompatibilityError(
                    "All items of the data dtype must be sub-dtypes of the plot data_types in correct order!")


class XYPlot(PlotABC):
    """Generates and updates a two-dimensional x-y-plot."""

    _data_types = (np.floating, np.floating)

    def __init__(self, figsize: Tuple[float, float] = (7, 5.5)):
        """Initializes the XYPlot object.

        :param figsize: Size of the figure in inch (see matplotlib.figure.Figure)."""
        PlotABC.__init__(self)
        self.figsize = figsize
        self.ax = None

    def make_plot(self):
        self._figure, self.ax = plt.subplots(figsize=self.figsize)
        self.ax.set_box_aspect(self.figsize[1] / self.figsize[0])
        self.ax.tick_params(axis='both', labelsize=10)
        self.ax.xaxis.set_major_formatter('{:.1E}'.format)
        self.ax.yaxis.set_major_formatter('{:.1E}'.format)
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        self.ax.plot([], [], linestyle='None', marker='o')
        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')

    def update_plot(self, data: np.ndarray):
        self.check_compatibility(data.dtype)
        x_label, y_label = data.dtype.names
        self.ax.set_xlabel(x_label, fontsize=14, fontweight='bold')
        self.ax.set_ylabel(y_label, fontsize=14, fontweight='bold')
        x_data, y_data = data[x_label], data[y_label]
        line = self.ax.lines[0]
        line.set_data(x_data, y_data)
        x_ticks = np.linspace(min(x_data), max(x_data), 5)
        y_ticks = np.linspace(min(y_data), max(y_data), 5)
        self.ax.relim()
        self.ax.autoscale()
        self.ax.xaxis.set_major_locator(ticker.FixedLocator(x_ticks))
        self.ax.yaxis.set_major_locator(ticker.FixedLocator(y_ticks))
        self.figure.canvas.draw()

    def clear_plot(self):
        line = self.ax.lines[0]
        line.set_data([], [])
        self.figure.canvas.draw()


class DataStreamPlotABC(DataStreamABC, PlotABC):
    """Creates an ``mp.Queue`` object which is used to stream data from a measurement (implementing ``MeasurementABC``)
    to a ``matplotlib.figure.Figure`` object where the streamed data is put into. A child class implements the methods
    for updating the data and the figure. Its intended use is within the ExperimentGUI class."""

    def __init__(self):
        DataStreamABC.__init__(self)
        PlotABC.__init__(self)

    @abstractmethod
    def update_plot(self):
        """Fetches the data from the `data_stream` and puts it in the figure."""
        pass


class XYDataStreamPlot(DataStreamPlotABC):
    """Generates and updates a two-dimensional x-y-plot with the data which is put in the `data_stream` queue."""

    _data_types = (np.floating, np.floating)

    def __init__(self, x_label: str, y_label: str, figsize: Tuple[float, float] = (7, 5.5)):
        """Initializes the XYDataStreamPlot object and populates the `data_stream` property.

        :param x_label: Label of the x axis.
        :param y_label: Label of the y axis.
        :param figsize: Size of the figure in inch (see matplotlib.figure.Figure)."""
        DataStreamPlotABC.__init__(self)
        self.x_label = x_label
        self.y_label = y_label
        self.figsize = figsize
        self._line = None
        self._x_sc = None
        self._y_sc = None

    def make_plot(self):
        self._x_sc, self._y_sc = bqplot.LinearScale(min=-1, max=1), bqplot.LinearScale(min=-1, max=1)
        x_ax = bqplot.Axis(scale=self._x_sc, label=self.x_label, tick_format='.1f', grid_lines='solid',
                           label_offset='30')
        y_ax = bqplot.Axis(scale=self._y_sc, label=self.y_label, tick_format='.1e', grid_lines='solid',
                           label_offset='-50', orientation='vertical')
        x_ax.num_ticks = 7
        self._line = bqplot.Lines(x=[], y=[], scales={'x': self._x_sc, 'y': self._y_sc})
        self._figure = bqplot.Figure(marks=[self._line], axes=[x_ax, y_ax],
                                     figsize=self.figsize, padding_x=0, padding_y=0,
                                     fig_margin={'top': 10, 'bottom': 45, 'left': 65, 'right': 30})

    def update_plot(self):
        while not self.data_stream.empty():
            data = self.data_stream.get()
            if len(data) == 2:
                self._line.x = list(self._line.x) + [data[0]]
                self._line.y = list(self._line.y) + [data[1]]
        if len(self._line.x) > 1:
            self._x_sc.min = None
            self._x_sc.max = None
            self._y_sc.min = None
            self._y_sc.max = None

    def clear_plot(self):
        self.update_plot()
        self._x_sc.min = -1
        self._x_sc.max = 1
        self._y_sc.min = -1
        self._y_sc.max = 1
        self._line.x = []
        self._line.y = []
