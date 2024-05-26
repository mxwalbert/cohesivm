"""Module containing the classes which handle the data stream from measurement methods."""
from __future__ import annotations
import threading
import multiprocessing as mp
from abc import ABC


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


class FakeQueue:
    """Mimics the queue.Queue class to be used as default value for methods which implement an optional data stream.
    Simplifies the methods because they do not have to care if the queue is actually present and also prevents
    unnecessary data accumulation."""
    @staticmethod
    def put(data):
        """Does nothing."""
        pass


class ProgressBar(DataStreamABC):
    """Generates two tqdm progressbars which display the progress of an ``ExperimentABC``, one for the pixels and the
    second for the datapoints of the current ``MeasurementABC``."""

    terminate_string = 'terminate_progressbar'

    def __init__(self, num_pixels: int, num_datapoints: int):
        """Initializes the ProgressBar object.

        :param num_pixels: The number of pixel_ids which are measured in the ``ExperimentABC``.
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
