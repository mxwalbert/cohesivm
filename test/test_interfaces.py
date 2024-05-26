import pytest
import random
import numpy as np
from cohesivm import interfaces, config
from cohesivm.database import Dimensions

interface_types_to_be_tested = [
    interfaces.InterfaceType.HI_LO
]

interfaces_to_be_tested = [
    interfaces.TrivialHILO(Dimensions.Point()),
    interfaces.MA8X8(config.get_option('MA8X8', 'com_port'), Dimensions.Point())
]


@pytest.mark.parametrize("interface_type", interface_types_to_be_tested)
def test_interface_types(interface_type):
    should_be = interface_type
    assert interface_type == should_be
    should_not_be = str(interface_type)
    assert interface_type != should_not_be


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_sample_layout(interface):
    assert len(interface.pixel_positions) == len(interface.pixel_ids)
    assert len(interface.pixel_dimensions) == len(interface.pixel_ids)
    id_array = np.array(interface.pixel_ids)
    assert np.all(np.unique(id_array) == id_array)
    position_array = np.vstack(interface.pixel_positions.values())
    assert np.all(np.unique(position_array, axis=1) == position_array)
    assert np.all(id_array == np.array(list(interface.pixel_positions.keys())))
    assert np.all(id_array == np.array(list(interface.pixel_dimensions.keys())))


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_select_pixel_valid_pixel(interface):
    pixel = interface.pixel_ids[0]
    try:
        interface.select_pixel(pixel)
    except Exception as exc:
        assert False, f"Selecting a valid pixel raised an exception: {exc}"


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_select_pixel_invalid_pixel(interface):
    pixel = '999999999'
    while pixel in interface.pixel_ids:
        pixel = str(random.randint(111111111, 999999999))
    with pytest.raises(ValueError):
        interface.select_pixel(pixel)
