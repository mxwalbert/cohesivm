import copy
import pytest
import numpy as np
from cohesivm.analysis.iv import CurrentVoltageCharacteristic


def iv_equation(v, il=0.5, i0=1e-10, n=1, t=300, q=1.602176634e-19, k=1.38064852e-23):
    return -il + i0 * np.exp((q * v) / (n * k * t))


def iv_hysteresis(v, vf=0.1, n2=2, il=0.5, i0=1e-10, n=1, t=300, q=1.602176634e-19, k=1.38064852e-23):
    voc = np.log(il / i0) * (n * k * t) / q
    i1 = (il - vf * voc) / np.exp(np.log(il / i0) * n / n2)
    return -il + i1 * np.exp((q * v) / (n2 * k * t)) + vf * v


@pytest.fixture
def analysis():
    dtype = [('Voltage (V)', float), ('Current (A)', float)]
    v = np.arange(-1, 10, 0.0001)
    currents = {
        'linear': [vi - 8 for vi in v],
        'quadratic': [(vi / 5) ** 2 - 2 for vi in v],
        'exponential': [np.exp(vi) - 10000 for vi in v],
        'equation': [iv_equation(vi) for vi in v],
        'hysteresis': [iv_hysteresis(vi) for vi in v]
    }
    dataset = {n: np.array([(vi, ii) for vi, ii in zip(v, i)], dtype=dtype) for n, i in currents.items()}
    return CurrentVoltageCharacteristic(dataset)


def test_voc(analysis):
    assert analysis.voc('linear').round(3) == 8.000
    assert analysis.voc('quadratic').round(3) == 7.071
    assert analysis.voc('exponential').round(3) == np.log(10000).round(3)
    assert analysis.voc('equation').round(3) == 0.577


def test_isc(analysis):
    assert analysis.isc('linear').round(3) == -8.000
    assert analysis.isc('quadratic').round(3) == -2.000
    assert analysis.isc('equation').round(3) == -0.500


def test_jsc(analysis):
    analysis._areas = {'quadratic': 2.}
    assert analysis.jsc('quadratic').round(3) == analysis.isc('quadratic').round(3) / 2.


def test_mpp_v(analysis):
    assert analysis.mpp_v('linear').round(3) == 4.000
    assert analysis.mpp_v('equation').round(4) == 0.4995


def test_mpp_i(analysis):
    assert analysis.mpp_i('linear').round(3) == -4.000
    assert analysis.mpp_i('equation').round(4) == iv_equation(0.4995).round(4)


def test_mpp_j(analysis):
    analysis._areas = {'linear': 2.}
    assert analysis.mpp_j('linear').round(3) == analysis.mpp_i('linear').round(3) / 2


def test_ff(analysis):
    assert analysis.ff('linear').round(3) == 0.250


def test_eff(analysis):
    assert analysis.eff('linear').round(3) == 16.000


def test_rs(analysis):
    assert analysis.rs('linear').round(3) == 1.000
    assert analysis.rs('exponential').round(3) == 0.000


def test_rsh(analysis):
    assert (1 / analysis.rsh('linear')).round(3) == 1.000
    assert (1 / analysis.rsh('quadratic')).round(3) == 0.000


def test_hysteresis(analysis):
    analysis_hysteresis = copy.deepcopy(analysis)
    analysis_hysteresis._hysteresis = True
    analysis_hysteresis.data['hysteresis'] = np.hstack([
        analysis.data['equation'],
        np.flip(analysis.data['hysteresis'])
    ])
    assert analysis_hysteresis.voc('hysteresis')[0].round(3) == analysis_hysteresis.voc('hysteresis')[1].round(3)
    assert analysis_hysteresis.voc('hysteresis')[0].round(3) == analysis.voc('equation').round(3)
    assert analysis_hysteresis.isc('hysteresis')[0].round(3) == analysis_hysteresis.isc('hysteresis')[1].round(3)
    assert analysis_hysteresis.isc('hysteresis')[0].round(3) == analysis.isc('equation').round(3)
    assert analysis_hysteresis.mpp_v('hysteresis')[0] > analysis_hysteresis.mpp_v('hysteresis')[1].round(3)
    assert analysis_hysteresis.ff('hysteresis')[0].round(3) > analysis_hysteresis.ff('hysteresis')[1].round(3)
    assert analysis_hysteresis.eff('hysteresis')[0].round(3) > analysis_hysteresis.eff('hysteresis')[1].round(3)
