import pytest
import random
import numpy as np
from cohesivm import interfaces, config

interface_types_to_be_tested = [
    interfaces.InterfaceType.HI_LO
]

interfaces_to_be_tested = [
    interfaces.TrivialHILO(),
    interfaces.MA8X8(config.get('MA8X8', 'com_port'))
]


@pytest.mark.parametrize("interface_type", interface_types_to_be_tested)
def test_interface_types(interface_type):
    should_be = interface_type
    assert interface_type == should_be
    should_not_be = str(interface_type)
    assert interface_type != should_not_be


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_sample_layout(interface):
    assert len(interface.sample_layout.keys()) == len(interface.pixels)
    for k in interface.sample_layout.keys():
        assert type(k) == str
        assert k in interface.pixels
    location_array = np.vstack(list(interface.sample_layout.values()))
    assert np.all(np.unique(location_array, axis=1) == location_array)


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_select_pixel_valid_pixel(interface):
    pixel = interface.pixels[0]
    try:
        interface.select_pixel(pixel)
    except Exception as exc:
        assert False, f"Selecting a valid pixel raised an exception: {exc}"


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_select_pixel_invalid_pixel(interface):
    pixel = '999999999'
    while pixel in interface.pixels:
        pixel = str(random.randint(111111111, 999999999))
    with pytest.raises(ValueError):
        interface.select_pixel(pixel)
