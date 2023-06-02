from cohesivm import database
import numpy as np
import pytest
import h5py
import os


cases_metadata_exceptions = [
    ({1: np.array([1])}, {'0': np.array([0.5, 0.5])}, TypeError),
    ({'a': np.array([1])}, {'0': [0.5, 0.5]}, TypeError),
    ({'a': np.array([1])}, {'0': np.array(0.5)}, ValueError)
]


@pytest.mark.parametrize("settings,sample_layout,expected", cases_metadata_exceptions)
def test_metadata_exceptions(settings, sample_layout, expected):
    with pytest.raises(expected):
        database.Metadata('Test', settings, 'test_sample', sample_layout)


@pytest.fixture
def metadata():
    settings = {'a': np.array([1]), 'test_b': np.array([2, 3]), 'test_c': np.array([4])}
    sample_layout = {'0': np.array([0.5, 0.5])}
    return database.Metadata(measurement='Test',
                             settings=settings,
                             sample_id='test_sample',
                             sample_layout=sample_layout)


def test_settings_string(metadata):
    assert metadata.settings_string == 'a:1,tb:2-3,tc:4'


@pytest.fixture
def db():
    return database.Database('test.hdf5')


@pytest.fixture
def stem(db, metadata):
    yield db.initialize_dataset(metadata)
    os.remove(db.path)


def test_initialize_dataset(db, metadata, stem):
    with h5py.File(db.path, "r") as h5:
        assert {metadata.measurement, 'SAMPLES'} == set(h5.keys())
        assert h5[stem] == h5['SAMPLES'][metadata.sample_id][db._datetime]
    for _ in range(3):
        metadata.measurement = 'Test2'
        assert db.initialize_dataset(metadata)
        metadata.settings = {'a': np.array([1])}
        assert db.initialize_dataset(metadata)
        metadata.sample_id = 'test_sample2'
        assert db.initialize_dataset(metadata)
        metadata.sample_layout = {'1': np.array([0.25, 0.25])}
        assert db.initialize_dataset(metadata)


def test_save_and_load_data(db, stem):
    a = np.ones(shape=(100,), dtype=[('A', float), ('B', float)])
    pixel = '0'
    db.save(a, stem, pixel)
    b = db.load(stem, pixel)[0]
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
        db.save(data, stem, pixel)
    for c, d in zip(db.load(stem, pixels), datasets):
        assert (c == d).all()


@pytest.fixture
def settings_collection():
    return [
        # {'a': np.array([1]), 'test_b': np.array([2, 3]), 'test_c': np.array([4])}, ## Already in database
        {'a': np.array([1]), 'test_b': np.array([3, 4]), 'test_c': np.array([4])},
        {'a': np.array([2]), 'test_b': np.array([2, 3]), 'test_c': np.array([5])},
        {'a': np.array([2]), 'test_b': np.array([2]), 'test_c': np.array([4])},
        {'a': np.array([2, 3]), 'test_b': np.array([2, 3]), 'test_c': np.array([7])}
    ]


def test_get_filters(db, metadata, stem, settings_collection):
    for settings in settings_collection:
        tmp_metadata = metadata.copy()
        tmp_metadata.settings = settings
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


def test_filter_by_settings(db, metadata, stem, settings_collection):
    assert db.filter_by_settings(metadata.measurement, metadata.settings)[0] == stem
    for settings in settings_collection:
        tmp_metadata = metadata.copy()
        tmp_metadata.settings = settings
        db.initialize_dataset(tmp_metadata)
    assert len(db.filter_by_settings(metadata.measurement, {'a': np.array([1])})) == 2
    assert len(db.filter_by_settings(metadata.measurement, {'a': np.array([1]), 'test_b': np.array([2, 3])})) == 1
    assert len(db.filter_by_settings(metadata.measurement, {'a': np.array([1]), 'test_c': np.array([4])})) == 2
    assert len(db.filter_by_settings(metadata.measurement, {'test_b': np.array([2])})) == 1
    tmp_metadata = metadata.copy()
    tmp_metadata.measurement = 'Test2'
    stem2 = db.initialize_dataset(tmp_metadata)
    assert db.filter_by_settings(tmp_metadata.measurement, tmp_metadata.settings)[0] == stem2
    assert len(db.filter_by_settings(tmp_metadata.measurement, {'a': np.array([1])})) == 1


def test_get_sample_ids(db, metadata, stem):
    assert db.get_sample_ids() == ['test_sample']
    tmp_metadata = metadata.copy()
    tmp_metadata.sample_id = 'test_sample2'
    db.initialize_dataset(tmp_metadata)
    assert db.get_sample_ids() == ['test_sample', 'test_sample2']


def test_filter_by_sample_id(db, metadata, stem, settings_collection):
    for settings in settings_collection:
        tmp_metadata = metadata.copy()
        tmp_metadata.settings = settings
        db.initialize_dataset(tmp_metadata)
    tmp_metadata = metadata.copy()
    tmp_metadata.sample_id = 'test_sample2'
    db.initialize_dataset(tmp_metadata)
    assert stem in db.filter_by_sample_id(metadata.sample_id)
    assert len(db.filter_by_sample_id(metadata.sample_id)) == 5
    assert len(db.filter_by_sample_id(tmp_metadata.sample_id)) == 1
