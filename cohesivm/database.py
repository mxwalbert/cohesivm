"""This module contains the classes and utility functions for the data management."""
from __future__ import annotations
import sys
import datetime
import builtins
import inspect
import numpy as np
import h5py
import pathlib
import hashlib
from typing import Iterable, Dict, List, Set, Tuple, Union
from abc import ABC, abstractmethod
from cohesivm import config


DatabaseValue = Union[Tuple[Union[int, float, bool]], int, float, bool, str]
DatabaseDict = Dict[str, DatabaseValue]


class Dimensions:
    """Contains classes and methods to represent the dimensions of a physical object. The inner classes follow the
    :class:`Shape` abstract base class.
    """
    @classmethod
    def parameters_from_string(cls, dimensions_string: str) -> Tuple[str, dict]:
        """Parses a parameter tuple from the string representation. Can be used to create a :class:`Shape`
        object or a :class:`matplotlib.patches.Patch` object.

        :param dimensions_string: String representation of a :class:`Shape` object.
        :returns: A tuple of the name of the :class:`Shape` class and the keyword arguments.
        """
        class_name, kwargs = dimensions_string.split(':')
        if len(kwargs) > 0:
            kwargs = {kwarg.split('=')[0]: kwarg.split('=')[1] for kwarg in kwargs.split(';')}
        else:
            kwargs = {}
        for parameter in inspect.signature(getattr(cls, class_name).__init__).parameters.values():
            if parameter.name == 'self':
                continue
            raw_value = kwargs[parameter.name]
            if type(parameter.annotation) == str:
                if len(parameter.annotation.split('[')) == 1:
                    value = getattr(builtins, parameter.annotation)(raw_value)
                else:
                    outer_class, inner_class = parameter.annotation[:-1].split('[')
                    if outer_class.lower() != 'list':
                        raise NotImplementedError('Only lists of values can be parsed as parameters!')
                    value = [getattr(builtins, inner_class)(v) for v in raw_value[1:-1].split(',')]
            else:
                value = parameter.annotation(raw_value)
            kwargs[parameter.name] = value
        return class_name, kwargs

    @classmethod
    def object_from_parameters(cls, parameters: Tuple[str, dict]) -> Shape:
        """Parses a :class:`Shape` object from a parameters tuple which can be obtained from the
        :meth:`parameters_from_string` method.

        :param parameters: A tuple of the name of the :class:`Shape` class and the keyword arguments.
        :returns: The parsed :class:`Shape` object.
        """
        class_name, kwargs = parameters
        dimension_class = getattr(cls, class_name)
        return dimension_class(**kwargs)

    @classmethod
    def object_from_string(cls, dimensions_string: str) -> Shape:
        """Parses a :class:`Shape` object from its string representation.

        :param dimensions_string: String representation of a :class:`Shape` object.
        :returns: The parsed :class:`Shape` object.
        """
        parameters = cls.parameters_from_string(dimensions_string)
        return cls.object_from_parameters(parameters)

    class Shape(ABC):
        """Abstract base class. Stores the attributes which describe the dimensions. Implements a string representation
        and an equality comparison."""
        def __str__(self) -> str:
            kwargs = ';'.join([f'{arg}={getattr(self, arg)}' for arg in inspect.getfullargspec(self.__init__).args[1:]])
            return f'{self.__class__.__name__}:{kwargs}'

        def __eq__(self, other: Dimensions.Shape) -> bool:
            return vars(self) == vars(other)

        @abstractmethod
        def area(self) -> float:
            """Returns the area of the shape."""

    class Point(Shape):
        """A dimensionless point."""

        def area(self) -> float:
            return 0.

    class Line(Shape):
        """A line defined by its length.

        :param length: Length of the line.
        :param unit: Scale unit of the length."""
        def __init__(self, length: float, unit: str = 'mm') -> None:
            self._length = length
            self._unit = unit

        def area(self) -> float:
            return 0.

    class Rectangle(Shape):
        """A rectangular shape defined by its width and height. The origin is in the bottom left corner.

        :param width: Length of the rectangle in the x-direction.
        :param height: Length of the rectangle in the y-direction. Can be omitted to define a square.
        :param unit: Scale unit of the width and height."""
        def __init__(self, width: float, height: float = None, unit: str = 'mm') -> None:
            self._width = width
            self._height = width if height is None else height
            self._unit = unit

        @property
        def width(self) -> float:
            """Length of the rectangle in the x-direction."""
            return self._width

        @property
        def height(self) -> float:
            """Length of the rectangle in the y-direction."""
            return self._height

        @property
        def unit(self) -> str:
            """Scale unit of the width and height."""
            return self._unit

        def area(self) -> float:
            return self.width * self.height

    class Circle(Shape):
        """A circular shape defined by its radius. The origin is in the center.

        :param radius: Length of the circle radius.
        :param unit: Scale unit of the radius."""
        def __init__(self, radius: float, unit: str = 'mm') -> None:
            self._radius = radius
            self._unit = unit

        @property
        def radius(self) -> float:
            """Length of the circle radius."""
            return self._radius

        @property
        def unit(self) -> str:
            """Scale unit of the radius."""
            return self._unit

        def area(self) -> float:
            return self.radius * self.radius * np.pi

    class Generic(Shape):
        """A generic shape defined by its x and y coordinates.

        :param x_coords: List of x coordinates.
        :param y_coords: List of y coordinates.
        :param unit: Scale unit of the coordinates."""

        def __init__(self, x_coords: List[float], y_coords: List[float], unit: str = 'mm') -> None:
            if len(x_coords) != len(y_coords):
                raise ValueError("x_coords and y_coords must have the same length.")
            self._x_coords = x_coords
            self._y_coords = y_coords
            self._unit = unit

        @property
        def x_coords(self) -> List[float]:
            """List of x coordinates."""
            return self._x_coords

        @property
        def y_coords(self) -> List[float]:
            """List of y coordinates."""
            return self._y_coords

        @property
        def unit(self) -> str:
            """Scale unit of the coordinates."""
            return self._unit

        def area(self) -> float:
            """Use the Shoelace formula to calculate the area of the polygon. Only works for closed shapes."""
            n = len(self._x_coords)
            area = 0.0
            for i in range(n):
                j = (i + 1) % n
                area += self._x_coords[i] * self._y_coords[j]
                area -= self._y_coords[i] * self._x_coords[j]
            area = abs(area) / 2.0
            return area


class Metadata:
    """Contains the metadata of the experiment which is stored in the database. Follows the Dublin Core Metadata
    Initiative and uses standard values from the ``config.ini`` where applicable.

    :param measurement: Name of the measurement procedure as implemented in the corresponding class.
    :param measurement_settings: Dictionary containing the measurement settings.
    :param sample_id: Unique identifier of the sample.
    :param device: Name of the used device class.
    :param channels: List of class names of the channels.
    :param channels_settings: List of settings dictionaries of the channels.
    :param interface: Name of the used interface class.
    :param interface_dimensions: String representation of a :class:`Shape` object which corresponds to the shape of the
        interface.
    :param contact_ids: List of contact id strings.
    :param contact_positions: List of the contact position tuples which correspond to the coordinates of the contacts
        on the interface.
    :param pixel_dimensions: List of :class:`Shape` strings which represent the sizes and shapes of the pixels on
        the sample.
    :param dcmi: Optional dictionary of terms of the Dublin Core Metadata Initiative which will overwrite the
        default values.
    """
    def __init__(self, measurement: str, measurement_settings: DatabaseDict, sample_id: str, device: str,
                 channels: List[str], channels_settings: List[DatabaseDict], interface: str,
                 interface_dimensions: str, contact_ids: List[str], contact_positions: List[Tuple[float, float]],
                 pixel_dimensions: List[str], dcmi: Dict[str, str] = None) -> None:
        self._measurement = measurement
        self._measurement_settings = measurement_settings
        self._settings_hash = self.parse_settings_hash(measurement_settings)
        self._sample_id = sample_id
        self._device = device
        self._channels = channels
        self._channels_settings = channels_settings
        self._interface = interface
        self._interface_dimensions = interface_dimensions
        self._contact_ids = contact_ids
        self._contact_positions = contact_positions
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
        if dcmi is not None:
            for k, v in dcmi.items():
                self._dcmi[k] = v

    def __str__(self) -> str:
        return (f'Metadata for {self.measurement} of "{self.sample_id}" '
                f'using the {self.interface} interface on the {self.device}"')

    def __repr__(self) -> str:
        return f'Metadata({self.measurement}, {self.device}, {self.interface})'

    @property
    def measurement(self) -> str:
        """Name of the measurement procedure as implemented in the corresponding class."""
        return self._measurement

    @property
    def measurement_settings(self) -> DatabaseDict:
        """Dictionary containing the measurement settings."""
        return self._measurement_settings

    @property
    def settings_hash(self) -> str:
        """The :attr:`measurement_settings` parsed into a string."""
        return self._settings_hash

    @property
    def sample_id(self) -> str:
        """Unique identifier of the sample."""
        return self._sample_id

    @property
    def device(self) -> str:
        """Name of the used device class."""
        return self._device

    @property
    def channels(self) -> List[str]:
        """List of class names of the channels."""
        return self._channels

    @property
    def channels_settings(self) -> List[DatabaseDict]:
        """List of settings dictionaries of the channels."""
        return self._channels_settings

    @property
    def interface(self) -> str:
        """Name of the used interface class."""
        return self._interface

    @property
    def interface_dimensions(self) -> str:
        """String representation of a :class:`Shape` object which corresponds to the shape of the interface."""
        return self._interface_dimensions

    @property
    def contact_ids(self) -> List[str]:
        """List of contact id strings."""
        return self._contact_ids

    @property
    def contact_positions(self) -> List[Tuple[float, float]]:
        """List of the contact position tuples which correspond to the coordinates of the contacts on the interface."""
        return self._contact_positions

    @property
    def contact_position_dict(self) -> Dict[str, Tuple[float, float]]:
        """A dictionary mapping the :attr:`contact_ids` to the :attr:`contact_positions`."""
        return dict(zip(self.contact_ids, self.contact_positions))

    @property
    def pixel_dimensions(self) -> List[str]:
        """List of :class:`Shape` strings which represent the sizes and shapes of the pixels on the sample."""
        return self._pixel_dimensions

    @property
    def pixel_dimension_dict(self) -> Dict[str, str]:
        """A dictionary mapping the :attr:`contact_ids` to the :attr:`pixel_dimensions`."""
        return dict(zip(self.contact_ids, self.pixel_dimensions))

    @property
    def dcmi(self) -> Dict[str, str]:
        """Dictionary containing the applicable core terms of the Dublin Core Metadata Initiative."""
        return self._dcmi

    @staticmethod
    def parse_settings_hash(settings: DatabaseDict) -> str:
        """Parses the `settings` in form of a hash string.

        :param settings: Dictionary containing the settings.
        :returns: Settings hash string.
        """
        parts = []
        for k, v in settings.items():
            encoded_string = (str(k) + str(v)).encode()
            parts.append(hashlib.sha256(encoded_string).hexdigest()[:16])
        return ':'.join(parts)


Dataset = Tuple[Dict[str, np.ndarray], Metadata]


class Database:
    """Handles data management with methods for storing and retrieving data from an HDF5 file. A new file is created
    during initialization if no existing one is found.

    :param path: String of the HDF5 file path which must have an '.hdf5' or '.h5' suffix.
    :raises ValueError: If the suffix of `path` is not correct.
    :raises PermissionError: If the path cannot be written.
    :raises IsADirectoryError: If the path is not a file.
    """
    def __init__(self, path: str) -> None:
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
        self.__timestamp = self._utc_time()

    @property
    def path(self) -> pathlib.Path:
        """The file path of the HDF5 database file."""
        return self._path

    @staticmethod
    def _utc_time() -> str:
        if sys.version_info[1] <= 11:
            return datetime.datetime.utcnow().isoformat()
        else:
            return datetime.datetime.now(datetime.UTC).isoformat()

    @property
    def timestamp(self) -> str:
        """UTC datetime string in ISO format which is updated to the current time before it is returned."""
        while self.__timestamp == self._utc_time():
            pass
        self.__timestamp = self._utc_time()
        return self.__timestamp

    @property
    def _timestamp(self) -> str:
        """UTC datetime string in ISO format without updating it."""
        return self.__timestamp

    @property
    def timestamp_size(self) -> int:
        """The string length of the `self.timestamp`."""
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
            date = datetime.datetime.fromisoformat(timestamp).date().isoformat()
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
            data_group.attrs.create('interface_dimensions', m.interface_dimensions)
            data_group.attrs.create('contact_ids', m.contact_ids)
            data_group.attrs.create('contact_positions', m.contact_positions)
            data_group.attrs.create('pixel_dimensions', m.pixel_dimensions)
            for k, v in m.dcmi.items():
                data_group.attrs.create(f'dcmi_{k}', v)
            if m.sample_id not in db['SAMPLES'].keys():
                db['SAMPLES'].create_group(m.sample_id)
            db['SAMPLES'][m.sample_id][timestamp] = h5py.SoftLink(dataset)
        return dataset

    def delete_dataset(self, dataset: str) -> None:
        """Deletes a dataset in the database.

        :param dataset: Dataset path in the database.
        """
        timestamp = dataset.split('/')[-1][:self.timestamp_size]
        sample_id = dataset.split('/')[-1][self.timestamp_size + 1:]
        with h5py.File(self.path, "r+") as db:
            del db[f'SAMPLES/{sample_id}/{timestamp}']
            del db[dataset]

    def delete_data(self, dataset: str, contact_id: str) -> None:
        """Deletes a single data array from the specified dataset.

        :param dataset: Dataset path in the database.
        :param contact_id: ID of the contact, i.e., the identifier of the data array which should be deleted.
        """
        with h5py.File(self.path, "a") as db:
            del db[f'{dataset}/{contact_id}']

    def save_data(self, data: np.ndarray, dataset: str, contact_id: str = '0') -> None:
        """Stores a data array in the database. Overrides existing data.

        :param data: Data array to be stored which should be a structured Numpy array. The names of the fields should
            contain the unit of the quantity in parentheses at the end of the string, e.g., 'Voltage (V)'
        :param dataset: Dataset path in the database.
        :param contact_id: ID of the contact from the contact_ids of the Interface object. Defaults to '0'.
        """
        with h5py.File(self.path, "a") as db:
            try:
                db.create_dataset(f'{dataset}/{contact_id}', data=data)
            except ValueError:
                del db[f'{dataset}/{contact_id}']
                db.create_dataset(f'{dataset}/{contact_id}', data=data)

    def load_data(self, dataset: str, contact_ids: Union[str, Iterable[str]]) -> List[np.ndarray]:
        """Loads individual data arrays from a dataset.

        :param dataset: Dataset path in the database.
        :param contact_ids: ID(s) of the contact(s) to load data from. Can be a single string or an iterable of strings.
        :returns: List of loaded data arrays corresponding to the specified dataset and contact IDs.
        """
        if type(contact_ids) == str:
            contact_ids = [contact_ids]
        data_loaded = []
        with h5py.File(self.path, "r") as db:
            for contact_id in contact_ids:
                data_loaded.append(db[f'{dataset}/{contact_id}'][()])
        return data_loaded

    def load_metadata(self, dataset: str) -> Metadata:
        """Loads the metadata of a dataset.

        :param dataset: Dataset path in the database.
        :returns: The metadata corresponding to the specified dataset.
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

    def load_dataset(self, dataset: str) -> Dataset:
        """Loads an entire dataset including the metadata.

        :param dataset: Dataset path in the database.
        :returns: A dictionary of contact IDs and loaded data arrays together with the corresponding metadata.
        """
        data_loaded = {}
        with h5py.File(self.path, "r") as db:
            for contact_id in db[dataset].keys():
                data_loaded[contact_id] = db[f'{dataset}/{contact_id}'][()]
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

    def get_measurement_settings(self, dataset: str) -> DatabaseDict:
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

    def get_filters(self, measurement: str) -> Dict[str, Set[DatabaseValue]]:
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

    def filter_by_settings(self, measurement: str, settings: DatabaseDict) -> List[str]:
        """Filters the measurements by the specified settings.

        :param measurement: String identifier of the measurement in the database.
        :param settings: Dictionary containing the settings to search for.
        :returns: List of dataset paths matching the specified settings.
        """
        settings_batch = {k: [v] for k, v in settings.items()}
        return self.filter_by_settings_batch(measurement, settings_batch)

    def filter_by_settings_batch(self, measurement: str,
                                 settings_batch: Dict[str, List[DatabaseValue]]) -> List[str]:
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
        """Returns a list of sample_id strings which are available in the database under /SAMPLES.

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
