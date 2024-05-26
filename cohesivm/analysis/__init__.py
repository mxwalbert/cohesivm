"""This module is used to analyze the measurements by implementing specific functions for each type of measurement. The
results can be aggregated in property maps and visualized for combinatorial analysis as well."""
from __future__ import annotations

import functools
import itertools
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker
from typing import Dict, Tuple, Callable, Any, List
from ..database import database_value_type, dataset_type


def result_buffer(func):
    @functools.wraps(func)
    def wrapper(self, pixel_id, *args, **kwargs):
        if pixel_id not in self._buffer[func.__name__]:
            self._buffer[func.__name__][pixel_id] = func(self, pixel_id, *args, **kwargs)
        return self._buffer[func.__name__][pixel_id]
    return wrapper


class AnalysisABC:
    """Implements specific analysis functions for a type of measurement."""

    def __init__(self, functions: Dict[str, Callable[[str], database_value_type]],
                 plots: Dict[str, Callable[[str], plt.Figure]],
                 dataset: Dict[str, np.ndarray] | dataset_type,
                 pixel_positions: Dict[str, Tuple[float, float]] = None):
        """Initializes the analysis object.

        :param functions: A dictionary of the available analysis functions. The methods should take the pixel id as only
            argument and return single values or a tuple of values.
        :param plots: A dictionary of the available analysis plots. The methods should take the pixel id as only
            argument and return a ``matplotlib.pyplot.Figure`` object.
        :param dataset: A tuple of a dictionary of pixel IDs and data arrays and the corresponding Metadata object.
        :param pixel_positions: An optional dictionary of pixel IDs and the corresponding positions/coordinates on the
            sample. Should be provided if the metadata is not contained in the dataset.
        """
        self._functions = functions
        self._plots = plots
        if type(dataset) == tuple:
            self.dataset = dataset[0]
            self.metadata = dataset[1]
            self.pixel_positions = dict(zip(dataset[1].pixel_ids, dataset[1].pixel_positions))
        else:
            self.dataset = dataset
            self.metadata = None
            self.pixel_positions = pixel_positions
        self._buffer = {func.__name__: {} for func in self.functions.values()}

    @property
    def functions(self) -> Dict[str, Callable[[str], database_value_type]]:
        """A dictionary of the available analysis functions."""
        return self._functions

    @property
    def plots(self) -> Dict[str, Callable[[str], plt.Figure]]:
        """A dictionary of the available analysis plots."""
        return self._plots

    def generate_result_dict(self, function_name: str) -> Dict[str, Any]:
        """Applies an analysis function to each measurement in the dataset.

        :param function_name: The string name of the analysis function from `functions` dictionary.
        :returns: A dictionary of pixel IDs and the corresponding analysis results.
        """
        result_dict = {}
        for pixel in self.dataset.keys():
            try:
                results = self.functions[function_name](pixel)
            except ValueError:
                results = np.nan
            result_dict[pixel] = results
        return result_dict

    def generate_result_maps(self, function_name: str | None, result_dict: None | Dict[str, Any] = None) -> List[np.ndarray]:
        """Applies an analysis function to each measurement in the dataset and uses the pixel positions to construct
        Numpy arrays of the results which represent the sample layout. Optionally uses the provided `result_dict`. If
        the pixel positions do not fall on a regular grid, the gaps will be filled with ``numpy.nan``.

        :param function_name: The string name of the analysis function from the `functions` dictionary. Will be ignored
            if a `result_dict` is provided.
        :param result_dict:
        :returns: A list of Numpy arrays with analysis results structured corresponding to the `pixel_positions`.
        """
        if self.pixel_positions is None:
            raise ValueError('The parameter `pixel_positions` must be filled in order to execute this method!')
        a = np.array(list(self.pixel_positions.values()))
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
        result_size = np.flip(np.ceil(length / min_dist).astype(int)) + 1
        result_map = np.ones(result_size) * np.nan
        result_maps = [result_map]
        if result_dict is None:
            result_dict = self.generate_result_dict(function_name)
        for pixel, result in result_dict.items():
            x, y = ((np.array(self.pixel_positions[pixel]) - origin) / min_dist).round(6).astype(int)
            if type(result) == tuple:
                if len(result_maps) != len(result):
                    result_maps = [result_map.copy() for _ in result]
            else:
                result = (result,)
            for r, rm in zip(result, result_maps):
                rm[y, x] = r
        return result_maps


def plot_result_map(result_map: np.ndarray, title: str = None,
                    save_path: str = None, vrange: tuple[float, float] = (None, None)):
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
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path, bbox_inches='tight', transparent=True)
        plt.close()
