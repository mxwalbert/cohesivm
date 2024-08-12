from __future__ import annotations
import time
from typing import Union, Dict
from cohesivm.interfaces import Interface, HighLow
from cohesivm.database import Dimensions
from cohesivm.serial_communication import SerialCommunication


class MA8X8(Interface):
    """The implementation of the Measurement Array 8x8 interface which consist of 64 front contacts and a single
    back contact on an area of 25 mm x 25 mm. The interface is controlled by an Arduino Nano Every board which is
    connected through a serial COM port.

    :param com_port: The COM port of the Arduino Nano Every board.
    :param pixel_dimensions: The sizes and shapes of the pixels on the sample.
    """
    _interface_type = HighLow
    _contact_ids = [str(i + 1 + 10 * (j + 1)) for j in range(8) for i in range(8)]
    _contact_positions = {c: (2.7 + (int(c) % 10 - 1) * 2.8, 25.0 - 2.7 - (int(c) // 10 - 1) * 2.8)
                          for c in _contact_ids}
    _interface_dimensions = Dimensions.Rectangle(25., 25.)

    def __init__(self, com_port: str, pixel_dimensions: Union[Dimensions.Shape, Dict[str, Dimensions.Shape]]) -> None:
        super().__init__(pixel_dimensions)
        self.arduino = SerialCommunication(com_port, baudrate=9600, timeout=2)

    def select_contact(self, contact_id: str) -> None:
        """Select a contact on the Measurement Array 8x8 by sending a signal to the Arduino board.

        :param contact_id: The id of the contact to activate.
        :raises ValueError: If the contact is not available on the interface.
        :raises RuntimeError: If the contact selection fails.
        """
        super().select_contact(contact_id)

    def _select_contact(self, contact_id: str) -> None:
        with self.arduino as serial:
            response = serial.send_and_receive_data(str(self.contact_ids.index(contact_id) + 1))
            if response != '1':
                raise RuntimeError(f"Failed to activate contact {contact_id}")
            time.sleep(0.5)
