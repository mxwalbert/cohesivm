import numpy as np
import pytest
import h5py
import os
import copy
from typing import Dict
from cohesivm.database import Database, Metadata, Dimensions


@pytest.fixture
def metadata_dict():
    metadata_dict = {
        'measurement': 'Test',
        'measurement_settings': {'a': 1, 'test_b': np.array([2, 3]), 'test_c': 4},
        'sample_id': 'test_sample',
        'device': 'test_device',
        'channels': ['test_channel'],
        'channels_settings': [{'test': 1, 'test_b': np.array([2])}, {'test': 2, 'test_b': np.array([3, 4])}],
        'interface': 'test_interface',
        'sample_dimensions': Dimensions.Point(),
        'sample_layout': {'0': (0.5, 0.5)},
        'pixel_dimensions': {'0': Dimensions.Point()}
    }
    return metadata_dict


@pytest.fixture
def metadata(metadata_dict: Dict):
    return Metadata(**metadata_dict)


def test_settings_string(metadata: Metadata):
    assert metadata.settings_string == 'a:1,test_b:2-3,test_c:4'


@pytest.fixture
def db() -> Database:
    return Database('test.hdf5')


@pytest.fixture
def dataset(db: Database, metadata: Metadata) -> str:
    yield db.initialize_dataset(metadata)
    os.remove(db.path)


def test_initialize_dataset(db: Database, metadata: Metadata, dataset: str):
    with h5py.File(db.path, "r") as h5:
        assert {metadata.measurement, 'SAMPLES'} == set(h5.keys())
        assert h5[dataset] == h5['SAMPLES'][metadata.sample_id][db._timestamp]


def test_save_and_load_data(db: Database, dataset: str):
    a = np.ones(shape=(100,), dtype=[('A', float), ('B', float)])
    pixel = '0'
    db.save(a, dataset, pixel)
    b = db.load_data(dataset, pixel)[0]
    assert (a == b).all()
    assert b.dtype.names == ('A', 'B')
    pixels = ['1', '2', '3']
    a2 = a.copy()
    a2['A'] += 1
    a2['B'] += 1
    a3 = a.copy()
    a3['A'] *= 10
    a3['B'] -= 1
    datasets = [a, a2, a3]
    for pixel, data in zip(pixels, datasets):
        db.save(data, dataset, pixel)
    for c, d in zip(db.load_data(dataset, pixels), datasets):
        assert (c == d).all()


def test_load_metadata(db: Database, metadata_dict: Dict, dataset: str):
    for key, value in db.load_metadata(dataset).items():
        if key == 'dcmi':
            continue
        elif key == 'measurement_settings':
            for setting_key, setting_value in value.items():
                if type(setting_value) == np.ndarray:
                    assert np.alltrue(value[setting_key] == setting_value)
                else:
                    assert value[setting_key] == setting_value
        elif key == 'channels_settings':
            for channel_settings in value:
                for setting_key, setting_value in channel_settings.items():
                    if type(setting_value) == np.ndarray:
                        assert np.alltrue(channel_settings[setting_key] == setting_value)
                    else:
                        assert channel_settings[setting_key] == setting_value
        else:
            assert metadata_dict[key] == value
    Metadata(**db.load_metadata(dataset))


@pytest.fixture
def settings_collection():
    return [
        # {'a': 1), 'test_b': np.array([2, 3]), 'test_c': 4}, ## Already in database
        {'a': 1, 'test_b': np.array([3, 4]), 'test_c': 4},
        {'a': 2, 'test_b': np.array([2, 3]), 'test_c': 5},
        {'a': 2, 'test_b': 2, 'test_c': 4},
        {'a': np.array([2, 3]), 'test_b': np.array([2, 3]), 'test_c': 7}
    ]


def test_get_filters(db: Database, metadata: Metadata, dataset: str, settings_collection: Dict):
    for measurement_settings in settings_collection:
        tmp_metadata = copy.deepcopy(metadata)
        for k in measurement_settings.keys():
            if type(measurement_settings[k]) == np.ndarray:
                if measurement_settings[k].ndim != 1:
                    measurement_settings[k] = measurement_settings[k].flatten()
        tmp_metadata._measurement_settings = measurement_settings
        tmp_metadata._settings_string = tmp_metadata.parse_settings_string(measurement_settings)
        db.initialize_dataset(tmp_metadata)
    expected_filters = {
        'a': {(1,), (2,), (2, 3)},
        'test_b': {(2,), (2, 3), (3, 4)},
        'test_c': {(4,), (5,), (7,)}
    }
    filters = db.get_filters(metadata.measurement)
    assert len(expected_filters.keys()) == len(filters.keys())
    for k, v in filters.items():
        assert expected_filters[k] == v


def test_filter_by_settings(db: Database, metadata: Metadata, dataset: str, settings_collection: Dict):
    assert db.filter_by_settings(metadata.measurement, metadata.measurement_settings)[0] == dataset
    for measurement_settings in settings_collection:
        tmp_metadata = copy.deepcopy(metadata)
        for k in measurement_settings.keys():
            if type(measurement_settings[k]) == np.ndarray:
                if measurement_settings[k].ndim != 1:
                    measurement_settings[k] = measurement_settings[k].flatten()
        tmp_metadata._measurement_settings = measurement_settings
        tmp_metadata._settings_string = tmp_metadata.parse_settings_string(measurement_settings)
        db.initialize_dataset(tmp_metadata)
    assert len(db.filter_by_settings(metadata.measurement, {'a': 1})) == 2
    assert len(db.filter_by_settings(metadata.measurement, {'a': 1, 'test_b': np.array([2, 3])})) == 1
    assert len(db.filter_by_settings(metadata.measurement, {'a': 1, 'test_c': 4})) == 2
    assert len(db.filter_by_settings(metadata.measurement, {'test_b': 2})) == 1
    tmp_metadata = copy.deepcopy(metadata)
    tmp_metadata._measurement = 'Test2'
    stem2 = db.initialize_dataset(tmp_metadata)
    assert db.filter_by_settings(tmp_metadata.measurement, tmp_metadata.measurement_settings)[0] == stem2
    assert len(db.filter_by_settings(tmp_metadata.measurement, {'a': 1})) == 1


def test_get_sample_ids(db: Database, metadata: Metadata, dataset: str):
    assert db.get_sample_ids() == ['test_sample']
    tmp_metadata = copy.deepcopy(metadata)
    tmp_metadata._sample_id = 'test_sample2'
    db.initialize_dataset(tmp_metadata)
    assert db.get_sample_ids() == ['test_sample', 'test_sample2']


def test_filter_by_sample_id(db: Database, metadata: Metadata, dataset: str, settings_collection: Dict):
    for measurement_settings in settings_collection:
        tmp_metadata = copy.deepcopy(metadata)
        for k in measurement_settings.keys():
            if type(measurement_settings[k]) == np.ndarray:
                if measurement_settings[k].ndim != 1:
                    measurement_settings[k] = measurement_settings[k].flatten()
        tmp_metadata._measurement_settings = measurement_settings
        tmp_metadata._settings_string = tmp_metadata.parse_settings_string(measurement_settings)
        db.initialize_dataset(tmp_metadata)
    tmp_metadata = copy.deepcopy(metadata)
    tmp_metadata._sample_id = 'test_sample2'
    db.initialize_dataset(tmp_metadata)
    assert dataset in db.filter_by_sample_id(metadata.sample_id)
    assert len(db.filter_by_sample_id(metadata.sample_id)) == 5
    assert len(db.filter_by_sample_id(tmp_metadata.sample_id)) == 1
