"""Module containing the classes and utility functions for the data management."""
from __future__ import annotations
from datetime import datetime
import inspect
import numpy as np
import h5py
import pathlib
from typing import Iterable, Dict, List, Set, Tuple, Union, Any
from abc import ABC, abstractmethod
from . import config

database_dict_type = Dict[
    str,
    Union[np.ndarray[Union[np.integer, np.floating, bool]], int, float, bool, str]
]


class Dimensions:
    """Contains inner classes which represent the dimensions of a physical object."""
    @classmethod
    def parameters_from_string(cls, dimensions_string: str):
        """Parses a parameter tuple from the string representation. Can be used to create a ``Dimension.Shape``
        object or a ``matplotlib.patches.Patch`` object."""
        class_name, kwargs = dimensions_string.split(':')
        if len(kwargs) > 0:
            kwargs = {kwarg.split('=')[0]: kwarg.split('=')[1] for kwarg in kwargs.split(',')}
        else:
            kwargs = {}
        for parameter in inspect.signature(getattr(cls, class_name).__init__).parameters.values():
            if parameter.name != 'self':
                kwargs[parameter.name] = parameter.annotation([parameter.name])
        return class_name, kwargs

    @classmethod
    def object_from_parameters(cls, parameters: Tuple[str, dict]):
        """Parses a ``Dimension.Shape`` object from a parameters tuple which can be obtained from the
        `parameters_from_string` method."""
        class_name, kwargs = parameters
        dimension_class = getattr(cls, class_name)
        return dimension_class(**kwargs)

    @classmethod
    def object_from_string(cls, dimensions_string: str):
        """Parses a ``Dimension.Shape`` object from its string representation."""
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
            """A rectangular shape defined by its width and height. The origin is in the bottom left corner."""
            self.width = width
            self.height = width if height is None else height
            self.unit = unit

        def area(self) -> float:
            return self.width * self.height

    class Circle(Shape):
        def __init__(self, radius: float, unit: str = 'mm'):
            """A circular shape defined by its radius. The origin is in the center."""
            self.radius = radius
            self.unit = unit

        def area(self) -> float:
            return self.radius * self.radius * np.pi


class Metadata:
    """Contains the metadata of the experiment which is stored in the database. Follows the Dublin Core Metadata
    Initiative and uses standard values from the `config.ini` where applicable."""
    def __init__(self, measurement: str, measurement_settings: database_dict_type, sample_id: str, device: str,
                 channels: List[str], channels_settings: List[database_dict_type], interface: str,
                 sample_dimensions: Dimensions.Shape, sample_layout: Dict[str, Tuple[float, float]],
                 pixel_dimensions: Dimensions.Shape | Dict[str, Dimensions.Shape], **kwargs):
        """Initializes Metadata.

        :param measurement: Name of the measurement procedure as implemented in the corresponding class.
        :param measurement_settings: Dictionary containing the measurement settings which is used for the group name in
            the database and will be stored as attributes. Numpy arrays will be flattened.
        :param sample_id: Unique identifier of the sample which is used for the dataset name.
        :param device: Name of the used device class which is stored as attribute alongside the dataset.
        :param channels: List of class names of the channels.
        :param channels_settings: List of settings dictionaries of the channels.
        :param interface: Name of the used interface class which is stored as attribute alongside the dataset.
        :param sample_dimensions: The physical size and shape of the sample.
        :param sample_layout: Dictionary containing the pixel ids and their coordinates in mm on the sample.
        :param pixel_dimensions: The physical size and shape of the pixels on the sample.
        :param **kwargs: Keyword arguments which correspond to the terms of the Dublin Core Metadata Initiative.
        """
        self._measurement = measurement
        for k in measurement_settings.keys():
            if type(measurement_settings[k]) == np.ndarray:
                if measurement_settings[k].ndim != 1:
                    measurement_settings[k] = measurement_settings[k].flatten()
        self._measurement_settings = measurement_settings
        self._settings_string = self.parse_settings_string(measurement_settings)
        self._sample_id = sample_id
        self._device = device
        self._channels = np.array(channels, dtype='S')
        self._channels_settings = np.stack(
            [self.to_string_array(channel_settings) for channel_settings in channels_settings]
        )
        self._interface = interface
        self._sample_dimensions = str(sample_dimensions)
        self._sample_layout = self.to_string_array(sample_layout)
        if issubclass(type(pixel_dimensions), Dimensions.Shape):
            pixel_dimensions = {pixel: pixel_dimensions for pixel in sample_layout.keys()}
        self._pixel_dimensions = self.to_string_array(pixel_dimensions)
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
        """Name of the measurement class."""
        return self._measurement

    @property
    def measurement_settings(self) -> database_dict_type:
        """Dictionary containing the measurement settings."""
        return self._measurement_settings

    @property
    def settings_string(self) -> str:
        """A string representation of the settings which is used to store the dataset in the database."""
        return self._settings_string

    @property
    def sample_id(self) -> str:
        """Unique identifier of the sample."""
        return self._sample_id

    @property
    def device(self) -> str:
        """Name of the used device class."""
        return self._device

    @property
    def channels(self) -> np.ndarray:
        """Class names of the channels as Numpy array."""
        return self._channels

    @property
    def channels_settings(self) -> np.ndarray:
        """The settings for each channel as database-compatible structured Numpy array."""
        return self._channels_settings

    @property
    def interface(self) -> str:
        """Name of the used interface class."""
        return self._interface

    @property
    def sample_dimensions(self) -> str:
        """The physical size and shape of the sample."""
        return self._sample_dimensions

    @property
    def sample_layout(self) -> np.ndarray:
        """Structured Numpy array containing the pixel ids and their coordinates in mm on the sample."""
        return self._sample_layout

    @property
    def pixel_dimensions(self) -> np.ndarray:
        """Structured Numpy array containing the pixel ids and their physical size and shape on the sample."""
        return self._pixel_dimensions

    @property
    def dcmi(self) -> Dict[str, str]:
        """Dictionary containing the applicable core terms of the Dublin Core Metadata Initiative."""
        return self._dcmi

    @staticmethod
    def to_string_array(input_dict: Dict[str, Any]) -> np.ndarray:
        """Converts a dictionary to a Numpy structured string array with the keys as names and dtype='S' for the
        values."""
        values = tuple([str(value).encode('utf-8') for value in input_dict.values()])
        string_dtype = h5py.string_dtype('utf-8', max(map(len, values)))
        keys = [(f'{key},{value.__class__.__name__}', string_dtype) for key, value in input_dict.items()]
        return np.array(values, dtype=keys)

    @staticmethod
    def from_string_array(string_array: np.ndarray) -> Dict[str, Any]:
        """Converts the Numpy structured string array back to a dictionary."""
        output_dictionary = {}
        for name in string_array.dtype.names:
            name_parts = name.split(',')
            key = ','.join(name_parts[:-1])
            class_name = name_parts[-1]
            if class_name == 'ndarray':
                value = np.array(string_array[name].astype(str).strip('[]').split())
                try:
                    int(value[0])
                    if '.' in value[0]:
                        value = value.astype(float)
                    else:
                        value = value.astype(int)
                except ValueError:
                    if value[0] in ['True', 'False']:
                        value = value.astype(bool)
            elif class_name == 'tuple':
                value = eval(string_array[name].astype(str))
            else:
                try:
                    value = eval(class_name)(string_array[name].astype(str))
                except NameError:
                    value = Dimensions.object_from_string(string_array[name].astype(str))
            output_dictionary[key] = value
        return output_dictionary

    @staticmethod
    def parse_settings_string(settings: dict) -> str:
        """Parses the settings in form of a string which is used to store the dataset in the database.

        :param settings: Dictionary containing the settings which should be parsed as string.
        :returns: Settings string.
        """
        parts = []
        for k, v in settings.items():
            if type(v) == np.ndarray:
                values = '-'.join(v.astype(str))
            else:
                values = str(v)
            parts.append(f"{k}:{values}")
        return ','.join(parts)


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

    def initialize_dataset(self, m: Metadata) -> str:
        """Pre-structures the data in groups according to the metadata and returns the path of the dataset.

        :param m: Metadata object which contains all the information to structure the dataset. The information is saved
            in the database alongside the data.
        :returns: Dataset path in the database.
        """
        timestamp = self.timestamp
        dataset = f'/{m.measurement}/{m.settings_string}/{timestamp}-{m.sample_id}'
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
            if m.settings_string not in db[m.measurement].keys():
                settings_group = db[m.measurement].create_group(m.settings_string)
                for k, v in m.measurement_settings.items():
                    settings_group.attrs.create(k, v)
            data_group = db.create_group(dataset)
            data_group.attrs.create('measurement', m.measurement)
            data_group.attrs.create('measurement_settings', Metadata.to_string_array(m.measurement_settings))
            data_group.attrs.create('sample_id', m.sample_id)
            data_group.attrs.create('device', m.device)
            data_group.attrs.create('channels', m.channels)
            data_group.attrs.create('channels_settings', m.channels_settings)
            data_group.attrs.create('interface', m.interface)
            data_group.attrs.create('sample_dimensions', m.sample_dimensions)
            data_group.attrs.create('sample_layout', m.sample_layout)
            data_group.attrs.create('pixel_dimensions', m.pixel_dimensions)
            data_group.attrs.create('dcmi', m.to_string_array(m.dcmi))
            if m.sample_id not in db['SAMPLES'].keys():
                db['SAMPLES'].create_group(m.sample_id)
            db['SAMPLES'][m.sample_id][timestamp] = h5py.SoftLink(dataset)
        return dataset

    def delete_dataset(self, dataset: str):
        """Deletes a dataset in the database.

        :param dataset: Dataset path in the database.
        """
        with h5py.File(self.path, "a") as db:
            del db[dataset]

    def save(self, data: np.ndarray, dataset: str, pixel: str = 0):
        """Stores a dataset in the database.

        :param data: Actual data to be stored which should be a structured Numpy array. The names of the fields should
            contain the unit of the quantity in parentheses at the end of the string, e.g., 'Voltage (V)'
        :param dataset: Dataset path in the database.
        :param pixel: ID of the pixel which corresponds to the sample_layout from the Interface object.
        """
        with h5py.File(self.path, "a") as db:
            db.create_dataset(f'{dataset}/{pixel}', data=data)

    def load_data(self, dataset: str, pixels: str | Iterable[str]) -> List[np.ndarray]:
        """Loads individual data arrays from a dataset.

        :param dataset: Dataset path in the database.
        :param pixels: ID(s) of the pixel(s) to load data from. Can be a single pixel ID or an iterable of pixel IDs.
        :returns: List of loaded data arrays corresponding to the specified dataset and pixel IDs.
        """
        if type(pixels) == str:
            pixels = [pixels]
        data_loaded = []
        with h5py.File(self.path, "r") as db:
            for pixel in pixels:
                data_loaded.append(db[f'{dataset}/{pixel}'][()])
        return data_loaded

    def load_metadata(self, dataset: str) -> Dict[str, Any]:
        """Loads the metadata of a dataset.

        :param dataset: Dataset path in the database.
        :returns: Dictionary containing the parameters to construct a Metadata object.
        """
        with h5py.File(self.path, "r") as db:
            metadata = dict(db[dataset].attrs)
        metadata['measurement_settings'] = Metadata.from_string_array(metadata['measurement_settings'])
        metadata['channels'] = metadata['channels'].astype(str).tolist()
        metadata['channels_settings'] = [
            Metadata.from_string_array(settings) for settings in metadata['channels_settings']
        ]
        metadata['sample_dimensions'] = Dimensions.object_from_string(metadata['sample_dimensions'])
        metadata['sample_layout'] = Metadata.from_string_array(metadata['sample_layout'])
        metadata['pixel_dimensions'] = Metadata.from_string_array(metadata['pixel_dimensions'])
        return metadata

    def load_dataset(self, dataset: str) -> Tuple[Dict[str, np.ndarray], Dict[str, Any]]:
        """Loads an entire dataset including the metadata.

        :param dataset: Dataset path in the database.
        :returns: Dictionary of pixel IDs and loaded data arrays and the corresponding Metadata object.
        """
        data_loaded = {}
        with h5py.File(self.path, "r") as db:
            for pixel in db[dataset].keys():
                data_loaded[pixel] = db[f'{dataset}/{pixel}'][()]
        metadata = self.load_metadata(dataset)
        return data_loaded, metadata

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
                    filters[k].add(tuple(v[()]) if type(v) == np.ndarray else (v,))
        return filters

    def filter_by_settings(self, measurement: str, settings: dict) -> List[str]:
        """Filters the measurements by the specified settings.

        :param measurement: String identifier of the measurement in the database.
        :param settings: Dictionary containing the key-value pairs of the settings to search for.
        :returns: List of dataset paths matching the specified settings.
        """
        matched_datasets = []
        filter_criteria = Metadata.parse_settings_string(settings).split(',')
        with h5py.File(self.path, "r") as db:
            for settings_string in db[measurement].keys():
                if all(criterium in settings_string.split(',') for criterium in filter_criteria):
                    for group in db[measurement][settings_string].keys():
                        matched_datasets.append(f'/{measurement}/{settings_string}/{group}')
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
