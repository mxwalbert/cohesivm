"""Module containing the classes which handle the data stream from measurement methods."""
import matplotlib.pyplot as plt
from cohesivm.abcs import PlotABC


class FakeQueue:
    """Mimics the queue.Queue class to be used as default value for methods which implement an optional data stream.
    Simplifies the methods because they do not have to care if the queue is actually present and also prevents
    unnecessary data accumulation."""
    @staticmethod
    def put(data):
        pass


class Simple2DPlot(PlotABC):
    def __init__(self, xlabel: str, ylabel: str):
        PlotABC.__init__(self)
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ax = None

    def make_plot(self):
        self._figure, self.ax = plt.subplots()
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
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
                self.ax.relim()
                self.ax.autoscale()
