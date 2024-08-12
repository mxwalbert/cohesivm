import numpy as np
import pytest
import h5py
import os
import copy
import hashlib
from typing import Dict
from cohesivm.database import Database, Metadata, Dimensions


metadata_dict = {
    'measurement': 'TestMeasurement',
    'measurement_settings': {'a': 1, 'test_b': (2, 3), 'test_c': 4},
    'sample_id': 'test_sample',
    'device': 'TestDevice',
    'channels': ['TestChannel1', 'TestChannel2'],
    'channels_settings': [{'setting1': 1, 'setting2': 2}, {'setting3': 2., 'setting4': (3, 4)}],
    'interface': 'TestInterface',
    'interface_dimensions': str(Dimensions.Point()),
    'contact_ids': ['0'],
    'contact_positions': [(0, 0)],
    'pixel_dimensions': [str(Dimensions.Point())]
}


@pytest.fixture
def metadata():
    return Metadata(**metadata_dict)


def test_settings_hash(metadata: Metadata):
    settings_hash = [
        hashlib.sha256('a1'.encode()).hexdigest()[:16],
        hashlib.sha256('test_b(2, 3)'.encode()).hexdigest()[:16],
        hashlib.sha256('test_c4'.encode()).hexdigest()[:16]
    ]
    assert metadata.settings_hash == ':'.join(settings_hash)


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
    contact_id = '0'
    db.save_data(a, dataset, contact_id)
    b = db.load_data(dataset, contact_id)[0]
    assert (a == b).all()
    assert b.dtype.names == ('A', 'B')
    contact_ids = ['1', '2', '3']
    a2 = a.copy()
    a2['A'] += 1
    a2['B'] += 1
    a3 = a.copy()
    a3['A'] *= 10
    a3['B'] -= 1
    datasets = [a, a2, a3]
    for contact_id, data in zip(contact_ids, datasets):
        db.save_data(data, dataset, contact_id)
    for c, d in zip(db.load_data(dataset, contact_ids), datasets):
        assert (c == d).all()


def test_load_metadata(db: Database, metadata: Metadata, dataset: str):
    settings_hash = metadata.settings_hash
    metadata = db.load_metadata(dataset)
    assert settings_hash == metadata.settings_hash


@pytest.fixture
def settings_collection():
    return [
        # {'a': 1), 'test_b': (2, 3), 'test_c': 4}, ## Already in database
        {'a': 1, 'test_b': (3, 4), 'test_c': 4},
        {'a': 2, 'test_b': (2, 3), 'test_c': 5},
        {'a': 2, 'test_b': 2, 'test_c': 4},
        {'a': (2, 3), 'test_b': (2, 3), 'test_c': 7}
    ]


def test_get_filters(db: Database, metadata: Metadata, dataset: str, settings_collection: Dict):
    for measurement_settings in settings_collection:
        tmp_metadata = copy.deepcopy(metadata)
        tmp_metadata._measurement_settings = measurement_settings
        tmp_metadata._settings_hash = tmp_metadata.parse_settings_hash(measurement_settings)
        db.initialize_dataset(tmp_metadata)
    expected_filters = {
        'a': {1, 2, (2, 3)},
        'test_b': {2, (2, 3), (3, 4)},
        'test_c': {4, 5, 7}
    }
    filters = db.get_filters(metadata.measurement)
    assert len(expected_filters.keys()) == len(filters.keys())
    for k, v in filters.items():
        assert expected_filters[k] == v


def test_filter_by_settings(db: Database, metadata: Metadata, dataset: str, settings_collection: Dict):
    assert db.filter_by_settings(metadata.measurement, metadata.measurement_settings)[0] == dataset
    for measurement_settings in settings_collection:
        tmp_metadata = copy.deepcopy(metadata)
        tmp_metadata._measurement_settings = measurement_settings
        tmp_metadata._settings_hash = tmp_metadata.parse_settings_hash(measurement_settings)
        db.initialize_dataset(tmp_metadata)
    assert len(db.filter_by_settings(metadata.measurement, {'a': 1})) == 2
    assert len(db.filter_by_settings(metadata.measurement, {'a': 1, 'test_b': (2, 3)})) == 1
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
        tmp_metadata._measurement_settings = measurement_settings
        tmp_metadata._settings_hash = tmp_metadata.parse_settings_hash(measurement_settings)
        db.initialize_dataset(tmp_metadata)
    tmp_metadata = copy.deepcopy(metadata)
    tmp_metadata._sample_id = 'test_sample2'
    db.initialize_dataset(tmp_metadata)
    assert dataset in db.filter_by_sample_id(metadata.sample_id)
    assert len(db.filter_by_sample_id(metadata.sample_id)) == 5
    assert len(db.filter_by_sample_id(tmp_metadata.sample_id)) == 1
