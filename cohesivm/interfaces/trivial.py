from cohesivm.database import Dimensions
from cohesivm.interfaces import Interface, HighLow


class TrivialHighLow(Interface):
    """This interface is the conventional, single-point connection to a sample with one positive/high-voltage terminal
    and one negative/low-voltage terminal. It can be used if the selection of contacts is carried out manually
    (not recommended).

    :param pixel_dimensions: The size and shape of the pixel on the sample.
    """
    _interface_type = HighLow
    _contact_ids = ['0']
    _contact_positions = {'0': (0., 0.)}
    _interface_dimensions = Dimensions.Point()

    def __init__(self, pixel_dimensions: Dimensions.Shape) -> None:
        super().__init__(pixel_dimensions)

    def _select_contact(self, contact_id: str) -> None:
        pass
