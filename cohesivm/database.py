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
    def __init__(self, measurement: str, settings: Dict[str, np.ndarray] | Dict[str, Iterable], sample_id: str,
                 sample_layout: Dict[str, np.ndarray] | Dict[str, Iterable], timestamp: datetime = None):
        """Initializes Metadata.

        :param measurement: Name of the measurement procedure as implemented in the corresponding class.
        :param settings: Dictionary containing the measurement settings which is used for the group name in the database
            and will be stored as attributes. The keys must be strings and the values must be one-dimensional numpy
            arrays.
        :param sample_id: Unique identifier of the sample which is used for the dataset name.
        :param sample_layout: Dictionary containing the pixel ids and their location on the sample. Should be generated
            by the interface object. The keys must be strings and the values must be one-dimensional numpy arrays.
        :param timestamp: Datetime, e.g., begin of the measurement, in UTC time.
        :raises TypeError: If the type of any key in `settings` or `sample_layout` is not a string, if the type of any
            value in `settings` or `sample_layout` is not a numpy array or if the dtype of any value in `settings` or
            `sample_layout` is not numeric. Also, if `measurement` or `sample_id` cannot be cast to a string.
        :raises ValueError: If any value in `settings` or `sample_layout` is not a one-dimensional numpy array.
        """

        self.measurement = measurement
        self.settings = settings
        self.sample_id = sample_id
        self.sample_layout = sample_layout
        if not timestamp:
            timestamp = datetime.utcnow()
        self.timestamp = timestamp

    @property
    def measurement(self) -> str:
        return self._measurement

    @measurement.setter
    def measurement(self, new_value: str):
        try:
            new_value = str(new_value)
        except Exception:
            raise TypeError("The new value for the `measurement` property must be of type string! Casting it failed.")
        self._measurement = new_value

    @property
    def settings(self) -> Dict[str, np.ndarray]:
        return self._settings

    @settings.setter
    def settings(self, new_value: Dict[str, np.ndarray] | Dict[str, Iterable]):
        self._check_database_dict(new_value)
        self._settings = new_value
        self._parse_settings_string()

    @property
    def sample_id(self) -> str:
        return self._sample_id

    @sample_id.setter
    def sample_id(self, new_value: str):
        try:
            new_value = str(new_value)
        except Exception:
            raise TypeError("The new value for the `sample_id` property must be of type string! Casting it failed.")
        self._sample_id = new_value

    @property
    def sample_layout(self) -> Dict[str, np.ndarray]:
        return self._sample_layout

    @sample_layout.setter
    def sample_layout(self, new_value: Dict[str, np.ndarray] | Dict[str, Iterable]):
        self._check_database_dict(new_value)
        self._sample_layout = new_value

    @property
    def timestamp(self) -> np.ndarray:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_value: datetime):
        if type(new_value) is not datetime:
            raise TypeError("The `timestamp` property must be of type datetime.datetime!")
        self._timestamp = np.array([new_value.isoformat()]).astype('S')

    @staticmethod
    def _check_database_dict(database_dict):
        for k in database_dict.keys():
            if type(k) != str:
                raise TypeError(f'Type of key {k} must be string!')
            if type(database_dict[k]) != np.ndarray:
                try:
                    database_dict[k] = np.array(database_dict[k])
                except Exception:
                    raise TypeError(f'Type of {database_dict[k]} (key={k}) must be np.ndarray! Casting it failed.')
            if not np.issubdtype(database_dict[k].dtype, np.number):
                raise TypeError(f'DType of numpy array {database_dict[k]} (key={k}) must be numeric!')
            if database_dict[k].ndim != 1:
                raise ValueError(f"Numpy array must be one-dimensional! "
                                 f"Shape of '{k}':{database_dict[k]} is {database_dict[k].shape}.")

    def _parse_settings_string(self):
        self.settings_string = self.parse_settings_string(self._settings)

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

    def copy(self) -> Metadata:
        """Returns a deepcopy of the Metadata instance."""
        return copy.deepcopy(self)


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
        self._path = path
        self.__timestamp = datetime.utcnow().isoformat()

    @property
    def path(self) -> pathlib.Path:
        return self._path

    @property
    def timestamp(self) -> str:
        """UTC datetime string in ISO format which is updated to the current time before it is returned."""
        while self.__timestamp == datetime.utcnow().isoformat():
            pass
        self.__timestamp = datetime.utcnow().isoformat()
        return self.__timestamp

    @property
    def _timestamp(self) -> str:
        """UTC datetime string in ISO format without updating it."""
        return self.__timestamp

    def initialize_dataset(self, m: Metadata) -> str:
        """Pre-structures the data in groups according to the metadata and returns the stem of the dataset.

        :param m: Metadata object which contains all the information to structure the dataset. The information is saved
            in the database alongside the data.
        :returns: Stem of the dataset path in the database.
        """
        timestamp = self.timestamp
        stem = f'/{m.measurement}/{m.settings_string}/{timestamp}-{m.sample_id}'
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
            data_group.attrs.create('datetime', m.timestamp)
            if m.sample_id not in db['SAMPLES'].keys():
                db['SAMPLES'].create_group(m.sample_id)
            db['SAMPLES'][m.sample_id][timestamp] = h5py.SoftLink(stem)
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
