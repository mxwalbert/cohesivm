"""Module containing the classes and utility functions for the data management."""
from __future__ import annotations
from datetime import datetime
import builtins
import inspect
import numpy as np
import h5py
import pathlib
import hashlib
from typing import Iterable, Dict, List, Set, Tuple, Union
from abc import ABC, abstractmethod
from . import config


database_value_type = Union[Tuple[Union[int, float, bool]], int, float, bool, str]
database_dict_type = Dict[str, database_value_type]


class Dimensions:
    """Contains inner classes which represent the dimensions of a physical object."""
    @classmethod
    def parameters_from_string(cls, dimensions_string: str) -> Tuple[str, dict]:
        """Parses a parameter tuple from the string representation. Can be used to create a ``Dimension.Shape``
        object or a ``matplotlib.patches.Patch`` object.

        :param dimensions_string: String representation of a ``Dimension.Shape`` object.
        :returns: A tuple of the name of the ``Dimension.Shape`` class and the keyword arguments.
        """
        class_name, kwargs = dimensions_string.split(':')
        if len(kwargs) > 0:
            kwargs = {kwarg.split('=')[0]: kwarg.split('=')[1] for kwarg in kwargs.split(',')}
        else:
            kwargs = {}
        for parameter in inspect.signature(getattr(cls, class_name).__init__).parameters.values():
            if parameter.name != 'self':
                parameter_class = getattr(builtins, parameter.annotation) if type(parameter.annotation) == str else parameter.annotation
                kwargs[parameter.name] = parameter_class(kwargs[parameter.name])
        return class_name, kwargs

    @classmethod
    def object_from_parameters(cls, parameters: Tuple[str, dict]) -> Shape:
        """Parses a ``Dimension.Shape`` object from a parameters tuple which can be obtained from the
        `parameters_from_string` method.

        :param parameters: A tuple of the name of the ``Dimension.Shape`` class and the keyword arguments.
        :returns: The parsed ``Dimension.Shape`` object.
        """
        class_name, kwargs = parameters
        dimension_class = getattr(cls, class_name)
        return dimension_class(**kwargs)

    @classmethod
    def object_from_string(cls, dimensions_string: str) -> Shape:
        """Parses a ``Dimension.Shape`` object from its string representation.

        :param dimensions_string: String representation of a ``Dimension.Shape`` object.
        :returns: The parsed ``Dimension.Shape`` object.
        """
        parameters = cls.parameters_from_string(dimensions_string)
        return cls.object_from_parameters(parameters)

    class Shape(ABC):
        """Stores the attributes which describe the dimensions and implements a string representation."""
        def __str__(self):
            kwargs = ','.join([f'{arg}={getattr(self, arg)}' for arg in inspect.getfullargspec(self.__init__).args[1:]])
            return f'{self.__class__.__name__}:{kwargs}'

        def __eq__(self, other: Dimensions.Shape) -> bool:
            """Custom equality comparison for Dimensions.Shape instances."""
            return vars(self) == vars(other)

        @abstractmethod
        def area(self) -> float:
            """Returns the area of the shape."""

    class Point(Shape):
        def __init__(self):
            """A dimensionless point."""

        def area(self) -> float:
            return 0.

    class Rectangle(Shape):
        def __init__(self, width: float, height: float = None, unit: str = 'mm'):
            """A rectangular shape defined by its width and height. The origin is in the bottom left corner.

            :param width: Length of the rectangle in the x-direction.
            :param height: Length of the rectangle in the y-direction. Can be omitted to define a square.
            :param unit: The scale unit of the width and height.
            """
            self.width = width
            self.height = width if height is None else height
            self.unit = unit

        def area(self) -> float:
            return self.width * self.height

    class Circle(Shape):
        def __init__(self, radius: float, unit: str = 'mm'):
            """A circular shape defined by its radius. The origin is in the center.

            :param radius: The length of the circle radius.
            :param unit: The scale unit of the radius.
            """
            self.radius = radius
            self.unit = unit

        def area(self) -> float:
            return self.radius * self.radius * np.pi


class Metadata:
    """Contains the metadata of the experiment which is stored in the database. Follows the Dublin Core Metadata
    Initiative and uses standard values from the `config.ini` where applicable."""
    def __init__(self, measurement: str, measurement_settings: database_dict_type, sample_id: str, device: str,
                 channels: List[str], channels_settings: List[database_dict_type], interface: str,
                 sample_dimensions: str, pixel_ids: List[str], pixel_positions: List[Tuple[float, float]],
                 pixel_dimensions: List[str], **kwargs):
        """Initializes Metadata.

        :param measurement: Name of the measurement procedure as implemented in the corresponding class.
        :param measurement_settings: Dictionary containing the measurement settings.
        :param sample_id: Unique identifier of the sample.
        :param device: Name of the used device class.
        :param channels: List of class names of the channels.
        :param channels_settings: List of settings dictionaries of the channels.
        :param interface: Name of the used interface class.
        :param sample_dimensions: String representation of a ``Dimension.Shape`` object.
        :param pixel_ids: List of pixel id strings.
        :param pixel_positions: List of the pixel position tuples from the interface's `pixel_positions`.
        :param pixel_dimensions: List of ``Dimension.Shape`` strings.
        :param **kwargs: Keyword arguments which correspond to the terms of the Dublin Core Metadata Initiative.
        """
        self._measurement = measurement
        self._measurement_settings = measurement_settings
        self._settings_hash = self.parse_settings_hash(measurement_settings)
        self._sample_id = sample_id
        self._device = device
        self._channels = channels
        self._channels_settings = channels_settings
        self._interface = interface
        self._sample_dimensions = sample_dimensions
        self._pixel_ids = pixel_ids
        self._pixel_positions = pixel_positions
        self._pixel_dimensions = pixel_dimensions
        self._dcmi = {
            'identifier': None,
            'title': None,
            'date': None,
            'description': '"No description"',
            'publisher': config.get_option('DCMI', 'publisher'),
            'creator': config.get_option('DCMI', 'creator'),
            'type': 'dctype:Dataset',
            'rights': config.get_option('DCMI', 'rights'),
            'subject': config.get_option('DCMI', 'subject')
        }
        for kwarg, value in kwargs.items():
            if kwarg in self._dcmi.keys():
                self._dcmi[kwarg] = value

    @property
    def measurement(self) -> str:
        return self._measurement

    @property
    def measurement_settings(self) -> database_dict_type:
        return self._measurement_settings

    @property
    def settings_hash(self) -> str:
        return self._settings_hash

    @property
    def sample_id(self) -> str:
        return self._sample_id

    @property
    def device(self) -> str:
        return self._device

    @property
    def channels(self) -> List[str]:
        return self._channels

    @property
    def channels_settings(self) -> List[database_dict_type]:
        return self._channels_settings

    @property
    def interface(self) -> str:
        return self._interface

    @property
    def sample_dimensions(self) -> str:
        return self._sample_dimensions

    @property
    def pixel_ids(self) -> List[str]:
        return self._pixel_ids

    @property
    def pixel_positions(self) -> List[Tuple[float, float]]:
        return self._pixel_positions

    @property
    def pixel_dimensions(self) -> List[str]:
        return self._pixel_dimensions

    @property
    def dcmi(self) -> Dict[str, str]:
        """Dictionary containing the applicable core terms of the Dublin Core Metadata Initiative."""
        return self._dcmi

    @staticmethod
    def parse_settings_hash(settings: database_dict_type) -> str:
        """Parses the dictionary of settings in form of a string hash.

        :param settings: Dictionary containing the settings.
        :returns: Settings hash string.
        """
        parts = []
        for k, v in settings.items():
            encoded_string = (str(k) + str(v)).encode()
            parts.append(hashlib.sha256(encoded_string).hexdigest()[:16])
        return ':'.join(parts)


dataset_type = Tuple[Dict[str, np.ndarray], Metadata]


class Database:
    """Handles data management with methods for storing and retrieving data from an HDF5 file."""
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
        """The file location of the database."""
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

    @property
    def timestamp_size(self) -> int:
        """The sting length of the `self.timestamp`."""
        return len(self.timestamp)

    def initialize_dataset(self, m: Metadata) -> str:
        """Pre-structures the data in groups according to the metadata and returns the path of the dataset.

        :param m: Metadata object which contains all the information to structure the dataset. The information is saved
            in the database alongside the data.
        :returns: Dataset path in the database.
        """
        timestamp = self.timestamp
        dataset = f'/{m.measurement}/{m.settings_hash}/{timestamp}-{m.sample_id}'
        if m.dcmi['identifier'] is None:
            m.dcmi['identifier'] = f'"{dataset}"'
        if m.dcmi['title'] is None:
            m.dcmi['title'] = f'"Dataset for {m.measurement} of {m.sample_id}"'
        if m.dcmi['date'] is None:
            date = datetime.fromisoformat(timestamp).date().isoformat()
            m.dcmi['date'] = f'"{date}Z"^^dcterms:W3CDTF'
        with h5py.File(self.path, "a") as db:
            if m.measurement not in db.keys():
                db.create_group(m.measurement)
            if m.settings_hash not in db[m.measurement].keys():
                settings_group = db[m.measurement].create_group(m.settings_hash)
                for k, v in m.measurement_settings.items():
                    settings_group.attrs.create(k, v)
            data_group = db.create_group(dataset)
            data_group.attrs.create('measurement', m.measurement)
            for k, v in m.measurement_settings.items():
                data_group.attrs.create(f'{m.measurement}_{k}', v)
            data_group.attrs.create('sample_id', m.sample_id)
            data_group.attrs.create('device', m.device)
            data_group.attrs.create('channels', m.channels)
            for channel, channel_settings in zip(m.channels, m.channels_settings):
                for k, v in channel_settings.items():
                    data_group.attrs.create(f'{channel}_{k}', v)
            data_group.attrs.create('interface', m.interface)
            data_group.attrs.create('sample_dimensions', m.sample_dimensions)
            data_group.attrs.create('pixel_ids', m.pixel_ids)
            data_group.attrs.create('pixel_positions', m.pixel_positions)
            data_group.attrs.create('pixel_dimensions', m.pixel_dimensions)
            for k, v in m.dcmi.items():
                data_group.attrs.create(f'dcmi_{k}', v)
            if m.sample_id not in db['SAMPLES'].keys():
                db['SAMPLES'].create_group(m.sample_id)
            db['SAMPLES'][m.sample_id][timestamp] = h5py.SoftLink(dataset)
        return dataset

    def delete_dataset(self, dataset: str):
        """Deletes a dataset in the database.

        :param dataset: Dataset path in the database.
        """
        timestamp = dataset.split('/')[-1][:self.timestamp_size]
        sample_id = dataset.split('/')[-1][self.timestamp_size + 1:]
        with h5py.File(self.path, "r+") as db:
            del db[f'SAMPLES/{sample_id}/{timestamp}']
            del db[dataset]

    def save_data(self, data: np.ndarray, dataset: str, pixel: str = '0'):
        """Stores a data array in the database.

        :param data: Data array to be stored which should be a structured Numpy array. The names of the fields should
            contain the unit of the quantity in parentheses at the end of the string, e.g., 'Voltage (V)'
        :param dataset: Dataset path in the database.
        :param pixel: ID of the pixel from the pixel_ids of the Interface object.
        """
        with h5py.File(self.path, "a") as db:
            db.create_dataset(f'{dataset}/{pixel}', data=data)

    def load_data(self, dataset: str, pixel_ids: str | Iterable[str]) -> List[np.ndarray]:
        """Loads individual data arrays from a dataset.

        :param dataset: Dataset path in the database.
        :param pixel_ids: ID(s) of the pixel(s) to load data from. Can be a single value or an iterable of pixel IDs.
        :returns: List of loaded data arrays corresponding to the specified dataset and pixel IDs.
        """
        if type(pixel_ids) == str:
            pixel_ids = [pixel_ids]
        data_loaded = []
        with h5py.File(self.path, "r") as db:
            for pixel in pixel_ids:
                data_loaded.append(db[f'{dataset}/{pixel}'][()])
        return data_loaded

    def load_metadata(self, dataset: str) -> Metadata:
        """Loads the metadata of a dataset.

        :param dataset: Dataset path in the database.
        :returns: A ``Metadata`` object.
        """
        with h5py.File(self.path, "r") as db:
            metadata = dict(db[dataset].attrs)
        metadata_keys = list(metadata.keys())
        for k in metadata_keys:
            if type(metadata[k]) == np.ndarray:
                metadata[k] = tuple(metadata[k])
        metadata['measurement_settings'] = {}
        measurement = metadata['measurement']
        for k in filter(lambda x: x.startswith(f'{measurement}_'), metadata_keys):
            metadata['measurement_settings'][k.replace(f'{measurement}_', '')] = metadata[k]
            del metadata[k]
        metadata['channels_settings'] = []
        for channel in metadata['channels']:
            channel_settings = {}
            for k in filter(lambda x: x.startswith(f'{channel}_'), metadata_keys):
                channel_settings[k.replace(f'{channel}_', '')] = metadata[k]
                del metadata[k]
            metadata['channels_settings'].append(channel_settings)
        metadata['dcmi'] = {}
        for k in filter(lambda x: x.startswith(f'dcmi_'), metadata_keys):
            metadata['dcmi'][k.replace(f'dcmi_', '')] = metadata[k]
            del metadata[k]
        return Metadata(**metadata)

    def load_dataset(self, dataset: str) -> dataset_type:
        """Loads an entire dataset including the metadata.

        :param dataset: Dataset path in the database.
        :returns: A tuple of a dictionary of pixel IDs and loaded data arrays and the corresponding Metadata object.
        """
        data_loaded = {}
        with h5py.File(self.path, "r") as db:
            for pixel in db[dataset].keys():
                data_loaded[pixel] = db[f'{dataset}/{pixel}'][()]
        metadata = self.load_metadata(dataset)
        return data_loaded, metadata

    def get_dataset_length(self, dataset: str) -> int:
        """Returns the number of data arrays in a dataset.

        :param dataset: Dataset path in the database.
        :returns: Number of data arrays.
        """
        with h5py.File(self.path, "r") as db:
            dataset_length = len(db[dataset].keys())
        return dataset_length

    def get_measurements(self) -> List[str]:
        """Returns a list of measurement name strings which are available in the database.

        :returns: List of measurement name strings.
        """
        with h5py.File(self.path, "r") as db:
            measurements = list(db.keys())
        del measurements[measurements.index('SAMPLES')]
        return measurements

    def get_measurement_settings(self, dataset: str) -> database_dict_type:
        """Returns the measurement settings of the provided dataset.

        :param dataset: Dataset path in the database.
        :returns: Dictionary of the measurement settings.
        """
        _, measurement, settings_hash, _ = dataset.split('/')
        with h5py.File(self.path, "r") as db:
            measurement_settings = dict(db[measurement][settings_hash].attrs)
        for k in measurement_settings.keys():
            if type(measurement_settings[k]) == np.ndarray:
                measurement_settings[k] = tuple(measurement_settings[k])
        return measurement_settings

    def get_filters(self, measurement: str) -> Dict[str, Set[database_value_type]]:
        """Retrieve the unique filter values for a given measurement procedure in the database.

        This method scans the specified measurement group in the database and collects the unique filter values
        for each filter attribute. The filters are returned as a dictionary where the keys represent the filter
        attribute names, and the values are sets of unique filter values as tuples.

        :param measurement: The name of the measurement group in the database.
        :returns: A dictionary of filter attributes and their unique filter values.
        """
        filters = {}
        with h5py.File(self.path, "r") as db:
            for settings_group in db[measurement].values():
                for k, v in settings_group.attrs.items():
                    if k not in filters.keys():
                        filters[k] = set()
                    filters[k].add(tuple(v[()]) if type(v) == np.ndarray else v)
        return filters

    def filter_by_settings(self, measurement: str, settings: database_dict_type) -> List[str]:
        """Filters the measurements by the specified settings.

        :param measurement: String identifier of the measurement in the database.
        :param settings: Dictionary containing the settings to search for.
        :returns: List of dataset paths matching the specified settings.
        """
        matched_datasets = []
        filter_criteria = Metadata.parse_settings_hash(settings).split(':')
        with h5py.File(self.path, "r") as db:
            for settings_hash in db[measurement].keys():
                if all(criterium in settings_hash.split(':') for criterium in filter_criteria):
                    for dataset in db[measurement][settings_hash].keys():
                        matched_datasets.append(f'/{measurement}/{settings_hash}/{dataset}')
        return matched_datasets

    def filter_by_settings_batch(self, measurement: str,
                                 settings_batch: Dict[str, List[database_value_type]]) -> List[str]:
        """Subsequently filters the measurements by the specified settings batch.

        :param measurement: String identifier of the measurement in the database.
        :param settings_batch: Dictionary mapping the setting names to value lists which are used to subsequently filter
            the measurements.
        :returns: List of dataset paths matching the specified settings batch.
        """
        with h5py.File(self.path, "r") as db:
            available_hashes = set(db[measurement].keys())
        for setting, values in settings_batch.items():
            matched_hashes = set()
            for value in values:
                criterium = Metadata.parse_settings_hash({setting: value})
                matched_hashes = matched_hashes | set(filter(lambda x: criterium in x.split(':'), available_hashes))
            available_hashes = available_hashes & matched_hashes
        matched_datasets = []
        with h5py.File(self.path, "r") as db:
            for settings_hash in available_hashes:
                for group in db[measurement][settings_hash].keys():
                    matched_datasets.append(f'/{measurement}/{settings_hash}/{group}')
        return matched_datasets

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
        :returns: List of dataset paths matching the specified sample id.
        """
        matched_datasets = []
        with h5py.File(self.path, "r") as db:
            for softlink in db['SAMPLES'][sample_id].keys():
                matched_datasets.append(db['SAMPLES'][sample_id].get(softlink, getlink=True).path)
        return matched_datasets
