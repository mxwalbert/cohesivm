"""Module containing the classes which handle the data stream from measurement methods."""
from __future__ import annotations
import threading
import multiprocessing as mp
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from abc import ABC, abstractmethod
from typing import Tuple


class DataStreamABC(ABC):
    """Creates an ``mp.Queue`` object which is used to stream data from a ``MeasurementABC``. A child class implements
    the methods for pulling the data from the queue and processing it."""

    def __init__(self):
        self._data_stream = mp.Queue()

    @property
    def data_stream(self) -> mp.Queue:
        """The ``mp.Queue`` object, where data is streamed to. Must be injected into the ``MeasurementABC`` or the
        ``ExperimentABC``."""
        return self._data_stream


class PlotABC(DataStreamABC):
    """Creates an ``mp.Queue`` object which is used to stream data from a measurement (implementing ``MeasurementABC``)
    to a ``matplotlib.figure.Figure`` object where the streamed data is put into. A child class implements the methods
    for updating the data and the figure. Its intended use is within the GUI class."""
    _data_types = NotImplemented

    def __init__(self):
        DataStreamABC.__init__(self)
        self._figure = None

    @property
    def data_types(self) -> Tuple[type]:
        """A tuple of Numpy data types which corresponds to the expected shape of data points."""
        if self._data_types is NotImplemented:
            raise NotImplementedError
        return self._data_types

    @property
    def figure(self) -> plt.Figure | None:
        """The ``matplotlib.pyplot.Figure`` object which is populated with the data."""
        return self._figure

    @abstractmethod
    def make_plot(self):
        """Generates the canvas of the plot and populates the static elements."""
        pass

    @abstractmethod
    def update_plot(self):
        """Fetches the data from the `data_stream` and puts it in the figure."""
        pass

    @abstractmethod
    def clear_plot(self):
        """Restores the plot to its initial state and removes all displayed data."""
        pass


class FakeQueue:
    """Mimics the queue.Queue class to be used as default value for methods which implement an optional data stream.
    Simplifies the methods because they do not have to care if the queue is actually present and also prevents
    unnecessary data accumulation."""
    @staticmethod
    def put(data):
        pass


class ProgressBar(DataStreamABC):
    """Generates two tqdm progressbars which display the progress of an ``ExperimentABC``, one for the pixels and the
    second for the datapoints of the current ``MeasurementABC``."""

    terminate_string = 'terminate_progressbar'

    def __init__(self, num_pixels: int, num_datapoints: int):
        """Initializes the ProgressBar object.

        :param num_pixels: The number of pixels which are measured in the ``ExperimentABC``.
        :param num_datapoints: The number of datapoints of each ``MeasurementABC``.
        """
        DataStreamABC.__init__(self)
        self.num_pixels = num_pixels
        self.num_datapoints = num_datapoints
        self.progress_pixels = None
        self.progress_datapoints = None

    def show(self):
        """Displays the progressbars and starts a worker thread which pulls the data from the `data_stream` and updates
        the progressbars."""
        if self.num_pixels == 0:
            return
        try:
            if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
                from tqdm import tqdm_notebook as tqdm
            else:
                raise NameError
        except NameError:
            from tqdm import tqdm
        self.progress_pixels = tqdm(total=self.num_pixels, desc='Pixels', leave=False, dynamic_ncols=True)
        self.progress_datapoints = tqdm(total=self.num_datapoints, desc='Datapoints', leave=False, dynamic_ncols=True)
        thread = threading.Thread(target=self._update)
        thread.start()

    def _update(self):
        """Updates the progressbars by pulling data from the `data_stream`. Closes the progressbars when the expected
        total number of datapoints were pulled or when the `terminate_string` is received."""
        while True:
            if not self.data_stream.empty():
                data = self.data_stream.get()
                if type(data) == str:
                    if data == self.terminate_string:
                        break
                self.progress_datapoints.update(1)
                if self.progress_datapoints.n == self.num_datapoints:
                    self.progress_pixels.update(1)
                    if self.progress_pixels.n == self.num_pixels:
                        break
                    self.progress_datapoints.reset()
        self.progress_pixels.close()
        self.progress_datapoints.close()

    def close(self):
        """Puts the `terminate_string` into the `data_stream`."""
        self.data_stream.put(self.terminate_string)


class Simple2DPlot(PlotABC):
    """Generates and updates a two-dimensional x-y-plot with the data which is put in the `data_stream` queue."""

    _data_types = (np.floating, np.floating)

    def __init__(self, x_label: str, y_label: str, figsize: Tuple[float, float] = (7, 5.5)):
        """Initializes the Simple2DPlot object and populates the `data_stream` property.

        :param x_label: Label of the x axis.
        :param y_label: Label of the y axis.
        :param figsize: Size of the figure in inch (see matplotlib.figure.Figure)."""
        PlotABC.__init__(self)
        self.x_label = x_label
        self.y_label = y_label
        self.figsize = figsize
        self.ax = None

    def make_plot(self):
        self._figure, self.ax = plt.subplots(figsize=self.figsize)
        self.ax.set_box_aspect(self.figsize[1] / self.figsize[0])
        self.ax.set_xlabel(self.x_label, fontsize=14, fontweight='bold')
        self.ax.set_ylabel(self.y_label, fontsize=14, fontweight='bold')
        self.ax.tick_params(axis='both', labelsize=10)
        self.ax.xaxis.set_major_formatter('{:.1E}'.format)
        self.ax.yaxis.set_major_formatter('{:.1E}'.format)
        self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=5))
        self.ax.plot([], [])

    def update_plot(self):
        line = self.ax.lines[0]
        while not self.data_stream.empty():
            data = self.data_stream.get()
            if len(data) == 2:
                old_x, old_y = line.get_data()
                new_x = list(old_x) + [data[0]]
                new_y = list(old_y) + [data[1]]
                line.set_data(new_x, new_y)
                if len(new_x) > 1:
                    x_ticks = np.linspace(min(new_x), max(new_x), 5)
                    y_ticks = np.linspace(min(new_y), max(new_y), 5)
                    self.ax.relim()
                    self.ax.autoscale()
                    self.ax.xaxis.set_major_locator(ticker.FixedLocator(x_ticks))
                    self.ax.yaxis.set_major_locator(ticker.FixedLocator(y_ticks))

    def clear_plot(self):
        self.update_plot()
        line = self.ax.lines[0]
        line.set_data([], [])
