"""This Module contains the :class:`Analysis` Abstract Base Class and the implemented analysis classes
(standalone modules) which follow this ABC. The main responsibility is to quickly have access to analysis results
of measurement data."""
from __future__ import annotations
import functools
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from typing import Dict, Tuple, Callable, Any, List, Union
from cohesivm.database import DatabaseValue, Dataset, Metadata


def result_buffer(func: Callable) -> Callable:
    """Decorator for members of the :attr:`Analysis.functions` which enables the function to store the results in the
    :class:`Analysis` object. If another function depends on these results it skips the repeated calculation.

    :param func: The function to be decorated.
    :returns: The decorated function.
    """
    @functools.wraps(func)
    def wrapper(self, contact_id, *args, **kwargs):
        if func.__name__ not in self._buffer:
            self._buffer[func.__name__] = {}
        if contact_id not in self._buffer[func.__name__]:
            self._buffer[func.__name__][contact_id] = func(self, contact_id, *args, **kwargs)
        return self._buffer[func.__name__][contact_id]
    return wrapper


class Analysis:
    """Implements specific analysis functions for a type of measurement.

    :param functions: A dictionary of the available analysis functions. The methods should take the contact id as
            only argument and return single values or a tuple of values.
    :param plots: A dictionary of the available analysis plots. The methods should take the contact id as only
        argument and return a :class:`matplotlib.pyplot.Figure` object.
    :param dataset: A tuple of (1) data arrays which are mapped to contact IDs and (2) the corresponding metadata of
        the dataset. Optionally, only a data dictionary is provided but then, a ``contact_position_dict`` is required.
    :param contact_position_dict: An optional dictionary of contact IDs and the corresponding positions/coordinates on
        the sample. Should be provided if the :class:`~cohesivm.dataset.Metadata` is not contained in the ``dataset``.
    """

    def __init__(self, functions: Dict[str, Callable[[str], DatabaseValue]],
                 plots: Dict[str, Callable[[str], plt.Figure]],
                 dataset: Union[Dataset, Dict[str, np.ndarray]],
                 contact_position_dict: Dict[str, Tuple[float, float]] = None
                 ) -> None:
        self._functions = functions
        self._plots = plots
        if type(dataset) == tuple:
            self._data = dataset[0]
            self._metadata = dataset[1]
            self._contact_position_dict = dataset[1].contact_position_dict
        else:
            self._data = dataset
            self._metadata = None
            self._contact_position_dict = contact_position_dict
        self._buffer = {}

    @property
    def data(self) -> Dict[str, np.ndarray]:
        """A mapping of the contacts IDs and the corresponding data arrays."""
        return self._data

    @property
    def metadata(self) -> Union[Metadata, None]:
        """The metadata associated with the data of this analysis."""
        return self._metadata

    @property
    def contact_position_dict(self) -> Union[Dict[str, Tuple[float, float]], None]:
        """A mapping of contact IDs with the corresponding positions/coordinates on the sample"""
        return self._contact_position_dict

    @property
    def functions(self) -> Dict[str, Callable[[str], DatabaseValue]]:
        """A dictionary of the available analysis functions."""
        return self._functions

    @property
    def plots(self) -> Dict[str, Callable[[str], plt.Figure]]:
        """A dictionary of the available analysis plots."""
        return self._plots

    def generate_result_dict(self, function_name: str) -> Dict[str, Any]:
        """Applies an analysis function to each measurement in the data.

        :param function_name: The string name of the analysis function from :attr:`functions`.
        :returns: A dictionary of contact IDs and the corresponding analysis results.
        """
        result_dict = {}
        for contact_id in self.data.keys():
            try:
                results = self.functions[function_name](contact_id)
            except ValueError:
                results = np.nan
            result_dict[contact_id] = results
        return result_dict

    def generate_result_maps(self, function_name: Union[str, None], result_dict: Union[None, Dict[str, Any]] = None) -> List[np.ndarray]:
        """Applies an analysis function to each measurement in the data and uses the contact positions to construct
        Numpy arrays of the results which represent the sample layout. Optionally uses the provided ``result_dict``.
        If the contact positions do not fall on a regular grid, the gaps will be filled with :attr:`numpy.nan`.

        :param function_name: The string name of the analysis function from the :attr:`functions`. Will be ignored
            if a ``result_dict`` is provided.
        :param result_dict: A dictionary of contact IDs and the corresponding analysis results.
        :returns: A list of :class:`numpy.ndarray` objects with analysis results structured corresponding to the
            :attr:`contact_position_dict`.
        """
        if self.contact_position_dict is None:
            raise ValueError('The parameter `contact_position_dict` must be filled in order to execute this method!')
        a = np.array(list(self.contact_position_dict.values()))
        origin = np.min(a, axis=0)
        length = np.max(a, axis=0) - origin
        distances = [[round(abs(p[1] - p[0]), 6) for p in itertools.combinations(a[:, i], r=2)] for i in [0, 1]]
        min_dist = []
        for dist in distances:
            if len(dist) > 1:
                dist = np.array(dist)
                min_dist.append(min(dist[dist > 0]))
            else:
                min_dist.append(1)
        min_dist = np.array(min_dist)
        result_size = np.flip(np.ceil((length + 1e-9) / min_dist).astype(int))
        result_map = np.ones(result_size) * np.nan
        result_maps = [result_map]
        if result_dict is None:
            result_dict = self.generate_result_dict(function_name)
        for contact, result in result_dict.items():
            x, y = ((np.array(self.contact_position_dict[contact]) - origin) / min_dist).round(6).astype(int)
            if type(result) == tuple:
                if len(result_maps) != len(result):
                    result_maps = [result_map.copy() for _ in result]
            else:
                result = (result,)
            for r, rm in zip(result, result_maps):
                rm[y, x] = r
        return result_maps


def plot_result_map(result_map: np.ndarray, title: str = None,
                    save_path: str = None, vrange: Tuple[float, float] = (None, None)):
    """Displays a result map as pixel plot with a corresponding color bar.

    :param result_map: A Numpy array of analysis results.
    :param title: An optional title for the plot.
    :param save_path: An optional path and filename to save the plot as an image.
    :param vrange: An optional value range for the pixel plot.
    """
    fig, ax = plt.subplots()
    img = ax.imshow(result_map, origin='lower', vmin=vrange[0], vmax=vrange[1])
    cax = ax.inset_axes([0, -0.1, 1, 0.0667], transform=ax.transAxes)
    if title is not None:
        ax.set_title(title)
    ax.set_xticks([])
    ax.set_yticks([])
    tick_values = [np.nanmin(result_map), np.nanmean(result_map), np.nanmax(result_map)]
    cbar = fig.colorbar(img, ax=ax, cax=cax, orientation="horizontal", ticks=tick_values)
    cbar.ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%.2f'))
    plt.tight_layout()
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path, bbox_inches='tight', transparent=True)
        plt.close()


from . import iv
