"""This module contains the classes which handle the data stream from measurement methods."""
from __future__ import annotations
import multiprocessing as mp
from abc import ABC


class DataStream(ABC):
    """Creates a :class:`multiprocessing.Queue` object which is used to stream data from a
    :class:`~cohesivm.measurements.Measurement`. A child class implements the methods for pulling the data from the
    queue and processing it."""

    def __init__(self):
        self._data_stream = mp.Queue()

    @property
    def data_stream(self) -> mp.Queue:
        """The :class:`multiprocessing.Queue` object, where data is streamed to. Must be injected into the
        :class:`~cohesivm.measurements.Measurement` or the :class:`~cohesivm.experiment.Experiment`."""
        return self._data_stream


class FakeQueue:
    """Mimics the :class:`multiprocessing.Queue` and can be used as default value for methods which implement an
    optional data stream. Simplifies the methods because they do not have to care if the queue is actually present
    and also prevents unnecessary data accumulation."""
    @staticmethod
    def put(data):
        """Does nothing."""
        pass
