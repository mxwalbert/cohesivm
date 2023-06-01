"""Module containing the classes and utility functions for the data management."""
from __future__ import annotations
from datetime import datetime
import numpy as np
import h5py
import pathlib
from typing import Iterable, Dict, List, Set, Tuple
import copy


class Metadata:
    """
    Contains the metadata of the experiment which is stored in the database.
    """
    def __init__(self, measurement: str, settings: dict, sample_id: str, sample_layout: dict, dt: datetime = None):
        """Initializes Metadata.

        :param measurement: Name of the measurement procedure as implemented in the corresponding class.
        :param settings: Dictionary containing the measurement settings which is used for the group name in the database
            and will be stored as attributes. The keys must be strings and the values must be one-dimensional numpy
            arrays.
        :param sample_id: Unique identifier of the sample which is used for the dataset name.
        :param sample_layout: Dictionary containing the pixel ids and their location on the sample. Should be generated
            by the interface object. The keys must be strings and the values must be one-dimensional numpy arrays.
        :param dt: Datetime, e.g., begin of the measurement, in UTC time.
        :raises TypeError: If the type of any key in `settings` or `sample_layout` is not a string, if the type of any
            value in `settings` or `sample_layout` is not a numpy array or if the dtype of any value in `settings` or
            `sample_layout` is not numeric.
        :raises ValueError: If any value in `settings` or `sample_layout` is not a one-dimensional numpy array.
        """

        self.settings = settings
        self.measurement = measurement
        self.sample_id = sample_id
        self.sample_layout = sample_layout
        if not dt:
            dt = datetime.utcnow()
        self.datetime = np.array([dt.isoformat()]).astype('S')

    @property
    def settings(self) -> Dict[str, np.ndarray]:
        return self._settings

    @settings.setter
    def settings(self, new_value):
        self.__check_database_dict(new_value)
        self._settings = new_value
        self.__parse_settings_string()

    @property
    def sample_layout(self) -> Dict[str, np.ndarray]:
        return self._sample_layout

    @sample_layout.setter
    def sample_layout(self, new_value):
        self.__check_database_dict(new_value)
        self._sample_layout = new_value

    @staticmethod
    def __check_database_dict(database_dict):
        for k, v in database_dict.items():
            if type(k) != str:
                raise TypeError(f'Type of key {k} must be string!')
            if type(v) != np.ndarray:
                raise TypeError(f'Type of value {v} (key={k}) must be np.ndarray!')
            if not np.issubdtype(v.dtype, np.number):
                raise TypeError(f'DType of numpy array {v} (key={k}) must be numeric!')
            if v.ndim != 1:
                raise ValueError(f'Numpy array must be one-dimensional! Shape of {k}:{v} is {v.shape}.')

    def __parse_settings_string(self):
        self.settings_string = self.parse_settings_string(self._settings)

    def copy(self) -> Metadata:
        return copy.deepcopy(self)

    @staticmethod
    def parse_settings_string(settings: dict) -> str:
        """Parses the settings in form of a string which is used to store the dataset in the database.

        :param settings: Dictionary containing the settings which should be parsed as string.
        :returns: Settings string.
        """
        parts = []
        for k, v in settings.items():
            prefix = ''.join([kk[0] for kk in k.split('_')])
            parts.append(f"{prefix}:{'-'.join(v.astype(str))}")
        return ','.join(parts)


class Database:
    """
    Handles data management with methods for storing and retrieving data from an HDF5 file.
    """
    def __init__(self, path: str):
        """Initializes Database. A new file is created if no existing one is found.

        :param path: String of the HDF5 file path which must have an '.hdf5' or '.h5' suffix.
        :raises ValueError: If the suffix of `path` is not correct.
        :raises PermissionError: If the path cannot be written.
        :raises IsADirectoryError: If the path is not a file.
        """
        path = pathlib.Path(path)
        if path.suffix not in ['.hdf5', '.h5']:
            raise ValueError("HDF5 file must have an '.hdf5' or '.h5' suffix.")
        if not path.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
            except PermissionError:
                raise
            with h5py.File(path, "w") as db:
                db.create_group('SAMPLES')
        elif not path.is_file():
            raise IsADirectoryError('The provided path is a directory but should be an HDF5 file.')
        self.path = path
        self._datetime = datetime.utcnow().isoformat()

    @property
    def datetime(self) -> str:
        """UTC datetime string in ISO format which is updated to the current time before it is returned."""
        while self._datetime == datetime.utcnow().isoformat():
            pass
        self._datetime = datetime.utcnow().isoformat()
        return self._datetime

    def initialize_dataset(self, m: Metadata) -> str:
        """Pre-structures the data in groups according to the metadata and returns the stem of the dataset.

        :param m: Metadata object which contains all the information to structure the dataset. The information is saved
            in the database alongside the data.
        :returns: Stem of the dataset path in the database.
        """
        stem = f'/{m.measurement}/{m.settings_string}/{self.datetime}-{m.sample_id}'
        with h5py.File(self.path, "a") as db:
            if m.measurement not in db.keys():
                db.create_group(m.measurement)
            if m.settings_string not in db[m.measurement].keys():
                settings_group = db[m.measurement].create_group(m.settings_string)
                for k, v in m.settings.items():
                    settings_group.attrs.create(k, v)
            data_group = db.create_group(stem)
            for k, v in m.sample_layout.items():
                data_group.attrs.create(k, v)
            data_group.attrs.create('datetime', m.datetime)
            if m.sample_id not in db['SAMPLES'].keys():
                db['SAMPLES'].create_group(m.sample_id)
            db['SAMPLES'][m.sample_id][self.datetime] = h5py.SoftLink(stem)
        return stem

    def save(self, data: np.ndarray, stem: str, pixel: str = 0):
        """Stores a dataset in the database.

        :param data: Actual data to be stored which should be a structured Numpy array. The names of the fields should
            contain the unit of the quantity in parentheses at the end of the string, e.g., 'Voltage (V)'
        :param stem: Stem of the dataset path in the database.
        :param pixel: ID of the pixel which corresponds to the sample_layout from the Interface object.
        """
        with h5py.File(self.path, "a") as db:
            db.create_dataset(f'{stem}/{pixel}', data=data)

    def load(self, stem: str, pixels: str | Iterable[str]) -> List[np.ndarray]:
        """Loads the data from the specified datasets in the database.

        :param stem: Stem of the dataset path in the database.
        :param pixels: ID(s) of the pixel(s) to load data from. Can be a single pixel ID or an iterable of pixel IDs.
        :returns: List of loaded data arrays corresponding to the specified datasets and pixel IDs.
        """
        if type(pixels) == str:
            pixels = [pixels]
        data_loaded = []
        with h5py.File(self.path, "r") as db:
            for pixel in pixels:
                data_loaded.append(db[f'{stem}/{pixel}'][()])
        return data_loaded

    def get_filters(self, measurement: str) -> Dict[str, Set[Tuple]]:
        """Retrieve the unique filter values for a given measurement procedure in the database.

        This method scans the specified measurement group in the database and collects the unique filter values
        for each filter attribute. The filters are returned as a dictionary where the keys represent the filter
        attribute names, and the values are sets of unique filter values as tuples.

        :param measurement: The name of the measurement group in the database.
        :returns: A dictionary of filter attributes and their unique filter values as tuples.
        """
        filters = {}
        with h5py.File(self.path, "r") as db:
            for settings_group in db[measurement].values():
                for k, v in settings_group.attrs.items():
                    if k not in filters.keys():
                        filters[k] = set()
                    filters[k].add(tuple(v[()]))
        return filters

    def filter_by_settings(self, measurement: str, settings: dict) -> List[str]:
        """Filters the measurements by the specified settings.

        :param measurement: String identifier of the measurement in the database.
        :param settings: Dictionary containing the key-value pairs of the settings to search for.
        :returns: List of group paths matching the specified settings.
        """
        matched_groups = []
        filter_criteria = Metadata.parse_settings_string(settings).split(',')
        with h5py.File(self.path, "r") as db:
            for settings_string in db[measurement].keys():
                if all(criterium in settings_string.split(',') for criterium in filter_criteria):
                    for group in db[measurement][settings_string].keys():
                        matched_groups.append(f'/{measurement}/{settings_string}/{group}')
        return matched_groups

    def get_sample_ids(self) -> List[str]:
        """Returns a list of sample_id strings which are available in the database under /SAMPLES

        :returns: List of sample_id strings.
        """
        with h5py.File(self.path, "r") as db:
            sample_ids = list(db['SAMPLES'].keys())
        return sample_ids

    def filter_by_sample_id(self, sample_id: str) -> List[str]:
        """Filters the measurements by the specified sample.

        :param sample_id: String identifier of the sample in the database.
        :returns: List of group paths matching the specified sample id.
        """
        matched_groups = []
        with h5py.File(self.path, "r") as db:
            for softlink in db['SAMPLES'][sample_id].keys():
                matched_groups.append(db['SAMPLES'][sample_id].get(softlink, getlink=True).path)
        return matched_groups
