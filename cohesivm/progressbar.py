from __future__ import annotations
import threading
import contextlib
from typing import Generator
from cohesivm.data_stream import DataStream
from cohesivm.experiment import Experiment


class ProgressBar(DataStream):
    """Generates two tqdm progressbars which display the progress of an :class:`~cohesivm.experiment.Experiment`, one
    for the contacts and the second for the datapoints of the current :class:`~cohesivm.measurements.Measurement`.

    :param experiment: An experiment for which the progress should be displayed.
    """

    def __init__(self, experiment: Experiment) -> None:
        DataStream.__init__(self)
        self.num_contacts = len(experiment.selected_contacts)
        self.num_datapoints = experiment.measurement.output_shape[0]
        self.progress_contacts = None
        self.progress_datapoints = None
        experiment.data_stream = self.data_stream

    @property
    def terminate_string(self) -> str:
        """The string which is used to signal that the worker thread should be terminated."""
        return 'terminate_progressbar'

    @contextlib.contextmanager
    def show(self) -> Generator[None, None, None]:
        """Displays the progressbars and starts a worker thread which pulls the data from
        the :attr:`~cohesivm.datastream.DataStream.data_stream` and updates the progressbars.
        Should be used in form of a resource such that the worker is terminated if an error occurs.

        Example
        -------

        .. code-block:: python

            with pbar.show():
                experiment.quickstart()
        """
        if self.num_contacts == 0:
            return
        try:
            if get_ipython().__class__.__name__ == 'ZMQInteractiveShell':
                from tqdm import tqdm_notebook as tqdm
            else:
                raise NameError
        except NameError:
            from tqdm import tqdm
        self.progress_contacts = tqdm(total=self.num_contacts, desc='Contacts', leave=False, dynamic_ncols=True)
        self.progress_datapoints = tqdm(total=self.num_datapoints, desc='Datapoints', leave=False, dynamic_ncols=True)
        thread = threading.Thread(target=self._update)
        thread.start()
        try:
            yield
        finally:
            self.close()

    def _update(self) -> None:
        """Updates the progressbars by pulling data from the :attr:`~cohesivm.experiment.Experiment.data_stream`.
        Closes the progressbars when the expected total number of datapoints were pulled or when the
        :attr:`terminate_string` is received."""
        while True:
            if not self.data_stream.empty():
                data = self.data_stream.get()
                if type(data) == str:
                    if data == self.terminate_string:
                        break
                self.progress_datapoints.update(1)
                if self.progress_datapoints.n == self.num_datapoints:
                    self.progress_contacts.update(1)
                    if self.progress_contacts.n == self.num_contacts:
                        break
                    self.progress_datapoints.reset()
        self.progress_contacts.close()
        self.progress_datapoints.close()

    def close(self) -> None:
        """Puts the :attr:`terminate_string` into the :attr:`~cohesivm.datastream.DataStream.data_stream`."""
        self.data_stream.put(self.terminate_string)
