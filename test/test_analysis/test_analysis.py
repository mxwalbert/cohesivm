import pytest
import numpy as np
from .. import DemoAnalysis


@pytest.fixture
def dataset():
    return {
        '1': np.zeros(100),
        '2': np.ones(100),
        '3': np.ones(100) * 3,
        '4': np.ones(100) * 2,
        '5': np.ones(100) * 5,
        '6': np.ones(100) * 6
    }


@pytest.fixture
def contact_positions():
    return {
        '1': (0., 0.),
        '2': (1., 0.),
        '3': (0., 1.),
        '4': (1., 1.),
        '5': (0., 2.),
        '6': (1., 2.)
    }


def test_generate_result_dict(dataset):
    analysis = DemoAnalysis(dataset)
    result_dict = analysis.generate_result_dict('Maximum')
    assert result_dict == {'1': 0, '2': 1, '3': 3, '4': 2, '5': 5, '6': 6}


def test_result_buffer(dataset):
    analysis = DemoAnalysis(dataset)
    result_dict = analysis.generate_result_dict('Maximum')
    assert analysis._buffer['max']['1'] == result_dict['1']


def test_generate_result_map(dataset, contact_positions):
    analysis = DemoAnalysis(dataset, contact_positions)
    result_map = analysis.generate_result_maps('Maximum')[0]
    assert np.allclose(result_map, [[0., 1.], [3., 2.], [5., 6.]], equal_nan=True)
    del dataset['5']
    analysis = DemoAnalysis(dataset, contact_positions)
    result_map = analysis.generate_result_maps('Maximum')[0]
    assert np.allclose(result_map, [[0., 1.], [3., 2.], [np.nan, 6.]], equal_nan=True)
    del dataset['6']
    del contact_positions['6']
    analysis = DemoAnalysis(dataset, contact_positions)
    result_map = analysis.generate_result_maps('Maximum')[0]
    assert np.allclose(result_map, [[0., 1.], [3., 2.], [np.nan, np.nan]], equal_nan=True)
    del contact_positions['5']
    analysis = DemoAnalysis(dataset, contact_positions)
    result_map = analysis.generate_result_maps('Maximum')[0]
    assert np.allclose(result_map, [[0., 1.], [3., 2.]], equal_nan=True)
    del dataset['3']
    del dataset['4']
    del contact_positions['3']
    del contact_positions['4']
    analysis = DemoAnalysis(dataset, contact_positions)
    result_map = analysis.generate_result_maps('Maximum')[0]
    assert np.allclose(result_map, [[0., 1.]], equal_nan=True)
    del dataset['2']
    del contact_positions['2']
    analysis = DemoAnalysis(dataset, contact_positions)
    result_map = analysis.generate_result_maps('Maximum')[0]
    assert np.allclose(result_map, [[0.]], equal_nan=True)


def test_non_regular_result_map(dataset):
    contact_positions = {
        '1': (0.1, 0.1),
        '2': (1.5, 0.1),
        '3': (0.1, 1.5),
        '4': (1.5, 1.5),
        '5': (0.1, 3.),
        '6': (1.5, 3.)
    }
    analysis = DemoAnalysis(dataset, contact_positions)
    result_map = analysis.generate_result_maps('Maximum')[0]
    assert np.allclose(result_map, [[0., 1.], [3., 2.], [5., 6.]], equal_nan=True)
