"""This module contains plot classes which are used to (interactively) display the measurement progress and results."""
from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from abc import ABC, abstractmethod
from typing import Tuple, List, Type, Union, TypeVar
from cohesivm import CompatibilityError


class Plot(ABC):
    """This class serves as a blueprint for creating various plot types using Matplotlib. It ensures that derived
    classes implement methods for creating, updating, and clearing plots, and provides mechanisms for checking
    data compatibility."""

    _data_types = NotImplemented

    def __init__(self):
        self._figure = None

    @property
    def figure(self) -> Union[plt.Figure, None]:
        """The :class:`matplotlib.figure.Figure` object which is populated with the data."""
        return self._figure

    @abstractmethod
    def make_plot(self) -> None:
        """Generates the canvas of the plot and populates the static elements."""
        pass

    @abstractmethod
    def update_plot(self, *args, **kwargs) -> None:
        """Populates the figure with the data."""
        pass

    @abstractmethod
    def clear_plot(self) -> None:
        """Restores the plot to its initial state and removes all displayed data."""
        pass

    @property
    def data_types(self) -> Tuple[Type]:
        """A tuple of Numpy data types which corresponds to the expected shape of data points."""
        if self._data_types is NotImplemented:
            raise NotImplementedError
        return self._data_types

    def check_compatibility(self, data_dtype: Union[np.dtype, List[Tuple[str, Type]]]) -> None:
        """Checks if the types of the data are compatible with the plot.

        :param data_dtype: The data type of the expected data.
        :raises CompatibilityError: If the expected data is not compatible with the plot.
        """
        data_dtype = np.dtype(data_dtype)
        if len(data_dtype) != len(self.data_types):
            raise CompatibilityError(
                "The dtype of the data and the data_types of the plot must have the same lengths!")
        for mtype_name, ptype in zip(data_dtype.names, self.data_types):
            if not np.issubdtype(data_dtype[mtype_name], ptype):
                raise CompatibilityError(
                    "All items of the data dtype must be sub-dtypes of the plot data_types in correct order!")


class XYPlot(Plot):
    """Generates and updates a two-dimensional x-y-plot.

    :param figsize: Size of the figure in inch (see :class:`matplotlib.figure.Figure`).
    :param origin: Flag if the origin (0, 0) should be displayed by a vertical and a horizontal line.
    """

    _data_types = (np.floating, np.floating)

    def __init__(self, figsize: Tuple[float, float] = (7, 5.5), origin: bool = True) -> None:
        Plot.__init__(self)
        self.figsize = figsize
        self.origin = origin
        self.ax = None

    def make_plot(self) -> None:
        self._figure, self.ax = plt.subplots(figsize=self.figsize)
        self.ax.set_box_aspect(self.figsize[1] / self.figsize[0])
        self.ax.tick_params(axis='both', labelsize=10)
        self.ax.xaxis.set_major_formatter('{:.1E}'.format)
        self.ax.yaxis.set_major_formatter('{:.1E}'.format)
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        self.ax.plot([], [], linestyle='None', marker='o')
        if self.origin:
            self.ax.axhline(y=0, color='k')
            self.ax.axvline(x=0, color='k')

    def update_plot(self, data: np.ndarray) -> None:
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
        self.figure.tight_layout()

    def clear_plot(self) -> None:
        line = self.ax.lines[0]
        line.set_data([], [])
        self.figure.canvas.draw()
