import pytest
import numpy as np
from cohesivm import interfaces, config
from cohesivm.database import Dimensions
from . import DemoInterfaceType

interface_types_to_be_tested = [
    interfaces.HighLow
]

interface_instances = [
    interfaces.TrivialHighLow(Dimensions.Point()),
    interfaces.MA8X8(config.get_option('MA8X8', 'com_port'), Dimensions.Point())
]

interfaces_to_be_tested = [
    interface_instances[0],
    pytest.param(interface_instances[1], marks=pytest.mark.hardware('ma8x8'))
]


@pytest.mark.parametrize("interface_type", interface_types_to_be_tested)
def test_interface_types(interface_type):
    should_be = interface_type
    assert interface_type == should_be
    should_not_be = str(interface_type)
    assert interface_type != should_not_be
    assert interface_type != DemoInterfaceType


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_sample_layout(interface):
    assert len(interface.contact_positions) == len(interface.contact_ids)
    assert len(interface.pixel_dimensions) == len(interface.contact_ids)
    id_array = np.array(interface.contact_ids)
    assert np.all(np.unique(id_array) == id_array)
    position_array = np.vstack(list(interface.contact_positions.values()))
    assert np.all(np.unique(position_array, axis=1) == position_array)
    assert np.all(id_array == np.array(list(interface.contact_positions.keys())))
    assert np.all(id_array == np.array(list(interface.pixel_dimensions.keys())))


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_select_contact_valid_contact(interface):
    contact_id = interface.contact_ids[0]
    try:
        interface.select_contact(contact_id)
    except Exception as exc:
        assert False, f"Selecting a valid contact raised an exception: {exc}"


@pytest.mark.parametrize("interface", interfaces_to_be_tested)
def test_select_contact_invalid_contact(interface):
    contact_id = ' '
    while contact_id in interface.contact_ids:
        contact_id += ' '
    with pytest.raises(ValueError):
        interface.select_contact(contact_id)
